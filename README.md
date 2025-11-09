# Composite-Microservice

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Microservice URLs

- User Service: https://users-api-121084561869.us-central1.run.app
- Item Service: https://microservice-item-848539791549.us-central1.run.app
- Transaction Service: http://34.172.7.104:8000

## OpenAPI Python Client

```bash
openapi-python-client generate --path ./client/openapi-item.json --output-path ./client/item
openapi-python-client generate --path ./client/openapi-transaction.json --output-path ./client/transaction
openapi-python-client generate --path ./client/openapi-user.json --output-path ./client/user
```
