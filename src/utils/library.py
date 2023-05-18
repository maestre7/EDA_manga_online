
# Native
from uuid import uuid4
from shutil import rmtree
from datetime import datetime
from pathlib import Path

# Thrid
import pandas as pd

# Own
from utils.conn_selenium_v3 import conn_uc, click, get_elements, get_element
from utils.variables import xpath


class Library:

    def __init__(self, url, type) -> None:
        self.url = url
        self.type = type
        self.out = []
        self.driver = None
        self.create_reg()

    def main_process(self) -> None:
        print("main_process")
        try:
            self.initiation()
            self.get_books()
            self.collection_process()
            out_df = pd.DataFrame(self.out)
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
            pop_up = self.check_pop_up()
            print("pop_up:", pop_up)

        except Exception as err:
            raise Exception(f"{__name__}-initiation: {err}, self.url: {self.url}")
        
    def get_books(self):
        print("get_books")
        try:
            we_books_links = get_elements(self.driver, "xpath", xpath["recover_links"])
            self.list_urls = [book.get_attribute('href') for book in we_books_links]

        except Exception as err:
            raise Exception(f"{__name__}-get_books: {err}, xpath: {xpath['recover_links']}")
        
    def collection_process(self):
        print("collection_process")
        try:
            for book_url in self.list_urls:
                self.open_tab(book_url)
                self.get_information()
                self.closed_tad()

        except Exception as err:
            raise Exception(f"{__name__}-collection_process: {err}, self.list_urls: {self.list_urls}")

    
    def open_tab(self, new_url):

        try:
            self.driver.execute_script("window.open('');") # Open a new window
            # Switch to the new window and open new URL
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get(new_url)

        except Exception as err:
            raise Exception(f"{__name__}: {err}, new_url: {new_url}")

  
    def get_information(self) :
        print("get_information")
        try:
            list_name = []
            # UUID
            uuid = uuid4()
            # Demography
            book_demography = get_element(self.driver, "xpath", xpath["book_demography"])
            demography = book_demography.text if book_demography else None
            # Type
            book_type = get_element(self.driver, "xpath", xpath["book_type"])
            type = book_type.text if book_type else None
            # Title
            book_name00 = get_element(self.driver, "xpath", xpath["book_name00"])
            if book_name00:
                name00 = book_name00.text
                name = name00.rsplit(' ( ', 1)[0] if name00[-1] == ')' else name00
                list_name.append(name) # Title
            # Sub-Title
            book_name01 = get_element(self.driver, "xpath", xpath["book_name01"])
            if book_name01:
                list_name.append(book_name01.text) # Sub-Title
            # Synonyms
            book_synonyms = get_element(self.driver, "xpath", xpath["book_synonyms"])
            if book_synonyms:
                [list_name.append(i.text) for i in book_synonyms]
            # Genre
            book_genre = get_element(self.driver, "xpath", xpath["book_genre"])
            str_genre = ', '.join([g.text for g in book_genre])
            # Synopsis
            book_synopsis = get_element(self.driver, "xpath", xpath["book_synopsis"])
            synopsis = book_synopsis.text if book_synopsis else None

            str_name = ":::".join(list_name)
            dict_out = {"uuid": uuid, "type": type, "demography": demography, "genre": str_genre }
            dict_out["synopsis"] = synopsis
            dict_out["name"] = name
            #dict_out["synonyms"] = str_name
            self.out.append(dict_out)

        except Exception as err:
            print("err:", err)
            res_pop_up = self.check_pop_up() # pop_up: //button[text()="ACEPTO"]

            if res_pop_up:
                print("vuelve a ejecutar el proceso_recolector")
                self.get_information()
            else:
                res_not_found = self.check_not_found() # not_found: //h1[text()="404 Not Found"]
                raise Exception(f"{__name__}: {err}, not_found: {res_not_found}")


    def closed_tad(self):

        try:
            # Closing new_url tab
            self.driver.close()
            
            # Switching to old tab
            self.driver.switch_to.window(self.driver.window_handles[0])
        except Exception as err:
            raise Exception(f"{__name__}: {err}")

    def check_pop_up(self):
        print("check_pop_up")
        try:
            return click(self.driver, "xpath", xpath['pop_up'], log = False)
        except Exception as err:
            raise Exception(f"{__name__}: {err}, xpath: {xpath['pop_up']}")
        
    def check_not_found(self):

        try:
            return get_element(self.driver, "xpath", xpath['upkeep'], log = False)
        except Exception as err:
            raise Exception(f"{__name__}: {err}, xpath: {xpath['upkeep']}")
        
    def create_reg(self):
        time = datetime.now()
        to_directory = "./data/"
        to_directory += f"{time.day}_{time.month}"
        # Carpeta destino
        self.to_directory = Path(to_directory)

        if not self.to_directory.exists():
           self.to_directory.mkdir()
    
def main():
    app = Library()
    app.main_process()
    return 0

if __name__ == '__main__':
    main()