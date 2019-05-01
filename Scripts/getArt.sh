scp -r fabusr@158.39.75.116:/home/fabusr/2org-hlf-deployment-prod/crypto-config /Users/fridtjof/2org-hlf-deployment-prod/crypto-config
scp -r fabusr@158.39.75.116:/home/fabusr/2org-hlf-deployment-prod/network-config /Users/fridtjof/2org-hlf-deployment-prod/network-config

python3 scprToAll.py /Users/fridtjof/2org-hlf-deployment-prod/crypto-config /home/fabusr/2org-hlf-deployment-prod/
python3 scprToAll.py /Users/fridtjof/2org-hlf-deployment-prod/network-config /home/fabusr/2org-hlf-deployment-prod/