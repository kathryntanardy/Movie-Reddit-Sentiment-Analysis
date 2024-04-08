import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def sentiment_analyze(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    return score


def get_words(tokenized, final_words):
    for word in tokenized:
        if word not in stopwords.words('english'):
            final_words.append(word)


def main():
    # Read Data
    data = pd.read_csv("barbie_cleaned.csv")

    # Convert to lower case
    data['comment_body'] = data['comment_body'].apply(lambda x: x.lower())

    # Sentiment Analyze
    data['sentiment'] = data['comment_body'].apply(lambda x: sentiment_analyze(x))

    # Get sentiment words
    tokenized_data = data
    tokenized_data['tokenized'] = tokenized_data['comment_body'].apply(lambda x: word_tokenize(x, "english"))

    final_words = []
    tokenized_data['tokenized'].apply(lambda x: get_words(x, final_words))



if __name__ == '__main__':
    main()