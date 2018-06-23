#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request
from flask_restful import reqparse

from . import app
from .formatters import format_cause_response, format_history_response, get_mocked_info_response_format, \
    get_euipo_format
from .services import gs1, recheck, bigchain


@app.route('/', methods=['GET'])
def index():
    """
    Main route, it works!
    """
    return jsonify({})

# MOCK SCANTRUST BACKEND
# urls need to stay the same (api/v2) since the various frontend components 
# take a host:port as base, not a full base url (e.g. :5000/api/v2/) 


@app.route('/api/v2/', methods=['GET'])
def api_index():
    """
    Main route, it works!
    """
    return jsonify({})


@app.route('/api/v2/consumer/scan/<string:uuid>/combined-info/', methods=['GET'])
def combined_info(uuid):
    """
    Main route, it works!
    """
    return jsonify(get_mocked_info_response_format(uuid))

# OTHER EXTERNAL SERVICES 
# * gs1 - calls the cloud gs1 services
# * recheck - uses a simple mock response, to avoide dependency on a in-dev mode service


@app.route('/api/gs1/', methods=['GET', 'POST'])
def get_gs1():
    """
    Call the cloud.gs1.org service to retrieve data based on the gtin.  
    """
    parser = reqparse.RequestParser()
    parser.add_argument('gtin', type=str, required=True)
    params = parser.parse_args()

    data = gs1.get_gtin(params.get('gtin'))
    return jsonify(data)


@app.route('/api/mock-services/recheck/')
def get_recheck():
    """
    Returns mock data as a standin as for the under-development ReCheck 
    service.  Also allows the local demo to run without a live service
    """
    data = recheck.DEFAULT_DATA
    return jsonify(data)


# APP ROUTES

@app.route('/api/users/info/', methods=['POST'])
def user_info():
    """
    Save the install_id and pub_key as an asset in DBD, setting ST as the owner.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('pub_key', type=str, required=True)
    request_params = parser.parse_args()

    user = bigchain.find_asset("\"scantrust:userdata\"  \"user\" \"%s\"" % request_params['pub_key'])
    if user:
        user["data"]["points"] = bigchain.get_points(request_params['pub_key'])
        return jsonify(user['data'])

    result = bigchain.onboard_user(request_params['pub_key'])
    result["points"] = bigchain.get_points(request_params['pub_key'])
    return jsonify(result)


@app.route('/api/users/history/', methods=['POST'])
def user_history():
    """
    Get the donation (transaction) history for a user.
    Grouped by cause.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('pub_key', type=str, required=True)
    request_params = parser.parse_args()
    history = bigchain.get_spent_tokens_public_key(request_params["pub_key"])

    return jsonify(format_history_response(history))


@app.route('/api/scans/add/', methods=['POST'])
def add_scan():
    """
    Add a scan as asset to BDB and transfer the ownership to the client.
    Assign the points to the users public key.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('message', type=str, required=True)
    parser.add_argument('pub_key', type=str, required=True)
    parser.add_argument('uuid', type=str, required=True)
    parser.add_argument('lat', type=float, required=True)
    parser.add_argument('lng', type=float, required=True)
    request_params = parser.parse_args()

    code = bigchain.find_asset("\"scantrust:codes\" \"%s\"" % request_params['message'])

    if not code:
        return not_found()

    transaction = {}
    transactions = bigchain.get_transactions(code['id'])
    points_awarded = False
    if len(transactions) >= 1:
        transaction = transactions[len(transactions) - 1]
    if transaction and not transaction['metadata'].get('is_consumed', True):
        # Create a new transaction to self, where the metadata states is_consumed=True
        # Assign points
        bigchain.transfer_asset_to_self(transaction["id"], {"is_consumed": True})
        bigchain.transfer_divisible_asset(request_params["pub_key"], code["data"]["points"])
        points_awarded = True

    scan_asset, new = bigchain.insert_scan(request_params, code["id"])
    if new:
        bigchain.transfer_st_asset(scan_asset, request_params["pub_key"], {})

    return jsonify(
        {
            "scan_asset_id": scan_asset,
            "points_awarded": points_awarded,
            "code_value": code["data"]["points"],
            "euipo_data": get_euipo_format()
        }
    )


@app.route('/api/causes/', methods=['GET'])
def get_causes():
    """
    Return a simple list of causes registered on the blockchain.
    """
    causes = bigchain.find_asset("\"scantrust:cause\"", multiple=True)
    return jsonify(format_cause_response(causes))


@app.errorhandler(404)
def not_found(error=None):
    """
    Handles 404 errors.
    """
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
