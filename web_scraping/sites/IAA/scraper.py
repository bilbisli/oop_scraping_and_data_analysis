from collections import defaultdict
from web_scraping.sites.IAA.pages import FlightBoardPage
from concurrent.futures import ThreadPoolExecutor
from mergedeep import merge, Strategy
from timeit import default_timer as timer
from datetime import datetime
import json


MINUTE = 60
TIME_FACTOR = MINUTE


def scrape_bbc_main_page_articles(exec_num=None, scrape_time=None, save_path='flight_data.json', verbose=True):

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
        with FlightBoardPage(observer=True, headless=False) as update_checker:
            start_time = timer()
            if verbose:
                print(f'{get_time()}: Starting scraping...')
            while check_conditions(exec_num, scrape_time, start_time, counter):
                counter += 1
                if verbose:
                    print(f'{get_time()}: Scraping round', counter)
                future_arrivals = arriv_exec.submit(arrivals.get_arrival_flights)
                future_departure = depart_exec.submit(departures.get_departure_flights)
                save_exec.submit(save_flights, future_arrivals, future_departure, save_path, verbose)
                
                # arrival = arrivals.get_arrival_flights()
                # print('Arrivals done!')
                # departure = departures.get_departure_flights()
                # print('Departures done!')
                # save_flights(arrival, departure, save_path=save_path)
                # print('Finished round', counter)

                if check_conditions(exec_num, scrape_time, start_time, counter):
                    update_checker.listen_for_changes()
            if verbose:
                print(f'{get_time()}: All jobs in queue - finishing up')
    if verbose:
        print(f'{get_time()}: Done.')


def check_conditions(exec_num, scrape_time, start_time, counter):
    time_cond = (timer() - start_time) / TIME_FACTOR < scrape_time
    count_cond = counter < exec_num
    cond1 = exec_num is None and scrape_time is None
    cond2 = exec_num is None and time_cond
    cond3 = scrape_time is None and count_cond
    cond4 = time_cond and count_cond
    res =  cond1 or cond2 or cond3 or cond4
    return res

def get_time():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

def save_flights(future_arrivals, future_departures, save_path, verbose=True):
    # arrivals = future_arrivals
    # departures = future_departures


    arrivals = future_arrivals.result()
    departures = future_departures.result()


    if verbose:
        print('saving...')


    unified_dict = dict()
    unified_dict['flights'] = {'arrivals': {}, 'departures': {}}
    arr_fields = arrivals.keys()
    dep_fields = departures.keys()
    arrivals_packed = list(zip(*arrivals.values()))
    departues_packed = list(zip(*departures.values()))
    
    for flight in arrivals_packed:
        unified_dict['flights']['arrivals'] = dict(zip(arr_fields, flight))
    for flight in departues_packed:
        unified_dict['flights']['departures'] = dict(zip(dep_fields, flight))
    
    print('arrivals:')
    # print(arrivals)
    print('departures:')
    # print(departures)

    # unified_dict = {'arrivals': arrivals, 'departures': departures}
    master_dict = {}
    try:
        with open(save_path, 'r') as fp:
            master_dict = json.load(fp)
    except FileNotFoundError:
        pass
        
    print(unified_dict)

    merge(master_dict, unified_dict, strategy=Strategy.REPLACE)
    
    # unique_end = datetime.now().strftime("%j_%H_%M_%S_%f_%Y")
    with open(save_path, 'w') as fp:
        json.dump(master_dict, fp, indent=4, sort_keys=True)

    if verbose:
        print('Saved')


    # print('arrivals 2:')
    # print({k: tuple(v) for k, v in future_arrivals.items()})
    # print('departures 2:')
    # print({k: tuple(v) for k, v in future_departures.items()})


if __name__ == '__main__':
    scrape_bbc_main_page_articles(exec_num=3, scrape_time=10)




        



