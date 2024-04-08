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
# Remove columns that contained removed comments (
# [removed] or [deleted])
data = data[data['comment'] != '[removed]']
data = data[data['comment'] != '[deleted]']

# Remove columns that contains img
data = data[~data['comment'].str.contains('.img')]
data = data[~data['comment'].str.contains('.jpg')]
data = data[~data['comment'].str.contains('.jpeg')]
data = data[~data['comment'].str.contains('.png')]
data = data[~data['comment'].str.contains('.gif')]
# print(data)


data['tokens'] = data['comment'].apply(lambda x: word_tokenize(x, "english"))
# print(data)
# print(data['tokens'])

# data['pos_tags'] = data['tokens'].apply(pos_tag)

stemmer = PorterStemmer()
data['stemmed'] = data['tokens'].apply(lambda x: [stemmer.stem(token) for token in x])
# print(data['stemmed']) 

lemmatizer = WordNetLemmatizer()
data['lemmatized'] = data['tokens'].apply(lambda x: [lemmatizer.lemmatize(token) for token in x])


print(data)
# #Remove columns that contain language aside from english
# def english_sentence(text):
#     try:
#         return detect(text) == 'en'
#     except LangDetectException:
#         return False

# data['english'] = data['comment_body'].apply(english_sentence)
# data = data[data['english']]
# data = data.drop(columns=['english'])

# #Remove curse word from the data 
# data['comment_body'] = data['comment_body'].apply(lambda x: profanity.censor(x, ''))
data.to_csv('example.csv', index=False)

