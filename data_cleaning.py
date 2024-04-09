from better_profanity import profanity
import pandas as pd
from langdetect import detect, LangDetectException
import string
import re

filepath = ['./data_scraped/ant_man_comments.csv',
            './data_scraped/barbie_comments.csv',
            './data_scraped/black_panther_comments.csv',
            './data_scraped/dune2_comments.csv',
            './data_scraped/guardians_of_the_galaxy_comments.csv',
            './data_scraped/hunger_games_comments.csv',
            './data_scraped/john_wick_4_comments.csv'
            './data_scraped/madame_web_comments.csv',
            './data_scraped/mission_impossible_comments.csv',
            './data_scraped/oppenheimer_comments.csv',
            './data_scraped/spider_verse_comments.csv',
            './data_scraped/the_marvels_comments.csv']

outputs = ['ant_man_clean.csv',
           'barbie_clean.csv',
           'black_panther_clean.csv',
           'dune2_clean.csv',
           'guardians_of_the_galaxy_clean.csv',
           'hunger_games_clean.csv',
           'john_wick_4_clean.csv',
           'madame_web_clean.csv',
           'mission_impossible_clean.csv'
           'oppenheimer_clean.csv'
           'spider_verse_clean.csv',
           'the_marvels_clean.csv']

# Remove words that start with https:// (to remove image files or sublinks )
def remove_https_words(text):
    # Define a pattern that matches words starting with 'https://'
    pattern = r'https://\S*'
    # Replace these occurrences with an empty string
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def remove_miscellaneous(string):
    # Define the pattern for matching all emojis
    miscellaneous_content = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642" 
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    # Remove emojis from the string
    return miscellaneous_content.sub(r'', string)

def remove_curse_withinwords(text):
    pattern = r'\b\S*shit\S*\b'

    # Replace the matched words with an empty string
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def remove_curse_withinwords2(text):
    pattern = r'\b\S*fuck\S*\b'

    # Replace the matched words with an empty string
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def remove_curse_withinwords3(text):
    pattern = r'\b\S*bitch\S*\b'
    #Replace the matched words with an empty string
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


for filepath, output in zip(filepath, outputs):
    data = pd.read_csv(filepath)
    data['comment'] = data['comment'].apply(lambda x: x.lower())
    # Remove columns that contained removed comments ([removed] or [deleted])
    data = data[data['comment'] != '[removed]']
    data = data[data['comment'] != '[deleted]']

    # Remove columns that contains img, emoji, other miscellaneous content
    data['comment'] = data['comment'].apply(lambda x: remove_https_words(x))
    data['comment'] = data['comment'].apply(lambda x: remove_miscellaneous(x))

    # Remove punctuations
    data['comment'] = data['comment'].apply(lambda x: x.translate(str.maketrans('','', string.punctuation)))

    #Remove curse words 
    data['comment'] = data['comment'].apply(lambda x: profanity.censor(x, ''))

    data['comment'] = data['comment'].apply(lambda x: remove_curse_withinwords(x))
    data['comment'] = data['comment'].apply(lambda x: remove_curse_withinwords2(x))
    data['comment'] = data['comment'].apply(lambda x: remove_curse_withinwords3(x))

    # Export to csv
    data.to_csv(output, index=False)


