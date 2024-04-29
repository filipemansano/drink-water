from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from pydantic import ValidationError

from source.model.meta_model import Meta
from source.model.person_model import Person
from source.api.helpers import format_validation_error

person_blueprint = Blueprint('person', __name__)

@person_blueprint.route('/', methods=['POST'])
def create_person():
    data = request.json
    try:
        Person.model_validate(obj=data, context={'mode':'create'})
    except ValidationError as e:
        return format_validation_error(e)
    
    person = current_app.config['services']['person'].create_person(**data)
    return jsonify(person.model_dump(exclude='password')), 201

@person_blueprint.route('/', methods=['PATCH'])
@jwt_required()
def update_person():
    data = request.json
    try:
        Person.model_validate(obj=data, context={'mode':'update'})
    except ValidationError as e:
        return format_validation_error(e)
    
    person_id = get_jwt_identity()
    current_app.config['services']['person'].update_person(person_id=person_id, **data)
    return jsonify({'message': 'Person updated'}), 200

@person_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_person():
    person_id = get_jwt_identity()
    person = current_app.config['services']['person'].get_person(person_id)
    if person:
        return jsonify(person.model_dump(exclude='password')), 200
    return jsonify({'message': 'Person not found'}), 404

@person_blueprint.route('/', methods=['DELETE'])
@jwt_required()
def delete_person():
    person_id = get_jwt_identity()
    current_app.config['services']['person'].delete_person(person_id)
    return jsonify({'message': 'Person deleted successfully'}), 200

@person_blueprint.route('/meta', methods=['POST'])
@jwt_required()
def add_meta():
    person_id = get_jwt_identity()
    data = request.json
    try:
        Meta.model_validate(obj=data, context={'mode':'create'})
    except ValidationError as e:
        return format_validation_error(e)
    
    meta = current_app.config['services']['person'].add_meta(person_id=person_id,**data)
    return jsonify(meta.model_dump()), 201

@person_blueprint.route('/meta/<meta_id>', methods=['PATCH'])
@jwt_required()
def update_meta(meta_id):
    data = request.json
    try:
         Meta.model_validate(obj=data, context={'mode':'update'})
    except ValidationError as e:
        return format_validation_error(e)
    
    person_id = get_jwt_identity()
    current_app.config['services']['person'].update_meta(person_id=person_id, meta_id=meta_id, **data)
    return jsonify({'message': 'Meta updated successfully'}), 200

@person_blueprint.route('/meta/<meta_id>', methods=['DELETE'])
@jwt_required()
def remove_meta(meta_id):
    person_id = get_jwt_identity()
    current_app.config['services']['person'].remove_meta(person_id, meta_id)
    return jsonify({'message': 'Meta removed successfully'}), 200