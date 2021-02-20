"""
api.py
- provides the API endpoints for consuming and producing 
  REST requests and responses
"""

#
# omitting inputs and other view functions
#

from functools import wraps
from bottle import request

import jwt
import os
import json


from dotenv import load_dotenv

load_dotenv()


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return json.dumps(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, os.getenv('SECRET_KEY'))
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify