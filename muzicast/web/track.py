from flask import Module, render_template, url_for, redirect, session, escape, request

track = Module(__name__)

@track.route('/<id>')
def index(id):
    return render_template("track.html")
