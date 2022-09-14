import datetime
from email import header
from dotenv import dotenv_values
config = dotenv_values('.env')
import requests
from flask_jwt_extended import create_access_token

class AuthController():
  def __init__(self):
    pass
  
  def login(self, data):
    exp_time = int(config['JWT_EXPIRATION'])
    headers = {
      "Content-Type": "application/json"
    }
    response = requests.post(url=f"{config['URL_AUTH']}/api/auth/",json=data, headers=headers)
    if response.status_code == 200:
      user = response.json()
      expires = datetime.timedelta(seconds=exp_time)
      access_token = create_access_token(identity=user['id'],
      expires_delta=expires,
      additional_claims={
        # 'role': user['role']['name'],
        'fullName': user['fullName']
      })
      return {
        "id": user['id'],
        "access_token": access_token
      }, 200
    return {
      "message": "Credenciales invalidas"
    }, 401
  
  def me(self, id):
    headers = {
      "Content-Type": "application/json"
    }
    response = requests.get(url=f"{config['URL_AUTH']}/api/users/{id}", headers=headers)
    if response.status_code == 200:
      return response.json(), 200
    return response.json(), 
    