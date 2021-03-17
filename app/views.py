# import ldap
from flask import Blueprint, render_template, g, jsonify
from flask_login import login_required
import requests
from .commonutils import CommonUtils
import json


main = Blueprint('main', __name__)
# #  template_folder='./template',
# #  static_folder='./static')
# #  static_url_path='/static')
comutilsobj = CommonUtils()

# # @auth.route('/', defaults={'path': ''})
# # @auth.route('/<path:path>')


@main.route('/')
@main.route('/home')
@login_required
# def home(path):
def home():
    # return "this is for logging in"
    return render_template('index.html')


@main.route('/getjigtable')
@login_required
def getjigtable():
    try:
        ret_data = {'status': True, 'error': '', 'rslt': ''}
        print("Getting Jigs Table Details")
        url = "http://192.168.0.103:8081/fprestapi/jigstbl"
        # data = {'jigid': 90}
        data = {}
        params = {'data': json.dumps(data)}
        data = comutilsobj.api_call_retry(url=url, parameters=params)
        jig_details = data['rslt']
        table_data = []
        for each in jig_details['idlejigs']:
            table_data.append(each)
        for each in jig_details['brokenjigs']:
            table_data.append(each)
        ret_data['rslt'] = table_data
        # main.logger.info(jig_details)
    except Exception as errmsg:
        # main.logger.error(str(errmsg))
        ret_data = {'status': False, 'error': str(errmsg), 'rslt': ''}
    return jsonify(ret_data)
