from flask import Blueprint, request, jsonify, current_app
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
    return jsonify(person.model_dump()), 201

@person_blueprint.route('/<person_id>', methods=['PATCH'])
def update_person(person_id):
    data = request.json
    
    try:
        Person.model_validate(obj=data, context={'mode':'update'})
    except ValidationError as e:
        return format_validation_error(e)
    
    current_app.config['services']['person'].update_person(person_id=person_id, **data)
    return jsonify({'message': 'Person updated'}), 200

@person_blueprint.route('/<person_id>', methods=['GET'])
def get_person(person_id):
    person = current_app.config['services']['person'].get_person(person_id)
    if person:
        return jsonify(person.model_dump()), 200
    return jsonify({'message': 'Person not found'}), 404

@person_blueprint.route('/<person_id>', methods=['DELETE'])
def delete_person(person_id):
    current_app.config['services']['person'].delete_person(person_id)
    return jsonify({'message': 'Person deleted successfully'}), 200

@person_blueprint.route('/<person_id>/meta', methods=['POST'])
def add_meta(person_id):
    data = request.json
    try:
        Meta.model_validate(obj=data, context={'mode':'create'})
    except ValidationError as e:
        return format_validation_error(e)
    
    meta = current_app.config['services']['person'].add_meta(person_id=person_id,**data)
    return jsonify(meta.model_dump()), 201

@person_blueprint.route('/<person_id>/meta/<meta_id>', methods=['PATCH'])
def update_meta(person_id, meta_id):
    data = request.json
    try:
         Meta.model_validate(obj=data, context={'mode':'update'})
    except ValidationError as e:
        return format_validation_error(e)
    
    current_app.config['services']['person'].update_meta(person_id=person_id, meta_id=meta_id, **data)
    return jsonify({'message': 'Meta updated successfully'}), 200

@person_blueprint.route('/<person_id>/meta/<meta_id>', methods=['DELETE'])
def remove_meta(person_id, meta_id):
    current_app.config['services']['person'].remove_meta(person_id, meta_id)
    return jsonify({'message': 'Meta removed successfully'}), 200