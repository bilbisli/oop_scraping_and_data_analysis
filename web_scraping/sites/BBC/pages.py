from tqdm import tqdm

from web_scraping.sites.BBC.handlers import NewsPageHandler, SportsPageHandler
from web_scraping.sites.BBC.locators import HomePageLocators
from web_scraping.utils import BasePage
from web_scraping.utils.data_models import Article


class MainPage(BasePage):
    def __init__(self, driver=None, article_locator=HomePageLocators.ARTICLE_LINKS):
        super().__init__(driver)

        self.article_locator = article_locator
        self.article_links = []
        self.base_url = 'https://www.bbc.com/'
        self.driver.get(self.base_url)

    def get_article_links(self, locator=None):
        """This method gets the articles links from the main page"""
        if locator is None:
            locator = self.article_locator

        self.article_links = locator.get_end_value(self.driver)
        return self.article_links

    def validate_links(self, links=None):
        if links is None:
            links = self.article_links

        def add_base_url(link):
            link = link.replace('http:', 'https:')
            if not link.startswith(self.base_url):
                if link[0] == '/':
                    link = link[1:]
                link = self.base_url + link
            return link

        links = list(map(add_base_url, links))
        self.article_links = links

        return links


class ArticlePage(BasePage):
    def __init__(self, driver=None):
        super().__init__(driver)

        self.articles = []
        self.handler = NewsPageHandler(SportsPageHandler(None))

    def get_articles_from_links(self, article_links=None, verbose=True):
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
