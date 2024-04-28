from flask import Blueprint, request, jsonify, current_app
from pydantic import ValidationError

from source.api.helpers import format_validation_error
from source.model.drink_model import Drink

drink_blueprint = Blueprint('drink', __name__)

@drink_blueprint.route('/<person_id>', methods=['POST'])
def add_drink(person_id):
    data = request.json
    try:
        Drink.model_validate(obj={"person_id": person_id, **data}, context={'mode':'create'})
    except ValidationError as e:
        return format_validation_error(e)
    
    drink = current_app.config['services']['drink'].create_drink(person_id, **data)
    return jsonify(drink.model_dump()), 201

@drink_blueprint.route('/<person_id>/<drink_id>', methods=['DELETE'])
def remove_drink(person_id, drink_id):
    current_app.config['services']['drink'].remove_drink(person_id, drink_id)
    return jsonify({'message': 'Drink removed successfully'}), 200