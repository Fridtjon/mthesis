#I1: ssh fabusr@158.39.75.116 "/home/fabusr/2org-hlf-deployment-prod/scripts/teardown.sh"
#I2: ssh fabusr@158.37.63.164 "/home/fabusr/2org-hlf-deployment-prod/scripts/teardown.sh"
#I3: ssh fabusr@158.37.63.165 "/home/fabusr/2org-hlf-deployment-prod/scripts/teardown.sh"
#I4: ssh fabusr@158.37.63.175 "/home/fabusr/2org-hlf-deployment-prod/scripts/teardown.sh"
#I5: ssh fabusr@158.37.63.184 "/home/fabusr/2org-hlf-deployment-prod/scripts/teardown.sh"
#ssh-copy-id fabusr@158.37.63.164
#ssh-copy-id fabusr@158.37.63.165
#ssh-copy-id fabusr@158.37.63.175
#ssh-copy-id fabusr@158.37.63.184
#ssh-copy-id fabusr@158.37.63.116
# 1. dep i1 2 3 4
# i1: 158.39.86.116
echo "Deploying instance 1."
ssh fabusr@158.39.75.116 "cd /home/fabusr/2org-hlf-deployment-prod ; ./scripts/depIns1.sh"
echo "Sleeping some time to let the orderers start up properly."
sleep 2
echo "Deploying other instances."
ssh fabusr@158.37.63.164 "cd /home/fabusr/2org-hlf-deployment-prod ; ./scripts/depIns2.sh"
ssh fabusr@158.37.63.165 "cd /home/fabusr/2org-hlf-deployment-prod ; ./scripts/depIns3.sh"
ssh fabusr@158.37.63.175 "cd /home/fabusr/2org-hlf-deployment-prod ; ./scripts/depIns4.sh"
ssh fabusr@158.37.63.184 "cd /home/fabusr/2org-hlf-deployment-prod ; ./scripts/depIns5.sh"
sleep 1
echo "Creating channel on instance 2."
ssh fabusr@158.37.63.164 "cd /home/fabusr/2org-hlf-deployment-prod ; ./scripts/I2_createChannel.sh"
sleep 1

echo "Next step: run spreadBlockFromInstance2.sh from Macintosh."
./spreadBlockFromInstance2.sh
sleep 1


ssh fabusr@158.37.63.165 "cd /home/fabusr/2org-hlf-deployment-prod ; ./scripts/I3_joinChannel.sh"
ssh fabusr@158.37.63.175 "cd /home/fabusr/2org-hlf-deployment-prod ; ./scripts/I4_joinChannel.sh"
ssh fabusr@158.37.63.184 "cd /home/fabusr/2org-hlf-deployment-prod ; ./scripts/I5_joinChannel.sh"

sleep 1
echo "Next step: run I2_instantiate_CC.sh on Instance 2."
ssh fabusr@158.37.63.164 "cd /home/fabusr/2org-hlf-deployment-prod ; ./scripts/I2_instantiate_CC.sh"
echo "Done. Ready for peer chaincode "
#sleep 5
#ssh fabusr@158.37.63.165 "cd /home/fabusr/2org-hlf-deployment-prod ; ./scripts/generateData.sh"
