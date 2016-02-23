from flask import render_template, flash, redirect, url_for, send_file

from .. import app, flask_login, MENUS

from ..util.permission import in_office, in_office_dynamic

from ..models.ranks import Rank
from ..models.users import User

from ..forms.ranks import Create, Assign


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


@app.route('/ranks/image/<name_short>')
def ranks_image(name_short):
    """Render the image for the rank

    :param name_short: The name_short attribute of the Rank
    :return: Image file
    """
    rank = Rank.by_name_short(name_short)

    return send_file(rank.image, mimetype=rank.image.content_type)


@app.route('/profile/xml/<name_short>.paa')
def ranks_image_squad(name_short):
    """Render the rank image for Squad XML

    :param name_short: The name_short attribute of the Rank
    :return: Image file
    """
    rank = Rank.by_name_short(name_short)

    return send_file(rank.image_squad, mimetype=rank.image_squad.content_type)


@app.route('/ranks/assign/<steam_id>', methods=['GET', 'POST'])
@flask_login.login_required
@in_office(['Organizational', 'HQ'])
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
