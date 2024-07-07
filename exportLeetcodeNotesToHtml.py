import sys
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re

# Check if URL argument is provided and exit if not
if len(sys.argv) != 2:
    print("Usage: python script_name.py <url>")
    sys.exit(1)

url = sys.argv[1]
filename = urlparse(url).path.strip('/').split('/')[-1] + '.html'

# Selenium in GUI mode
driver = webdriver.Chrome()

# Selenium in headless : not working due to cloudfare bot detection
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment this line to run in headless mode
# chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (necessary in headless mode sometimes)
# driver = webdriver.Chrome(options=chrome_options)

SESSION_COOKIE_NAME = 'LEETCODE_SESSION'
SESSION_COOKIE_VALUE = 'enter_session_cookie_value_here'
waitAfterRefreshTime = 10


cookies = [
    {'name': SESSION_COOKIE_NAME, 'value': SESSION_COOKIE_VALUE}
]

# Open the desired URL
driver.get(url)

for cookie in cookies:
    driver.add_cookie(cookie)

# Refresh the page to apply cookies
driver.refresh()

time.sleep(waitAfterRefreshTime)

# Wait until the element with class name 'break-words' is available
html_content = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'break-words'))
).get_attribute('outerHTML')

soup = BeautifulSoup(html_content, 'html.parser')

# Remove all <svg> elements
for svg in soup.find_all('svg'):
    svg.decompose()

# Add <br> after each <img> element
for img in soup.find_all('img'):
    img.insert_after(soup.new_tag('br'))


# Replace <a> containing <iframe> with simple <a> tag with link
for a_tag in soup.find_all('a', href=re.compile(r'^https://www\.youtube\.com/watch')):
    if 'href' in a_tag.attrs:
        a_tag['href'] = a_tag['href']  # Use entire YouTube URL as href attribute
        a_tag.string = f'{a_tag["href"]}'  # Set text inside <a> tag to full URL

# Remove color formatting from all elements
for element in soup.find_all():
    # Remove `color` attributes
    if element.has_attr('color'):
        del element['color']
    
    # Remove color-related properties from `style` attributes
    if element.has_attr('style'):
        styles = element['style'].split(';')
        # Keep only non-color styles
        new_styles = [style for style in styles if not re.search(r'color', style, re.IGNORECASE)]
        element['style'] = ';'.join(new_styles)

        # If the style attribute is now empty, remove it
        if not element['style']:
            del element['style']

# Save the modified HTML content to a file
with open(filename, 'w', encoding='utf-8') as file:
    file.write(str(soup))

# Print confirmation message
print("Content saved as " + filename)