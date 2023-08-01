#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


# In[2]:


# get current date and time
now = datetime.now()

# initialize the webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())


# In[3]:


# define a function to extract data from a single listing
def extract_listing_data(listing):
    title = listing.find('div', class_='title').text.strip()

    location_em =  listing.find('div', class_='sl-loc')
    location = location_em.text.strip() if location_em is not None else None

    rent_elem = listing.find('div', class_='fbavr price sl-price')
    rent = rent_elem.text.strip() if rent_elem is not None else None

    description = listing.find('div', class_='fbac').find('p').text.strip()
    date_elem = listing.find('div', class_='small-light').text.strip().split(' ')[0:]
    date_posted = ' '.join(date_elem).replace("Posted", "").split('\n')[0].strip()
    category = listing.find('div', class_='small-light').a.text
    url = listing.find('div', class_='lfloat gallery-img-bg smallimg sl-image').find('a').get('href')
    date_crawled = now.strftime("%Y-%m-%d")

    return {
        "title": title,
        "location": location,
        "rent": rent,
        "description": description,
        "date_posted": date_posted,
        "category": category,
        "url": url,
        "date_crawled": date_crawled
    }


# In[4]:


current_page = 1
data = []

# extract the job data
while current_page <= 12:
    # navigate to the listings page for the current page
    url = f"http://dhakaflats.com/listings.php?page={current_page}&search_id=16091"
    driver.get(url)

    # get the page source
    html = driver.page_source

    # parse the html with beautiful soup
    soup = BeautifulSoup(html, 'html.parser')

    # find all the listings
    listings = soup.find_all('div', class_='classified')

    # create a list to store the data
    for listing in listings:
        data.append(extract_listing_data(listing))
 
    print("Page ", current_page)
    current_page += 1


# close the webdriver
driver.quit()

# convert the data to a pandas dataframe and save to CSV
df = pd.DataFrame(data)
df.to_csv("dhakaflats.csv", index=False)


# In[ ]:




