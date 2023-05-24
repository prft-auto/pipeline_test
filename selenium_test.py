from selenium import webdriver
from selenium.webdriver.common.by import By
import webdrivermanager
import urllib3
import argparse

def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--selenium-grid", action='store', dest='grid', required=True, help="http://HOST:PORT/wd/hub")
    parser.add_argument("--elastic-search", action='store', dest='elastic', required=True, help='http://HOST:PORT')
    return parser.parse_args()

def get_selenium_drivers():
    webdrivermanager.ChromeDriverManager().download_and_install()

def get_selenium_remote(selenium_grid):
    chrome_opts = webdriver.ChromeOptions()
    driver = webdriver.Remote(selenium_grid, options=chrome_opts)
    return driver

def load_automation_site(driver: webdriver.Remote):
    driver.get("https://the-internet.herokuapp.com/")
    print(driver.find_element(By.LINK_TEXT("Broken Images")).text)


def elastic_update(elastic):
    CONTENT_TYPE = "Content-Type"
    CONTENT_TYPE_VALUE = "application/json"
    elastic_location = f"{elastic}/default_test/_doc"
    poolmanager = urllib3.PoolManager()
    response = poolmanager.request(
        "POST",
        elastic_location,
        headers={CONTENT_TYPE: CONTENT_TYPE_VALUE},
        body='{"name": "test1", "location": "https://the-internet.herokuapp.com/", "success": "True"}',
        timeout=20
    )
    if 200 != response.status:
        print(f"Unsuccessful send to: {elastic_location}")
    else:
        print(f"Successful send to: {elastic_location}")


if '__main__' == __name__:
    args = get_args()
    get_selenium_drivers()
    driver = get_selenium_remote(args.grid)
    load_automation_site(driver)
    elastic_update(args.elastic)




