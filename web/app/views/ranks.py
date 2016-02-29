from flask import render_template, flash, redirect, url_for, send_file, request, abort

from .. import app, flask_login, MENUS

from ..util.permission import in_office, in_office_dynamic

from ..models.ranks import Rank
from ..models.users import User

from ..forms.ranks import Create, Assign, Edit


MENUS.append({'parent_url': "url_for('office', office_name='Organizational')",
              'url': "url_for('ranks')",
              'name': 'Ranks'})


@app.route('/ranks')
def ranks():
    """List all ranks"""
    all_ranks = Rank.all()

    return render_template('ranks/all.html',
                           ranks=all_ranks,
                           has_permission=in_office_dynamic(['HQ'], ['Organizational']))


@app.route('/ranks/<name_short>')
def ranks_rank(name_short):
    """List the individual rank

    :param name_short: A string representation fo the short name of the Rank
    :return: render_template() or redirect()
    """
    rank = Rank.by_name_short(name_short)
    if not rank:
        abort(404)

    return render_template('ranks/rank.html',
                           rank=rank,
                           has_permission=in_office_dynamic(['HQ'], ['Organizational']))


@app.route('/ranks/create', methods=['GET', 'POST'])
@flask_login.login_required
@in_office(['HQ'], ['Organizational'])
def ranks_create():
    """Create a new rank"""
    form = Create()

    if form.validate_on_submit():
        db_change = Rank.create(
            name=form.name.data,
            name_short=form.name_short.data,
            description=form.description.data,
            order=form.order.data,
            ts_group=form.ts_group.data,
            image=form.image.data,
            image_squad=form.image_squad.data
        )
        if db_change:
            flash('Rank successfully created!', 'success')
        else:
            flash('Rank failed to be created!', 'danger')
        return redirect(url_for('ranks'))

    return render_template('ranks/create.html', form=form)


@app.route('/ranks/<name_short>/edit', methods=['GET', 'POST'])
@flask_login.login_required
@in_office(['HQ'], ['Organizational'])
def ranks_edit(name_short):
    """Edit the given rank

    :param name_short: A string representation fo the short name of the Rank
    :return: render_template() or redirect()
    """
    rank = Rank.by_name_short(name_short)
    if not rank:
        flash('{0} Rank not found!'.format(name_short), 'warning')
        return redirect(url_for('ranks'))

    form = Edit()

    # Populate fields with default values
    if request.method == 'GET':
        form.name.data = rank.name
        form.name_short.data = rank.name_short
        form.description.data = rank.description
        form.order.data = rank.order
        form.ts_group.data = rank.ts_group

    # Add office name to form to allow for validation
    if request.method == 'POST':
        form.exclude_id.data = rank.id
    if form.validate_on_submit():
        db_change = rank.edit(
            name=form.name.data,
            name_short=form.name_short.data,
            description=form.description.data,
            order=form.order.data,
            ts_group=form.ts_group.data,
            image=form.image.data,
            image_squad=form.image_squad.data
        )
        if db_change:
            flash('Rank successfully edited!', 'success')
        else:
            flash('Rank failed to be edited!', 'danger')
        return redirect(url_for('ranks_rank', name_short=rank.name_short))

    return render_template('ranks/edit.html', form=form, rank=rank)


@app.route('/ranks/image/<name_short>.png')
def ranks_image(name_short):
    """Render the image for the rank

    :param name_short: The name_short attribute of the Rank
    :return: Image file
    """
    rank = Rank.by_name_short(name_short)

    if not rank.image:
        abort(404)

    return send_file(rank.image, mimetype=rank.image.content_type)


@app.route('/ranks/image/<name_short>_thumb.png')
def ranks_image_thumb(name_short):
    """Render the image for the rank

    :param name_short: The name_short attribute of the Rank
    :return: Image file
    """
    rank = Rank.by_name_short(name_short)

    if not rank.image.thumbnail:
        abort(404)

    return send_file(rank.image.thumbnail, mimetype=rank.image.content_type)


@app.route('/profile/xml/<_id>.paa')
def ranks_image_squad(_id):
    """Render the rank image for Squad XML

    :param _id: Object ID of the rank
    :return: Image file
    """
    image_squad = Rank.image_by_id(_id)

    if not image_squad:
        abort(404)

    return send_file(image_squad, mimetype=image_squad.content_type)


@app.route('/ranks/assign/<steam_id>', methods=['GET', 'POST'])
@flask_login.login_required
@in_office(['HQ', 'Organizational'])
def ranks_assign(steam_id):
    """Assign a rank to the user with the given steam ID

    :param steam_id: Steam ID of user to give rank to
    :return: render_template() or redirect()
    """
    user = User.by_steam_id(steam_id)
    form = Assign()

    if user.rank:
        exclude = user.rank.name_short
    else:
        exclude = ''
    form.rank.choices = Rank.select_field_ranks(blank=True, exclude=exclude)

    if form.validate_on_submit():
        db_change = user.assign_rank(form.rank.data)
        if db_change:
            flash('Rank successfully assigned!', 'success')
        else:
            flash('Rank failed to be assigned!', 'danger')
        return redirect(url_for('profile', steam_id=user.steam_id))

    return render_template('ranks/assign.html', form=form, user=user)
