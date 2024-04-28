from flask import Flask
from source.api.flask.person_api import person_blueprint
from source.api.flask.drink_api import drink_blueprint
from source.events.drink_events_listener import DrinkEventListener
from source.factories.messaging_adapter import MessagingFactory
from source.factories.repository_factory import RepositoryFactory
from source.repository.drink_repository import IDrinkRepository
from source.repository.person_repository import IPersonRepository
from source.services.drink_service import DrinkService
from source.services.person_service import PersonService

repo_factory = RepositoryFactory()
messasing_factory = MessagingFactory()

person_service = PersonService(
    repository=repo_factory.get_repository(IPersonRepository),
)

drink_service = DrinkService(
    repository=repo_factory.get_repository(IDrinkRepository), 
    event_manager=messasing_factory.get_adapter()
)

drink_listener = DrinkEventListener(service=drink_service)
drink_listener.register_listeners()

app = Flask(__name__)
app.config['services'] = {
    'person': person_service,
    'drink': drink_service,
}

app.register_blueprint(person_blueprint, url_prefix='/person')
app.register_blueprint(drink_blueprint, url_prefix='/drink')

if __name__ == '__main__':
    app.run(debug=True, port=5003)