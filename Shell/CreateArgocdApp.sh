#!/bin/bash

LIST=$(argocd app list -o name)
APPS=($LIST)
if [[ " ${APPS[*]} " =~ "saleor-strapi" ]]
then
  echo "Application saleor-strapi exists"
else 
  echo "Application saleor-strapi does not exist"
  argocd app create saleor-strapi --repo git@github.com:NTTDATA-UK-DEA/saleor-strapi.git --path charts/saleor-platform  --dest-server https://kubernetes.default.svc --values values.yaml
fi 