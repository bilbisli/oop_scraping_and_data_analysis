import os

from web_scraping.sites import BBC, IAA
from web_scraping.utils.data_analysis import ArticleSummarization, SentimentAnalysis
from web_scraping.utils.tools import search_json, search_csv


def example():
    """
    Just an example of how the system can be used
    """
    print('Loading system...')
    sum_model = ArticleSummarization.get_model()
    print('Model 1/2 loaded')
    sent_model = SentimentAnalysis.get_model()
    print('Model 2/2 loaded')
    while True:
        user_choice = prompt_input(menu_str(), lambda x: x.isdigit() and int(x) in range(1, 8), int)
        if user_choice == 1:
            path = input('Choose a path to save the csv file (including file_name.csv):\n')
            add_sentiment = prompt_input("Add sentiment analysis?\n(0) no\n(1) yes",
                                         lambda x: x.isdigit() and int(x) in range(2),
                                         int)
            add_summary = prompt_input("Add summary?\n(0) no\n(1) yes",
                                       lambda x: x.isdigit() and int(x) in range(2),
                                       int)
            BBC.scraper(save_path=path,
                        summarization=add_summary,
                        sentiment_analysis=add_sentiment,
                        sum_model=sum_model,
                        sent_model=sent_model)
        elif user_choice == 2:
            path = input('Choose a path to save the json file (including file_name.json):\n')
            time_limit = prompt_input("Enter time limit (0 for no limit): ",
                                      lambda x: x.isdigit(),
                                      float)
            execution_limit = prompt_input("Enter number of updates limit (0 for no limit): ",
                                           lambda x: x.isdigit(),
                                           int)
            print('Note: three browsers will be opened during this operation')
            IAA.scraper(save_path=path, exec_num=execution_limit, scrape_time=time_limit)
        elif user_choice == 3:
            path = prompt_input('Choose a path of json to search (including file_name.json)', os.path.exists)
            phrases = input(
                'Enter phrases to search seperated by space padded commas (phrase1 , phrase2):\n').split(' , ')
            search_results = search_json(file_path=path, keywords=phrases)
            print('The search results are:')
            for result in search_results:
                print(result)
        elif user_choice == 4:
            path = prompt_input('Choose a path of csv to search (including file_name.csv)', os.path.exists)
            phrases = input(
                'Enter phrases to search seperated by space padded commas (phrase1 , phrase2):\n').split(' , ')
            print('The search results are:')
            search_results = search_csv(file_path=path, keywords=phrases)
            for result in search_results:
                print(result)
        elif user_choice == 5 or user_choice == 6:
            print("Enter text and press 'enter' twice when finished:")
            article_content = ''
            while True:
                input_str = input()
                if not input_str:
                    break
                article_content += input_str + '\n'
            print('Processing...')
            if user_choice == 5:
                sentiment = SentimentAnalysis.analyse_sentiment(article_content, model=sent_model)['label']
                print('The text sentiment is:')
                print(sentiment)
            else:
                summary = ArticleSummarization.summarize(article_content, model=sum_model)['summary_text']
                print('The text summary is:')
                print(summary)
        elif user_choice == 7:
            break
        else:
            print('Something went wrong')
            break
    print("Goodbye.")


def menu_str():
    menu = """Choose an option:
    (1) Scrape BBC main page for articles
    (2) Scrape IAA flight board for flight updates
    (3) Search json (flights)
    (4) Search csv (articles)
    (5) Analyse sentiment of text
    (6) Summarize text
    (7) Exit
    """
    return menu


def prompt_input(message, cond=None, convert=None, error_msg='Invalid choice'):
    while True:
        print(message)
        user_choice = input("Enter your choice: ")
        if not cond or cond(user_choice):
            break
        print(error_msg)
    if convert:
        user_choice = convert(user_choice)
    return user_choice


if __name__ == '__main__':
    example()
