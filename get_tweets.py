##### Import libraries
import matplotlib.pyplot as plt
import pandas as pd
import tweepy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

##### Twitter API authentication
api_key = 'G672XzBKHq1sYwY9gTWEtNjmI'
api_secret_key = 'mtzCrt4fSku3dL1VsYw6BN6HO2ZfH6wg6E8CcGHZrH0guBKIwV'
access_token = '187872660-4F4OwkTbkNzRsSNKn9IpnD4Fb7kI5sGh5LHMSQFS'
access_token_secret = 'kfG6VHrLuGRt6MIpdSO1CS8SwceHEM5yypfonmzbAM8aS'

# Authorize the API Key
auth = tweepy.OAuthHandler(api_key, api_secret_key)

# Authorization to user's access token and access token secret
auth.set_access_token(access_token, access_token_secret)

# Call the api
api = tweepy.API(auth)


##### Sentiment Analysis

def percentage(subset, total):
    return float(subset) / float(total) * 100


keyword = input('Please enter keyword or hashtag to search: ')
num_of_tweets = int(input('Number of Tweets to analyze: '))

tweets = tweepy.Cursor(api.search, q=keyword, lang='en').items(num_of_tweets)
positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
positive_list = []
negative_list = []
neutral_list = []

for tweet in tweets:
    # Show text of tweet
    print(tweet.text)
    tweet_list.append(tweet.text)
    analysis = TextBlob(tweet.text)
    score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
    pos = score['pos']
    neg = score['neg']
    neu = score['neu']
    comp = score['compound']
    polarity += analysis.sentiment.polarity

    if pos > neg:
        positive_list.append(tweet.text)
        positive += 1

    elif neg > pos:
        negative_list.append(tweet.text)
        negative += 1

    elif neg == pos:
        neutral_list.append(tweet.text)
        neutral += 1

    positive_perc = format(percentage(positive, num_of_tweets), '.1f')
    negative_perc = format(percentage(negative, num_of_tweets), '.1f')
    neutral_perc = format(percentage(neutral, num_of_tweets), '.1f')
    polarity_perc = percentage(polarity, num_of_tweets)

##### Number of Tweets (Total, Positive, Negative, Neutral)
tweet_df = pd.DataFrame(tweet_list)
positive_df = pd.DataFrame(positive_list)
negative_df = pd.DataFrame(negative_list)
neutral_df = pd.DataFrame(neutral_list)

print('Total number of tweets: ', len(tweet_df))
print('Number of positive tweets: ', len(positive_df))
print('Number of negative tweets: ', len(negative_df))
print('Number of neutral tweets: ', len(neutral_df))

##### Creating PieCart
labels = ['Positive [' + str(positive_perc) + '%]',
          'Negative [' + str(negative_perc) + '%]',
          'Neutral [' + str(neutral_perc) + '%]']
proportions = [positive_perc, negative_perc, neutral_perc]
colors = ['mediumseagreen', 'firebrick', 'cornflowerblue']
patches, texts = plt.pie(proportions, colors=colors, startangle=90)
plt.style.use('fivethirtyeight')
plt.legend(labels)
plt.title('Sentiment Analysis Result for keyword = ' + f'\'{keyword}\'')
plt.axis('equal')
plt.show()