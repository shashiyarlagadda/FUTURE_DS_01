import tweepy
import re
from textblob import TextBlob
import pandas as pd

# Step 1: Authenticate
client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAMkB1AEAAAAAwQLoijl%2FKd3aJsYKSexJoGh5N8Y%3DfjreFBsLIU7RyUHiyOxe1J7yd6TYLdD4ywdSWOqR27FXOJfuNM")

# Step 2: Clean Tweet Text
def clean_text(text):
    text = re.sub(r"http\S+|www.\S+", "", text)
    text = re.sub(r"[^A-Za-z0-9\s]+", "", text)
    return text.lower()

# Step 3: Get Sentiment
def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Step 4: Search for Tweets
query = "AI trends"
max_results = 50
response = client.search_recent_tweets(query=query,
                                       max_results=max_results,
                                       tweet_fields=["text", "lang"])

# Step 5: Process Tweets
tweet_data = []
for tweet in response.data:
    if tweet.lang != "en":
        continue
    original = tweet.text
    cleaned = clean_text(original)
    sentiment = get_sentiment(cleaned)
    tweet_data.append([original, cleaned, sentiment])

# Step 6: Export to Excel
df = pd.DataFrame(tweet_data, columns=["Original Tweet", "Cleaned Tweet", "Sentiment"])
df.to_excel("twitter_sentiment_analysis.xlsx", index=False)
print("Saved as twitter_sentiment_analysis.xlsx")
