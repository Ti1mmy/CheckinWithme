from google_sentiment_analysis import google_sentiment_analysis
from watson import watson_tone_analysis

ranges = {
    "strong_pos": 0.45,
    "positive": 0.15,
    "negative": -0.15,
    "strong_neg": -0.45
}

negative = ["anger", "fear", "sadness"]

positive = ["joy"]


def tone_result(text: str):
    # Google
    tone_google = google_sentiment_analysis(text)
    
    # Watson
    tone_watson = watson_tone_analysis(text)
    
    # TODO Move to switch statements when Python 3.10 releases
    if tone_watson and tone_google:
        if tone_watson['tone_id'] in negative:
            if tone_google['score'] <= ranges["negative"]:
                return {'tone_id': tone_watson['tone_id']}
            else:
                # ML Libraries disagree on sentiment - will ask again for a more definitive statement
                return None
        else:
            if tone_google['score'] >= ranges["positive"]:
                return {'tone_id': tone_watson['tone_id']}
            else:
                # ML Libraries disagree on sentiment - will ask again for a more definitive statement
                return None
    elif tone_google:
        if tone_google['score'] >= ranges["strong_pos"]:
            return {'tone_id': positive[0]}
        elif tone_google['score'] <= ranges['negative']:
            # Google Sentiment Analysis believes the statement to be negative, but can't pinpoint the tone.
            # Will return separate -1 value for response
            return -1            
    elif tone_watson:
        return {'tone_id': tone_watson['tone_id']}
    else:
        return None

