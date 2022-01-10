from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ToneAnalyzerV3

from dotenv import load_dotenv

import os


load_dotenv()
api_key = os.environ.get("WATSON_KEY")
watson_url = os.environ.get("WATSON_URL")
    
def reload_watson_api():   
    global ta
    watson_authenticator = IAMAuthenticator(api_key)   # authentication
    ta = ToneAnalyzerV3(version='2017-09-21', authenticator=watson_authenticator)   # sets up analyzer instance
    ta.set_service_url(watson_url)


language_tones = ['analytical', 'confident', 'tentative']


def watson_tone_analysis(message: str) -> dict:
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

reload_watson_api()