cryptogen generate --config=./fabric-config/crypto-config.yaml
export FABRIC_CFG_PATH=$PWD/fabric-config
configtxgen -profile TwoOrgsOrdererGenesis -outputBlock ./network-config/genesis.block
export CHANNEL_NAME=mychannel 
configtxgen -profile TwoOrgsChannel -outputCreateChannelTx ./network-config/channel.tx -channelID $CHANNEL_NAME
configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./network-config/Org1MSPanchors.tx -channelID $CHANNEL_NAME -asOrg Org1MSP
configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./network-config/Org2MSPanchors.tx -channelID $CHANNEL_NAME -asOrg Org2MSP
