# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")



if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())



# obtain high resolution images for each of Mar's hemispheres
url = 'https://marshemispheres.com/'
browser.visit(url)

# pull html into Beautiful Soup parser
html=browser.html
soup=bs(html, 'html.parser')

# create list for dictionay to hold title and the high resolution urls
img_title_list = []


high_reso_image = soup.find_all('div', class_ = 'description')

for image in high_reso_image:
   
    image_title = image.find('h3').get_text()
   
    img_url = image.find('a', class_ = 'itemLink product-item')['href']
    hemis_url = url + img_url
 
    browser.visit(hemis_url)
    html = browser.html
    soup = bs(html,'html.parser')
    img_src = soup.find('img', class_='wide-image')['src']
    highresol_imgurl = url + img_src

  
    hemisphere_image_url = [{
        "title": image_title,
        "image_url": highresol_imgurl
    }]
  
    img_title_list += hemisphere_image_url


browser.quit()


mars_information = {
    "news_title": news_titles.text,
    "news_p": news_p.text,
    "featured_imge_url": featured_imge_url,
    "facts_table": table_df.to_html(),
    "hemispheres": img_title_list
    }
   
return mars_information







