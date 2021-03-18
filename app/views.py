# import ldap
from flask import Blueprint, render_template, g, jsonify, request
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
        for each in jig_details['inusejigs']:
            table_data.append(each)
        ret_data['rslt'] = table_data
        # main.logger.info(jig_details)
    except Exception as errmsg:
        # main.logger.error(str(errmsg))
        ret_data = {'status': False, 'error': str(errmsg), 'rslt': ''}
    return jsonify(ret_data)


@main.route('/postjigdetails', methods=['POST'])
@login_required
def postjigdetails():
    try:
        rec_data = request.get_json()
        ret_data = {'status': True, 'error': '', 'rslt': ''}
        url = "http://192.168.0.103:8081/fprestapi/jigstbl"
        data = {'jigid': rec_data['jigid']}
        params = {'data': json.dumps(data)}
        data = comutilsobj.api_call_retry(url=url, parameters=params)
        jig_details = json.loads(data['rslt'][0]['jig_cfg'])
        jig_details['jigType'] = comutilsobj.remove_unwanted_str(
            jig_details['jigType'])
        ret_data['rslt'] = jig_details
    except Exception as errmsg:
        ret_data = {'status': False, 'error': str(errmsg), 'rslt': ''}
    return jsonify(ret_data)


@main.route('/postreservejig', methods=['POST'])
@login_required
def postreservejig():
    try:
        print('trace : postreservejig')
        rec_data = request.get_json()
        ret_data = {'status': True, 'error': '', 'rslt': ''}
        jigid = rec_data.get('jigid')
        jig_owner = rec_data.get('jigowner')
        url = "http://localhost:8079/api/experimental/dags/reserve_firepit_jig/dag_runs"
        tmp_data = {'jig_owner': jig_owner, 'jig': jigid}
        data1 = json.dumps({"conf": json.dumps(tmp_data)})
        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
        }
        req = requests.post(url, data=data1, headers=headers)
        print(req)
        if str(req.status_code) != '200':
            raise Exception(
                "Error reaching the airflow with response {}".format(req.status_code))
        print(req.text)
        ret_data['rslt'] = req.text
    except Exception as errmsg:
        ret_data = {'status': False, 'error': str(errmsg), 'rslt': ''}
    return jsonify(ret_data)
