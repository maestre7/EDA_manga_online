
# Native


# Own
from utils.chapter import main_process
from utils.execute_concurrency import execute_concurrency


process = ["manga_shoujo", "manga_josei", "manhwa_josei", "manhwa_seinen", "manhwa_shounen"]

def main():

    try:
        list_execute_concurrency = []
        for type_demo in process:
            list_execute_concurrency.append((main_process,(type_demo,)))
            
        result = execute_concurrency(list_execute_concurrency, 'processes', 2)
    except Exception as err:
        print(f"{__name__}: {err}")
    else:
        print(result)


if __name__ == '__main__':
    main()