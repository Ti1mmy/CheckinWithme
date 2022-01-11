# Imports the Google Cloud client library
from google.cloud import language_v1
import os
# Explicitly use service account credentials by specifying the private key
# file.
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

# Instantiates a client
client = language_v1.LanguageServiceClient()


def google_sentiment_analysis(text: str):
    try:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        sentiment_score = {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude
        }
    except Exception:
        return None
    output = sentiment_score if sentiment_score else None
    return output
