docker exec cli peer chaincode invoke -o orderer0.example.com:7050 -C mychannel -n hashcode -c '{"Args":["init_doc","Filename.file","content","Floff the creator"]}'
docker exec cli peer chaincode invoke -o orderer0.example.com:7050 -C mychannel -n hashcode -c '{"Args":["init_doc","hyperledger.fabric","is working","Fabric"]}'
