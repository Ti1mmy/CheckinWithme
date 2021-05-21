from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import tuple_factory
import json
from time import gmtime, strftime

with open('config.json', 'r') as config:
    conf = json.load(config)
    
cloud_config = {}
cloud_config['secure_connect_bundle'] = conf['secure_connect_bundle']

auth_provider = PlainTextAuthProvider(conf["CLIENT_ID"], conf["CLIENT_SECRET"])
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('my_moods')

# row = session.execute("select title from movies_and_tv")

def update_mood(uuid: int, mood: str):
    today = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    session.execute(f"""
                    CREATE TABLE IF NOT EXISTS user{uuid} (
                        date text,
                        mood text,
                        PRIMARY KEY (date, mood)
                    )
                    """)
    session.execute(f"INSERT INTO user{uuid} (date, mood) VALUES ('{today}', '{mood}')")

my_moods = session.execute('select (date, mood) from user215212898778218496')

for thing in my_moods:
    print(thing)