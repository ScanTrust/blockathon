#! /usr/bin/env python
# -*- coding: utf-8 -*
import flask_restful
from flask import Flask
from flask_cors import CORS


import conf

# Create Flask application
app = Flask(__name__)
app.debug = True

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = 'qsdkqlsdjfghhliqjkyezgkjl'

# Allow CORS requests
CORS(app)
# REST Web service

api = flask_restful.Api(app=app)

import api.views
import mock_st_backend.views