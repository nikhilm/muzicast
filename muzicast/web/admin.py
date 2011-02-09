import sys
import signal

from flask import Module, render_template, url_for, redirect, session, escape, request

from flaskext.principal import Principal, Permission, RoleNeed, PermissionDenied, Identity, identity_changed, identity_loaded

from muzicast.web.util import is_first_run

admin = Module(__name__)

principals = Principal(admin)
admin_permission = Permission(RoleNeed('admin'))

@admin.route('/')
def index():
    # if it's the first run, we allow in
    # otherwise we ask for the password
    if is_first_run():
        identity_changed.send(admin, identity=Identity('admin'))

    try:
        admin_permission.test()
        return render_template('admin/index.html')
    except PermissionDenied:
        return redirect(url_for('login'))

@identity_loaded.connect
def on_admin_login(sender, identity):
    identity.provides.add(RoleNeed('admin'))

@admin.route('/login', methods=['POST', 'GET'])
def login():
    wrong = False
    if request.method == 'POST':
# TODO use actual password
        if request.form['password'] == 'password':
            session['admin'] = True
            identity_changed.send(admin, identity=Identity('admin'))
            return redirect(url_for('index'))
        else:
            wrong = True
    return render_template('admin/login.html', wrong=wrong)

@admin.route('/stop', methods=['POST'])
def stop():
    signal.alarm(1)
    #TODO: do cleanup
    return render_template('admin/stopped.html')
    #TODO: do more cleanup

@admin.route('/password', methods=['POST'])
def change_password():
    pass

def shutdown(signal, stack_frame):
    sys.exit(0)
signal.signal(signal.SIGALRM, shutdown)
