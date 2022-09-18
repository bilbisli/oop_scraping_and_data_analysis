import json
from timeit import default_timer as timer

from mergedeep import merge, Strategy

from web_scraping.sites.IAA.pages import FlightBoardPage
from web_scraping.utils.tools import get_time

MINUTE = 60
TIME_FACTOR = MINUTE


def scrape_iaa_flights(save_path='flight_data.json', exec_num=None, scrape_time=None, verbose=True):
    """
    This function fetches all the flight data from the IAA flight board in realtime
    opens 3 browsers: for arrivals, for departures & for update observer
    Args:
        exec_num (int): number of times to fetch the updated flight data - no limit by default
        scrape_time (float|int): time period in which flight retrieval will be done - no limit by default
        save_path (str): path in which to save the unified flight data (including file_name.json)
        verbose (bool): toggles verbosity of the system
    """
    if verbose:
        print('Preparing scraping...')
    with FlightBoardPage(headless=False) as arrivals, FlightBoardPage(headless=False) as departures:
        ## threads are used when slow value get is done to serve as queue
        # ThreadPoolExecutor(max_workers=1) as save_exec, \
        # ThreadPoolExecutor(max_workers=1) as arriv_exec, \
        # ThreadPoolExecutor(max_workers=1) as depart_exec:
        counter = 0
        with FlightBoardPage(observer=True, headless=False) as update_checker:
            start_time = timer()
            if verbose:
                print(f'{get_time()}: Starting scraping...')
            while check_conditions(exec_num, scrape_time, start_time, counter):
                counter += 1
                if verbose:
                    print(f'{get_time()}: Scraping round', counter)
                    print(f'{get_time()}: Fetching flights...')

                ## using threads as queue when using slow value get so as not to interrupt current data retrieval
                # future_arrivals = arriv_exec.submit(arrivals.get_arrival_flights)
                # future_departure = depart_exec.submit(departures.get_departure_flights)
                # save_exec.submit(save_flights, future_arrivals, future_departure, save_path, verbose)
                # for fast value fetch method no threads are needed
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
                    if verbose:
                        print(f'{get_time()}: Waiting for flight table update...')
                    update_checker.listen_for_changes()
            if verbose:
                print(f'{get_time()}: Finishing up')
    if verbose:
        print(f'{get_time()}: Done.')


def check_conditions(exec_num, scrape_time, start_time, counter):
    """
    This function is a helper that calculates whether scraping should be continued for another round or not
    Args:
        exec_num (int): number of times to fetch the updated flight data - no limit by default
        scrape_time (float|int): the time period in which flight retrieval will be done - no limit by default
        start_time (float|int): the time scraping started
        counter: the current scrape round count

    Returns:
        bool: whether to continue scraping or not
    """
    time_cond = scrape_time and (timer() - start_time) / TIME_FACTOR < scrape_time
    count_cond = exec_num and counter < exec_num
    cond1 = not exec_num and not scrape_time
    cond2 = exec_num is None and time_cond
    cond3 = not scrape_time and count_cond
    cond4 = time_cond and count_cond
    res = cond1 or cond2 or cond3 or cond4
    return res


def save_flights(arrivals, departures, save_path, encoding='utf-8'):
    ## for slow value get - future result retrieval
    # arrivals = arrivals.result()
    # departures = departures.result()

    unified_dict = dict()
    unified_dict['flights'] = {'arrivals': {}, 'departures': {}}
    arr_fields = arrivals.keys()
    dep_fields = departures.keys()
    arrivals_packed = list(zip(*arrivals.values()))
    departures_packed = list(zip(*departures.values()))
    for arr_flight, dep_flight in zip(arrivals_packed, departures_packed):
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
    scrape_iaa_flights(exec_num=3, scrape_time=5)
