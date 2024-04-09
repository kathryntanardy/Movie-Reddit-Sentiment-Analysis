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


def main():
    # Read Data
    data = pd.read_csv("ant_man_comments.csv")

    # Sentiment Analyze
    data['sentiment'] = data['comment'].apply(lambda x: sentiment_analyze(x))

    # Get Positive, Neutral, Negative columns
    data['neg'] = data['sentiment'].apply(lambda x: x.get('neg'))
    data['neu'] = data['sentiment'].apply(lambda x: x.get('neu'))
    data['pos'] = data['sentiment'].apply(lambda x: x.get('pos'))

    # Average
    average_neg = data['neg'].mean()
    average_neu = data['neu'].mean()
    average_pos = data['pos'].mean()
    print("average negative =", average_neg)
    print("average neutral =",average_neu)
    print("average positive =",average_pos)

    data.to_csv("data_sentiment.csv")

    # Get sentiment words
    tokenized_data = data
    tokenized_data['tokenized'] = tokenized_data['comment'].apply(lambda x: word_tokenize(x, "english"))

    final_words = []
    tokenized_data['tokenized'].apply(lambda x: get_words(x, final_words))

    tokenized_data = tokenized_data.drop(labels=['comment', 'date', 'sentiment', 'neg', 'neu', 'pos'], axis=1)

    tokenized_data = tokenized_data.explode('tokenized')

    count = tokenized_data.groupby('tokenized').size()

    count = count.reset_index(name='count')
    count.rename(columns={'tokenized': 'words'}, inplace=True)


    print(count)
    count.to_csv('count.csv')

    # # Count Words
    # word_counts = Counter(final_words)
    # print(word_counts)


if __name__ == '__main__':
    main()