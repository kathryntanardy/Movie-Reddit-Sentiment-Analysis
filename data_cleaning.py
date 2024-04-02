from better_profanity import profanity
import pandas as pd
from langdetect import detect, LangDetectException


data = pd.read_csv('barbie.csv')
ß
#Remove columns that contained removed comments ([removed] or [deleted])
data = data[data['comment_body'] != '[removed]']
data = data[data['comment_body'] != '[deleted]']

data = data[~data['comment_body'].str.contains('.img')]
data = data[~data['comment_body'].str.contains('.jpg')]
data = data[~data['comment_body'].str.contains('.jpeg')]
data = data[~data['comment_body'].str.contains('.png')]
data = data[~data['comment_body'].str.contains('.gif')]

#Remove columns that contain language aside from english
def english_sentence(text):
    try:
        return detect(text) == 'en'
    except LangDetectException:
        return False

data['english'] = data['comment_body'].apply(english_sentence)
data = data[data['english']]
data = data.drop(columns=['english'])

#Remove curse word from the data 
data['comment_body'] = data['comment_body'].apply(lambda x: profanity.censor(x, ''))
data.to_csv('barbie_cleaned.csv', index=False)

