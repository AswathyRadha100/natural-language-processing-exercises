# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import unicodedata
import re
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
import acquire as a


def basic_clean(text):
    '''
    This function performs basic text cleaning on the input text.
    
    It includes the following steps:
    1. Lowercasing: Converts all characters in the text to lowercase.
    2. Unicode Normalization: Transforms Unicode characters to their closest ASCII representation.
    3. Removal of Non-Alphanumeric Characters: Removes characters that are not letters, digits, spaces, or single quotes.

    Parameters:
    text (str): The input text to be cleaned.

    Returns:
    str: The cleaned text with all the transformations applied.
    '''
    text = unicodedata.normalize('NFKD', text.lower())\
        .encode('ascii', 'ignore')\
        .decode('utf-8', 'ignore')
    return re.sub(r"[^a-z0-9'\s]", '', text)


def stem(text):
    '''
    This function takes in a string and returns it with stemming applied.
    
    Parameters:
    text (str): The input text to be stemmed.
    
    Returns:
    str: The input text after stemming.
    '''
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in text.split()]
    return ' '.join(stems)


def lemmatize(text):
    '''
    This function takes in a string and returns it with lemmatization applied.
    
    Parameters:
    text (str): The input text to be lemmatized.
    
    Returns:
    str: The input text after lemmatization.
    '''
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in text.split()]
    return ' '.join(lemmas)


def remove_stopwords(text):
    '''
    This function takes in a string and returns it with stopwords removed.
    
    Parameters:
    text (str): The input text to have stopwords removed.
    
    Returns:
    str: The input text after removing stopwords.
    '''
    tokenizer = ToktokTokenizer()
    stopword_list = stopwords.words('english')
    stopword_list.remove('no')
    stopword_list.remove('not')
    tokens = tokenizer.tokenize(text)
    filtered_tokens = [t for t in tokens if t not in stopword_list]
    return ' '.join(filtered_tokens)


def prep_article_data(text):
    '''
    This function takes in a text and returns a dictionary containing different versions of the text (original, stemmed, lemmatized, and cleaned).
    
    Parameters:
    text (str): The input text to be processed.
    
    Returns:
    dict: A dictionary with keys 'original', 'stemmed', 'lemmatized', and 'clean', each containing the corresponding text.
    '''
    return {
        'original': text,
        'stemmed': stem(basic_clean(text)),
        'lemmatized': lemmatize(basic_clean(text)),
        'clean': remove_stopwords(basic_clean(text))
    }


def wrangle_news(base_url = 'https://inshorts.com/en/read/',
categories = [
    'business',
    'entertainment',
    'technology',
    'sports']):
        
    '''
    This function scrapes news articles, preprocesses the text data, and returns a DataFrame.
    
    Parameters:
    base_url (str): The base URL for the news website.
    categories (list): A list of news categories to scrape.
    
    Returns:
    pandas.DataFrame: A DataFrame containing preprocessed news articles.
    '''
     
    news_df = a.scrape_news_articles(categories, base_url)
    news_df = prep_article_data(news_df)



    return news_df


def wrangle_codeup_blog(blog_links = ['https://codeup.edu/featured/apida-heritage-month/',
 'https://codeup.edu/featured/women-in-tech-panelist-spotlight/',
 'https://codeup.edu/featured/women-in-tech-rachel-robbins-mayhill/',
 'https://codeup.edu/codeup-news/women-in-tech-panelist-spotlight-sarah-mellor/',
 'https://codeup.edu/events/women-in-tech-madeleine/',
 'https://codeup.edu/codeup-news/panelist-spotlight-4/']):
    
    '''
    This function scrapes Codeup blog posts, preprocesses the text data, and returns a DataFrame.
    
    Parameters:
    blog_links (list): A list of URLs to Codeup blog posts.
    
    Returns:
    pandas.DataFrame: A DataFrame containing preprocessed Codeup blog post data.
    '''
     
    codeup_df = a.scrape_blog_articles(blog_links)
    codeup_df = prep_article_data(codeup_df)

    return codeup_df


