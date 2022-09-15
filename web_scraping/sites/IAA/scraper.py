import chromedriver_autoinstaller as browser_installer
from selenium.webdriver import Chrome as Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from web_scraping.sites.IAA.pages import FlightBoardPage
from concurrent.futures import ThreadPoolExecutor


def scrape_bbc_main_page_articles(exec_num=None, timer=None, save_path='bbc_articles.csv', verbose=True):

    if verbose:
        print('Preparing scraping...')

    with (
        FlightBoardPage(headless=False) as arrivals,
        FlightBoardPage(headless=False) as departures,
        ThreadPoolExecutor(max_workers=1) as save_exec,
        ThreadPoolExecutor(max_workers=1) as arriv_exec,
        ThreadPoolExecutor(max_workers=1) as depart_exec,
        ):
        counter = 0
        save_vals = []
        with FlightBoardPage(headless=False, observer=True) as update_checker:
            if verbose:
                print('Starting scraping...')
            while counter < exec_num or exec_num == None:           # TODO: timer & exec_num
                counter += 1
                print('Scraping round', counter)
                future_arrivals = arriv_exec.submit(arrivals.get_arrival_flights)
                future_departure = depart_exec.submit(departures.get_departure_flights)
                save_exec.submit(save_flights, future_arrivals, future_departure, verbose)
                
                # arrival = arrivals.get_arrival_flights()
                # print('Arrivals done!')
                # departure = departures.get_departure_flights()
                # print('Departures done!')
                # save_flights(arrival, departure)
                # print('Finished round', counter)

                if counter < exec_num:
                    update_checker.listen_for_changes()

            print('All jobs in queue, finishing up and shutting down')

                
def save_flights(future_arrivals, future_departures, verbose=True):
    if verbose:
        print('saving...')
    arrivals = future_arrivals.result()
    departures = future_departures.result()
    print('arrivals:')
    print(arrivals)
    print('departures:')
    print(departures)
    print('arrivals 2:')
    print({k: tuple(v) for k, v in future_arrivals.items()})
    print('departures 2:')
    print({k: tuple(v) for k, v in future_departures.items()})


if __name__ == '__main__':
    scrape_bbc_main_page_articles(exec_num=1)




        



