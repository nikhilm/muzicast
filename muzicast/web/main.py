from flask import Module, render_template, url_for, redirect, session, escape, request

from muzicast.web.util import is_first_run

main = Module(__name__)

@main.route('/')
def index():
    #just do first run check
    if is_first_run():
        return redirect(url_for('admin.index'))

    # TODO: will need attributes for template
    return render_template('home')
