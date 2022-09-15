import chromedriver_autoinstaller as browser_installer
from selenium.webdriver import Chrome as Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class Scraper(Driver):
    """
    This class represents a scraping tool based on a selenium Scraper
    """
    def __init__(self, *args, **kwargs) -> None:
        # Makes sure current version of the browser exists and in path (to be used as driver)
        browser_installer.install()

        # Default option for scraping is headless
        if 'options' not in kwargs or kwargs['options'] == 'add':
            kwargs['options'] = Options()
            kwargs['options'] = self.get_options()

        super().__init__(*args, **kwargs)
    
    @staticmethod
    def get_options():
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument("--log-level=3")
        options.add_argument("--disable-notifications")
        options.add_argument("--window-size=2160,3840")
        options.add_argument('--ignore-ssl-errors')
        # options.add_argument('--no-sandbox')
        return options
