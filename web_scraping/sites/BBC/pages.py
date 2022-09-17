from tqdm import tqdm

from web_scraping.sites.BBC.handlers import NewsPageHandler, SportsPageHandler
from web_scraping.sites.BBC.locators import HomePageLocators
from web_scraping.utils import BasePage
from web_scraping.utils.data_models import Article


class MainPage(BasePage):
    """This class represents the BBC main page"""
    def __init__(self, driver=None, article_locator=HomePageLocators.ARTICLE_LINKS):
        """
        Args:
            driver: driver of the web page
            article_locator: main page articles feature locator - link by default
        """
        super().__init__(driver)
        self.article_locator = article_locator
        self.article_links = []
        self.base_url = 'https://www.bbc.com/'
        self.driver.get(self.base_url)

    def get_article_links(self, locator=None):
        """
        This method gets the articles links from the main page
        Args:
            locator: the article link locator
        Returns:
            list[str]: list of article links in the page
        """
        if locator is None:
            locator = self.article_locator
        self.article_links = locator.get_end_value(self.driver)
        return self.article_links

    def validate_links(self, links=None):
        """
        This method is a helper to validate links which may cause errors
        Args:
            links (list[str]): the links to validate

        Returns:
            list[str]: list of validated links
        """
        if links is None:
            links = self.article_links

        def add_base_url(link):
            # check https use
            link = link.replace('http:', 'https:')
            # add base page url if missing
            if not link.startswith(self.base_url):
                if link[0] == '/':
                    link = link[1:]
                link = self.base_url + link
            return link

        links = list(map(add_base_url, links))
        self.article_links = links
        return links


class ArticlePage(BasePage):
    """
    This class represents an article page
    Note:
        Since there are many types (and formats) of article pages which all have the same common elements which are the
        properties of an article such as title, author, source, publish time and content a Chain of Responsibility
        design pattern may apply to handle the search of appropriate set of locators for a given page
    """
    def __init__(self, driver=None, article_links=None):
        """
        Args:
            driver: driver of the web page
            article_links (list[str]): the links to the pages of the articles to be retrieved
        """
        super().__init__(driver)
        self.article_links = article_links
        self.articles = []
        # the chain of responsibility construction
        self.handler = NewsPageHandler(SportsPageHandler(None))

    def get_articles_from_links(self, article_links=None, verbose=True):
        """
        This method fetches articles from known pages (which have a handler in the chain of responsibility)
        Args:
            article_links (list[str]): the links to the pages of the articles to be retrieved
            verbose (bool): toggles verbosity of the method whether to display progress bar or not

        Returns:
            list[Article]: the list of article objects
        """
        if article_links is None:
            article_links = self.article_links
        articles_bar = tqdm(article_links, leave=False, disable=not verbose)
        for link in articles_bar:
            locator_cls = self.handler.handle(link)
            if locator_cls is not None:
                self.driver.get(link)
                try:
                    title = locator_cls.ARTICLE_TITLE.get_end_value(self.driver, single=True)
                except Exception as e:
                    continue
                try:
                    content = locator_cls.ARTICLE_CONTENT.get_end_value(self.driver)
                except Exception as e:
                    continue
                try:
                    date_time = locator_cls.ARTICLE_DATE_TIME.get_end_value(self.driver, single=True)
                except Exception as e:
                    date_time = None
                try:
                    author = locator_cls.ARTICLE_AUTHOR.get_end_value(self.driver, single=True, wait_time=0.5)
                except Exception as e:
                    author = ''
                try:
                    source = locator_cls.ARTICLE_SOURCE.get_end_value(self.driver, single=True, wait_time=0.5)
                except Exception as e:
                    source = ''
                article = Article(title, link, content, date_time, author, source)
                self.articles.append(article)
        return self.articles
