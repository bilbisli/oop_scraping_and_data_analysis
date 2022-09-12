import chromedriver_autoinstaller as browser_installer
from selenium.webdriver import Chrome as Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class Scraper(Driver):
    """
    This class represents a news scraping tool based on a selenium Scraper
    """
    def __init__(self, *args, **kwargs) -> None:
        # Makes sure current version of the browser exists and in path (to be used as driver)
        browser_installer.install()



        # Default option for scraping is headless
        if 'options' not in kwargs:
            kwargs['options'] = Options()
            kwargs['options'].add_argument("--headless")

        super().__init__(*args, **kwargs)



        



