from flask import render_template, flash, redirect, url_for

from app import app, flask_login
from app.models import User, Office
from app.forms import CreateOffice


@app.route('/create-office', methods=['GET', 'POST'])
@flask_login.login_required
def create_office():
    """Create a new office"""
    form = CreateOffice()
    form.members.choices = User.select_field_ranked()

    if form.validate_on_submit():
        Office.create_office(
            form.name.data,
            form.name_short.data,
            form.members.data)
        flash('Office successfully created!', 'success')
        return redirect(url_for('home'))

    return render_template('offices/create_office.html', form=form)
