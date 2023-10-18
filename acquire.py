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

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


# +

def scrape_blog_articles(blog_links):
    """
    Scrapes blog articles from a list of blog links and returns them as a Pandas DataFrame.

    Parameters:
    blog_links (list): A list of URLs to the blog articles to be scraped.

    Returns:
    pandas.DataFrame: A DataFrame containing the scraped blog article titles and content.
    """
    all_blogs = []

    for link in blog_links:
        response = requests.get(link, headers={'User-Agent': 'Robinson Rulez'})
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1', class_='entry-title').text
        body = soup.find('div', class_='entry-content').text.strip()
        row = {'title': title, 'article': body}
        all_blogs.append(row)

    articles = pd.DataFrame(all_blogs)
    
    return articles



# +

def scrape_news_articles(categories, base_url):
    """
    Scrapes articles from web pages for specified categories and constructs a DataFrame.

    Parameters:
    categories (list): A list of category names to scrape.
    base_url (str): The base URL to construct category-specific URLs.

    Returns:
    pandas.DataFrame: A DataFrame containing scraped articles with 'title', 'body', and 'category' columns.
    """
    all_articles = pd.DataFrame(columns=['title', 'body', 'category'])
    t_sum = 0

    for category in categories:
        t_0 = time.time()
        print(f'Grabbing contents for {category}.')
        # Construct a URL based on the base URL concatenated with the category.
        category_url = base_url + category
        # Get the response text from the constructed URL.
        raw_content = requests.get(category_url).text
        # Turn the content into soup:
        soup = BeautifulSoup(raw_content, 'html.parser')
        # Title content:
        titles = [element.text for element in soup.find_all('span', itemprop='headline')]
        # Body content:
        bodies = [element.text for element in soup.find_all('div', itemprop='articleBody')]
        # Create a DataFrame for the category.
        category_df = pd.DataFrame({'title': titles, 'body': bodies, 'category': category})
        all_articles = pd.concat([all_articles, category_df], axis=0, ignore_index=True)
        t_n = time.time()
        t_delta = t_n - t_0
        print(f'Time to grab contents of {category}: {round(t_delta, 2)} seconds')
        t_sum += t_delta

    print('Job finished!')
    print(f'It took {round((t_sum / 60), 2)} minutes to execute scraping')
    return all_articles

# -


