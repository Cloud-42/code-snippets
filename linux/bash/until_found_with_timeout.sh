WAIT_COUNT=0
until [ $WAIT_COUNT -eq 20 ] || [ "$(kubectl get secrets -n dev | grep postgres)" ]; do
  echo "Waiting for RDS secret to be present. Wait count = $WAIT_COUNT"
  sleep 60
  WAIT_COUNT=$(($WAIT_COUNT+1)) 
done
