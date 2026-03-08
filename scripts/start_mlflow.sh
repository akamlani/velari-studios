#!/bin/sh
mlflow server                           \
--host 0.0.0.0                          \
--port 5001                             \
--allowed-hosts '*'                     \
--cors-allowed-origins '*'              \
--backend-store-uri sqlite:///mlflow.db \
--default-artifact-root ./mlruns