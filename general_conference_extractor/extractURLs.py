# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_Extract_URLs.ipynb.

# %% auto 0
__all__ = ['extract_talk_urls', 'generate_conference_urls']

# %% ../nbs/01_Extract_URLs.ipynb 3
from bs4 import BeautifulSoup
import requests
import re

def extract_talk_urls(html):
    """
    Extracts URLs for talks from a given General Conference year page.

    Args:
        url (str): The URL of a General Conference year page, e.g., 'https://www.churchofjesuschrist.org/study/general-conference/1994/04?lang=eng'

    Returns:
        list[str]: A list of URLs for talks from the given General Conference year page.
    """
    response = requests.get(str(url))
    soup = BeautifulSoup(response.content, 'html.parser')

    # Define a regular expression pattern to match the desired URLs

    # for more recent talks
    url_pattern = re.compile(r'/study/general-conference/\d{4}/(04|10)/\d{2}[a-zA-Z]+.*\?lang=eng')

    # Find all <a> tags with an 'href' attribute that matches the pattern
    links = soup.find_all('a', href=url_pattern)
    
    # for older talks
    if len(links) == 0:
        url_pattern = re.compile(r'/study/general-conference/\d{4}/(04|10)/(?!.*session)[a-zA-Z]+.*\?lang=eng')
        links = soup.find_all('a', href=url_pattern)
    
    # Extract the URLs
    talk_urls = ['https://www.churchofjesuschrist.org/' + link['href'] for link in links]
    
    return talk_urls

# %% ../nbs/01_Extract_URLs.ipynb 5
def generate_conference_urls(start_year, end_year=None, most_recent_april=False):
    """
    Generates General Conference year page URLs for talks from years within a specified range.

    Args:
        start_year (int): The start year for the range of years.
        end_year (int, optional): The end year for the range of General years. Default is None (just produces the URLs for that year provided by start_year).
        most_recent_april (bool, optional): Decides whether to generate the URL for the October conference of that year depending on if the most recent April conference took place at the provided final year in the range. Default is False.

    Returns:
        list[str]: A list of General Conference year page URLs from the years within the specified range.
    """
    conference_urls = []
    months = ['04', '10']
    if end_year is None:
        urls = [f"https://www.churchofjesuschrist.org/study/general-conference/{start_year}/{month}?lang=eng" for month in months]
    else:
        urls = []
        for year in range(start_year, end_year+1, 1):
            year_urls = [f"https://www.churchofjesuschrist.org/study/general-conference/{year}/{month}?lang=eng" for month in months]
            urls.append(year_urls)
        urls = [item for sublist in urls for item in sublist]
        
        if most_recent_april == True:
            urls = urls[:-1]
            
    return urls
