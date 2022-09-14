from web_scraping.utils import Scraper


class BasePage(object):
    """Base class to initialize the base page that will be called from all
    pages"""

    def __init__(self, driver=None):
        if driver is None:
            driver = Scraper()
        self.driver = driver

    def __enter__(self):
        return self
  
    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.close()
