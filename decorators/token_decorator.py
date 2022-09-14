from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import decode_token
import requests
from werkzeug.datastructures import ImmutableMultiDict
from dotenv import dotenv_values
config = dotenv_values('.env')

def token(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.headers.get('Authorization','No hay token')
    parts = token.split()
    if parts[0] != 'Bearer':
      return jsonify({
        'message': 'Token esta mal formateado'
      }), 401
    decoded = decode_token(parts[1])
    http_args = request.args.to_dict()
    http_args['user_id'] = decoded['sub']
    http_args['role'] = decoded['role']
    request.args =  ImmutableMultiDict(http_args)
    result = f(*args, **kwargs)
    return result
  return decorated

def role(role):
  def inner_decorator(f):
    @wraps(f)
    def decorated(*args, **kwargs):
      try:
        headers = {
          "Content-Type": "application/json"
        }
        response = requests.get(f"{config['URL_AUTH']}/api/roles/{role}", headers=headers)
        if response.status_code == 200:
          permission = response.json()
          flag = False
          method = request.method.lower()
          url = request.path
          for p in permission:
            if p['method'].lower() == method and url == p['url']:
              flag = True
              break
          if flag:
            result = f(*args, *kwargs)
            return result
        return jsonify({
          "message": "No tiene permisos"
        }), 403
      except:
        return jsonify({
          "message": "No tiene permisos"
        }), 403
    return decorated
  return inner_decorator
      
