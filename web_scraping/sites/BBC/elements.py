from web_scraping.sites.BBC.locators import HomePageLocators
from web_scraping.utils import BasePageElement


class ArticleLinkElements(BasePageElement):
    """This represents an article link element"""
    locator = HomePageLocators.ARTICLE_LINKS
