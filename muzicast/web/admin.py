import os
import sys
import signal

try: import simplejson as json
except ImportError: import json

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

@admin.route('/password', methods=['POST'])
def change_password():
    pass

@admin.route('/dirlist', methods=['GET'])
def dirlist():
    if len(request.args) != 1:
        abort(400)

    req_path = request.args.keys()[0]
    # TODO: lots of security checks
    if req_path == "/":
        # TODO: on windows for root, get drive letters
        pass

    ret = []
    for entry in os.listdir(req_path):
        path = os.path.join(req_path, entry)
        # TODO: don't set state if no subdir
        if os.path.isdir(path):
            ret.append({'data': entry, 'metadata': path, 'state': 'closed'})

    return json.dumps(ret)

@admin.route('/stop', methods=['POST'])
def stop():
    signal.alarm(1)
    #TODO: do cleanup
    return render_template('admin/stopped.html')
    #TODO: do more cleanup

def shutdown(signal, stack_frame):
    sys.exit(0)
signal.signal(signal.SIGALRM, shutdown)
