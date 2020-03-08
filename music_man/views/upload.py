from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort

mod = Blueprint('upload', __name__)


@mod.route('/upload-song')
def index():
    print('inside')

    return render_template(
        'upload.html'
    )
