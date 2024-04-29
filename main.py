import os
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
from source.api.flask.person_api import person_blueprint
from source.api.flask.drink_api import drink_blueprint
from source.events.drink_events_listener import DrinkEventListener
from source.factories.messaging_factory import MessagingFactory
from source.factories.repository_factory import RepositoryFactory
from source.repository.abstract.drink_repository import IDrinkRepository
from source.repository.abstract.person_repository import IPersonRepository
from source.services.auth_service import AuthService
from source.services.drink_service import DrinkService
from source.services.person_service import PersonService
from dotenv import load_dotenv

load_dotenv()

repo_factory = RepositoryFactory()
messasing_factory = MessagingFactory()
adapter = messasing_factory.get_adapter()
person_repository = repo_factory.get_repository(IPersonRepository)

person_service = PersonService(
    repository=person_repository,
    event_manager=adapter
)

drink_service = DrinkService(
    repository=repo_factory.get_repository(IDrinkRepository),
    person_repository=person_repository, 
    event_manager=adapter
)

# queue
drink_listener = DrinkEventListener(service=drink_service)
drink_listener.register_listeners()

# http
app = Flask(__name__)
app.config['services'] = {
    'person': person_service,
    'drink': drink_service,
}

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

jwt = JWTManager(app)
auth_service = AuthService(person_repository=person_repository)

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    person = auth_service.authenticate(email, password)
    if person == False:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=person.id)
    return jsonify(access_token=access_token)

app.register_blueprint(person_blueprint, url_prefix='/person')
app.register_blueprint(drink_blueprint, url_prefix='/drink')

if __name__ == '__main__':
    app.run(debug=True, port=5003)