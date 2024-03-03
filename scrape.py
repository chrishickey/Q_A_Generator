# !/usr/bin/env python3
import os
import time
import argparse

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from qanda_scrapper.language_loader import load_english

LANGUAGE_LOADER_DICT = {
    "EN": load_english,
    "KR": lambda *args, **kwargs: None,  # Stub as noting needs to be done
}


def parse_arguments() -> argparse.Namespace:
    # setup arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url", help="Starting url to scrape from.")
    parser.add_argument("text_dir", help="Directory to save scraped text.")
    parser.add_argument("--language", help="Langauge to loads screen", default="KO")
    return parser.parse_args()


def get_chrome_driver() -> Chrome:
    options = webdriver.ChromeOptions()
    # Window size needed to be increased or else language tab doesn't exist
    options.add_argument("--window-size=2560,1440")
    options.page_load_strategy = "none"
    driver = Chrome(options=options)
    driver.implicitly_wait(10)
    return driver


def main(base_url: str, text_dir: str, language: str):
    assert language in LANGUAGE_LOADER_DICT
    os.makedirs(text_dir, exist_ok=True)
    driver = get_chrome_driver()
    driver.get(base_url)
    LANGUAGE_LOADER_DICT[language](driver=driver)
    all_web_pages = {base_url}
    searched_web_pages = set()
    file_counter = 1
    saved_hashes = []
    while all_web_pages - searched_web_pages:
        for url in all_web_pages - searched_web_pages:
            driver.get(url)
            searched_web_pages.add(url)
            time.sleep(2)
            text = driver.find_element(By.TAG_NAME, "body").text
            hashed_text = hash(text)
            if hashed_text not in saved_hashes:
                with open(os.path.join(text_dir, f"{file_counter}.txt"), "w+") as fh:
                    fh.write(text)
                saved_hashes.append(hashed_text)
                file_counter += 1
                links = driver.find_elements(By.TAG_NAME, "a")

                for link in links:
                    href = link.get_attribute("href")
                    if href and href not in all_web_pages and base_url in href:
                        all_web_pages.add(href)


if __name__ == "__main__":
    args = parse_arguments()
    main(args.base_url, args.text_dir, args.language)
