import os
import sys
import signal

try: import simplejson as json
except ImportError: import json

from flask import Module, render_template, url_for, redirect, session, escape, request, jsonify, current_app

from flaskext.principal import Principal, Permission, RoleNeed, PermissionDenied, Identity, identity_changed, identity_loaded

from muzicast.web.util import is_first_run
from muzicast.config import GlobalConfig

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

    paths = []

    config = GlobalConfig()
    if 'collection' in config and 'paths' in config['collection']:
        paths = config['collection']['paths']

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
            d = {'data': entry, 'metadata': path, 'state': 'closed', 'attr': {}}
            if path in paths:
                d['attr']['class'] = "jstree-checked"
            else:
                for p in paths:
                    if p.startswith(path):
                        d['attr']['class'] = "jstree-undetermined"
            ret.append(d)

    return jsonify(tree=ret)

@admin.route('/stop', methods=['POST'])
def stop():
    signal.alarm(1)
    #TODO: do cleanup
    return render_template('admin/stopped.html')
    #TODO: do more cleanup

@admin.route('/rescan', methods=['POST'])
def rescan():
    # TODO(nikhil) rescan
    return redirect(url_for('/'))

@admin.route('/save_directories', methods=['POST'])
def save_directories():
    config = GlobalConfig()
    collection_paths = []
    if 'collection' in config and 'paths' in config['collection']:
        collection_paths = config['collection']['paths']

    paths = set()
    def parse_paths(root, base=''):
        """
        If class is jstree-undetermined
        some directory below it is checked so
        we have to crawl this level.

        If it is jstree-unchecked, don't bother

        If it is jstree-checked, we handle it, but
        we don't need to crawl lower.
        """

        if not 'class' in root['attr']:
            return

        if root['data'] == 'Computer' and base is '':
            # TODO(nikhil) handle windows
            root['data'] = '/'

        abspath = os.path.join(base, root['data'])

        if 'class' in root['attr'] and 'jstree-checked' in root['attr']['class']:
            paths.add(abspath)
            return
        elif 'class' in root['attr'] and 'jstree-undetermined' in root['attr']['class']:
            for cp in collection_paths:
                if cp.startswith(abspath):
                    paths.add(cp)

        if abspath in collection_paths and 'jstree-unchecked' in root['attr']['class']:
            collection_paths.remove(abspath)
            paths.remove(abspath)

        crawl = 'jstree-undetermined' in root['attr']['class']
        if crawl and 'children' in root:
            for child in root['children']:
                parse_paths(child, os.path.join(base, root['data']))

    listing = json.loads(request.data)
    parse_paths(listing[0])

    if not 'collection' in config:
        config['collection'] = {'paths': []}
    config['collection']['paths'] = list(paths)
    config.save()

    return jsonify(success=True)

def shutdown(signal, stack_frame):
    sys.exit(0)
signal.signal(signal.SIGALRM, shutdown)
