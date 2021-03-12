from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)
#  template_folder='./template',
#  static_folder='./static')
#  static_url_path='/static')


@auth.route('/', defaults={'path': ''})
@auth.route('/<path:path>')
def login(path):
    # return "this is for logging in"
    return render_template('index.html')
