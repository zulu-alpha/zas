from collections import namedtuple

from flask import render_template, flash, redirect, url_for, send_file, request, abort

from .. import app, flask_login, MENUS

from ..util.permission import in_office, in_office_dynamic, msg, permissions_redirect
from ..util.helper import convert_from_utc

from ..models.events import Mission, ElectiveMission, Training, ElectiveTraining, Selection, Misc

from ..forms.events import CreateMission, EditMission, CreateElectiveMission, EditElectiveMission,\
    CreateTraining, EditTraining, CreateElectiveTraining, EditElectiveTraining, CreateSelection, \
    EditSelection, CreateMisc, EditMisc, SignUpModify, Publish, Cancel


def handle_url_elective(elective):
    """Validates the elective URL variable and returns a namedtuple containing a user presentable
    name, a url friendly name and if it has elective in the url

    :param elective: String representing the value of the elective URL parameter
    :return: namedtuple(presentable_name, name, is_url_elective) or HTTP 400
    """
    url_elective = namedtuple('URLElective', 'presentable_name name is_url_elective')
    if elective == 'elective':
        return url_elective('Elective ', 'elective', True)
    if not elective:
        return url_elective('', '', False)
    # If URL parameter is not a valid choice
    abort(400)


def handle_type(url_type, url_elective):
    """Validates the url_type URL variable and if it can be have elective in the URL and returns a
    namedtuple containing a user presentable name, url friendly name and a bool for each event type
    if it is that type. It also includes is_elective which is unlike is not just for if the URL has
    elective in it's name, but in that it tells you if the event is an elective event (eg: misc
    would not have an elective url, but would be an elective event).

    :param url_type: String representing the value of the type URL parameter
    :param url_elective: handle_url_elective() namedtuple
    :return: namedtuple(presentable_name, name, is_mission, is_training, is_selection, is_misc,
                        is_elective) or HTTP 400
    """
    # If URL parameters are a valid combination
    valid_combinations = (('mission', True),
                          ('mission', False),
                          ('training', True),
                          ('training', False),
                          ('selection', False),
                          ('misc', False))
    if (url_type, url_elective.is_url_elective) not in valid_combinations:
        abort(400)

    event_type = namedtuple('EventType', 'presentable_name name is_mission is_training '
                                         'is_selection is_misc is_elective')

    if url_type == 'mission':
        return event_type(
            'Mission', url_type, True, False, False, False, url_elective.is_url_elective)

    if url_type == 'training':
        return event_type(
            'Training', url_type, False, True, False, False, url_elective.is_url_elective)

    if url_type == 'selection':
        return event_type('Selection', url_type, False, False, True, False, True)

    if url_type == 'misc':
        return event_type('Misc', url_type, False, False, False, True, True)


def event_permission(event_type, author, redirect_user, head_only=False):
    """Validates if the given user has the permission to edit or create the given event. Can be used
    to do a redirect on permission failure or to just return a Bool of the result.

    :param event_type: handle_type() namedtuple
    :param author: User Document of event author or None
    :param redirect_user: Bool on if the user should be redirected on permission failure with a
                          message.
    :param head_only: Bool if to only allow the head of the relevant office
    :return: Bool True if has permission, else redirect with flash message
    """
    # Only allow office heads
    if head_only:
        # Missions office head can work on mission or misc
        if event_type.is_mission or event_type.is_misc:
            head = ['HQ', 'Missions']
            if in_office_dynamic(member=head):
                return True
            elif redirect_user:
                flash(msg(member=None, head=head))

        # Training office head can work on training or selection
        if event_type.is_training or event_type.is_selection:
            head = ['HQ', 'Training']
            if in_office_dynamic(member=head):
                return True
            elif redirect_user:
                flash(msg(member=None, head=head))

    else:
        # Allow the author to edit an event
        if author:  # Put author and author equality check separately due to Pycharm complaining
            if author == flask_login.current_user:
                return True

        # Missions office members can work on mission or misc
        if event_type.is_mission or event_type.is_misc:
            member = ['HQ', 'Missions']
            if in_office_dynamic(member=member):
                return True
            elif redirect_user:
                flash(msg(member=member, head=None))

        # Training office members can work on training or selection
        if event_type.is_training or event_type.is_selection:
            member = ['HQ', 'Training']
            if in_office_dynamic(member=member):
                return True
            elif redirect_user:
                flash(msg(member=member, head=None))

    if redirect:
        return permissions_redirect()
    return False


def get_class_and_form(event_type, is_edit):
    """Get the appropriate event document class and form with the given handle_type() namedtuple and
    taking into account if it is being edited

    :param event_type: handle_type() namedtuple
    :param is_edit: Bool on if the event is being edited
    :return: namedtuple(doc_class, form)
    """
    class_and_form = namedtuple('ClassAndForm', 'doc_class form')

    if event_type.is_mission and not event_type.is_elective:
        if not is_edit:
            form = CreateMission()
        else:
            form = EditMission()
        return class_and_form(Mission, form)

    if event_type.is_mission and event_type.is_elective:
        if not is_edit:
            form = CreateElectiveMission()
        else:
            form = EditElectiveMission()
        return class_and_form(ElectiveMission, form)

    if event_type.is_training and not event_type.is_elective:
        if not is_edit:
            form = CreateTraining()
        else:
            form = EditTraining()
        return class_and_form(Training, form)

    if event_type.is_training and event_type.is_elective:
        if not is_edit:
            form = CreateElectiveTraining()
        else:
            form = EditElectiveTraining()
        return class_and_form(ElectiveTraining, form)

    if event_type.is_selection:
        if not is_edit:
            form = CreateSelection()
        else:
            form = EditSelection()
        return class_and_form(Selection, form)

    if event_type.is_misc:
        if not is_edit:
            form = CreateMisc()
        else:
            form = EditMisc()
        return class_and_form(Misc, form)


@app.route('/events')
def events():
    """Gets all events of all types"""
    return 'meh'


@app.route('/events/<type_url>/<event_id>', defaults={'elective': ''})
@app.route('/events/<elective>-<type_url>/<event_id>')
def event(elective, type_url, event_id):
    """View given event

    :param elective: Elective text if elective
    :param type_url: Type of event
    :param event_id: MongoDB Document ID
    :return: render_template(), abort() or redirect()
    """
    url_elective = handle_url_elective(elective)
    event_type = handle_type(type_url, url_elective)
    doc_class = get_class_and_form(event_type, False).doc_class

    event_doc = doc_class.by_id(event_id)
    if not event_doc:
        abort(404)

    if event_doc.published:
        has_permission = event_permission(event_type, event_doc.author, True)
    else:
        has_permission = event_permission(event_type, event_doc.author, False)

    publish_form = Publish()
    cancel_form = Cancel()

    sign_up_modify_form = SignUpModify()
    sign_up_modify_form.side.choices = event_doc.sides_choices
    sign_state = event.get_signed_up_user(flask_login.current_user)
    if not sign_state or sign_state and sign_state.cancelled:
        sign_up_modify_form.commitment.choices = (('certain', 'Certain'), ('maybe', 'Maybe'))
    if sign_state and not sign_state.cancelled:
        # If more than one side to sign up for, then a choice is redundant
        if sign_up_modify_form.side.choices < 2:
            if sign_state and not sign_state.maybe:
                sign_up_modify_form.commitment.choices = (('cancel', 'Cancel'), ('maybe', 'Maybe'))
            elif sign_state and sign_state.maybe:
                sign_up_modify_form.commitment.choices = (('certain', 'Certain'), ('cancel', 'Cancel'))
        else:
            event_sign_up_modify.commitment = (('certain', 'Certain'), ('maybe', 'Maybe'),
                                               ('cancel', 'Cancel'))

    return render_template('events/event.html',
                           event=event_doc,
                           event_type=event_type,
                           url_elective=url_elective,
                           has_permission=has_permission,
                           convert_from_utc=convert_from_utc,
                           publish_form=publish_form,
                           cancel_form=cancel_form,
                           sign_up_modify_form=sign_up_modify_form)


@app.route('/events/create')
@in_office(['HQ', 'Missions', 'Training'])
def event_create_any():
    return render_template('events/create_any.html')


@app.route('/events/<type_url>/create', defaults={'elective': ''}, methods=['GET', 'POST'])
@app.route('/events/<elective>-<type_url>/create', methods=['GET', 'POST'])
@flask_login.login_required
def event_create(elective, type_url):
    """Create a new event

    :param elective: Elective text if elective
    :param type_url: Type of event
    :return: render_template(), abort() or redirect()
    """
    url_elective = handle_url_elective(elective)
    event_type = handle_type(type_url, url_elective)
    doc_class, form = get_class_and_form(event_type, False)

    event_permission(event_type, None, True)

    if form.validate_on_submit():
        author = flask_login.current_user
        event_id = doc_class.create(author, form)
        if event_id:
            flash('Event successfully created!', 'success')
        else:
            flash('Event failed to be created!', 'danger')
        return redirect(url_for('event',
                                elective=url_elective.name,
                                type_url=event_type.name,
                                event_id=event_id))
    return render_template('events/create.html',
                           event_type=event_type,
                           url_elective=url_elective,
                           form=form)


@app.route('/events/<type_url>/edit/<event_id>', defaults={'elective': ''}, methods=['GET', 'POST'])
@app.route('/events/<elective>-<type_url>/edit/<event_id>', methods=['GET', 'POST'])
@flask_login.login_required
def event_edit(elective, type_url, event_id):
    """Modify the given event

    :param elective: Elective text if elective
    :param type_url: Type of event
    :param event_id: MongoDB Document ID
    :return: render_template(), abort() or redirect()
    """
    url_elective = handle_url_elective(elective)
    event_type = handle_type(type_url, url_elective)
    doc_class, form = get_class_and_form(event_type, True)

    event_doc = doc_class.by_id(event_id)
    if not event_doc:
        abort(404)
    event_permission(event_type, event_doc.author, True)

    form.event.data = event_doc

    if form.validate_on_submit():
        event_id = event_doc.edit(form)
        if event_id:
            flash('Event successfully edited!', 'success')
        else:
            flash('Event failed to be edited!', 'danger')
        return redirect(url_for('event',
                                elective=url_elective.name,
                                type_url=event_type.name,
                                event_id=event_id))

    form = event_doc.populate_form(form)
    return render_template('events/edit.html',
                           event=event_doc,
                           event_type=event_type,
                           url_elective=url_elective,
                           form=form)


@app.route('/events/<type_url>/publish/<event_id>', defaults={'elective': ''}, methods=['POST'])
@app.route('/events/<elective>-<type_url>/publish/<event_id>', methods=['POST'])
def event_publish(elective, type_url, event_id):
    """Publish the given event

    :param elective: Elective text if elective
    :param type_url: Type of event
    :param event_id: MongoDB Document ID
    :return: redirect()
    """
    url_elective = handle_url_elective(elective)
    event_type = handle_type(type_url, url_elective)
    doc_class = get_class_and_form(event_type, True).doc_class

    event_doc = doc_class.by_id(event_id)
    if not event_doc:
        abort(404)
    event_permission(event_type, event_doc.author, True, head_only=True)

    form = Publish()
    form.event.data = event_doc

    url = url_for('event', elective=elective, type_url=type_url, event_id=event_doc.id)

    if form.validate_on_submit():
        result = event_doc.publish(url)
        if result.success:
            flash(result.message, 'success')
        else:
            flash(result.message, 'danger')

    return redirect(url)


@app.route('/events/<type_url>/cancel/<event_id>', defaults={'elective': ''}, methods=['POST'])
@app.route('/events/<elective>-<type_url>/cancel/<event_id>', methods=['POST'])
def event_cancel(elective, type_url, event_id):
    """Cancel the given event

    :param elective: Elective text if elective
    :param type_url: Type of event
    :param event_id: MongoDB Document ID
    :return: redirect()
    """
    url_elective = handle_url_elective(elective)
    event_type = handle_type(type_url, url_elective)
    doc_class = get_class_and_form(event_type, True).doc_class

    event_doc = doc_class.by_id(event_id)
    if not event_doc:
        abort(404)
    event_permission(event_type, event_doc.author, True)

    form = Cancel()
    form.event.data = event_doc

    if form.validate_on_submit():
        if event_doc.cancelable.is_cancelable:
            if event_doc.cancel():
                flash('Event cancelled!', 'success')
            else:
                flash('Something went wrong and the event was not published!', 'danger')
        else:
            flash(event_doc.cancelable.message, 'danger')

    return redirect(url_for('event', elective=elective, type_url=type_url, event_id=event_doc.id))


@app.route('/events/<type_url>/sign-up/<event_id>', defaults={'elective': ''}, methods=['POST'])
@app.route('/events/<elective>-<type_url>/sign-up/<event_id>', methods=['POST'])
@flask_login.login_required
def event_sign_up_modify(elective, type_url, event_id):
    """Change Sign Up state for the given event (certain, maybe, cancel)

    :param elective: Elective text if elective
    :param type_url: Type of event
    :param event_id: MongoDB Document ID
    :return: redirect()
    """
    url_elective = handle_url_elective(elective)
    event_type = handle_type(type_url, url_elective)
    doc_class = get_class_and_form(event_type, True).doc_class

    event_doc = doc_class.by_id(event_id)
    if not event_doc:
        abort(404)

    form = SignUpModify()
    form.event.data = event_doc

    if form.validate_on_submit():
        if form.commitment.data == 'cancel':
            result = event_doc.sign_up_cancel(flask_login.current_user)
            if result.success:
                flash(result.message, 'success')
            else:
                flash(result.message, 'danger')
        elif form.commitment.data in ['certain', 'maybe']:
            maybe = form.commitment.data == 'maybe'
            result = event_doc.sign_up(flask_login.current_user, form.side.data, maybe=maybe)
            if result.success:
                flash(result.message, 'success')
            else:
                flash(result.message, 'danger')

    return redirect(url_for('event', elective=elective, type_url=type_url, event_id=event_doc.id))
