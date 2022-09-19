# Modular OOP Web Scraping & Data Analysis
Scraping web sites and summarizing them with sentiment analysis + real-time flight scraping and json\csv search capabilities


## Features
- Retrieving articles that are currently on [BBC main page](https://www.bbc.com/)
- Summarizing articles to desired min/max length (up to 512) - may be applied upon article retrieval
- Text Sentiment Analysis - may be applied upon article retrieval
- Search phrases in a csv file and retrieve a desired value in the row where the phrase was found
- Retrieve live flight data from [IAA Flight Board Page](http://www.iaa.gov.il/he-IL/airports/BenGurion/Pages/OnlineFlights.aspx)
- Search phrases in a json file and retrieve the path leading to where the phrase was found
- Use as base module to construct your own OOP modular web scraper

## Installation
The project was develepoed in _python 3.10.6_ with _selenium_

Install the dependencies using the requirements.txt:
```sh
cd oop_scraping_and_data_analysis-main
pip install -r requirements.txt
```
* Finally, add the 'web_scraping' module to **`PATH`**



## Usage
```python
from web_scraping.sites import BBC, IAA
from web_scraping.utils.tools import search_json, search_csv

articles_path = '~/my/path/to/file/articles.csv'
flights_path = '~/my/path/to/file/flights.json'
BBC.scraper(save_path=articles_path, summarization=True, sentiment_analysis=True)
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
```
Output:
```
Getting article links from main page...
Getting articles...
Summarizing articles...
Note: This may take a while
Analysing sentiments...
Note: This may take a while
Saving articles...
Articles saved!
Preparing scraping...
2022/09/18 08:11:15: Starting scraping...
2022/09/18 08:11:15: Scraping round 1
2022/09/18 08:11:15: Fetching flights...
2022/09/18 08:11:54: Flights fetched
2022/09/18 08:11:54: saving...
2022/09/18 08:12:06: Saved!
2022/09/18 08:12:06: Waiting for flight table update...
2022/09/18 08:12:16: Scraping round 2
2022/09/18 08:12:16: Fetching flights...
2022/09/18 08:12:48: Flights fetched
2022/09/18 08:12:48: saving...
2022/09/18 08:12:48: Saved!
2022/09/18 08:12:48: Waiting for flight table update...
2022/09/18 08:13:45: Scraping round 3
2022/09/18 08:13:45: Fetching flights...
2022/09/18 08:14:07: Flights fetched
2022/09/18 08:14:07: saving...
2022/09/18 08:14:07: Saved!
2022/09/18 08:14:07: Finishing up
2022/09/18 08:14:18: Done.
The articles search results are:
https://www.bbc.com/news/entertainment-arts-62925113
https://www.bbc.com/news/uk-62943911
https://www.bbc.com/news/uk-62944148
https://www.bbc.com/news/uk-england-suffolk-62924487
https://www.bbc.com/sport/football/62859265
https://www.bbc.com/sport/football/62859267
The flight search results are:
flights > arrivals > 5W 7085 אבו דאבי 18/09 > city > אבו דאבי
flights > arrivals > 5W 7085 אבו דאבי 18/09 > flight > 5W 7085
flights > arrivals > EY 598 אבו דאבי 18/09 > city > אבו דאבי
flights > arrivals > LY 9600 אבו דאבי 18/09 > city > אבו דאבי
flights > departures > 5W 7086 אבו דאבי 18/09 > city > אבו דאבי
flights > departures > EY 599 אבו דאבי 18/09 > city > אבו דאבי
flights > departures > LY 9601 אבו דאבי 18/09 > city > אבו דאבי

Process finished with exit code 0
```



## Module Structure
The structure of the modules was constructed base on [Selenium docs on Page Objects ](https://selenium-python.readthedocs.io/page-objects.html#page-elements) and improved upon it
```
./oop_scraping_and_data_analysis
├── __init__.py
└── web_scraping                <----- main module
    ├── __init__.py
    ├── example.py              <----- example of using the different modules
    ├── sites                   <----- stores all the site specific modules
    │   ├── BBC                 <----- BBC website article scraping module
    │   │   ├── __init__.py      
    │   │   ├── elements.py     *
    │   │   ├── handlers.py     **
    │   │   ├── locators.py     ***
    │   │   ├── pages.py        ****
    │   │   └── scraper.py      *****
    │   ├── IAA                 <----- IAA website realtime flight scraping module
    │   │   ├── __init__.py
    │   │   ├── elements.py     *
    │   │   ├── locators.py     ***
    │   │   ├── pages.py        ****
    │   │   └── scraper.py      *****
    │   └── __init__.py
    └── utils                   <----- base module for site specific modules to build upon
        ├── __init__.py
        ├── data_analysis.py    <----- sentiment analysis & article summarizationare 
        ├── data_models.py      <----- data schemas (articles)
        ├── elements.py         *
        ├── handlers.py         **
        ├── locators.py         ***
        ├── pages.py            ****
        ├── scraper.py          *****
        └── tools.py            <-----  general tools - search functions are here
```
| Ref | Name | Details |
| ------| ------ | ------ |
|*| **`elements`** | Page element objects to systematically interact with the elements of the web page|
|**| **`handlers`** | Handelrs were my own addition which implement the Chain of Responsibility Dsign Pattern for handling many different article pages which are built diffrently than each other|
| *** | **`locators`** | Locators are used for locating elements in the page, i improved the design by adding a Locator class which not only stores what's necessary for locating elements in the page but also fetching the desired values from the elements (text for example) |
| **** | **`pages`** | Pages are abstractions of a web page which consist the operations that can be done on a web page for the desired task at hand  |
|  ***** | **`scraper`** | The base Scraper schema is built around a web driver to allow the opening and interactions with the browser and the other scraper files host the function that does the heavy lifting of the web scraping pipeline |

This kind of structure makes the system extremely modular



## Key Classes & Functions
##### Data Analysis
-  `web_scraping.utils.tools.search_json` - The **function** that searches flight data (json) file - uses the 'search_dict' function for the search operation, search example:
```
UA 9121
flights > departures > UA 9121 פרנקפורט 18/09 > flight > UA 9121
```
-  `web_scraping.utils.tools.search_csv` - The **function** that searches the article data (csv) file, search example: 
```
coffin , power plant
https://www.bbc.com/news/uk-62938463
https://www.bbc.com/news/uk-england-suffolk-62924487
https://www.bbc.com/news/world-europe-62943902
```


- `web_scraping.utils.data_analysis.SentimentAnalysis` -- The sentiment analysis ***class*** -  chosen RoBertA model trained for sentiment analysis on twitter
- `web_scraping.utils.data_analysis.ArticleSummarization` -- The article summarization ***class*** - chosen the _bart-large-cnn_ model for it's good performance and because it was trained on (CNN) news articles which is the data that we are dealing with
##### BBC Module
- `web_scraping.sites.BBC.scraper.scrape_bbc_main_page_articles` - The BBC website scraping **function**
- `web_scraping.sites.BBC.pages.ArticlePage` - The article page ***class*** which implements Chain of Responsibility in order to find the appropriate locator pack to handle different (News & Sports) pages formatting in the same pipeline thus making the system more adjustable
##### IAA Module
- `web_scraping.sites.IAA.scraper.scrape_iaa_flights` - The IAA website scraping **function**
- `web_scraping.sites.IAA.pages.FlightBoardPage` - The flight board page ***class*** which can act either as a listener, which waits until the flight table is updated or as a worker, fetching arrival/departure flight data once the listener is prompted by a flight data change
##### General
- `web_scraping.example` - A simple _**script**_ as an example of using the different modules as a way to show how the system works



## Challenges & Final Thoughts
1. At first I was trying to plan and think how to design and build the system to be modular, utilizing OOP concepts. after some thoughts & sketches, I thought where else is best to start if not at the documentation so I searched and found the ***Selenium docs on Page Objects*** which was exactly what I needed.
2. A challenge that I encountered was that in the main BBC web page there are many articles which lead to differently structured web pages which challenged me to think of a general solution that will work with minimal additions and modifications for each type of web page so the Chain of Responsibility Design Pattern immediately came to mind since that's exactly what a needed - so I constructed locator packs for different web pages (i've done two for POC) and handlers for the chain which were each responsible of identifying their own type of article web page and after that the pipeline stayed the same, using the retrieved locator pack extracted from the chain.
3. The realtime flight data retrieval was also a challnge. I thought of a design where there will be three drivers: (1) for fetching arrival flight data (2) for fetching departure flight data and (3) for listening for if the data is updating andonce it does triggering the other two to work. That system seemed to work well but there was a problem where getting the values (text) in the 'traditional' way via the web elements took a really long time (more time then it took for a flight data) so I realised it is not sustainable and thought of a solution - using multithreading. since there might be a lot of waiting time involved, threads should improve performance greatly. hence I've used thread poolsto act as a queue to for each retrieval of a flight table (arrival/departure) and threads for value retrieval from elements. In the end the threads improved the retrieval time but still it wasn't good enough. After a lot of trial and error and searching for a solution, A solution came up - using selenium execute_script command to retrieve the values, which proved to be a huge improvement and finally the performance was good enough to keep up with the table updates and the threads could be removed.
4. Another problem I seemed to have was while running the drivers in the IAA website in headless mode they tended to have more problems than non-headless mode. I also realized that after a number of runs in a short period the site started blocking the drivers. In the end using the three browsers in non-headless mode together with a VPN solved the problem.


