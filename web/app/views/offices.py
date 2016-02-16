from flask import render_template, flash, redirect, url_for, request, g

from app.util.permission import in_office, in_office_dynamic

from app import app, flask_login
from app.models import User, Office
from app.forms import CreateOffice, EditOfficeMembers, EditOfficeHead


@app.route('/office/create', methods=['GET', 'POST'])
@flask_login.login_required
@in_office(['HQ'])
def create_office():
    """Create a new office"""
    form = CreateOffice()
    form.head.choices = User.select_field_ranked()

    if form.validate_on_submit():
        office_obj = Office.create_office(
            form.name.data,
            form.name_short.data,
            form.head.data)
        flash('Office successfully created!', 'success')
        return redirect(url_for('office', office_name=office_obj.name_short))

    return render_template('offices/create.html', form=form)


@app.route('/office/<office_name>')
def office(office_name):
    """View an office

    :param office_name:
    :return: render_template() or redirect()
    """
    office_obj = Office.by_name_short(office_name)

    if not office_obj:
        flash('An office named {0} was not found!'.format(office_name), 'warning')
        return redirect(url_for('home'))

    return render_template(
        'offices/office.html',
        office=office_obj,
        has_permission=in_office_dynamic(['HQ'], [office_name]),
        has_permission_hq=in_office_dynamic(['HQ'])
    )


@app.route('/office/<office_name>/edit/members', methods=['GET', 'POST'])
@flask_login.login_required
@in_office(['HQ'], ['DYNAMIC'])
def edit_office_members(office_name):
    """Add/Remove members of the office

    :param office_name: The name of the office to edit
    :return: render_template() or redirect()
    """
    office_obj = Office.by_name_short(office_name)

    form = EditOfficeMembers(office_name=office_name)
    all_users = User.select_field_ranked()
    members = Office.select_field_members(office_name)

    form.members_add.choices = [user for user in all_users if user not in members]
    form.members_remove.choices = members

    # Add office name to form to allow for validation
    if request.method == 'POST':
        form.office_name.data = office_name
    if form.validate_on_submit():
        Office.add_remove_members(
            office_name,
            form.members_add.data,
            form.members_remove.data)
        flash('Members successfully amended!', 'success')
        return redirect(url_for('office', office_name=office_name))

    return render_template('offices/edit_members.html', form=form, office=office_obj)


@app.route('/office/<office_name>/edit/head', methods=['GET', 'POST'])
@flask_login.login_required
@in_office(['HQ'])
def new_office_head(office_name):
    """Change the head of the office

    :param office_name: The name of the office to edit
    :return: render_template() or redirect()
    """
    office_obj = Office.by_name_short(office_name)

    form = EditOfficeHead(office_name=office_name)
    members = Office.select_field_members(office_name)

    # Make sure there are new members to choose from
    if len(members) <= 1:
        flash('You need more than one member in the office in order to change the head!', 'danger')
        return redirect(url_for('office', office_name=office_name))
    # Subtract existing head
    members.remove((office_obj.head.steam_id, office_obj.head.arma_name))
    form.head.choices = members

    # Add office name to form to allow for validation
    if request.method == 'POST':
        form.office_name.data = office_name
    if form.validate_on_submit():
        Office.change_head(
            office_name,
            form.head.data)
        flash('Head successfully changed!', 'success')
        return redirect(url_for('office', office_name=office_name))

    return render_template('offices/edit_head.html', form=form, office=office_obj)
