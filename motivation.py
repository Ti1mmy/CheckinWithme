import requests as rq
import json
import random


def get_motivation():
    limit = '15'

    res = rq.get("https://oauth.reddit.com/r/GetMotivated/top/?t=week?",
                headers=headers,
                params={'limit': limit}).json()

    return res['data']['children'][random.randrange(0, int(limit))-1]['data']['url']
    

with open("config/reddit_keys.json") as temp_file:
    reddit_keys = json.load(temp_file)

auth = rq.auth.HTTPBasicAuth(reddit_keys['personal_use'], reddit_keys['secret'])

data = {'grant_type': 'password',
        'username': 'johnnyboi32123',
        'password': '123456789qwerty'}

headers = {'User-Agent': 'MyBot/0.0.1'}

res = rq.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

get_motivation()
