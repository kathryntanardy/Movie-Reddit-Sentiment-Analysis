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

reddit_filepath = ['./sentiment_data/ant_man_sentiment.csv',
                   './sentiment_data/barbie_sentiment.csv',
                   './sentiment_data/black_panther_sentiment.csv',
                   './sentiment_data/dune2_sentiment.csv',
                   './sentiment_data/guardians_of_the_galaxy_sentiment.csv',
                   './sentiment_data/hunger_games_sentiment.csv',
                   './sentiment_data/john_wick_4_sentiment.csv',
                   './sentiment_data/madame_web_sentiment.csv',
                   './sentiment_data/mission_impossible_sentiment.csv',
                   './sentiment_data/oppenheimer_sentiment.csv',
                   './sentiment_data/spider_verse_sentiment.csv',
                   './sentiment_data/the_marvels_sentiment.csv']

plot_name = ['./sentiment_time_graph/ant_man_timestamp.png',
        './sentiment_time_graph/barbie_timestamp.png',
        './sentiment_time_graph/black_panther_timestamp.png',
        './sentiment_time_graph/dune2_timestamp.png',
        './sentiment_time_graph/guardians_of_the_galaxy_timestamp.png',
        './sentiment_time_graph/hunger_games_timestamp.png',
        './sentiment_time_graph/john_wick_4_timestamp.png',
        './sentiment_time_graph/madame_web_timestamp.png',
        './sentiment_time_graph/mission_impossible_timestamp.png',
        './sentiment_time_graph/oppenheimer_timestamp.png',
        './sentiment_time_graph/spider_verse_timestamp.png',
        './sentiment_time_graph/the_marvels_timestamp.png']

movie_name = ['Ant Man', 'Barbie', 'Black Panther', 'Dune 2', 'Guardians of The Galaxy', 'Hunger Games', 'John Wick 4', 'Madame Web', 'Mission Impossible', 'Oppenheimer', 'Spiderverse', 'The Marvels']

# reddit_filepath = ['./sentiment_data/ant_man_sentiment.csv']

# plot = ['ant_man_timestamp.png']


for reddit, plot, movie in zip(reddit_filepath, plot_name, movie_name):
    reddit_data = pd.read_csv(reddit)
    reddit_data = reddit_data.drop(labels=['comment','sentiment', 'negative', 'neutral', 'positive'], axis=1)
    date_format = "%Y-%m-%d %H:%M:%S"
    reddit_data.loc[:, 'date'] = reddit_data['date'].apply(lambda x: datetime.strptime(x, date_format))
    reddit_data.loc[:,'timestamp'] = reddit_data['date'].apply(lambda x:x.timestamp())

    reddit_data = reddit_data.sort_values(by=['date'])
    start_date = reddit_data['date'].iloc[0]
    end_date = start_date + pd.Timedelta(days=6)
    reddit_data = reddit_data[(reddit_data['date'] >= start_date) & (reddit_data['date'] <= end_date)]

    fit = linregress(reddit_data.loc[:,'timestamp'], reddit_data.loc[:,'rating'])
    reddit_data['prediction'] = fit.slope*reddit_data.loc[:,'timestamp'] + fit.intercept
    print("The slope for the movie ", movie, " is: ",fit.slope)
    
    plt.plot(reddit_data.loc[:,'date'], reddit_data.loc[:,'rating'], 'b.', alpha=0.5, label="Ratings")
    plt.plot(reddit_data.loc[:,'date'], reddit_data.loc[:,'prediction'], 'r-', linewidth=3)
    plt.xticks(rotation=25)
    plt.xlabel('Date (First Week of Release)')
    plt.ylabel('Sentiment Ratings')
    plt.title('Reddit Sentiment Ratings Over Time (' + movie + ')')
#     plt.savefig(plot)
    plt.show()
