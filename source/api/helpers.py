from flask import jsonify

def format_validation_error(e):
    errors = [{"field": (error['loc'][0] if error['loc'] else 'root'), "message": error['msg']} for error in e.errors()]
    return jsonify({"message": "validation error", "errors": errors}), 400