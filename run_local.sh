#!/bin/bash

SERVER_PORT=${1-5000}
export SERVER_PORT=${SERVER_PORT}
export AUTH0_DOMAIN=https://login-sandbox.sensynehealth.com/
export AUTH0_AUDIENCE=https://dev.sensynehealth.com/
export AUTH0_METADATA=https://gdm.sensynehealth.com/metadata
export AUTH0_JWKS_URL=https://login-sandbox.sensynehealth.com/.well-known/jwks.json
export AUTH0_HS_KEY=secret
export AUTH0_MGMT_CLIENT_ID=someid
export AUTH0_MGMT_CLIENT_SECRET=secret
export AUTH0_AUTHZ_CLIENT_ID=someid
export AUTH0_AUTHZ_CLIENT_SECRET=secret
export AUTH0_AUTHZ_WEBTASK_URL=https://draysonhealth-sandbox.eu.webtask.io/someid/api
export AUTH0_CLIENT_ID=someid
export NONCUSTOM_AUTH0_DOMAIN=https://draysonhealth-sandbox.eu.auth0.com
export ENVIRONMENT=DEVELOPMENT
export ALLOW_DROP_DATA=True
export PROXY_URL=http://localhost
export HS_KEY=secret
export FLASK_APP=dhos_notifications_api/autoapp.py
export DISABLE_EMAIL_SEND=False
export IGNORE_JWT_VALIDATION=True
export SMTP_HOST=dummy
export SMTP_AUTH_PASS=dummy
export SMTP_AUTH_USER=dummy
export EMAIL_SENDER=dummy
export TOKEN_URL=https://draysonhealth-sandbox.eu.auth0.com/oauth/token
export REDIS_INSTALLED=False
export LOG_LEVEL=${LOG_LEVEL:-DEBUG}
export LOG_FORMAT=${LOG_FORMAT:-COLOUR}
export CUSTOMER_CODE=DEV


if [ -z "$*" ]
then
  python -m dhos_notifications_api
else
  flask $*
fi
