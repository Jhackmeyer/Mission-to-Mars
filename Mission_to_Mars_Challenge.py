
# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Set up chrome
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Mars Article

# Set url and visit
url = 'https://redplanetscience.com'
browser.visit(url)
# Set optional delay for loading page
browser.is_element_present_by_css('div.list_text', wait_time = 1)


# Set up html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# Scrape for article title
slide_elem.find('div', class_= 'content_title')



# Save text as new variable
news_title = slide_elem.find('div', class_= 'content_title').get_text()
news_title


# Retrieve article summary, as well
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images
# 


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()



# Parse html
html = browser.html
img_soup = soup(html, 'html.parser')



# Find relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel



# Create url for image
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts


# Create Dataframe from html from new site, first table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
# Set columns
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df



# Convert back to html code
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

html = browser.html


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
hem_soup = soup(html, 'html.parser')
base_url= 'https://marshemispheres.com/'


# Scrape for images and titles, put into list of dictionaries
hemisphere_img = hem_soup.find_all('img', class_='thumb')
hemisphere_title = hem_soup.find_all('h3')
for x in range(0,4):
    dictionary={}
    end_url = hemisphere_img[0+x].get('src')
    dictionary["image"] = f'{base_url}{end_url}'
    dictionary["title"] = hemisphere_title[0+x].get_text()
    hemisphere_image_urls.append(dictionary)


# Check work
hemisphere_image_urls



# Wrong images, we need jpgs
base_url = 'https://marshemispheres.com/'
# Empty List
hemisphere_image_urls = []
#Loop through the images on site
for x in range (3,7):
    # Create empty dictionary
    dictionary={}
    # Click image
    hemisphere_main = browser.find_by_tag('img')[x]
    hemisphere_main.click()
    # Parse new page
    html = browser.html
    hem_soup = soup(html, 'html.parser')
    # Find image url and title
    hemisphere_img = hem_soup.find_all('a', target="_blank")[-2].get('href')
    hemisphere_title = hem_soup.find('h2', class_="title").get_text()
    # Add to dictionary
    dictionary["image"] = f'{base_url}{hemisphere_img}'
    dictionary["title"] = hemisphere_title
    # Add dictionary to list
    hemisphere_image_urls.append(dictionary)
    # Go back to previous page
    browser.back()


# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_image_urls)


# 5. Quit the browser
browser.quit()




