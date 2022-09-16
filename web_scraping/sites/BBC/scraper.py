from data_analysis.sentiment_analysis import analyse_sentiment
from web_scraping.utils import Scraper
from web_scraping.sites.BBC.locators import NewsPageLocators
from web_scraping.sites.BBC.pages import MainPage, ArticlePage
from data_analysis.article_summarization import summarize


def scrape_bbc_main_page_articles(save_path='bbc_articles.csv', summarization=True, sentiment_analysis=True, verbose=True):

    with MainPage() as main_page:
        if verbose:
            print('Getting article links from main page...')
        links = main_page.get_article_links()

    with ArticlePage() as article_page:
        if verbose:
            print('Getting articles...')
        articles = article_page.get_articles_from_links(links, verbose=verbose)
        if articles:
            if summarization:
                if verbose:
                    ('Summarizing articles...')
                for article in articles:
                    article.summary = summarize(article.content)['summary_text']
            if sentiment_analysis:
                if verbose:
                    ('Analysing sentiments...')
                for article in articles:
                    article.sentiment = analyse_sentiment(article.content)['label']
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
