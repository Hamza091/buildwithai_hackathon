import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

options = Options()
options.add_argument('--headless')  # Ensure Chrome runs headlessly
options.add_argument('--no-sandbox')  # Disable the sandboxing feature (sometimes required in WSL)
options.add_argument('--disable-dev-shm-usage')  # Avoid issues with shared memory
options.add_argument('--remote-debugging-port=9222')  # Debugging port for Chrome
options.add_argument('--disable-gpu')  # Disable GPU acceleration (not needed in WSL)

# Start the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Step 1: Fetch the website's HTML content dynamically using Selenium
url = "https://www.bikemonkey.net/events"  # Replace with the actual URL
driver.get(url)

# Wait for dynamic content to load (adjust the time as needed)
time.sleep(5)

# Step 2: Parse the rendered HTML content
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Step 3: Extract event links (based on the structure of the HTML)
event_links = []
for a_tag in soup.find_all('a', class_='event-logo'):
    event_url = a_tag.get('href')
    if event_url:
        event_links.append(event_url)

print("Event Links:")
print(event_links)

# Step 4: Visit each event link and fetch its full HTML
for event_url in event_links:
    # If the event URL is relative, join it with the base URL
    if event_url.startswith("/"):
        event_url = urljoin("https://www.bikemonkey.net", event_url)
    
    # Request the event page via Selenium to fetch the dynamic content
    driver.get(event_url)
    
    # Wait for dynamic content to load (adjust the time as needed)
    time.sleep(5)
    
    # Parse the event page's HTML content
    event_soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Create a valid filename by extracting the last part of the URL
    event_name = event_url.split('/')[-1]  # Get the last part of the URL as the filename
    if not event_name:  # Handle the case where the event URL ends with a slash
        event_name = "index"

    # Create a folder to store the HTML files if it doesn't exist
    os.makedirs("event_htmls", exist_ok=True)

    # Write the HTML content to a text file
    with open(f"event_htmls/{event_name}.txt", "w", encoding="utf-8") as file:
        file.write(str(event_soup.get_text()))  # Write the HTML content

    print(f"Successfully saved HTML for: {event_url}")

# Close the browser once done
driver.quit()
