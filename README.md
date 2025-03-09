# Assistant
### Run locally
To run the application in dev mode
```shell
fastapi dev app/main.py
```
To run with plain text logging mode (default is json)
```shell
export APP_LOG_FORMAT_MODE=text
fastapi dev app/main.py
```
### Run in production
Execute the following command
```shell
uvicorn app.main:app \
  --host 0.0.0.0 --port 8000 \
  --log-config app/config/logging.json \
  --workers 4 \
  --access-log \
  --timeout-graceful-shutdown 30
```
## Define variables
```shell
export ASSISTANT_URL=http://localhost:8000
```
To verify it is running
```shell
curl -v $ASSISTANT_URL/health/liveness
curl -v $ASSISTANT_URL/health/readiness
curl -v $ASSISTANT_URL/version
```
## Unit testing
To run all tests
```shell
pipenv run test
```
To run all tests with code coverage
```shell
pipenv run coverage
```
To create HTML code coverage report
```shell
pipenv run coverage-html
```
## OpenAPI
```shell
curl $ASSISTANT_URL/openapi.json
curl $ASSISTANT_URL/docs
curl $ASSISTANT_URL/redoc
```
