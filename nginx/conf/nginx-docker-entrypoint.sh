#!/usr/bin/env sh
#https://serverfault.com/questions/577370/how-can-i-use-environment-variables-in-nginx-conf
set -eu

#IP LOCALHOST
export LOCALHOST=$(ip route | awk '/^default via /{print $3}')

envsubst '${LOCALHOST} ${SEARCH_DOMAIN} ${SEARCH_PORT} ${SEARCH_SERVER_NAME}' < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/nginx.conf
#echo "$@"

exec "$@"