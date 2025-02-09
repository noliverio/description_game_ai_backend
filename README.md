# AI Description game Backend

Flask based backend for AI Description game.

## Config

Set the following env vars to configure the application.

|  config key name | description                                                             |
|----------------- | ------------------------------------------------------------------------|
|  open_ai_api_key | api key for open ai (should be managed with secret manager)             |
|  PROJECT_ID      | name of the GPC project with your storage bucket                        |
|  BUCKET_NAME     | name of the GCP storage bucket                                          |
|  DB_USER         | username to query your database                                         |
|  DB_PASS         | password to query your database (should be managed with secret manager) |
|  DB_NAME         | name of your database                                                   |
|  CONNECTION_NAME | connection string                                                       |
|


## Infra

This service is meant to be deployed in as a GCP Cloud run service behind an api gateway. 

If deployed that way no additional config to 
provide permissions to communicate with GCP infra is required. If deployed another way, providing an 
application_default_credentials.json in the along side the service may be required.

TODO: Need an openapi.yaml file to deploy the api gateway.
TODO: Maybe put the TF for this service into this repo.