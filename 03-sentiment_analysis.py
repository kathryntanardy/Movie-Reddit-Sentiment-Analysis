import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
import matplotlib.pyplot as plt
import ast
import re
import csv


def sentiment_analyze(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    return score

def sentiment_words(word, neg_words, neu_words, pos_words):
    word = str(word)
    score = SentimentIntensityAnalyzer().polarity_scores(word)

    if ((score['neg'] > score['pos']) and (score['neg'] > score['neu'])):
        neg_words.append(word)

    elif ((score['pos'] > score['neg']) and (score['pos'] > score['neu'])):
        pos_words.append(word)

    else:
        neu_words.append(word)


def get_words(tokenized, final_words):
    for word in tokenized:
        if (word not in stopwords.words('english')):
            final_words.append(word)


def remove_words(text, words_to_remove):
    pattern = r'\b(?:' + '|'.join(words_to_remove) + r')\b'

    # Replace the matched words with an empty string
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def analyze_data(comments_data, data_output, count_output):
    # Read Data
    data = pd.read_csv(comments_data)

    # Remove stop words
    data['comment'] = data['comment'].astype(str)
    data['comment'] = data['comment'].apply(lambda x: remove_words(x, stopwords.words('english')))
    new_data = data.copy(deep=True)

    # -------------------- Sentiment Analyze --------------------
    data['sentiment'] = data['comment'].apply(lambda x: sentiment_analyze(x))

    # Get Positive, Neutral, Negative columns
    data['negative'] = data['sentiment'].apply(lambda x: x.get('neg'))
    data['neutral'] = data['sentiment'].apply(lambda x: x.get('neu'))
    data['positive'] = data['sentiment'].apply(lambda x: x.get('pos'))

    # Give ratings to every comment
    data['rating'] = ((data['positive']) + (data['neutral'] / 2)) * 10
    # data['rating'] = (data['positive'] / (data['positive'] + data['negative'])) * 10

    # Average
    print("Before Removing neu words:")
    average_neg = data['negative'].mean()
    average_neu = data['neutral'].mean()
    average_pos = data['positive'].mean()
    average_rating = data['rating'].mean()
    print("average negative =", average_neg)
    print("average neutral =", average_neu)
    print("average positive =", average_pos)
    print("average rating =", average_rating)


    # -------------------- Get sentiment words --------------------
    tokenized_data = data
    tokenized_data['tokenized'] = tokenized_data['comment'].apply(lambda x: word_tokenize(x, "english"))  

    # Drop columns
    tokenized_data = tokenized_data.drop(labels=['comment', 'date', 'sentiment', 'negative', 'neutral', 'positive'], axis=1)

    # Explode
    tokenized_data = tokenized_data.explode('tokenized')

    # Get counts
    count = tokenized_data.groupby('tokenized').size()
    count = count.reset_index(name='count')
    count.rename(columns={'tokenized': 'words'}, inplace=True)
    count = count.sort_values(by=['count'], ascending=False)

    # Get neg, neu, pos words
    neg_words = []
    neu_words = []
    pos_words = []
    count['words'].apply(lambda x: sentiment_words(x, neg_words, neu_words, pos_words))

    # # Remove neutral words
    # count = count[~count['words'].isin(neu_words)]

    # # Export counts to csv
    # count.to_csv(count_output, index=False)


    # -------------------- Sentiment Analyze --------------------
    print("\nAfter:")
    data['comment'] = data['comment'].apply(lambda x: remove_words(x, neu_words))
    new_data['sentiment'] = new_data['comment'].apply(lambda x: sentiment_analyze(x))

    # Get Positive, Neutral, Negative columns
    new_data['negative'] = new_data['sentiment'].apply(lambda x: x.get('neg'))
    new_data['neutral'] = new_data['sentiment'].apply(lambda x: x.get('neu'))
    new_data['positive'] = new_data['sentiment'].apply(lambda x: x.get('pos'))

    # Remove rows with positive
    new_data = new_data[(new_data['positive'] != 0) & (new_data['negative'] != 0)]

    # # Give ratings to every comment
    new_data['rating'] = ((new_data['positive']) + (new_data['neutral'] / 2)) * 10
    # new_data['rating'] = (new_data['positive'] / (new_data['positive'] + new_data['negative'])) * 10

    # Export new data
    new_data.to_csv(data_output, index=False)

    # Average
    average_neg = new_data['negative'].mean()
    average_neu = new_data['neutral'].mean()
    average_pos = new_data['positive'].mean()
    average_rating = new_data['rating'].mean()
    print("average negative =", average_neg)
    print("average neutral =", average_neu)
    print("average positive =", average_pos)
    print("average rating =", average_rating)
    


cleaned_data = ['./cleaned_data/ant_man_clean.csv',
                    './cleaned_data/barbie_clean.csv',
                    './cleaned_data/black_panther_clean.csv',
                    './cleaned_data/dune2_clean.csv',
                    './cleaned_data/guardians_of_the_galaxy_clean.csv',
                    './cleaned_data/hunger_games_clean.csv',
                    './cleaned_data/john_wick_4_clean.csv',
                    './cleaned_data/madame_web_clean.csv',
                    './cleaned_data/mission_impossible_clean.csv',
                    './cleaned_data/oppenheimer_clean.csv',
                    './cleaned_data/spider_verse_clean.csv',
                    './cleaned_data/the_marvels_clean.csv']

data_output = ['./sentiment_data/ant_man_sentiment.csv',
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

count_output = ['./sentiment_data/ant_man_count.csv',
                './sentiment_data/barbie_count.csv',
                './sentiment_data/black_panther_count.csv',
                './sentiment_data/dune2_count.csv',
                './sentiment_data/guardians_of_the_galaxy_count.csv',
                './sentiment_data/hunger_games_count.csv',
                './sentiment_data/john_wick_4_count.csv'
                './sentiment_data/madame_web_count.csv',
                './sentiment_data/mission_impossible_count.csv',
                './sentiment_data/oppenheimer_count.csv',
                './sentiment_data/spider_verse_count.csv',
                './sentiment_data/the_marvels_count.csv']


for comments_file, data_file, count_file in zip(cleaned_data, data_output, count_output):
    print("\n")
    print(comments_file)
    print("-----------------------------------")
    analyze_data(comments_file, data_file, count_file)
    print(comments_file + " SUCCESS") 
    print("\n")