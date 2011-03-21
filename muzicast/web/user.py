from hashlib import sha1
from flask import Module, url_for, redirect, session, escape, request, current_app, abort, flash
from sqlobject.main import SQLObjectNotFound

from muzicast.web.util import render_master_page
from muzicast.web.playlist import set_active
from muzicast.meta import User

user = Module(__name__)

@user.route('/register', methods=['GET', 'POST'])
def register():
    success = False
    user = None
    if request.method == 'POST':
        try:
            user = User.byUsername(request.form['username'])
            flash("Username '%s' is already taken!"%request.form['username'], "error")
        except SQLObjectNotFound:
            # username available
            if not request.form['password']:
                flash("Please enter a password!", "error")
            else:
                user = User(username=request.form['username'], password=sha1(request.form['password']).hexdigest())
                current_app.logger.debug("%s", user)
                success = True

    return render_master_page('register.html', title='Muzicast: Register', registration_successful=success, user=user)

@user.route('/login', methods=['GET', 'POST'])
def login():
    success = False
    if request.method == 'POST':
        try:
            user = User.byUsername(request.form['username'])
            if user.password != sha1(request.form['password']).hexdigest():
                flash("Wrong password!", "error")
            else:
                # login successful
                session['user'] = user
                if user.current_playlist != -1:
                    set_active(user.current_playlist)
                success = True
        except SQLObjectNotFound:
            flash("No such user exists!", "error")

    if success:
        return redirect(url_for('main.index'))
    else:
        return render_master_page('login.html', title='Muzicast: Login')

@user.route('/edit', methods=['GET', 'POST'])
def edit():
    if 'user' not in session:
        return redirect(url_for('user.login'))

    if request.method == 'POST':
        try:
            if session['user'].password != sha1(request.form['password']).hexdigest():
                flash("Wrong password!", "error")
            else:
                new_password = request.form['new-password']
                cnf = request.form['confirm-password']

                if new_password != cnf:
                    flash("New password and Confirm password are not the same!", "error")
                else:
                    user.password = sha1(new_password).hexdigest()
                    flash("Password changed! Please login again.")
                    del session['user']
        except SQLObjectNotFound:
            flash("No such user exists!", "error")

    return render_master_page('user-edit.html', title='Muzicast: Change Password')

@user.route('/logout')
def logout():
    if 'user' in session:
        del session['user']
    return redirect(url_for('main.index'))
