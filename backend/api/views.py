#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request
from flask_restful import reqparse
from api import app
from api.bigchain_utils import insert_code, insert_scan, get_keypair


@app.route('/', methods=['GET'])
def index():
    """
    Main route, it works!
    """
    pub, priv = get_keypair()
    return jsonify({"pub": pub, "priv": priv})


# @app.route('/api/register/onboard/', methods=['POST'])
# def onboard():
#     """
#     Save the install_id and pub_key as an asset in DBD, setting ST as the owner.
#     """
#     parser = reqparse.RequestParser()
#     parser.add_argument('pub_key', type=str, required=True)
#     parser.add_argument('install_id', type=str, required=True)
#     request_params = parser.parse_args()
#
#     result = onboard_user(request_params['pub_key'], request_params['install_id'])
#
#     return jsonify(result)


@app.route('/api/codes/add/', methods=['POST'])
def add_code():
    """
    Add a code as asset to BDB.
    """
    data = request.get_json(force=True)

    if not data.get('message', None):
        return jsonify(error="Message is required."), 400
    result = insert_code(data)

    return jsonify(result)


@app.route('/api/scans/add/', methods=['POST'])
def add_scan():
    """
    Add a scan as asset to BDB and transfer the ownership to the client.
    Assign the points to the users public key.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('message', type=str, required=True)
    parser.add_argument('uuid', type=str, required=True)
    parser.add_argument('lat', type=float, required=True)
    parser.add_argument('lng', type=float, required=True)
    request_params = parser.parse_args()

    result = insert_scan(request_params)

    return jsonify(result)


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
