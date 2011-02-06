from flask import Module, render_template, url_for, redirect, session, escape, request

from flaskext.principal import Principal, Permission, RoleNeed, PermissionDenied, Identity, identity_changed, identity_loaded

admin = Module(__name__)

principals = Principal(admin)
admin_permission = Permission(RoleNeed('admin'))

@admin.route('/')
def index():
    try:
        admin_permission.test()
        return "hello admin"
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
