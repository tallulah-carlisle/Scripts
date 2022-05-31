#!/bin/bash

NS=$(kubectl get ns -l environment=preview -o jsonpath='{.items[*].metadata.name}')
NAMESPACES=($NS)
for NAMESPACE in "${NAMESPACES[@]}"
do
  echo "$NAMESPACE"
  kubectl delete ns "$NAMESPACE"
done