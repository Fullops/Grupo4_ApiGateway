from flask import Flask, jsonify, request  
from dotenv import dotenv_values
from flask_cors import CORS
from decorators.token_decorator import token
from routes.auth_routes import auth_module
from routes.department_routes import department_module
from flask_jwt_extended import JWTManager

app = Flask(__name__)
cors = CORS(app)
config = dotenv_values('.env')
jwt = JWTManager(app)
app.register_blueprint(auth_module,url_prefix='/auth')
app.register_blueprint(department_module, url_prefix='/facultades')
app.config["JWT_SECRET_KEY"]=config['JWT_SECRET']

@app.route('/')
def hello_world():
  dictToReturn = {'message': 'Hola mundo!'}
  return jsonify(dictToReturn)

if __name__ == '__main__':
    app.run(host='localhost', port=config["PORT"], debug=True)