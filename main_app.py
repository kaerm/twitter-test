import twitter
import json

import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.identity import DefaultAzureCredential

def getTweets():
    api = twitter.Api(consumer_key=os.getenv('TW_CONSUMER_KEY'),
                  consumer_secret=os.getenv('TW_CONSUMER_SEC'),
                  access_token_key=os.getenv('TW_ACCESS_KEY'),
                  access_token_secret=os.getenv('TW_ACCESS_SEC'))

    dump = api.GetSearch(raw_query="q=%23python%20-RT&count=100")
    
    documents = []

    # Collect a list of tweets
    for element in dump:
        documents.append(element.text)
    
    return documents

def analyzeSentiment(tweets):
    # Set up your endpoint from the portal as env variable TA_ENDPOINT or just paste as a string for local dev
    # DefaultAzureCredential expects 3 environment variables 
    # More info: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/identity/azure-identity#environment-variables
    text_analytics_client = TextAnalyticsClient(endpoint=os.getenv('TA_ENDPOINT'), 
                                                credential=DefaultAzureCredential())

    result = text_analytics_client.analyze_sentiment(tweets)
    docs = [doc for doc in result if not doc.is_error]

    # Process the result for each tweet. Results can be positive, negative, and neutral (ignored here)
    sum_sentiment = 0
    for idx, doc in enumerate(docs):
            if doc.sentiment == "positive":
                sum_sentiment += 1
            elif doc.sentiment == "negative":
                sum_sentiment -= 1
    
    return sum_sentiment/len(docs)

if __name__ == "__main__":
    tweets = getTweets()
    sentiment = analyzeSentiment(tweets)
    
    if sentiment > 0:
        print("Keep the Python spirit up!")
    else:
        print("We gotta do better!")