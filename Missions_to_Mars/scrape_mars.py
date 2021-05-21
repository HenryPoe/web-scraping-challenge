from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_news_url = 'https://redplanetscience.com/'
    space_image_url = 'https://spaceimages-mars.com/'
    mars_facts_url = 'https://galaxyfacts-mars.com/'
    mars_hemis_url = 'https://marshemispheres.com/'

    # Scrape from mars news
    browser.visit(mars_news_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve the latest news title and paragraph tag objects
    news_title_tag = soup.select_one(".content_title")
    news_p_tag = soup.select_one(".article_teaser_body")
    # Get the text in the title and paragraph html tags
    news_title = news_title_tag.string
    news_p = news_p_tag.string

    # Scrape from space image page
    browser.visit(space_image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Parse out the main image url
    image_tag = soup.find('img', class_='headerimage fade-in')
    src = image_tag['src']
    featured_space_image_url = space_image_url + src

    # Scrape from the mars facts website
    table = pd.read_html(mars_facts_url)
    # Convert the table to html table string
    mars_earth_html_table = table[0].to_html()

    # Scrape mars hemispheres page
    browser.visit(mars_hemis_url)
    hemisphere_image_urls = []
    # Get the links for all 4 hemisphere images
    for x in range(4):
        # Find all the hemisphere links on the home page and navigate to the next one
        links = browser.links.find_by_partial_text('Hemisphere')
        links[x].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        # Find the link and title to the full image
        hemi_img = soup.find('a', string='Sample')['href']
        title = soup.find('h2', class_='title').string
        temp_dict = {"title": title, "img_url": mars_hemis_url + hemi_img}
        hemisphere_image_urls.append(temp_dict)
        # Navigate back to the home page
        browser.back()

    # Quit the browser
    browser.quit()
    
    # Add mars data to dictionary
    mars_data = {
        "news_title": news_title,
        "news_text": news_p,
        "space_image": featured_space_image_url,
        "mars_comparison_table": mars_earth_html_table,
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_data
