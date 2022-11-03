WAIT=0
until [ $WAIT -eq 20 ] || [ "$(kubectl get secrets -n dev | grep postgres)" ]; do
  echo "Waiting for RDS secret to be present. Wait count = $WAIT"
  sleep 60
  (( WAIT++ ))
done
