import json
import random
import requests as rq

def get_motivation():
    res = rq.get("https://oauth.reddit.com/r/GetMotivated/top/?t=week?",   # gets top 15 posts of week
                headers=headers).json()

    return res['data']['children'][random.randrange(0, len(res['data']['children']))-1]['data']['url']   # randomly grabs one
    

with open("config/reddit_keys.json") as temp_file:
    reddit_keys = json.load(temp_file)

auth = rq.auth.HTTPBasicAuth(reddit_keys['personal_use'], reddit_keys['secret'])   # auth

data = {'grant_type': 'password',
        'username': 'johnnyboi32123',
        'password': '123456789qwerty'}   # need to login to reddit account

headers = {'User-Agent': 'MyBot/0.0.1'}

res = rq.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)   # gets access token

TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}   # adds auth token to headers

get_motivation()
