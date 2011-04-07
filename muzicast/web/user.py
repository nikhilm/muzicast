import string
import random
from hashlib import sha1
from flask import Module, url_for, redirect, session, escape, request, current_app, abort, flash
from sqlobject.main import SQLObjectNotFound

from muzicast.web.util import render_master_page
from muzicast.web.playlist import set_active
from muzicast.meta import User, Playlist

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
            if not request.form['username']:
                flash("Please enter a username", "error")
            elif not request.form['password']:
                flash("Please enter a password!", "error")
            elif not request.form['secret_answer']:
                flash("Please enter secret answer!", "error")
            else:
                user = User(username=request.form['username'],
                            password=sha1(request.form['password']).hexdigest(),
                            secret_question=request.form['secret_question'],
                            secret_answer=sha1(request.form['secret_answer']).hexdigest())
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
                session['user'] = {'username': user.username, 'current_playlist': -1}
                if user.current_playlist != -1:
                    set_active(user.current_playlist)
                success = True
        except SQLObjectNotFound:
            flash("No such user exists!", "error")

    if success:
        return redirect(url_for('main.index'))
    else:
        return render_master_page('login.html', title='Muzicast: Login')

@user.route('/forgotpassword')
def forgot_password():
    return render_master_page('forgot_password_1.html', title='Password reclamation')

@user.route('/forgotpassword/2', methods=['POST'])
def forgot_password_username():
    sq = user = None
    if not request.form['username']:
        flash("Enter username!", "error")
    else:
        try:
            user = User.byUsername(request.form['username'])
            sq = user.secret_question
        except SQLObjectNotFound:
            flash("No such user!", "error")

    if sq:
        return render_master_page('forgot_password_2.html', title='Answer secret question', user=user.username, secret_question=sq)
    else:
        return redirect(url_for('user.forgot_password'))

@user.route('/forgotpassword/reset', methods=['POST'])
def forgot_password_reset():
    new_pass = None
    if not request.form['username'] or not request.form['secret_answer']:
        flash("Invalid inputs!", "error")
    else:
        try:
            user = User.byUsername(request.form['username'])
            given = sha1(request.form['secret_answer']).hexdigest()
            actual = user.secret_answer

            if given != actual:
                flash("Wrong answer!", "error")
            else:
                new_pass = generate_random_password()
                user.password = sha1(new_pass).hexdigest()
        except SQLObjectNotFound:
            flash("No such user!", "error")

    if new_pass:
        return render_master_page('password_reset.html', title='Password reset', new_password=new_pass)
    else:
        return redirect(url_for('user.forgot_password'))

@user.route('/edit', methods=['GET', 'POST'])
def edit():
    if 'user' not in session:
        return redirect(url_for('user.login'))

    if request.method == 'POST':
        try:
            user = User.byUsername(session['user']['username'])
            if user.password != sha1(request.form['password']).hexdigest():
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

@user.route('/delete', methods=['POST'])
def delete():
    if 'user' not in session:
        return redirect(url_for('user.login'))

    if request.method == 'POST':
        try:
            user = User.byUsername(session['user']['username'])
            if user.password != sha1(request.form['password']).hexdigest():
                flash("Wrong password!", "error")
            else:
                playlists = Playlist.select(Playlist.q.user == user)
                [pl.destroySelf() for pl in playlists]
                user.destroySelf()
                del session['user']
                if 'playlist' in session:
                    del session['playlist']
                flash("User account deleted!")
        except SQLObjectNotFound:
            flash("No such user exists!", "error")

    return render_master_page('user-edit.html', title='Muzicast: Change Password')

@user.route('/logout')
def logout():
    if 'user' in session:
        del session['user']
    return redirect(url_for('main.index'))

def generate_random_password():
    pool = string.ascii_letters + string.digits + string.punctuation
    length = random.randint(6, 10)
    password = ""
    for i in range(length):
        password += random.choice(pool)
    return password
