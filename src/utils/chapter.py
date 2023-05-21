

# Native
from uuid import uuid4
import os

import pandas as pd
from bs4 import BeautifulSoup as bs
# Own
from utils.conn_selenium_v3 import get_elements, get_element, conn_link
from utils.variables import xpath


def main_process(type_demo):
    try:
        exe_df = pd.read_csv(f"./data/origin/{type_demo}.csv")

        os.makedirs(f"./data/{type_demo}", exist_ok=True)
        list_info = []

        for url in exe_df["Url"]:
            #sleep(randint(3,7))
            driver = conn_link(headless = False)
            #driver = conn_uc(headless = False)
            driver.get(url)
            body = driver.execute_script("return document.body")
            source = body.get_attribute('innerHTML')
            soup = bs(source, "html.parser")

            not_found = soup.find("h1", class_="display-1")

            if not not_found:
                data = get_information(driver)
                data2 = get_chapters(soup)
                data2.reverse()
                # UUID
                uuid = str(uuid4())
                data["uuid"] = uuid
                list_info.append(data)
                list_chapters_df = pd.DataFrame(data2)
                list_chapters_df.to_csv(f"./data/{type_demo}/{uuid}.csv")

            driver.quit()

        list_info_df = pd.DataFrame(list_info)
        list_info_df.to_csv(f"./data/{type_demo}.csv")

    except Exception as err:
        print(f"{__name__}: {err}")
    finally:
        if driver:
            driver.quit()



def get_information(driver):
    #print("get_information")
    dict_out = {}
    try:  
        list_name = []

        # Synopsis
        #print("Synopsis")
        book_synopsis = get_element(driver, "xpath", xpath["book_synopsis"], wait_time=1, log=False)
        dict_out["synopsis"] = book_synopsis.text if book_synopsis else None

        # Demography
        #print("Demography")
        book_demography = get_element(driver, "xpath", xpath["book_demography"], wait_time=1, log=False)
        dict_out["demography"] = book_demography.text if book_demography else None

        # Type
        #print("Type")
        book_type = get_element(driver, "xpath", xpath["book_type"], wait_time=1, log=False)
        dict_out["type"] = book_type.text if book_type else None

        # Title
        #print("Title")
        book_name00 = get_element(driver, "xpath", xpath["book_name00"], wait_time=1, log=False)
        if book_name00:
            name00 = book_name00.text
            """ if name00[-1] == ')':
                data_name = name00.rsplit(' ( ', 1)
                name = data_name[0]
                anno = data_name[1][:-1]
            else: 
                name = name00
                anno = None """

            dict_out["name"] = name00
            #dict_out["anno"] = anno
            list_name.append(name00) # Title

        # Sub-Title
        #print("Sub-Title")
        book_name01 = get_element(driver, "xpath", xpath["book_name01"], wait_time=1, log=False)
        if book_name01:
            list_name.append(book_name01.text) # Sub-Title

        # Synonyms
        #print("Synonyms")
        book_synonyms = get_elements(driver, "xpath", xpath["book_synonyms"], wait_time=1, log=False)
        if book_synonyms:
            [list_name.append(i.text) for i in book_synonyms]
        
        # Genre
        #print("Genre")
        book_genre = get_elements(driver, "xpath", xpath["book_genre"], wait_time=1, log=False)
        if book_genre:
            dict_out["genre"] = ', '.join([g.text for g in book_genre])
        else:
            dict_out["genre"] = None

        # Book_Score
        #print("Book_Score")
        book_score = get_element(driver, "xpath", xpath["book_score"], wait_time=1, log=False)
        dict_out["score"] = book_score.text if book_score else 0

        # Book_Status
        #print("Book_Status")
        book_status = get_element(driver, "xpath", xpath["book_status"], wait_time=1, log=False)
        dict_out["book_status"] = book_status.text if book_status else None

        # Book_Cover
        #print("Book_Cover")
        book_cover = get_element(driver, "xpath", xpath["book_cover"], wait_time=1, log=False)
        dict_out["book_cover"] = book_cover.get_attribute("src") if book_cover else None

        # Book_Social
        #print("Book_Social")
        book_social = get_elements(driver, "xpath", xpath["book_social"], wait_time=1, log=False)
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
        
    except Exception as err:
        raise Exception(f"{__name__}-get_information: {err}")
    else:
        return dict_out
    

def get_chapters(soup):
    #print("get_chapters")
    
    list_out = []

    try: # list chapters
        li = soup.find_all("li", class_="list-group-item p-0 bg-light upload-link")

        for element in li:
            dict_out = {}

            title_chapter = element.find("a", class_="btn-collapse").get_text()
            data_chapter = element.find_all("li", class_="list-group-item")

            list_url_fansub = []
            list_name_fansub = []
            list_date_upload = []
            list_url_chapter = []

            for fansub_chapter in data_chapter:
                info_chapter = fansub_chapter.div.find_all("div")
                list_url_fansub.append(info_chapter[0].span.a.get('href'))
                list_name_fansub.append(info_chapter[0].span.a.get_text())
                list_date_upload.append(info_chapter[1].span.get_text())
                list_url_chapter.append(info_chapter[-1].a.get('href'))

            dict_out["title_chapter"] = title_chapter
            dict_out["url_fansub"] = ", ".join(list_url_fansub)
            dict_out["name_fansub"] = ", ".join(list_name_fansub)
            dict_out["date_upload"] = ", ".join(list_date_upload)
            dict_out["url_chapter"] = ", ".join(list_url_chapter)
            
            list_out.append(dict_out)


    except Exception as err:
        raise Exception(f"{__name__}-get_chapters: {err}")
    else:
        return list_out