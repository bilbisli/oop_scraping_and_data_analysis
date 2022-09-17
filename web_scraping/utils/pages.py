from web_scraping.utils import Scraper


class BasePage(object):
    """
    Base class to initialize the base page that will be called from all web pages
    """
    def __init__(self, driver=None, options='add'):
        """
        Args:
            driver: driver: driver of the web page
            options (str): whether to add default options to driver or not
        """
        if driver is None:
            driver = Scraper(options=options)
        self.driver = driver

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if traceback:
            print(traceback)
        self.driver.quit()
