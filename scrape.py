from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")

PATH = "./driver/chromedriver"

#driver = webdriver.Chrome(PATH, options=chrome_options)
driver = webdriver.Chrome(PATH)


driver.get("https://news.kompas.com/")

payload = [
    "/html/body/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]/ul/div/div/li[1]/a",
]

links = []

try:
    for load in payload:
        try:
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, load))
            )
            links.append(element.get_attribute('href'))
        except:
           pass
finally:
    print(links)
    driver.quit()



if __name__ == "__main__":
    pass