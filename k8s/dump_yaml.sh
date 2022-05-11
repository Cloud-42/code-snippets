#!/bin/bash

DIR='k8s-manifests/namespaces'

mkdir -p $DIR

for NAMESPACE in $(kubectl get -o=name namespaces | cut -d '/' -f2)
do
    for TYPE in $(kubectl get -n $NAMESPACE -o=name pvc,configmap,serviceaccount,secret,ingress,service,deployment,statefulset,hpa,job,cronjob)
    do
        mkdir -p $(dirname $DIR/$NAMESPACE/$TYPE)
        kubectl get -n $NAMESPACE -o=yaml $TYPE > $DIR/$NAMESPACE/$TYPE.yaml
    done
done
