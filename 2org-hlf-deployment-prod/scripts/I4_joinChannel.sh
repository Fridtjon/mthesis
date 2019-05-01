docker cp mychannel.block peer0.org2.example.com:/mychannel.block
docker exec -e "CORE_PEER_LOCALMSPID=Org2MSP" -e "CORE_PEER_MSPCONFIGPATH=/var/hyperledger/users/Admin@org2.example.com/msp" peer0.org2.example.com peer channel join -b mychannel.block
rm -f mychannel.block
docker exec cli peer chaincode install -n hashcode -p github.com/chaincode -v v0
echo "Next step: run I5_joinChannel.sh on Instance 5."