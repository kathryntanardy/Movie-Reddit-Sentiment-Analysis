import sys
import pandas as pd
from scipy.stats import levene
from scipy.stats import ttest_ind
from scipy.stats import normaltest
from scipy.stats import mannwhitneyu
from scipy.stats import linregress
import time
from datetime import datetime
import matplotlib.pyplot as plt

# reddit_filepath = ['./sentiment_data/ant_man_sentiment.csv',
#                    './sentiment_data/barbie_sentiment.csv',
#                    './sentiment_data/black_panther_sentiment.csv',
#                    './sentiment_data/dune2_sentiment.csv',
#                    './sentiment_data/guardians_of_the_galaxy_sentiment.csv',
#                    './sentiment_data/hunger_games_sentiment.csv',
#                    './sentiment_data/john_wick_4_sentiment.csv',
#                    './sentiment_data/madame_web_sentiment.csv',
#                    './sentiment_data/mission_impossible_sentiment.csv',
#                    './sentiment_data/oppenheimer_sentiment.csv',
#                    './sentiment_data/spider_verse_sentiment.csv',
#                    './sentiment_data/the_marvels_sentiment.csv']

# plot = ['ant_man_timestamp.png',
#         'barbie_timestamp.png',
#         'black_panther_timestamp.png',
#         'dune2_timestamp.png',
#         'guardians_of_the_galaxy_timestamp.png',
#         'hunger_games_timestamp.png',
#         'john_wick_4_timestamp.png',
#         'madame_web_timestamp.png',
#         'mission_impossible_timestamp.png',
#         'oppenheimer_timestamp.png',
#         'spider_verse_timestamp.png',
#         'the_marvels_timestamp.png']

reddit_filepath = ['./sentiment_data/ant_man_sentiment.csv']

plot = ['ant_man_timestamp.png']


for reddit in reddit_filepath:
    reddit_data = pd.read_csv(reddit)
    reddit_data = reddit_data.drop(labels=['comment','sentiment', 'negative', 'neutral', 'positive'], axis=1)
    date_format = "%Y-%m-%d %H:%M:%S"
    reddit_data.loc[:, 'date'] = reddit_data['date'].apply(lambda x: datetime.strptime(x, date_format))
    reddit_data.loc[:,'timestamp'] = reddit_data['date'].apply(lambda x:x.timestamp())

    # reddit_data = reddit_data.sort_values(by=['timestamp'])
    # reddit_data = reddit_data.iloc[:2000]

    # reddit_data = reddit_data.sort_values(by=['date'])
    # start_date = reddit_data['date'].iloc[0]
    # end_date = start_date + pd.Timedelta(days=6)
    # reddit_data = reddit_data[(reddit_data['date'] >= start_date) & (reddit_data['date'] <= end_date)]

    print(reddit_data)
    
    fit = linregress(reddit_data.loc[:,'timestamp'], reddit_data.loc[:,'rating'])
    reddit_data['prediction'] = fit.slope*reddit_data.loc[:,'timestamp'] + fit.intercept
    
    plt.plot(reddit_data.loc[:,'date'], reddit_data.loc[:,'rating'], 'b.', alpha=0.5, label="Ratings")
    plt.plot(reddit_data.loc[:,'date'], reddit_data.loc[:,'prediction'], 'r-', linewidth=3)
    plt.xticks(rotation=25)
    plt.show()
    print(reddit_data)
