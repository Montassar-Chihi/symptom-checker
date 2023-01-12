from flask import jsonify
import http
from utils.app import app

class MyForbiddenException(Exception):
    def __init__(self, msg='Not permitted with your privileges', status=http.HTTPStatus.FORBIDDEN):
        self.info = {'status': status, 'msgs': [msg]}

_security = app.extensions["security"]

@_security.unauthz_handler
def my_unauthz_handler(func, params):
    raise MyForbiddenException()

@app.errorhandler(MyForbiddenException)
def my_exception(ex):
    return jsonify(ex.info), ex.info['status']