from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# initialize the Chrome driver
driver = webdriver.Chrome()

# navigate to the URL
driver.get("https://www.local.ch/en/",)

# Searching for "Clinic"
def search_query(query):
    search = driver.find_element("name", "what")
    search.clear()
    time.sleep(3)
    search.send_keys(query)
    time.sleep(3)
    search.send_keys(Keys.RETURN)
    time.sleep(3)

# extract the source code
def source():
    source_code = driver.page_source
    # Sleep for 3 second 
    time.sleep(3)
    # parse the source code with BeautifulSoup
    soup = BeautifulSoup(source_code, "html.parser")
    time.sleep(3)

# Extracting the data
def datasearch():
    searchResult = driver.find_element(By.CLASS_NAME, "search-header-results")
    data = searchResult.text
    print(f"there's {data}\n")
    time.sleep(2)

# Get the phone_numbers elements
def data_scrape():
    # data = driver.find_element(By.CLASS_NAME, "col-xs-12.col-md-8")
    # Loop in data end extract phone numbers
    components = driver.find_elements(By.CSS_SELECTOR, ".js-entry-card-container.row.lui-margin-vertical-xs.lui-sm-margin-vertical-m")
    for component in components:
        name = component.find_element(By.CSS_SELECTOR, ".lui-margin-vertical-zero.card-info-title").text
        addre = component.find_element(By.CSS_SELECTOR, ".card-info-address").text
        try:
            phone = component.find_element(By.CSS_SELECTOR, "a[title='Call']").get_attribute("href").replace("tel:", "")
            email = component.find_element(By.CSS_SELECTOR, "a[title='E-Mail']").get_attribute("href").replace("mailto:", "")

        except:
            phone = "Not available"
            email = "Not available"
        print(f"Name: {name}\nAddress: {addre}\nPhone: {phone}\nEmail: {email}\n")


# Sleep for 2 second
search_query("Clinique")
source()
datasearch()

# extract the total number of pages
total_pages = 100
print(f"Total Pages: {total_pages}\n")

# iterate over each page and extract data
for page in range(2, int(total_pages)+1):
    driver.get(f"https://www.local.ch/en/q?what=clinique&where=Switzerland&rid=E5ct&slot=tel&page={page}")
    time.sleep(3)
    source()
    datasearch()
    data_scrape()

driver.quit()
