from web_scraping.sites.BBC.locators import HomePageLocators
from web_scraping.utils import BasePageElement


class ArticleLinkElements(BasePageElement):
    locator = HomePageLocators.ARTICLE_LINKS
