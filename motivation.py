import json
import random
import requests as rq

with open("config/reddit_keys.json") as temp_file:
    reddit_keys = json.load(temp_file)
    


def refresh_reddit_token():
    global headers
    auth = rq.auth.HTTPBasicAuth(reddit_keys['personal_use'], reddit_keys['secret'])  # auth

    data = {'grant_type': 'password',
            'username': '',
            'password': ''}  # Add Reddit Login Creds

    headers = {'User-Agent': 'MyBot/0.0.1'}

    res = rq.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)  # gets access token
    print(res.json())
    TOKEN = res.json()['access_token']

    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}  # adds auth token to headers
    
refresh_reddit_token()

def get_motivation():
    res = rq.get("https://oauth.reddit.com/r/GetMotivated/top/?t=week?",  # gets top 15 posts of week
                 headers=headers).json()

    # randomly grabs one
    return res['data']['children'][random.randrange(0, len(res['data']['children'])) - 1]['data']['url']
