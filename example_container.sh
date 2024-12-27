#!/bin/bash

docker run --rm --name ldap \
  --env LDAP_ADMIN_PASSWORD=admin \
  --env LDAP_ROOT='dc=example,dc=in' \
  --env LDAP_PORT_NUMBER=389 \
  --publish 389:389 \
  --volume "./ldifs/:/ldifs/" \
  --volume "./schemas/:/schemas/" \
  --hostname 'ldap.example.in' \
  bitnami/openldap:latest
