# imports dependencies
import time
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import flask
import pymongo

def init_browser():
    executable_path = {"executable_path": "./chromedriver_win32/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)

def scrape ():
    """Scrapes website for mars data to returns a dictionary"""
    
    browser = init_browser()
    mars_data = {}

    # visit the NASA Mars News site and scrape headlines
    mars_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find(class_='content_title').text
    news_p = soup.find(class_='article_teaser_body').text
    mars_data["Headlines"] = news_title
    mars_data["article_teaser"] = news_p
    #print(mars_data)

    # visits the JPL website to scrape featured image
    browser = init_browser()
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(2)
    #print("Befor click of full image")
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    #print("Befor click of more info")
    browser.click_link_by_partial_text('more info')
    #print("after  more info")
    html = browser.html
    #print('---printing html---')
    #print(html)
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    image = soup.body.find("img",class_="main_image")["src"]
    
    featured_image_url = "https://jpl.nasa.gov"+image
    #print(featured_image_url)
    
    mars_data["featured_image"] = featured_image_url
    #print(mars_data)
    # visit the mars weather report twitter and scrape the latest tweet
    browser = init_browser()
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_twitter_weather = soup.find('p', class_="tweet-text").text
    mars_data["mars_weather"] = mars_twitter_weather
    #print(mars_data)
    # visit space facts and scrap the mars facts table
    mars_facts = "https://space-facts.com/mars"
    browser.visit(mars_facts)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_table = pd.read_html(mars_facts)
    mars_df = mars_table[0]
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)
    mars_data["facts_table"] = mars_df.to_html()
    #print(mars_data)
    # scrape images of Mars' hemispheres from the USGS site
    browser = init_browser()
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #print('before visiting hemurl')
    browser.visit(hem_url)
    time.sleep(2)
    html = browser.html
    #print('hemisphere url result',html)
    soup = BeautifulSoup(html, "html.parser")

    hemispheres = soup.find_all("div", class_="item")
    #print('hemispheres result',hemispheres)
    mars_hemispheres = []


    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        image_link = hemisphere.find("a")["href"]
        image_url = "https://astrogeology.usgs.gov/" + image_link    
        browser.visit(image_url)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        images_url = downloads.find("a")["href"]
        mars_hemispheres.append({"title": title,
                             "img_url": images_url})

    mars_data["hemisphere_images"] = mars_hemispheres
    browser.quit()

    return mars_data