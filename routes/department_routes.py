from flask import Blueprint, jsonify, request
from controllers.department_controller import DepartmentController
from decorators.token_decorator import role, token

department_module = Blueprint("department",__name__)
controller = DepartmentController()

@department_module.post('/')
@token
@role("Admin")
def create():
  response, code = controller.create(request.get_json())
  return jsonify(response), code
  # return jsonify({}), 200

