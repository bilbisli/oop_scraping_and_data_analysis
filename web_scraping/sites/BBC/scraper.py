from tqdm import tqdm

from web_scraping.sites.BBC.pages import MainPage, ArticlePage
from web_scraping.utils.data_analysis import ArticleSummarization
from web_scraping.utils.data_analysis import SentimentAnalysis
from web_scraping.utils.tools import get_time


def scrape_bbc_main_page_articles(save_path='bbc_articles.csv',
                                  summarization=False,
                                  sentiment_analysis=False,
                                  verbose=True,
                                  sum_model=None,
                                  sent_model=None):
    """
    This function fetches articles that are featured in the BBC main page
    Args:
        save_path (str): the path in which to save the unified article data (including file_name.csv)
        summarization: whether to add summarization to the articles or not
        sentiment_analysis: whether to add sentiment analysis to the articles or not
        verbose: toggles verbosity of the system
        sum_model: model for summarization - will load anew if not given
        sent_model: model for sentiment analysis - will load anew if not given
    """
    with MainPage() as main_page:
        if verbose:
            print(f'{get_time()}: Getting article links from main page...')
        links = main_page.get_article_links()
    with ArticlePage() as article_page:
        if verbose:
            print(f'{get_time()}: Getting articles...')
        articles = article_page.get_articles_from_links(links, verbose=verbose)
        if articles:
            if summarization:
                if verbose:
                    print(f'{get_time()}: Summarizing articles...')
                    print('Note: This may take a while')
                if not sum_model:
                    sum_model = ArticleSummarization.get_model()
                for article in tqdm(articles, leave=False, disable=not verbose):
                    article.summary = ArticleSummarization.summarize(article.content, model=sum_model)['summary_text']
            if sentiment_analysis:
                if verbose:
                    print(f'{get_time()}: Analysing sentiments...')
                    print('Note: This may take a while')
                if not sent_model:
                    sent_model = SentimentAnalysis.get_model()
                for article in tqdm(articles, leave=False, disable=not verbose):
                    article.sentiment = SentimentAnalysis.analyse_sentiment(article.content, model=sent_model)['label']
            if verbose:
                print(f'{get_time()}: Saving articles...')
            articles[0].save_articles(articles, save_path=save_path)
            if verbose:
                print(f'{get_time()}: Articles saved!')
        else:
            if verbose:
                print(f'{get_time()}: No articles found.')


if __name__ == '__main__':
    scrape_bbc_main_page_articles()
