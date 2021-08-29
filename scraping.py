# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    
    # Set up chrome browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    # Use mars_news to pull data
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    # Close browser
    browser.quit()

    return data



def mars_news(browser):

    # Set url and visit
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Set optional delay for loading page
    browser.is_element_present_by_css('div.list_text', wait_time = 1)

    # Set up html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except to handle errors
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Save text as new variable
        news_title = slide_elem.find('div', class_= 'content_title').get_text()

        # Retrieve article summary, as well
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p


# ## Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse html
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except to handle errors
    try:
            
        # Find relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')



    except AttributeError:
        return None

    # Create url for image
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts

def mars_facts():
    # Add try/except to handle errors
    try:
            
        # Create Dataframe from html from new site, first table
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Set columns
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)


    # Convert back to html code
    return df.to_html(classes="table table-striped")


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())




