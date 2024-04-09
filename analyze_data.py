import pandas as pd
from scipy.stats import levene
from scipy.stats import ttest_ind


imdb_filepath = 'filepath.csv'
reddit_filepath = 'filepath.csv'

for imdb, reddit in zip(imdb_filepath, reddit_filepath):
    imdb_rates = pd.read_csv(imdb)
    reddit_rates = pd.read_csv(reddit)

    equal_variance = levene(imdb_rates, reddit_rates).pvalue

    if(equal_variance < 0.05):
        print("Data passed the Levene's test with p-value: ", equal_variance)
        ttest = ttest_ind(imdb_rates, reddit_rates)
    else:
        print("Data did not pass the Levene's test with p-value: ", equal_variance)
        ttest = ttest_ind(imdb_rates, reddit_rates, equal_var = False)

