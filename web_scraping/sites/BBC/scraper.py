from web_scraping.utils import Scraper
from web_scraping.sites.BBC.locators import NewsPageLocators
from web_scraping.sites.BBC.pages import MainPage, ArticlePage


def scrape_bbc_main_page_articles(save_path=None):
    
    with MainPage() as main_page:
        print('Getting article links from main page...')
        links = main_page.get_article_links()

    with ArticlePage() as article_page:
        print('Getting articles...')
        articles = article_page.get_articles_from_links(links)
        if articles:
            print('Saving articles...')
            articles[0].save_articles(articles)
            print('Articles saved!')
        else:
            print('No articles found.')

    
if __name__ == '__main__':
    scrape_bbc_main_page_articles()
