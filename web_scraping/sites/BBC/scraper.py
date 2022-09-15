from web_scraping.utils import Scraper
from web_scraping.sites.BBC.locators import NewsPageLocators
from web_scraping.sites.BBC.pages import MainPage, ArticlePage


def scrape_bbc_main_page_articles(save_path='bbc_articles.csv', verbose=True):

    with MainPage() as main_page:
        if verbose:
            print('Getting article links from main page...')
        links = main_page.get_article_links()

    with ArticlePage() as article_page:
        if verbose:
            print('Getting articles...')
        articles = article_page.get_articles_from_links(links, verbose=verbose)
        if articles:
            if verbose:
                print('Saving articles...')
            articles[0].save_articles(articles, save_path=save_path)
            if verbose:
                print('Articles saved!')
        else:
            if verbose:
                print('No articles found.')

    
if __name__ == '__main__':
    scrape_bbc_main_page_articles()
