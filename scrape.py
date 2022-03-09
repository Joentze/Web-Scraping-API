from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")

PATH = "./driver/chromedriver"

#driver = webdriver.Chrome(PATH, options=chrome_options)

driver = webdriver.Chrome(PATH)
def get_hrefs(link:str, xpaths:list)->list:
    links = []
    driver.get(link)
    try:
        for xpath in xpaths:
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                links.append(element.get_attribute('href'))
            except:
               pass
    finally:
        driver.get("data:,")
    return links

def get_texts(link:str, contents:object)->object:
    response_content = {}
    driver.get(link)
    try:
        for name, content in contents.items():
            print(name, content)
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, content))
                )
                response_content[name] = element.get_attribute("innerHTML")
            except:
               pass
    finally:
        driver.get("data:,")
    return response_content



if __name__ == "__main__":
    pass