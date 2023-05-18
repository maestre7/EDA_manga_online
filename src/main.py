
from utils.library import Library

url = "https://lectortmo.com/library?order_item=likes_count&order_dir=desc&title=&_pg=1&filter_by=title&type=oel&demography=&status=&translation_status=&webcomic=&yonkoma=&amateur=&erotic="
#url = "https://lectortmo.com/library"
#url = "https://www.google.com/"
#url = "https://bot.sannysoft.com/"
type = "OEL"

def main():
    app = Library(url, type)
    app.main_process()
    return 0

if __name__ == '__main__':
    main()