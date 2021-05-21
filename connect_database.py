from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

with open('config.json', 'r') as config:
    conf = json.load(config)
    
cloud_config = {}
cloud_config['secure_connect_bundle'] = conf['secure_connect_bundle']

auth_provider = PlainTextAuthProvider(conf["CLIENT_ID"], conf["CLIENT_SECRET"])
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

row = session.execute("select release_version from system.local").one()
if row:
    print(row)
else:
    print("An error occurred.")