
scp fabusr@158.37.63.164:/home/fabusr/2org-hlf-deployment-prod/mychannel.block .
sleep 2
python3 scprToAll.py mychannel.block /home/fabusr/2org-hlf-deployment-prod/
rm mychannel.block
echo "Next step: run I3_joinChannel.sh on Instance 3."