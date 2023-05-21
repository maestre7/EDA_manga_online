
# Native
import logging
import os
from time import sleep
from pathlib import Path
from typing import Union, Optional, List, Any

# Third Parties
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
#from undetected_chromedriver import ChromeOptions, Chrome
import undetected_chromedriver as uc



logger = logging.getLogger(__name__)

options = {
    'ignore-certificate-errors': True,
    'ignore-ssl-errors': True,
    'disable-notifications': True,
    'no-sandbox': True,
    'verbose': True,
    'disable-gpu': True,
    'disable-extensions': True,
    'disable-software-rasterizer': True,
    'start-maximized': True,
    'disable-dev-shm-usage': True,
    'disable-infobars': True
}


def conn_link(headless: bool = True, **kwargs) -> webdriver.Chrome:
    '''Establishes a connection with Selenium using the specified webdriver.

    Args:
        headless (bool): Whether to run in headless mode (without browser window). Defaults to True.
        **kwargs: Additional keyword arguments to customize the Chrome options.

    Returns:
        webdriver.Chrome: The Selenium WebDriver instance for Chrome.

    Raises:
        SessionNotCreatedException: If a new session cannot be created.
        OSError: If an operating system-related error occurs.
        WebDriverException: If a WebDriver-related error occurs. 
    '''

    options = Options()
    if headless:
        options.add_argument('--headless')  # Run in headless mode (without browser window)

    # Custom options
    for key, value in kwargs.items():
        options.add_argument(f'--{key}={value}')

    try:
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    except SessionNotCreatedException as err:
        logger.exception('SessionNotCreatedException in conn_link')
        raise err

    except OSError as err:
        logger.exception('OSError in conn_link')
        raise err

    except WebDriverException as err:
        logger.exception('WebDriverException in conn_link')
        raise err
    


def conn_uc(headless: bool = True, folder: str = None) -> webdriver:
    '''Establishes a Selenium connection using undetected_chromedriver module.

    Args:
        headless (bool): Whether to run in headless mode (without browser window). Defaults to True.
        folder (str): Folder path where the UC profile data will be stored. If None, it uses the default folder './uc'. 
                              If a custom folder path is provided, it will be used. Defaults to None.

    Returns:
        undetected_chromedriver.Chrome: The Selenium WebDriver instance for UC (undetected_chromedriver).

    Raises:
        SessionNotCreatedException: If a new session cannot be created.
        OSError: If an operating system-related error occurs.
        WebDriverException: If a WebDriver-related error occurs.
    '''

    driver = None

    try:
        options = webdriver.ChromeOptions()

        # Folder installation for UC
        temp_folder = os.path.abspath('./uc') if not folder else folder
        path_folder = Path(temp_folder)
        if not path_folder.exists():
            path_folder.mkdir()

        uc.Chrome(user_data_dir= str(temp_folder)) # Set profile folder

        if headless:
            options.headless = True  # Run in headless mode (without browser window)

        driver = uc.Chrome(options=options)

    except (SessionNotCreatedException, OSError, WebDriverException) as err:
        logger.exception('Exception occurred in conn_uc')
        raise err

    return driver


def get_by_selector(selector_type: str) -> By:
    """
    Returns the appropriate By object based on the selector type.
    
    Parameters:
    - selector_type: The type of selector to use ('id', 'class', 'xpath', etc.).
    
    Returns:
    - The By object corresponding to the selector type.
    """

    if selector_type == 'id':
        return By.ID
    
    if selector_type == 'name':
        return By.NAME
    
    if selector_type == 'class':
        return By.CLASS_NAME
    
    if selector_type == 'tag':
        return By.TAG_NAME
    
    if selector_type == 'link_text':
        return By.LINK_TEXT
    
    if selector_type == 'partial_link_text':
        return By.PARTIAL_LINK_TEXT
    
    if selector_type == 'xpath':
        return By.XPATH
    
    if selector_type == 'css_selector':
        return By.CSS_SELECTOR
    
    raise ValueError('Invalid selector type')


def click(driver: webdriver.Chrome,
          selector_type: str,
          path: str,
          wait_time: float = 30,
          control: Optional[int] = None,
          log: bool = True) -> bool:
    '''
    Click on a selenium element based on selector type and path.
    
    Parameters:
    - driver: Selenium driver to run the automation.
    - selector_type: Type of selector to use ('id', 'class', 'xpath', etc.).
    - path: Value of the selector to use.
    - wait_time: Waiting time before giving an error.
    - control: Position of the element in a list (optional).
    - log: Whether to log exceptions or not.
    
    Returns:
    - True if the click was successful, False otherwise.
    '''
    success = False

    try:
        by_object = get_by_selector(selector_type)

        

        #if isinstance(wait_time, int) or isinstance(wait_time, float):
        wait = WebDriverWait(driver, wait_time)
        wait.until(EC.element_to_be_clickable((by_object, path)))

        element = driver.find_element(by_object, path)
        
        if control is not None:
            elements = driver.find_elements(by_object, path)
            if control >= len(elements):
                raise IndexError("Control value exceeds the number of elements")
            element = elements[control]

        element.click()
        success = True

    except (TimeoutException, ElementClickInterceptedException, NoSuchElementException, AttributeError, IndexError, TypeError) as err:
        if log:
            logger.exception(f'{__name__}: {err}, {selector_type}: {path}')
            raise Exception(f"{__name__}: {err}, {selector_type}: {path}")
        else:
            logger.info(f'{__name__}: {err}, {selector_type}: {path}')

    else:
        logger.info(f'{__name__}: {selector_type}: {path}, {isinstance(wait_time, int)} or {isinstance(wait_time, float)}')

    return success


def submit(driver: webdriver.Chrome, 
           selector_type: str, 
           path: str, 
           wait_time: int = 30
           ) -> bool:
    '''Submits a form element identified by the given selector and path in Selenium.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
        selector_type (str): The type of selector to use (e.g., "xpath", "css_selector", "id", etc.).
        path (str): The path or value of the selector.
        wait_time (int): The maximum time to wait for the element to be clickable (in seconds). Defaults to 30.

    Returns:
        bool: True if the submission is successful, False otherwise.

    Raises:
        TimeoutException: If the element is not clickable within the specified wait time.
        ElementClickInterceptedException: If another element is blocking the click action.
        AttributeError: If the selector type is invalid or not supported.
    '''

    success = None

    try:
        wait = WebDriverWait(driver, wait_time)

        # Select the appropriate selector based on the selector type
        by_object = get_by_selector(selector_type)
        element = wait.until(EC.element_to_be_clickable((by_object, path)))

        element.submit()
        success = True

    except (TimeoutException, ElementClickInterceptedException, AttributeError, TypeError) as err:
        logger.exception(f'{__name__}: {err}, {selector_type}: {path}')
        raise Exception(f'{__name__}: {err}, {selector_type}: {path}')

    else:
        logger.info(f'{__name__}: {selector_type}: {path}')

    return success


def keys(driver: webdriver.Chrome, 
         selector_type: str, 
         path: str, keys: str, 
         enter: bool = False, 
         wait_time: int = 30
         ) -> bool:
    '''Sends keys to an element identified by the given selector and path in Selenium.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
        selector_type (str): The type of selector to use (e.g., "xpath", "css_selector", "id", etc.).
        path (str): The path or value of the selector.
        keys (str): The keys to send to the element.
        enter (bool): Whether to simulate pressing the Enter key after sending the keys. Defaults to False.
        wait_time (int): The maximum time to wait for the element to be clickable (in seconds). Defaults to 30.

    Returns:
        bool: True if the keys are sent successfully, False otherwise.

    Raises:
        TimeoutException: If the element is not clickable within the specified wait time.
        ElementClickInterceptedException: If another element is blocking the action.
        AttributeError: If the selector type is invalid or not supported.
    '''

    success = None

    try:
        # Wait for the element to be clickable
        wait = WebDriverWait(driver, wait_time)
        # Select the appropriate selector based on the selector type
        by_object = get_by_selector(selector_type)
        wait.until(EC.element_to_be_clickable((by_object, path)))

        element = driver.find_element(by_object, path)

        if enter:
            element.send_keys(keys + Keys.ENTER)
        else:
            element.send_keys(keys)

        success = True

    except (TimeoutException, ElementClickInterceptedException, AttributeError, TypeError) as err:
        logger.exception(f"{__name__}: {err}, {selector_type}: {path}, {keys}, {enter}")
        raise Exception(f"{__name__}: {err}, {selector_type}: {path}, {keys}, {enter}")

    else:
        logger.info(f"{__name__}: {err}, {selector_type}: {path}, {keys}, {enter}")

    return success

def get_elements(driver: webdriver.Chrome, 
                 selector_type: str, 
                 path: str, 
                 wait_time: int = 30, 
                 control: int = None, 
                 log: bool = True
                 ) -> Union[List[Any], bool]:
    '''Retrieve the elements associated with the given XPath in Selenium.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
        selector_type (str): The type of selector to use (e.g., "xpath", "css_selector", "id", etc.).
        path (str): The selector path or value.
        wait_time (int): The maximum waiting time for the element to be clickable (in seconds). Default is 30.
        control (Union[int, None]): The control parameter specifies whether to retrieve all matching elements (None)
            or a specific element at the given index. Default is None.
        log (bool): Whether to log exceptions as errors or only as information. Default is True.

    Returns:
        Optional[WebElement]: The retrieved element if found, or None if not found or an exception occurred.

    Raises:
        TimeoutException: If the element is not clickable within the specified wait time.
        ElementClickInterceptedException: If another element is blocking the action.
        AttributeError: If the selector type is invalid or not supported.
    '''

    result = None

    try:
        # Select the appropriate selector based on the selector type
        by_object = get_by_selector(selector_type)
        # Wait for the element to be clickable
        wait = WebDriverWait(driver, wait_time)
        wait.until(EC.element_to_be_clickable((by_object, path)))

        elements = driver.find_elements(by_object, path)

        if control is not None:  # Differentiate between all matches or a specific one
            elements = elements[control]

        result = elements

    except (TimeoutException, ElementClickInterceptedException, AttributeError, TypeError) as err:
        if log:
            logger.exception(f"{__name__}: {err}, {selector_type}: {path}")
            raise Exception(f"{__name__}: {err}, {selector_type}: {path}")
        else:
            logger.info(f"{__name__}: {err}, {selector_type}: {path}")

    else:
        logger.info(f"{__name__}: {selector_type}: {path}")

    return result


def get_element(driver: webdriver.Chrome, 
                     selector_type: str, 
                     path: str, 
                     wait_time: int = 30,
                     log: bool = True
                     ) -> Optional[Any]:
    '''
    Retrieve the element associated with the given selector and path.
    
    Args:
        driver (webdriver.Chrome): The Selenium webdriver.Chrome instance.
        selector_type (str): The type of selector to use (e.g., 'id', 'class_name', 'xpath', etc.).
        selector_path (str): The path or value of the selector.
        wait_time (int, optional): The maximum time to wait for the element to be clickable in seconds. Default is 30.
        log (bool): Whether to log exceptions as errors or only as information. Default is True.
        
    Returns:
        Optional[WebElement]: The retrieved element if found, or None if not found or an exception occurred.
    '''

    element = None

    try:
        # Select the appropriate selector based on the selector type
        by_object = get_by_selector(selector_type)
        # Wait for the element to be clickable
        wait = WebDriverWait(driver, wait_time)
        wait.until(EC.element_to_be_clickable((by_object, path)))

        element = driver.find_element(by_object, path)

    except (TimeoutException, ElementClickInterceptedException, AttributeError, TypeError) as err:
        if log:
            logger.exception(f"{__name__}: {err}, {selector_type}: {path}")
            raise Exception(f"{__name__}: {err}, {selector_type}: {path}")
        else:
            logger.info(f"{__name__}: {err}, {selector_type}: {path}")
    else:
        logger.info(f"{__name__}: {selector_type}: {path}")
    
    return element


def center_scroll(wde, wait_time: float=0.5, log: bool = True):
    '''Centers the scroll on the webdriver_element.
    
    Args:
        wde (WebDriver Element): The WebDriver element to center the scroll on.
        wait_time (float, optional): The amount of time to wait after scrolling (in seconds). Default is 0.5.
        log (bool): Whether to log exceptions as errors or only as information. Default is True.

    Returns:
        bool: Returns True if the scroll was successfully centered, or False if an exception occurred.
    
    Raises:
        WebDriverException: If there is an exception related to the WebDriver.
        ElementClickInterceptedException: If another element is blocking the action.
    '''
    
    result = None
           
    try:
        wde.location_once_scrolled_into_view
        
        if wait_time is not None:
            sleep(wait_time)
            
        result = True
    
    except (WebDriverException, ElementClickInterceptedException) as err:
        if log:
            logger.exception(f"{__name__}-center_scroll: {err}")
            raise Exception(f"{__name__}-center_scroll: {err}")
        else:
            logger.info(f"{__name__}-center_scroll: {err}")
            result = False
    else:
        logger.info(f"{__name__}-center_scroll: Ok")

    return result
