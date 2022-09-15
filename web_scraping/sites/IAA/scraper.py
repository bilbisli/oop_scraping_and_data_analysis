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
    update_checker = FlightBoardPage(headless=False, observer=True)
    arrivals = FlightBoardPage(headless=False)
    departures = FlightBoardPage(headless=False)

    arriv_exec = ThreadPoolExecutor(max_workers=1)
    depart_exec = ThreadPoolExecutor(max_workers=1)
    save_exec = ThreadPoolExecutor(max_workers=1)

    try:
        if verbose:
            print('Starting scraping...')
        counter = 0
        while 0 < exec_num or exec_num == None:                                        # TODO: timer & exec_num
            if verbose:
                print('Starting scraping...')
            counter += 1
            print('Scraping round', counter)
            future_arrivals_file = arriv_exec.submit(arrivals.get_arrival_flights)
            future_departure_file = depart_exec.submit(departures.get_departure_flights)
            save_exec.submit(save_flights, future_arrivals_file, future_departure_file)
            update_checker.listen_for_changes()
    finally:
        if verbose:
            print('Finished scraping, shutting down')
        arriv_exec.shutdown()
        depart_exec.shutdown()
        save_exec.shutdown()
        if verbose:
            print('Finished shutdown')

                
def save_flights(future_arrivals_file, future_departure_file):
    future_arrivals = future_arrivals_file.result()
    future_departures = future_departure_file.result()
    print('arrivals:')
    print(future_arrivals)
    print('departures:')
    print(future_departures)


if __name__ == '__main__':
    scrape_bbc_main_page_articles(exec_num=4)




        



