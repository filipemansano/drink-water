## Sobre
Este projeto foi desenvolvido seguindo os princípios da arquitetura Ports and Adapters, também conhecida como arquitetura hexagonal. Este modelo arquitetônico permite isolar completamente a lógica de negócios dos frameworks e outras tecnologias externas, facilitando tanto os testes quanto futuras atualizações ou modificações de conectores e/ou portas.

Por exemplo, na camada de persistência, foi utilizado o MongoDB. No entanto, a lógica essencial, localizada na pasta services, opera independentemente deste detalhe técnico, interagindo apenas com interfaces abstratas. Isso significa que é possível substituir o MongoDB por um sistema de banco de dados relacional, como o SQL Server, sem que haja impacto na lógica central da aplicação.

Similar flexibilidade se aplica à camada HTTP: atualmente implementada com o Flask, ela poderia ser facilmente substituída por outro framework como FastAPI, AWS Lambda functions, ou similares, sem causar transtornos significativos.

Na camada de eventos, foi implementado um sistema local de publicação e assinatura (pub/sub) que opera de forma síncrona. A estrutura já está preparada para integração com qualquer outro sistema de mensageria, como Kafka, AWS SQS, RabbitMQ, entre outros. Essa preparação assegura que a expansão ou modificação do sistema de eventos possa ser realizada com mínima dificuldade.

Em resumo, este projeto exemplifica uma aplicação  modular e facilmente adaptável, que se beneficia da separação de preocupações e da flexibilidade proporcionada pela arquitetura hexagonal.

## Arquitetura
```
|-- source/
    |-- api/
    |   |-- helpers.py
    |   |-- flask/
    |       |-- person_api.py
    |       |-- drink_api.py
    |-- config/
    |   |-- config.yaml
    |   |-- settings.py
    |-- database/
    |   |-- mongodb_connection.py
    |-- enums/
    |   |-- gender_enum.py
    |   |-- drink_event_enum.py
    |   |-- meta_period_enum.py
    |   |-- meta_event_enum.py
    |   |-- person_event_enum.py
    |-- events/
    |   |-- drink_events_listener.py
    |   |-- event_manager.py
    |   |-- adapters/
    |       |-- local_event_adapter.py
    |       |-- sqs_event_adapter.py
    |-- factories/
    |   |-- messaging_factory.py
    |   |-- repository_factory.py
    |-- model/
    |   |-- meta_model.py
    |   |-- meta_history_model.py
    |   |-- drink_model.py
    |   |-- person_model.py
    |   |-- validators/
    |       |-- base_validator.py
    |-- repository/
    |   |-- abstract/
    |   |   |-- drink_repository.py
    |   |   |-- person_repository.py
    |   |-- mongodb/
    |       |-- drink_repository.py 
    |       |-- person_repository.py
    |-- services/
    |   |-- person_service.py
    |   |-- auth_service.py
    |   |-- drink_service.py
    |   |-- helpers.py
    |-- tests/
        |-- repository/
        |   |-- mongodb/
        |-- services/
            |-- person_test.py
```

* `api/` possui uma pasta para o framework Flask e potencialmente outros frameworks que possamos querer suportar no futuro.
* `config/` contém todos os arquivos de configuração, centralizando as definições que afetam o projeto todo.
* `repository/` está dividido em abstract/ para interfaces e pastas específicas de implementação (como mongodb/) para cada tipo de banco de dados suportado.
* `enums/` enumerações em geral.
* `services/` contém a lógica do negocio desacoplado do resto da aplicação.
* `model/`contém a representação dos objetos que o sistema utiliza


## Instalação
1 - crie um arquivo .env na raiz do projeto com a seguinte estrutura
```
MONGO_HOST=
MONGO_USERNAME=
MONGO_PASSWORD=
JWT_SECRET_KEY=
```

2 - crie e ative um ambiente virtual
```
python3 -m venv env
source ./env/bin/activate
```

3 - instale as dependencias a partir do requirements.txt
```
pip3 install -r requirements.txt
```

4 - execute a aplciação
```
python3 main.py
```

## Utilização

[POST] /person (criar uma nova conta)
```curl
curl --location 'http://127.0.0.1:5003/person/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Filipe Mansano",
    "age": 31,
    "weight": 82.5,
    "gender": 1,
    "email": "filipemansano@gmail.com",
    "password": "abc"
}'
```

[POST] /login (autenticar)
```curl
curl --location 'http://127.0.0.1:5003/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "filipemansano@gmail.com",
    "password": "abc"
}'
```

[GET] /person/ (obter detalhes do usuário logado)
```curl
curl --location 'http://127.0.0.1:5003/person/' \
--header 'Authorization: Bearer <token>'
```

[PATCH] /person/ (atualizar dados usuário logado)
```curl
curl --location --request PATCH 'http://127.0.0.1:5003/person/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer  <token>' \
--data '{
    "name": "Mansano"
}'
```

[DELETE] /person/ (deletar o usuário logado)
```curl
curl --location 'http://127.0.0.1:5003/person/' \
--header 'Authorization: Bearer <token>'
```

[POST] /person/meta (criar uma nova meta)
```curl
curl --location 'http://127.0.0.1:5003/person/meta' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer  <token>' \
--data '{
    "quantity": 2000, (Valor em ML)
    "period": 1  (1 = Diario, 2 = Semanal)
}'
```

[POST] /person/meta/{meta-id} (atualizar uma meta)
```curl
curl --location --request PATCH 'http://127.0.0.1:5003/person/meta/{meta-id}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer  <token>' \
--data '{
    "quantity": 1502
}'
```

[DELETE] /person/meta/{meta-id} (deletar uma meta)
```curl
curl --location --request DELETE 'http://127.0.0.1:5003/person/meta/{meta-id}' \
--header 'Authorization: Bearer  <token>'
```

[POST] /drink (inserir um registro de bebida)
```curl
curl --location 'http://127.0.0.1:5003/drink/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer  <token>' \
--data '{
    "ml": 10
}'
```

[DELETE] /drink/{drink-id} (deletar uma registro de bebida)
```curl
curl --location --request DELETE 'http://127.0.0.1:5003/drink/{drink-id}' 
--header 'Authorization: Bearer  <token>'
```

## Histórico
Toda vez que um novo registro de bebida é inserido é atualizado as metas que tem esse resultado gravado na coleção do mongodb
```json
{
  "_id": {
    "$oid": "662eec68ca20b7e8fc1beb61"
  },
  "meta": {
    "quantity": 1502,
    "id": "be10de6c-be29-49d3-8c3b-1777851cba1b",
    "period": 1
  },
  "inactive": false,
  "start": {
    "$date": "2024-04-28T00:00:00.000Z"
  },
  "end": {
    "$date": "2024-04-28T23:59:59.999Z"
  },
  "ml_dring": 10,
  "ml_drink_left": 1492,
  "achieved": false
}
```