from flask import render_template, request, flash, redirect, url_for, abort, make_response, \
    send_file

from .. import app, flask_login, CONFIG, MENUS
from ..util.permission import in_office_dynamic, owns_steam_id_page

from ..models.users import User
from ..models.ranks import Rank

from ..forms.profile import ArmaName, TSID, XMLDisplay, EmailUpdate


@app.route('/profile/<steam_id>')
@flask_login.login_required
def profile(steam_id):
    """The profile page of the given user by steam ID.

    :param steam_id: The steam ID of the user in question
    :return: render_template() or redirect()
    """
    user = User.by_steam_id(steam_id)
    is_owner = user.id == flask_login.current_user.id
    is_org = in_office_dynamic(['Organizational', 'HQ'])
    is_owner_or_org = is_owner or is_org
    return render_template('profile/view.html',
                           user=user,
                           is_owner=is_owner,
                           is_owner_or_org=is_owner_or_org,
                           is_org=is_org,
                           url_root=CONFIG['URL_ROOT'][:-1])


MENUS.append({'parent_url': "url_for('office', office_name='Organizational')",
              'url': "url_for('profile_all')",
              'name': 'All Users'})


@app.route('/profile/all')
@flask_login.login_required
def profile_all():
    """Shows all the users on the site in a sorted manner.

    :return: render_template() or redirect()
    """
    users_unsorted = User.all()
    ranks = Rank.all(reverse=True)
    users = []

    # Add ranks in order
    for rank in ranks:
        users.append({'rank': rank.name,
                      'users': [],
                      'rank_url': url_for('ranks_rank', name_short=rank.name_short)})
    users.append({'rank': 'No rank',
                  'users': []})

    # Add users to respective ranks
    for user in users_unsorted:
        if user.rank:
            for group in users:
                if user.rank.name == group['rank']:
                    group['users'].append(user)
                    continue
        else:
            users[-1]['users'].append(user)

    return render_template('profile/all.html', users=users)


@app.route('/profile/<steam_id>/update/arma-name', methods=['GET', 'POST'])
@flask_login.login_required
@owns_steam_id_page(exceptions=(['HQ'], ['Organizational']))
def update_arma_name(steam_id):
    """Updates the Arma name of the given user by steam id.

    :param steam_id: The steam ID of the user in question
    :return: render_template() or redirect()
    """
    user = User.by_steam_id(steam_id)

    form = ArmaName()

    # Add user id to form to allow for validation
    if request.method == 'POST':
        form.exclude_id.data = user.id
    if form.validate_on_submit():
        if user.update_arma_name(form.arma_name.data):
            flash('Arma name successfully changed!', 'success')
        else:
            flash('Arma name failed to update for some reason!', 'danger')
        return redirect(url_for('profile', steam_id=steam_id))

    return render_template('profile/update_name.html', user=user, form=form)


@app.route('/profile/<steam_id>/update/ts-id', methods=['GET', 'POST'])
@flask_login.login_required
@owns_steam_id_page(exceptions=(['HQ'], ['Organizational']))
def update_ts_id(steam_id):
    """Updates the Arma name of the given user by steam id.

    :param steam_id: The steam ID of the user in question
    :return: render_template() or redirect()
    """
    user = User.by_steam_id(steam_id)

    form = TSID()

    if form.validate_on_submit():
        if user.add_ts_id(form.ts_id.data):
            flash('TeamSpeak ID successfully added!', 'success')
        else:
            flash('TeamSpeak ID failed to be added for some reason!', 'danger')
        return redirect(url_for('profile', steam_id=steam_id))

    return render_template('profile/update_ts_id.html', user=user, form=form)


@app.route('/profile/xml/<steam_id>')
def profile_xml(steam_id):
    """Shows a personalized squad XML for the user

    :param steam_id: The steam ID of the user in question
    :return: render_template() in XML or abort(404) if no rank
    """
    user = User.by_steam_id(steam_id)

    if not user.rank:
        abort(404)

    display_za = user.xml_display == 'za'
    template = render_template('profile/squad.xml', user=user, display_za=display_za)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'

    return response


@app.route('/profile/<steam_id>/update/xml-display', methods=['GET', 'POST'])
@flask_login.login_required
@owns_steam_id_page(exceptions=(['HQ'], ['Organizational']))
def update_xml_display(steam_id):
    """Change the kind of squad XML to display.

    :param steam_id: The steam ID of the user in question
    :return: render_template() or redirect()
    """
    user = User.by_steam_id(steam_id)

    if not user.rank:
        flash('You need to have a rank to adjust this!', 'warning')
        return redirect(url_for('profile', steam_id=steam_id))
    if user.rank:
        if user.rank.name_short == 'HON':
            flash('You cannot adjust this as an honorary member!', 'warning')
            return redirect(url_for('profile', steam_id=steam_id))

    form = XMLDisplay()
    if user.xml_display == 'rank':
        choices = [('za', 'General ZA')]
    else:
        choices = [('rank', 'Rank')]
    form.xml_display.choices = choices

    if form.validate_on_submit():
        if user.update_xml_display(form.xml_display.data):
            flash('Squad XML Display type successfully updated!', 'success')
        else:
            flash('Squad XML Display type failed to be changed for some reason!', 'danger')
        return redirect(url_for('profile', steam_id=steam_id))

    return render_template('profile/update_xml_display.html', user=user, form=form)


@app.route('/profile/xml/logo.paa')
def za_paa():
    """Render the ZA PAA logo

    :return: Image file
    """
    return send_file('.' + url_for('static', filename='xml/za_logo.paa'), mimetype='image/paa')


@app.route('/profile/<steam_id>/update/email', methods=['GET', 'POST'])
@flask_login.login_required
@owns_steam_id_page(exceptions=(['HQ'], ['Organizational']))
def update_email(steam_id):
    """Updates the email of the user.

    :param steam_id: The steam ID of the user in question
    :return: render_template() or redirect()
    """
    user = User.by_steam_id(steam_id)

    form = EmailUpdate()

    # Add user id to form to allow for validation
    if request.method == 'POST':
        form.exclude_id.data = user.id
    if form.validate_on_submit():
        if user.update_email(form.email.data):
            flash('Email successfully added!', 'success')
        else:
            flash('Email failed to be added for some reason!', 'danger')
        return redirect(url_for('profile', steam_id=steam_id))

    return render_template('profile/update_email.html', user=user, form=form)
