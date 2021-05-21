from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import tuple_factory
import json
from time import gmtime, strftime
import datetime

with open('config.json', 'r') as config:
    conf = json.load(config)
    
cloud_config = {}
cloud_config['secure_connect_bundle'] = conf['secure_connect_bundle']

auth_provider = PlainTextAuthProvider(conf["CLIENT_ID"], conf["CLIENT_SECRET"])
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('my_moods')

# row = session.execute("select title from movies_and_tv")

def update_mood(uuid: int, mood: str, today: str = strftime("%Y-%m-%d %H:%M:%S", gmtime())):
    session.execute(f"""
                    CREATE TABLE IF NOT EXISTS user{uuid} (
                        date text,
                        mood text,
                        PRIMARY KEY (date, mood)
                    )
                    """)
    session.execute(f"INSERT INTO user{uuid} (date, mood) VALUES ('{today}', '{mood}')")

update_mood(1215212898778218496, 'joy', '2021-05-20 20:37:35')
update_mood(1215212898778218496, 'joy', '2021-05-19 20:37:35')
update_mood(1215212898778218496, 'anger', '2021-05-19 20:37:35')
update_mood(1215212898778218496, 'fear', '2021-05-19 20:37:35')
update_mood(1215212898778218496, 'joy', '2021-05-18 20:37:35')
update_mood(1215212898778218496, 'joy', '2021-05-16 20:37:35')
my_moods = session.execute(f'select (date, mood) from user{1215212898778218496}')
for thing in my_moods:
    print(thing.date__mood[0])
    print(thing.date__mood[1])


def get_moods(uuid: int):
    try:
        my_moods = session.execute(f'select (date, mood) from user{uuid}')
    except Exception:
        return False
    moodlist = [[], [], [], [], [], [], []]
    datetime_str = []
    current_date = datetime.datetime.now().date()

    for mood in my_moods:
        mood_date = datetime.datetime.strptime(mood.date__mood[0], "%Y-%m-%d %H:%M:%S").date()
        diff_days = (current_date - mood_date).days
        print(diff_days)

        if diff_days <= 7 and diff_days != 0: 
            moodlist[diff_days-1].append(mood.date__mood[1])

    return moodlist    
    
    if len(moodlist) < days:
        pass
