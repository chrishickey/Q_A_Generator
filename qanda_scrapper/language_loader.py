import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


# TODO: These selectors can be written better !
LANGUAGE_TAB_SELECTOR = (
    "#root > div > div > div.sc-iNiRlI.bJjJto > div > "
    "div.sc-eJobrH.fDjpTS.col-start-8.col-end-none > "
    "div:nth-child(4) > div > div > div"
)

ENGLISH_TAB = (
    "#root > div > div > div.sc-iNiRlI.bJjJto > div > "
    "div.sc-eJobrH.fDjpTS.col-start-8.col-end-none > "
    "div:nth-child(4) > div > div.sc-ArjuK.dTvijX > "
    "div.sc-cTJlEM.hJTTRl > svg > g > path:nth-child(1)"
)


def load_english(driver: WebDriver):
    time.sleep(1)
    # Find all <a> tags on the page
    element = driver.find_element(By.CSS_SELECTOR, LANGUAGE_TAB_SELECTOR)
    element.click()
    time.sleep(1)
    element = driver.find_element(By.CSS_SELECTOR, ENGLISH_TAB)
    element.click()
    time.sleep(1)
