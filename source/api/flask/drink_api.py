from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from pydantic import ValidationError

from source.api.helpers import format_validation_error
from source.model.drink_model import Drink

drink_blueprint = Blueprint('drink', __name__)

@drink_blueprint.route('/', methods=['POST'])
@jwt_required()
def add_drink():
    data = request.json
    person_id = get_jwt_identity()
    try:
        Drink.model_validate(obj={"person_id": person_id, **data}, context={'mode':'create'})
    except ValidationError as e:
        return format_validation_error(e)
    
    drink = current_app.config['services']['drink'].create_drink(person_id, **data)
    return jsonify(drink.model_dump()), 201


@drink_blueprint.route('/<person_id>/<drink_id>', methods=['DELETE'])
@jwt_required()
def remove_drink(drink_id):
    person_id = get_jwt_identity()
    current_app.config['services']['drink'].remove_drink(person_id, drink_id)
    return jsonify({'message': 'Drink removed successfully'}), 200