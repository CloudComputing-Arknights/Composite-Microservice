# Composite-Microservice

Live Demo: https://composite-microservice-191058157831.us-west2.run.app

API Gateway: https://composite-gateway-2frr3e2v.wl.gateway.dev

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
openapi-python-client generate --path ./openapi/openapi-item.json --output-path ./app/client/item
openapi-python-client generate --path ./openapi/openapi-transaction.json --output-path ./app/client/transaction
openapi-python-client generate --path ./openapi/openapi-user.json --output-path ./app/client/user
```

## Google Cloud Artifact Registry

### Initialize

1. Install gcloud CLI: [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)

2. Login
    ```bash
    gcloud auth login
    ```

3. Set Project
    ```bash
    gcloud config set project cc-composite-microservice
    ```

4. Create an Artifact Registry
    ```bash
    gcloud artifacts repositories create cloud-computing --repository-format=docker --location=us-west2 --description="Docker repository"
    ```

5. Configure Docker Authenticator
    ```bash
    gcloud auth configure-docker us-west2-docker.pkg.dev
    ```

### Build and Push to Artifact Registry

1. Login
    ```bash
    gcloud auth login
    ```

2. Set Project
    ```bash
    gcloud config set project cc-composite-microservice
    ```

3. Start Docker Desktop

4. Build
    ```bash
    docker build -t us-west2-docker.pkg.dev/cc-composite-microservice/cloud-computing/composite-microservice:latest .
    ```
    Docker configuration file `%HOMEPATH%\.docker\config.json` updated.

5. Push
    ```bash
    docker push us-west2-docker.pkg.dev/cc-composite-microservice/cloud-computing/composite-microservice:latest
    ```

### Clean Up

1. Clean Docker configuration file `%HOMEPATH%\.docker\config.json`:
    ```json
    {
        "credHelpers": {
            "us-west2-docker.pkg.dev": "gcloud"
        }
    }
    ```
2. Clean Local Docker images
3. Clean Artifact Registry
