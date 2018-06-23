#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request
from flask_restful import reqparse
from api import app
import api.bigchain_utils as utils
from api.formatters import format_cause_response, format_history_response, get_mocked_info_response_format


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