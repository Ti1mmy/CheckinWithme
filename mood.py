import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import datetime

#  watson_setup = json.load(open("watson.json"))
with open('watson.json') as json_file:
    watson_setup = json.load(json_file)
watson_authenticator = IAMAuthenticator(watson_setup['API_key'])
ta = ToneAnalyzerV3(version='2017-09-21', authenticator=watson_authenticator)
ta.set_service_url(watson_setup['url'])


moods = {
    
}

language_tones = ['analytical', 'confident', 'tentative']


def save_result(result):
    pass

def tone_result(message):
    results = ta.tone(message).get_result()
    most_confident_score = {'score': 0}
    
    for tone in results['document_tone']['tones']:
        if tone['tone_id'] not in language_tones:
            # Ignore language indicators
            if tone['score'] > most_confident_score['score']:
                most_confident_score = tone
    if most_confident_score == {'score': 0}:
        return None
    else:
        return most_confident_score


def get_mood_rating(most_confident_mood):
    # Moods: Anger, Fear, Joy, Sadness
    pass