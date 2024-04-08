from better_profanity import profanity
import pandas as pd
from langdetect import detect, LangDetectException
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

data = pd.read_csv('/Users/kathryntanardy/Desktop/movie-ratings/data_scraped/ant_man_comments.csv')

data['comment'] = data['comment'].apply(lambda x: x.lower())
print(data)
# Remove columns that contained removed comments ([removed] or [deleted])
data = data[data['comment'] != '[removed]']
data = data[data['comment'] != '[deleted]']

# Remove columns that contains img
data = data[~data['comment'].str.contains('.img')]
data = data[~data['comment'].str.contains('.jpg')]
data = data[~data['comment'].str.contains('.jpeg')]
data = data[~data['comment'].str.contains('.png')]
data = data[~data['comment'].str.contains('.gif')]

# Remove punctuations
data['comment_body'] = data['comment_body'].apply(lambda x: x.translate(str.maketrans('','', string.punctuation)))

# Export to csv
data.to_csv('example.csv', index=False)

