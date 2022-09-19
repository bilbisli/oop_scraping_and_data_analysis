from web_scraping.sites import BBC, IAA
from web_scraping.utils.tools import search_json, search_csv

articles_path = 'my_articles.csv'
BBC.scraper(save_path=articles_path, summarization=True, sentiment_analysis=True)
flights_path = 'my_flights.json'
IAA.scraper(save_path=flights_path, exec_num=3, scrape_time=5)

search_results = search_csv(file_path=articles_path,
                            keywords=['queen', 'brother', 'gang'])
print('The articles search results are:')
for result in search_results:
    print(result)

search_results = search_json(file_path=flights_path,
                             keywords=['5W 7085', 'דאבי'])
print('The flight search results are:')
for result in search_results:
    print(result)
