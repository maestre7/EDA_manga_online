
# Native
from uuid import uuid4
from shutil import rmtree
from datetime import datetime
from pathlib import Path
from time import sleep
from random import randint

# Thrid
import pandas as pd

# Own
from utils.conn_selenium_v3 import conn_uc, click, get_elements, get_element, center_scroll
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
            print("pandas DF")
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
                sleep(randint(7,13))
                self.check_pop_up()
                self.get_information()
                self.get_chapters()
                self.closed_tad()

        except Exception as err:
            raise Exception(f"{__name__}-collection_process: {err}, self.list_urls: {self.list_urls}")

    
    def open_tab(self, new_url):
        print("open_tab")
        try:
            self.driver.execute_script("window.open('');") # Open a new window
            # Switch to the new window and open new URL
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.get(new_url)

        except Exception as err:
            print("self.driver.window_handles:", self.driver.window_handles)
            raise Exception(f"{__name__}-open_tab: {err}, new_url: {new_url}")

  
    def get_information(self):
        print("get_information")
        try:
            dict_out = {}
            list_name = []
            # UUID
            dict_out["uuid"] = uuid4()

            # Synopsis
            print("Synopsis")
            book_synopsis = get_element(self.driver, "xpath", xpath["book_synopsis"], log=False)
            dict_out["synopsis"] = book_synopsis.text if book_synopsis else None

            center_scroll(book_synopsis, log=False)  # center_scroll

            # Demography
            print("Demography")
            book_demography = get_element(self.driver, "xpath", xpath["book_demography"], log=False)
            dict_out["demography"] = book_demography.text if book_demography else None

            # Type
            print("Type")
            book_type = get_element(self.driver, "xpath", xpath["book_type"], log=False)
            dict_out["type"] = book_type.text if book_type else None

            # Title
            print("Title")
            book_name00 = get_element(self.driver, "xpath", xpath["book_name00"], log=False)
            if book_name00:
                name00 = book_name00.text
                if name00[-1] == ')':
                    data_name = name00.rsplit(' ( ', 1)
                    name = data_name[0]
                    anno = data_name[1][:-1]
                else: 
                    name = name00
                    anno = None

                dict_out["name"] = name
                dict_out["anno"] = anno
                list_name.append(name) # Title

            # Sub-Title
            print("Sub-Title")
            book_name01 = get_element(self.driver, "xpath", xpath["book_name01"], log=False)
            if book_name01:
                list_name.append(book_name01.text) # Sub-Title

            # Synonyms
            print("Synonyms")
            book_synonyms = get_elements(self.driver, "xpath", xpath["book_synonyms"], log=False)
            if book_synonyms:
                [list_name.append(i.text) for i in book_synonyms]
            
            # Genre
            print("Genre")
            book_genre = get_elements(self.driver, "xpath", xpath["book_genre"], log=False)
            if book_genre:
                dict_out["genre"] = ', '.join([g.text for g in book_genre])
            else:
                dict_out["genre"] = None

            # Book_Score
            print("Book_Score")
            book_score = get_element(self.driver, "xpath", xpath["book_score"], log=False)
            dict_out["score"] = book_score.text if book_score else 0

            # Book_Status
            print("Book_Status")
            book_status = get_element(self.driver, "xpath", xpath["book_status"], log=False)
            dict_out["book_status"] = book_status.text if book_status else None

            # Book_Cover
            print("Book_Cover")
            book_cover = get_element(self.driver, "xpath", xpath["book_cover"], log=False)
            dict_out["book_cover"] = book_cover.get_attribute("src") if book_cover else None

            # Book_Social
            print("Book_Social")
            book_social = get_elements(self.driver, "xpath", xpath["book_social"], log=False)
            if book_social:
                social_list = [e.text for e in book_social]
                dict_out["read"] = social_list[0]
                dict_out["pending"] = social_list[1]
                dict_out["following"] = social_list[2]
                dict_out["favorite"] = social_list[3]
                dict_out["have"] = social_list[4]
                dict_out["abandoned"] = social_list[5]
            else:
                dict_out["read"] = None
                dict_out["pending"] = None
                dict_out["following"] = None
                dict_out["favorite"] = None
                dict_out["have"] = None
                dict_out["abandoned"] = None

            print("Out")
            
        except Exception as err:
            print("get_information-err:", err)
            res_pop_up = self.check_pop_up() # pop_up: //button/span[text()="ACEPTO"]

            if res_pop_up:
                print("vuelve a ejecutar el proceso_recolector")
                self.get_information()
            else:
                res_not_found = self.check_not_found() # not_found: //h1[text()="404 Not Found"]
                raise Exception(f"{__name__}-get_information: {err}, not_found: {res_not_found}")
        else:
            print("Append")
            self.out.append(dict_out)

    def get_chapters(self):
        print("get_chapters")

        try:
            list_out = []

            # Chapters_Titles
            print("chapters_titles")
            chapters_titles = get_elements(self.driver, "xpath", xpath["chapters_titles"], log=False)
            if chapters_titles:
                list_chapters_titles = [i.text for i in reversed(chapters_titles)]

             urls_web = recoger_elementos(driver, C.tmobook['chapters_urls'], wait_time = False) # Ojito no es click
                #sleep(uniform(0,2))
                if not urls_web in [False, None]:
                    sal_urls = [i.get_attribute("href") for i in reversed(urls_web)]


        except Exception as err:
            print("get_chapters-err:", err)
            res_pop_up = self.check_pop_up() # pop_up: //button/span[text()="ACEPTO"]

            if res_pop_up:
                print("vuelve a ejecutar el proceso_recolector")
                self.get_chapters()
            else:
                res_not_found = self.check_not_found() # not_found: //h1[text()="404 Not Found"]
                raise Exception(f"{__name__}-get_chapters: {err}, not_found: {res_not_found}")



    def closed_tad(self):
        print("closed_tad")
        try:
            # Closing new_url tab
            self.driver.close()
            
            # Switching to old tab
            self.driver.switch_to.window(self.driver.window_handles[0])
        except Exception as err:
            print("self.driver.window_handles:", self.driver.window_handles)
            raise Exception(f"{__name__}-closed_tad: {err}")

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