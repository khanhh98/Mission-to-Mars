

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():       
# Set executable path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless= True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres":hemispheres(browser),
        "last_modified": dt.datetime.now()

    }
    # Stop webdriver and return data
    browser.quit()
    return data

# Define the function
def mars_news(browser):
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title
        news_title = slide_elem.find('div', class_= 'content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_= 'article_teaser_body').get_text()
    except AttributeError:
        return None, None
 
    return news_title, news_p

# ### Featured Image

def featured_image(browser):

# Vist url
    url_2 = 'https://spaceimages-mars.com'
    browser.visit(url_2)





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

# Scrape table about Mars facts
def mars_facts():
    try:
        # Use 'read_html' to scrape the facts table into a dataFrame
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataFrame
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
        

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

# Getting hemisphere url
def hemispheres(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url + 'index.html')

    # Click the link, find the sample anchor, return the href
    hemisphere_image_urls = []
    for i in range(4):
        # Find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item img")[i].click()
        hemi_data = scrape_hemisphere(browser.html)
        hemi_data['img_url'] = url + hemi_data['img_url']
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemi_data)
        # Finally, we navigate backwards
        browser.back()

    return hemisphere_image_urls


# Define function to scrape data
def scrape_hemisphere(html_text):
    # Parse HTML text
    soup_hemi = soup(html_text, "html.parser")

    try:
        title_hemi = soup_hemi.find("h2", class_="title").get_text()
        url_hemi = soup_hemi.find("a", text="Sample").get("href")
    except AttributeError:
        title_hemi = None
        url_hemi = None
    hemisphere_dict = {
        "title": title_hemi,
        "img_url": url_hemi
    }
    return hemisphere_dict

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())







