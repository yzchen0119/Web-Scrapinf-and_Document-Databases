from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import io

# Initialize browser
def init_browser(): 
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)    

def scrape_info():
    
    browser = init_browser()
 
    mars_collection = {}
    
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    news_html = browser.html
    soup = BeautifulSoup(news_html, 'html.parser')
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text    
    mars_collection['news_title'] = news_title
    mars_collection['news_p'] = news_p
    
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    img_html = browser.html
    soup = BeautifulSoup(img_html, 'html.parser')
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url
    mars_collection['featured_image_url'] = featured_image_url  
    
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')    
    tweets = soup.find_all('div', class_='js-tweet-text-container')
    for tweet in tweets: 
        weather_tweet = tweet.find('p').text
        pic_text = tweet.find('p').find('a').text
        mars_weather = weather_tweet.replace(pic_text, '')        
        if 'sol' and 'low' in mars_weather:
            print(mars_weather)
            break
        else: 
            pass
    mars_collection['mars_weather'] = mars_weather
    
    facts_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)
    facts_df = mars_facts[1]
    facts_df.columns = ['Description', 'Value']
    html_table = facts_df.to_html(header=False, index=False, classes="dataframe table table-striped") 
    mars_collection['facts'] = html_table
    
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    soup = BeautifulSoup(hemispheres_html, 'html.parser')
    imgs = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    main_url = 'https://astrogeology.usgs.gov'
    for img in imgs: 
        title = img.find('h3').text
        partial_url = img.find('a', class_='itemLink product-item')['href'] 
        browser.visit(main_url + partial_url)
        img_html = browser.html
        soup = BeautifulSoup(img_html, 'html.parser')
        img_url = main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url}) 
    mars_collection['hemisphere_image_urls'] = hemisphere_image_urls
    
    browser.quit()
    
    return mars_collection
    
    