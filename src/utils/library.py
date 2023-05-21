
# Native
from datetime import datetime
from pathlib import Path
from time import sleep
from random import randint

# Thrid
import pandas as pd

# Own
from utils.conn_selenium_v3 import conn_uc, click, get_element, get_elements, center_scroll
from utils.variables import xpath


class Library:

    def __init__(self, url, type) -> None:
        self.url = url
        self.type = type
        self.list_urls = []
        self.driver = None
        self.next_page = True
        self.create_reg()

    def create_reg(self):
        time = datetime.now()
        to_directory = "./data/"
        to_directory += f"{time.day}_{time.month}"
        # Carpeta destino
        self.to_directory = Path(to_directory)

        if not self.to_directory.exists():
           self.to_directory.mkdir()


    def main_process(self) -> None:
        print("main_process")
        try:
            self.initiation()
            while self.next_page:
                sleep(randint(7,13))
                print("window_handles:", len(self.driver.window_handles))
                if len(self.driver.window_handles) != 1:
                    self.driver.switch_to.window(self.driver.window_handles[0])
                self.check_pop_up()
                self.get_books()
                self.next()
                
            print("pandas DF")
            out_df = pd.DataFrame(self.list_urls)
            out_df.to_csv(f"{self.to_directory}/{self.type}.csv")

        except Exception as err:
            print(f"{__name__}: {err}")

        finally:
            if self.driver:
                self.driver.quit()

    def initiation(self) -> None:
        print("initiation")
        try:
            self.driver = conn_uc(headless = False)
            self.driver.get(self.url)

        except Exception as err:
            raise Exception(f"{__name__}-initiation: {err}, self.url: {self.url}")
        
    def get_books(self):
        print("get_books")
        try:
            we_books_links = get_elements(self.driver, "xpath", xpath["recover_links"])
            list_urls = [book.get_attribute('href') for book in we_books_links]
            self.list_urls.extend([url for url in list_urls])
        except Exception as err:
            raise Exception(f"{__name__}-get_books: {err}, xpath: {xpath['recover_links']}")
        
    def next(self):
        print("next")
        try:
            next_page = get_element(self.driver, "xpath", xpath['next_page'])
            center_scroll(next_page)
            self.next_page = click(self.driver, "xpath", xpath['next_page'], log = False)

        except Exception as err:
            raise Exception(f"{__name__}-next: {err}") 
        
    def check_pop_up(self):
        print("check_pop_up")
        try:
            wait_time = sleep(randint(7,13))
            return click(self.driver, "xpath", xpath['pop_up'], wait_time=wait_time, log = False)
        except Exception as err:
            raise Exception(f"{__name__}: {err}, xpath: {xpath['pop_up']}")