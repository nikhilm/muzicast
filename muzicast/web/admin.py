import os
import sys
import signal
import string
import threading
import time
from hashlib import sha256

try: import simplejson as json
except ImportError: import json

from flask import Module, render_template, url_for, redirect, session, escape, request, jsonify, current_app, flash

from muzicast.web.principal import Principal, Permission, RoleNeed, PermissionDenied, Identity, identity_changed, identity_loaded

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
        return render_template('admin/index.html', first_run=is_first_run())
    except PermissionDenied:
        return redirect(url_for('login'))

@identity_loaded.connect
def on_admin_login(sender, identity):
    identity.provides.add(RoleNeed('admin'))

@admin.route('/login', methods=['POST', 'GET'])
def login():
    if is_first_run():
        return redirect(url_for('index'))

    wrong = False
    if request.method == 'POST':
        input = sha256(request.form['password']).hexdigest()
        config = GlobalConfig()
        if 'password' not in config:
            wrong = True
        elif input == config['password']:
            session['admin'] = True
            identity_changed.send(admin, identity=Identity('admin'))
            return redirect(url_for('index'))
        else:
            wrong = True
    return render_template('admin/admin_login.html', wrong=wrong)

@admin.route('/password', methods=['POST'])
def change_password():
    try:
        input = sha256(request.form['password']).hexdigest()
        config = GlobalConfig()
        config['password'] = input
        config.save()
        flash("Password changed successfully.")
    except Exception:
        flash("Error changing password!", "error")
    return redirect(url_for('index'))

@admin.route('/dirlist', methods=['GET'])
def dirlist():
    if len(request.args) != 1:
        abort(400)

    paths = []

    config = GlobalConfig()
    if 'collection' in config and 'paths' in config['collection']:
        paths = config['collection']['paths']

    req_path = request.args.keys()[0]
    ret = []

    current_app.logger.debug('req %s %s', req_path, sys.platform)
    if req_path == "/" and sys.platform == 'win32':
        req_path = ''
        drives = []
        for letter in string.uppercase:
            if os.path.exists(letter+":\\"):
                drives.append(letter + ":\\")
	for drive in drives:
            d = {'data': drive, 'metadata': drive, 'state': 'closed', 'attr': {}}
            if drive in paths:
                d['attr']['class'] = "jstree-checked"
            else:
                for p in paths:
                    if p.startswith(drive):
                        d['attr']['class'] = "jstree-undetermined"
            ret.append(d)
	return jsonify(tree=ret)

    for entry in os.listdir(os.path.join(req_path)):
        path = os.path.join(req_path, entry)
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
    def kill():
        os.kill(os.getpid(), signal.SIGINT)
    t = threading.Timer(2, kill)
    t.start()
    return render_template('admin/stopped.html')

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
            if sys.platform == 'win32':
	        root['data'] = ''
	    else:
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
    config['collection']['paths_saved_at'] = int(time.time())
    config.save()

    return jsonify(success=True)
