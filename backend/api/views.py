#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request
from flask_restful import reqparse
from api import app
import api.bigchain_utils as utils
from api.formatters import format_cause_response, format_history_response
from . import gs1


@app.route('/', methods=['GET'])
def index():
    """
    Main route, it works!
    """
    return jsonify({})


@app.route('/api/users/info/', methods=['POST'])
def user_info():
    """
    Save the install_id and pub_key as an asset in DBD, setting ST as the owner.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('pub_key', type=str, required=True)
    request_params = parser.parse_args()

    user = utils.find_asset("\"scantrust:userdata\"  \"user\" \"%s\"" % request_params['pub_key'])
    if user:
        user["data"]["points"] = utils.get_points(request_params['pub_key'])
        return jsonify(user['data'])

    result = utils.onboard_user(request_params['pub_key'])
    result["points"] = utils.get_points(request_params['pub_key'])
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
    history = utils.get_spent_tokens_public_key(request_params["pub_key"])

    return jsonify(format_history_response(history))


@app.route('/api/gs1/', methods=['GET', 'POST'])
def get_gs1():
    parser = reqparse.RequestParser()
    parser.add_argument('gtin', type=str, required=True)
    params = parser.parse_args()

    data = gs1.get_gtin(params.get('gtin'))
    return jsonify(data)


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

    code = utils.find_asset("\"scantrust:codes\" \"%s\"" % request_params['message'])

    if not code:
        return not_found()

    transaction = {}
    transactions = utils.get_transactions(code['id'])
    points_awarded = False
    if len(transactions) >= 1:
        transaction = transactions[len(transactions) - 1]
    if transaction and not transaction['metadata'].get('is_consumed', True):
        # Create a new transaction to self, where the metadata states is_consumed=True
        # Assign points
        utils.transfer_asset_to_self(transaction["id"], {"is_consumed": True})
        utils.transfer_divisible_asset(request_params["pub_key"], code["data"]["points"])
        points_awarded = True

    scan_asset, new = utils.insert_scan(request_params, code["id"])
    if new:
        utils.transfer_st_asset(scan_asset, request_params["pub_key"], {})

    return jsonify({"scan_asset_id": scan_asset, "points_awarded": points_awarded, "code_value": code["data"]["points"]})


@app.route('/api/causes/', methods=['GET'])
def get_causes():
    """
    Return a simple list of causes registered on the blockchain.
    """
    causes = utils.find_asset("\"scantrust:cause\"", multiple=True)
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
