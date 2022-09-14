from web_scraping.utils import BasePageElement
from web_scraping.sites.BBC.locators import HomePageLocators


class ArticleLinkElements(BasePageElement):
    locator = HomePageLocators.ARTICLE_LINKS
