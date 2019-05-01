docker cp mychannel.block peer1.org1.example.com:/mychannel.block
docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/var/hyperledger/users/Admin@org1.example.com/msp" peer1.org1.example.com peer channel join -b mychannel.block
rm -f mychannel.block
docker exec cli peer chaincode install -n hashcode -p github.com/chaincode -v v0
echo "Next step: run I4_joinChannel.sh on Instance 4."
