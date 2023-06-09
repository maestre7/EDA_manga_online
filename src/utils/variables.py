
#//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]
xpath = {
    "not_found": '//h1[text()="404 Not Found"]',
    "pop_up": '//button/span[text()="ACEPTO"]',
    "upkeep": '//h1[text()="En Mantenimiento"]',
    "recover_links": '//div[starts-with(@class,"element")]/a',
    "next_page": '//a[contains(text(),"Siguiente")]', # '//ul[starts-with(@class,"pagination")]/li[2]/a',
    "book_chapter": '//a[contains(@style,"display: block;")]',
    "book_cover": '//img[contains(@class,"book-thumbnail")]',
    "book_genre": '//h6[contains(@style,"display: inline-block;")]',
    "book_name00": '//h1[contains(@class,"element-title my-2")]',
    "book_name01": '//h2[contains(@class,"element-subtitle")]',
    "book_synonyms": '//span[@class="badge badge-pill badge-transparent p-2 text-truncate"]',
    "book_synopsis": '//p[@class="element-description"]',
    "book_demography": '//div[starts-with(@class,"demography")]',
    "book_type": '//h1[starts-with(@class,"book-type")]',
    "book_score": '//div[@class="score"]/a/span',
    "book_status" : '//span[starts-with(@class,"book-status")]',
    "book_social" : '//span[@class="element-header-bar-element-number"]',
    "chapters_all": '//button[@id="show-chapters"]',
    "chapters_titles": '//li[@class="list-group-item p-0 bg-light upload-link"]/h4/div/div[1]/a',
    "chapters_urls": '//ul[@class="list-group list-group-flush chapter-list"]/li[1]/div/div[6]/a',
    "reverse_order": '//a[@class="float-right btn btn-primary"]',
    "select_chapter_free": '//ul[@class="list-group list-group-flush"]/div/li[]/div/div/ul/li/div/div[6]/a',
    "select_chapter_free_10": '//ul[@class="list-group list-group-flush"]/li[]/div/div/ul/li/div/div[6]/a',
    "select_chapter_list": '//ul[@class="list-group list-group-flush"]/div/li[]/h4/div/div[1]/a',
    "select_chapter_list_10": '//ul[@class="list-group list-group-flush"]/li[]/h4/div/div[1]/a',
    "select_chapter_one": '//ul[@class="list-group list-group-flush chapter-list"]/li/div/div[4]/a',
}

urls = {
    "manga-seinen": "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=manga&demography=seinen&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic=",
    "manga-shoujo": "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=manga&demography=shoujo&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic=",
    "manga-shounen": "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=manga&demography=shounen&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic=",
    "manga-josei": "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=manga&demography=josei&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic=",
    "manga-kodomo": "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=manga&demography=kodomo&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic=",
    "manhua-seinen": "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=manhua&demography=seinen&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic=",
    "manhua-shoujo": "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=manhua&demography=shoujo&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic=",
    "manhua-shounen": "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=manhua&demography=shounen&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic=",
    "manhua-josei": "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=manhua&demography=josei&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic=",
    "manhua-kodomo": "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=manhua&demography=kodomo&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic=",
    "manhwa-seinen": "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=manhwa&demography=seinen&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic=",
    "manhwa-shoujo": "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=manhwa&demography=shoujo&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic=",
    "manhwa-shounen": "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=manhwa&demography=shounen&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic=",
    "manhwa-josei": "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=manhwa&demography=josei&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic=",
    "manhwa-kodomo": "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=manhwa&demography=kodomo&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic=",
}
