# create channel from peer0 on server2
# it connects to orderer0
docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/var/hyperledger/users/Admin@org1.example.com/msp" peer0.org1.example.com peer channel create -o orderer0.example.com:7050 -c mychannel -f /var/hyperledger/configs/channel.tx
sleep 5
# join peer0 to channel
# execute this command from server1
docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/var/hyperledger/users/Admin@org1.example.com/msp" peer0.org1.example.com peer channel join -b mychannel.block
echo "Created and joined peer."
sleep 5
docker exec cli peer chaincode install -n hashcode -p github.com/chaincode -v v0
docker cp peer0.org1.example.com:/mychannel.block .
echo "Next step: run spreadBlockFromInstance2.sh from Macintosh."
