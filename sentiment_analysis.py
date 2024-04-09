import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
import matplotlib.pyplot as plt
import ast


def sentiment_analyze(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    return score


def get_words(tokenized, final_words):
    for word in tokenized:
        if word not in stopwords.words('english'):
            final_words.append(word)


def analyze_data(comments_data, data_output, count_output):
    # Read Data
    data = pd.read_csv(comments_data)

    # -------------------- Sentiment Analyze --------------------
    data['comment'] = data['comment'].astype(str)
    data['sentiment'] = data['comment'].apply(lambda x: sentiment_analyze(x))

    # Get Positive, Neutral, Negative columns
    data['negative'] = data['sentiment'].apply(lambda x: x.get('neg'))
    data['neutral'] = data['sentiment'].apply(lambda x: x.get('neu'))
    data['positive'] = data['sentiment'].apply(lambda x: x.get('pos'))

    # Give ratings to every comment
    data['rating'] = ((data['positive']) + (data['neutral'] / 2)) * 10

    # Average
    average_neg = data['negative'].mean()
    average_neu = data['neutral'].mean()
    average_pos = data['positive'].mean()
    # print("average negative =", average_neg)
    # print("average neutral =",average_neu)
    # print("average positive =",average_pos)

    data.to_csv(data_output, index=False)

    # -------------------- Get sentiment words --------------------
    tokenized_data = data
    tokenized_data['tokenized'] = tokenized_data['comment'].apply(lambda x: word_tokenize(x, "english"))

    final_words = []
    tokenized_data['tokenized'].apply(lambda x: get_words(x, final_words))

    tokenized_data = tokenized_data.drop(labels=['comment', 'date', 'sentiment', 'negative', 'neutral', 'positive'], axis=1)

    tokenized_data = tokenized_data.explode('tokenized')

    count = tokenized_data.groupby('tokenized').size()

    count = count.reset_index(name='count')
    count.rename(columns={'tokenized': 'words'}, inplace=True)
    count = count.sort_values(by=['count'], ascending=False)

    count.to_csv(count_output, index=False)

    # # Count Words
    # word_counts = Counter(final_words)
    # print(word_counts)


def main():
    filepath = ['./cleaned_data/ant_man_comments.csv',
            './cleaned_data/black_panther_comments.csv',
            './cleaned_data/guardians_of_the_galaxy_comments.csv',
            './cleaned_data/madame_web_comments.csv',
            './cleaned_data/mission_impossible_comments.csv',
            './cleaned_data/spider_verse_comments.csv',
            './cleaned_data/the_marvels_comments.csv',
            './cleaned_data/barbie_comments.csv',
            './cleaned_data/dune2_comments.csv',
            './cleaned_data/oppenheimer_comments.csv'
    ]

    outputs = [
        'ant_man_clean.csv',
        'black_panther_clean.csv',
        'guardians_of_the_galaxy_clean.csv',
        'hunger_games_clean.csv',
        'madame_web_clean.csv',
        'spider_verse_clean.csv',
        'the_marvels_clean.csv',
        'barbie_clean.csv',
        'dune2_clean.csv',
        'oppenheimer_clean.csv'
    ]

    comments_data = ['./cleaned_data/ant_man_clean.csv',
                     './cleaned_data/barbie_clean.csv',
                     './cleaned_data/black_panther_clean.csv',
                     './cleaned_data/dune2_clean.csv',
                     './cleaned_data/guardians_of_the_galaxy_clean.csv',
                     './cleaned_data/hunger_games_clean.csv',
                     './cleaned_data/john_wick_4_clean.csv'
                     './cleaned_data/madame_web_clean.csv',
                     './cleaned_data/mission_impossible_clean.csv',
                     './cleaned_data/oppenheimer_clean.csv',
                     './cleaned_data/spider_verse_clean.csv',
                     './cleaned_data/the_marvels_clean.csv']
    
    data_output = ['data_sentiment.csv']
    count_output = ['count.csv']

    for comments_file, data_file, count_file in zip(comments_data, data_output, count_output):
        analyze_data(comments_file, data_file, count_file)
        print(comments_file + " SUCCESS") 

    

if __name__ == '__main__':
    main()