#===============================================================================  
#
# NOTE: There is no way to 100% reliably find the OS type but this
# seems to work well.
#
#===============================================================================

#!/bin/bash
wk -F= '/^NAME/{print $2}' /etc/os-release | grep -i ubuntu
RESULTUBUNTU=$?
if [ $RESULTUBUNTU -eq 0 ]; then
 
  echo "This is Ubuntu" 
  
fi

awk -F= '/^NAME/{print $2}' /etc/os-release | grep -i amazon
RESULTAMAZON=$?
if [ $RESULTAMAZON -eq 0 ]; then

  echo "This is Amazon Linux"  

fi
