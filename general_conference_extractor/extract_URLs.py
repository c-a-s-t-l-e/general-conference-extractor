# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_Extract_URLs.ipynb.

# %% auto 0
__all__ = ['extract_talk_urls', 'generate_conference_url', 'generate_conference_urls', 'extract_multiconference_talk_urls']

# %% ../nbs/01_Extract_URLs.ipynb 3
from bs4 import BeautifulSoup
import requests
import re

def extract_talk_urls(
    url:str # The URL of a General Conference year page, e.g., 'https://www.churchofjesuschrist.org/study/general-conference/1994/04?lang=eng'
    )-> list[str]: # A list of URLs for talks from the given General Conference year page.
    
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
def generate_conference_url(
                            year:int, # The chosen year
                            month:str # The chosen month represented as a two-digit string (e.g., '04' for April, '10' for October).
                           ) -> str: # A General Conference year page URL corresponding to the specified year and month.
    if month in ['04', '10']:
        return f"https://www.churchofjesuschrist.org/study/general-conference/{year}/{month}?lang=eng"
    else:
        raise ValueError("Month must be either '04' (April) or '10' (October).")

# %% ../nbs/01_Extract_URLs.ipynb 7
def generate_conference_urls(
                            start_year:int, # The start year for the range of years.
                            end_year:int, # The end year for the range of General years.
                            most_recent_april:bool=False # Decides whether to generate the URL for the October conference of that year depending on if the most recent April conference took place at the provided final year in the range. Default is False.
                            ) -> list[str]: #A list of General Conference year page URLs from the years within the specified range.
    months = ['04', '10']
    urls = []
    
    for year in range(start_year, end_year+1, 1):
        year_urls = [generate_conference_url(year, month) for month in months]
        urls.append(year_urls)
    urls = [item for sublist in urls for item in sublist]
    
    if most_recent_april == True:
        urls = urls[:-1]
            
    return urls

# %% ../nbs/01_Extract_URLs.ipynb 9
def extract_multiconference_talk_urls(start_year:int, # Start year
                                end_year:int # End year
                               ) -> list[str]: # List of conference talk URLs
    gen_conf_page_urls = generate_conference_urls(start_year, end_year)

    multi_conference_talks = []
    
    # extract all the talks urls from all years
    for url in gen_conf_page_urls:
        multi_conference_talks.append(extract_talk_urls(url))
    
    # flatten the list
    multi_conference_talks = [item for sublist in multi_conference_talks for item in sublist]

    return multi_conference_talks
