import sys
import pandas as pd
from scipy.stats import levene
from scipy.stats import ttest_ind
from scipy.stats import normaltest
from scipy.stats import mannwhitneyu
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

imdb_filepath = ['./imdb/ant_man_imdb.csv',
                 './imdb/barbie_imdb.csv',
                 './imdb/black_panther_imdb.csv',
                 './imdb/dune2_imdb.csv',
                 './imdb/guardians_of_the_galaxy_imdb.csv',
                 './imdb/hunger_games_imdb.csv',
                 './imdb/john_wick_4_imdb.csv',
                 './imdb/madame_web_imdb.csv',
                 './imdb/mission_impossible_imdb.csv',
                 './imdb/oppenheimer_imdb.csv',
                 './imdb/spider_verse_imdb.csv',
                 './imdb/the_marvels_imdb.csv']

reddit_plt = ['ant_man_reddit.png',
              'barbie_reddit.png',
              'black_panther_reddit.png',
              'dune2_reddit.png',
              'guardians_of_the_galaxy_reddit.png',
              'hunger_games_reddit.png',
              'john_wick_4_reddit.png',
              'madame_web_reddit.png',
              'mission_impossible_reddit.png',
              'oppenheimer_reddit.png',
              'spider_verse_reddit.png',
              'the_marvels_reddit.png']

plot = ['ant_man',
        'barbie',
        'black_panther',
        'dune2',
        'guardians_of_the_galaxy',
        'hunger_games',
        'john_wick_4',
        'madame_web',
        'mission_impossible',
        'oppenheimer',
        'spider_verse',
        'the_marvels']

print("\n")
print("---------------------------------------------------------------------------------------------------------")
print("Ho: mean of the ratings of the Reddit sentimental analysis is equal to the mean of the ratings of IMDB")
print("---------------------------------------------------------------------------------------------------------")

for imdb, reddit, plot in zip(imdb_filepath, reddit_filepath, plot):
    print("\n")
    print(imdb, "and ", reddit)
    print("--------------------------------------------------")

    imdb_rates = pd.read_csv(imdb)
    reddit_rates = pd.read_csv(reddit)

    #Remove irrelevant columns from the reddit_rates data
    reddit_rates = reddit_rates.drop(labels=['comment', 'date', 'sentiment', 'negative', 'neutral', 'positive'], axis=1)

    #Sample the same amount of data each from each sample
    imdb_rates = imdb_rates.sample(n=1000)
    reddit_rates = reddit_rates.sample(n=1000)

    
    #Create the first subplot
    plt.subplot(1, 2, 1)  # (rows, columns, panel number)
    plt.hist(imdb_rates['Rating'], bins=10, color='blue', label='IMDB Data')
    plt.xlim(0, 11) 
    plt.xlabel('Ratings')
    plt.ylabel('Frequency')
    plt.title('IMDB Rating Distribution')

    # Create second subplot
    plt.subplot(1, 2, 2)
    plt.hist(reddit_rates['rating'], bins=10, color='red', label='Reddit Data')
    plt.xlim(0, 11) 
    plt.xlabel('Ratings')
    plt.ylabel('Frequency')
    plt.title('Reddit Rating Distribution')
    # plt.savefig(plot)

    imdb_normality = normaltest(imdb_rates['Rating']).pvalue
    reddit_normality = normaltest(reddit_rates['rating']).pvalue
    print("Mean of the IMDB data: ", imdb_rates['Rating'].mean())
    print("Mean of the Reddit data: ", reddit_rates['rating'].mean())

    #Check the normality of both graphs
    isNormal = False
    if(imdb_normality >= 0.05 and reddit_normality >= 0.05):
        isNormal = True

    #Check whether both data have an equal variance
    isEqualVar = False
    equal_variance = levene(imdb_rates['Rating'], reddit_rates['rating']).pvalue
    if(equal_variance >= 0.05):
        isEqualVar = True

    #Handle statistical test based on the distribution of the graph
    if(isNormal and isEqualVar):
        print("Both data is normal and it passed the Levene's test, conducting T-test")
        test = ttest_ind(imdb_rates['Rating'], reddit_rates['rating'])
    elif(isNormal):
        print("Data is normal but does not pass the Levene's test, conducing T-test with unequal variance")
        test = ttest_ind(imdb_rates['Rating'], reddit_rates['rating'], equal_var = False)
    else:
        print("Data is not normal, conducting Mann-Whitney U Test")
        test = mannwhitneyu(imdb_rates['Rating'], reddit_rates['rating'])
        
    #Output the p-value of the statistical test 
    print("The p-value of the test conducted is: ", test.pvalue)
    if(test.pvalue < 0.05):
        print("Succesfully rejected Ho. Mean of the sentimental analysis rating is not equal to the mean of the IMDB data")
    else:
        print("No conclusion can be drawn from the statistical test")