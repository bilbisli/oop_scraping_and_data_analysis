from collections import defaultdict
from web_scraping.sites.IAA.pages import FlightBoardPage
# from concurrent.futures import ThreadPoolExecutor     # for speeding slow value retrieval
from mergedeep import merge, Strategy
from timeit import default_timer as timer
from web_scraping.utils.tools import get_time
import json


MINUTE = 60
TIME_FACTOR = MINUTE


def scrape_iaa_flights(exec_num=None, scrape_time=None, save_path='flight_data.json', verbose=True):

    if verbose:
        print('Preparing scraping...')
    with (
        FlightBoardPage(headless=False) as arrivals,
        FlightBoardPage(headless=False) as departures,
        ## threads are used when slow value get is done to improve the performance
        # ThreadPoolExecutor(max_workers=1) as save_exec,
        # ThreadPoolExecutor(max_workers=1) as arriv_exec,
        # ThreadPoolExecutor(max_workers=1) as depart_exec,
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

                ## improving slow values get with threads
                # future_arrivals = arriv_exec.submit(arrivals.get_arrival_flights)
                # future_departure = depart_exec.submit(departures.get_departure_flights)
                # save_exec.submit(save_flights, future_arrivals, future_departure, save_path, verbose)
                
                # for fast value get no threads are needed
                if verbose:
                    print(f'{get_time()}: Fetching flights...')
                arrival = arrivals.get_arrival_flights()
                departure = departures.get_departure_flights()
                if verbose:
                    print(f'{get_time()}: Flights fetched')
                if verbose:
                    print(f'{get_time()}: saving...')
                save_flights(arrival, departure, save_path=save_path)
                if verbose:
                    print(f'{get_time()}: Saved!')

                if check_conditions(exec_num, scrape_time, start_time, counter):
                    update_checker.listen_for_changes()
            if verbose:
                print(f'{get_time()}: Finishing up')
    if verbose:
        print(f'{get_time()}: Done.')


def check_conditions(exec_num, scrape_time, start_time, counter):
    time_cond = scrape_time and (timer() - start_time) / TIME_FACTOR < scrape_time
    count_cond = exec_num and counter < exec_num
    cond1 = exec_num is None and scrape_time is None
    cond2 = exec_num is None and time_cond
    cond3 = scrape_time is None and count_cond
    cond4 = time_cond and count_cond
    res =  cond1 or cond2 or cond3 or cond4
    return res

def save_flights(arrivals, departures, save_path, encoding='utf-8'):
    
    ## for slow value get - future result retrival
    # arrivals = arrivals.result()
    # departures = departures.result()

    unified_dict = dict()
    unified_dict['flights'] = {'arrivals': {}, 'departures': {}}
    arr_fields = arrivals.keys()
    dep_fields = departures.keys()
    arrivals_packed = list(zip(*arrivals.values()))
    departues_packed = list(zip(*departures.values()))
    for arr_flight, dep_flight in zip(arrivals_packed, departues_packed):
        flight_dict = dict(zip(arr_fields, arr_flight))
        flight_key = f'{flight_dict["flight"]} {flight_dict["city"]} {flight_dict["schedule_date"]}'
        unified_dict['flights']['arrivals'][flight_key] = flight_dict
        flight_dict = dict(zip(dep_fields, dep_flight))
        flight_key = f'{flight_dict["flight"]} {flight_dict["city"]} {flight_dict["schedule_date"]}'
        unified_dict['flights']['departures'][flight_key] = flight_dict

    master_dict = {}
    try:
        with open(save_path, 'r', encoding=encoding) as fp:
            master_dict = json.load(fp)
    except FileNotFoundError:
        pass
    merge(master_dict, unified_dict, strategy=Strategy.REPLACE)
    with open(save_path, 'w', encoding=encoding) as fp:
        json.dump(master_dict, fp, indent=4, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    scrape_iaa_flights(exec_num=3)
