import data_analysis.sentiment_analysis as sentiment_analyser
from web_scraping.utils import Scraper
from web_scraping.sites.BBC.locators import NewsPageLocators
from web_scraping.sites.BBC.pages import MainPage, ArticlePage
import data_analysis.article_summarization as summarizer
from tqdm import tqdm


def scrape_bbc_main_page_articles(save_path='bbc_articles.csv', summarization=False, sentiment_analysis=True, verbose=True):

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
                    ('Note: This may take a while')
                sum_model = summarizer.get_model()
                for article in tqdm(articles, leave=False, disable=not verbose):
                    article.summary = summarizer.summarize(article.content, model=sum_model)['summary_text']
            if sentiment_analysis:
                if verbose:
                    ('Analysing sentiments...')
                    ('Note: This may take a while')
                sent_model = sentiment_analyser.get_model()
                for article in tqdm(articles, leave=False, disable=not verbose):
                    article.sentiment = sentiment_analyser.analyse_sentiment(article.content, model=sent_model)['label']
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
