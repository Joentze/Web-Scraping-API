from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
GOOGLE_CHROME_PATH = os.environ["GOOGLE_CHROME_PATH"]
CHROMEDRIVER_PATH = os.environ["CHROMEDRIVER_PATH"]

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = GOOGLE_CHROME_PATH

#PATH = "./driver/chromedriver"
#driver = webdriver.Chrome(PATH)
def get_hrefs(link:str, xpaths:list)->list:
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
    driver.get(link)
    links = []
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
        driver.quit()
    return links

def get_texts(link:str, contents:object)->object:
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
    driver.get(link)
    response_content = {}
    try:
        for name, content in contents.items():
            print(name, content)
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, content))
                )
                response_content[name] = filter_text(element.get_attribute("innerHTML"))
            except:
                response_content["body"] = get_body_fallback(driver)
                break
    finally:
        driver.quit()
    return response_content

def get_from_child_one(grab_object:object)->list:
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
    driver.get(grab_object["link"])
    main_tag = grab_object["main_tag"]
    var = grab_object["identifier_type"]
    var_content = grab_object["identifier"]
    wait_time=int(grab_object["wait_time"])
    get_child = f"//{main_tag}[@{var}='{var_content}']//child::*"
    try:
        elements = WebDriverWait(driver, wait_time).until(
                EC.presence_of_all_elements_located((By.XPATH, get_child))
            )
        links = [element.get_attribute(grab_object["attribute"]) 
                for element in elements 
                if element.tag_name == grab_object["tag"]]
    finally:
        driver.quit()
    return links

def get_from_child_many(request_object:list)->list:
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
    grab_objects = request_object["grab_objects"]
    link = request_object["link"]
    driver.get(link)
    results = []
    try:
        for grab_object in grab_objects:
            try:
                main_tag = grab_object["main_tag"]
                var = grab_object["identifier_type"]
                var_content = grab_object["identifier"]
                wait_time=int(grab_object["wait_time"])
                get_child = f"//{main_tag}[@{var}='{var_content}']//child::*"
                elements = WebDriverWait(driver, wait_time).until(
                        EC.presence_of_all_elements_located((By.XPATH, get_child))
                    )
                results.append([element.get_attribute(grab_object["attribute"]) 
                                for element in elements 
                                if element.tag_name == grab_object["tag"]])
            except:
                pass
    finally:
        driver.quit()
    return results

def get_body_fallback(driver):
    print("trying something else")
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "/html/body"))
        )
        return filter_text(element.get_attribute("innerHTML"))
    except:
        pass

def filter_text(text):
    soup = BeautifulSoup(text, "html.parser")
    texts = soup.find_all(text=True)
    filtered_text = list(filter(tag_visible, texts))
    return " ".join(filtered_text)

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True



if __name__ == "__main__":
    pass