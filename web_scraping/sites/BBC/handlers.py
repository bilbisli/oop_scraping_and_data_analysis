from web_scraping.utils import BasePageHandler
from web_scraping.sites.BBC.locators import NewsPageLocators, SportPageLocators


class NewsPageHandler(BasePageHandler):
    """Concrete Handler for normal news page articles"""
    def __init__(self, nxt):
        locators = NewsPageLocators
        super().__init__(nxt, locators)

 
    def processRequest(self, request):
        '''return True if request is handled '''
 
        if '/news/' in request and '/live/' not in request:
            return True


class SportsPageHandler(BasePageHandler):
    """Concrete Handler for normal news page articles"""
    def __init__(self, nxt):
        locators = SportPageLocators
        super().__init__(nxt, locators)

 
    def processRequest(self, request):
        '''return True if request is handled '''
 
        if '/sport/' in request and '/live/' not in request:
            return True
