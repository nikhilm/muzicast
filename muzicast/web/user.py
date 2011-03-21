from hashlib import sha1
from flask import Module, url_for, redirect, session, escape, request, current_app, abort, flash
from sqlobject.main import SQLObjectNotFound

from muzicast.web.util import render_master_page
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
            	flash("Wrong password!")
            else:
                # login successful
            	session['username'] = user.username
            	success = True
        except SQLObjectNotFound:
            flash("No such user exists!", "error")

    if success:
    	return redirect(url_for('main.index'))
    else:
        return render_master_page('login.html', title='Muzicast: Login')
