import pandas as pd
from scipy.stats import levene
from scipy.stats import ttest_ind


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

imdb_filepath = ['./imdb/ant_man_imdb.csv',
                 './imdb/barbieimdb.csv',
                 './imdb/black_panther_imdb.csv',
                 './imdb/dune2_imdb.csv',
                 './imdb/guardians_of_the_galaxy_imdb.csv',
                 './imdb/hunger_games_imdb_imdb.csv',
                 './imdb/john_wick_4_imdb.csv',
                 './imdb/madame_web_imdb.csv',
                 './imdb/mission_impossible_imdb.csv',
                 './imdb/oppenheimer_imdb.csv',
                 './imdb/spider_verse_imdb.csv',
                 './imdb/the_marvels_imdb.csv']


for imdb, reddit in zip(imdb_filepath, reddit_filepath):
    print("\n")
    print(imdb, "and ", reddit)
    print("--------------------------------------------------")

    imdb_rates = pd.read_csv(imdb)
    reddit_rates = pd.read_csv(reddit)

    reddit_rates = reddit_rates.drop(labels=['comment', 'date', 'sentiment', 'negative', 'neutral', 'positive'], axis=1)
    print(reddit_rates)

    equal_variance = levene(imdb, reddit).pvalue

    if(equal_variance < 0.05):
        print("Data passed the Levene's test with p-value: ", equal_variance)
        ttest = ttest_ind(imdb_rates, reddit_rates)
    else:
        print("Data did not pass the Levene's test with p-value: ", equal_variance)
        ttest = ttest_ind(imdb_rates, reddit_rates, equal_var = False)

