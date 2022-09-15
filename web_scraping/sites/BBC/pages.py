
from multiprocessing.connection import wait
from web_scraping.sites.BBC.elements import ArticleLinkElements
from web_scraping.sites.BBC.locators import HomePageLocators, NewsPageLocators
from web_scraping.sites.BBC.handlers import NewsPageHandler, SportsPageHandler
from web_scraping.utils import BasePage
from web_scraping.utils.data_models import Article
from selenium.common.exceptions import TimeoutException
from tqdm import tqdm


class MainPage(BasePage):
    def __init__(self, driver=None, article_locator=HomePageLocators.ARTICLE_LINKS):
        super().__init__(driver)

        self.article_locator = article_locator
        self.article_links = []
        # self.article_titles = []
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
                # print(link)
                try:
                    title = locator_cls.ARTICLE_TITLE.get_end_value(self.driver, single=True)
                except Exception as e:
                    # print('1')
                    continue
                # print('getting content')
                try:
                    content = locator_cls.ARTICLE_CONTENT.get_end_value(self.driver)
                except Exception as e:
                    # print('2')
                    continue
                # print('getting date_time')
                try:
                    date_time = locator_cls.ARTICLE_DATE_TIME.get_end_value(self.driver, single=True)
                except Exception as e:
                    # print('3')
                    date_time = None
                # print('getting author')
                try:
                    author = locator_cls.ARTICLE_AUTHOR.get_end_value(self.driver, single=True, wait_time=0.5)
                except Exception as e:
                    # print('4')
                    author = ''
                # print('getting source')
                try:
                    source = locator_cls.ARTICLE_SOURCE.get_end_value(self.driver, single=True, wait_time=0.5)
                except Exception as e:
                    # print('5')
                    source = ''
                article = Article(title, link, content, date_time, author, source)
                self.articles.append(article)
        
        return self.articles


                    


            # # try:
            #     if '/news/' in link and '/live/' not in link:
            #         print(link)
            #         self.driver.get(link)
                    
            #         # TODO: Continue from here - time out exceptions, title from page and article element build
            #         try:
            #             self.contents.append(self.get_article_content())
            #         except TimeoutException:
            #             self.contents.pop()
            #             continue
            #         self.date_times.append(self.get_article_date_time())
            #         author, source = self.get_article_author_source()
            #         self.authors.append(author)
            #         self.sources.append(source)
            # # except Exception as e:
            # #     # print(e)
            # #     print('link failed:', link)

    # def get_article_content(self, locator=NewsPageLocators.ARTICLE_CONTENT):
    #     content_elements = self.get_elements(locator)
    #     content = ''
    #     content_bar = tqdm(content_elements, leave=False)
    #     for content_block in content_bar:
    #         content += content_block.text

    #     return content

    # def get_article_date_time(self, locator=NewsPageLocators.ARTICLE_DATE_TIME):
    #     article_date_time = self.get_element(locator).get_attribute('datetime')
        
    #     return article_date_time

    # def get_article_author_source(self, locator=NewsPageLocators.ARTICLE_AUTHOR_SOURCE):
    #     author_source = self.get_element(locator).text.split('\n')
    #     remove_by = re.compile(re.escape('by '), re.IGNORECASE)
    #     author = re.compile(re.escape('by '), re.IGNORECASE).sub('', author_source[0])
    #     source = author_source[-1]
        
    #     return author, source

# h = MainPage()
# res = h.get_article_links_and_titles()

# print(res[0])
# print(res[1])
# print(len(res[0]))
# print(len(res[1]))
# a = ArticlePage()
# a.get_articles_from_links(h.article_links)
# print(len(a.authors), len(a.contents), len(a.date_times), len(a.sources), len(h.article_links), len(h.article_titles))
# for i in range(len(h.article_links)):
#     print(h.article_titles[i], '---', a.authors[i])
# # print(a.validate_links())

