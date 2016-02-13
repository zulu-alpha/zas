from flask import render_template, flash, redirect, url_for, request

from app.util.permission import in_office, in_office_dynamic

from app import app, flask_login
from app.models import User, Office
from app.forms import CreateOffice


@app.route('/office/create', methods=['GET', 'POST'])
@flask_login.login_required
@in_office(['HQ'])
def create_office():
    """Create a new office"""
    form = CreateOffice()
    form.head.choices = User.select_field_ranked()

    if form.validate_on_submit():
        office = Office.create_office(
            form.name.data,
            form.name_short.data,
            form.head.data)
        flash('Office successfully created!', 'success')
        return redirect(url_for('office', name=office.name_short))

    return render_template('offices/create_office.html', form=form)


@app.route('/office/<name>')
def office(name):
    office_obj = Office.by_name_short(name)

    if not office_obj:
        flash('An office named {0} was not found!'.format(name), 'warning')
        return redirect(url_for('home'))

    return render_template(
        'offices/office.html',
        office=office_obj,
        has_permission=in_office_dynamic(['HQ'], [name])
    )
