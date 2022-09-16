
from web_scraping.utils import BasePage
from web_scraping.utils import Scraper
from web_scraping.sites.IAA.locators import FlightPageLocators
from web_scraping.sites.IAA.elements import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
from selenium.common.exceptions import TimeoutException


MAXIMUM_WAIT_FOR_UPDATE_MINUTES = 30
TIME_INTERVAL = 120

class FlightBoardPage(BasePage):
    def __init__(self, driver=None, headless=True, observer=False):

        options = Scraper.get_options()
        if headless is False:
            options.headless = False
        super().__init__(driver, options=options)

        self.base_url = 'https://www.iaa.gov.il/airports/ben-gurion/flight-board'
        self.driver.get(self.base_url)
        
        self.update_button = UpdateButton()
        self.load_button = LoadMoreButton()
        self.arrival_tab = ArrivalTab()
        self.departure_tab = DepartureTab()

        if observer is True:
            self.load_observable()


    def load_observable(self, obsrvbl_loc=None):

        if obsrvbl_loc is None:
            obsrvbl_loc = FlightPageLocators.AIRLINES
            self.obsrvbl_elmnt = obsrvbl_loc.get_elements(
                self.driver,
                single=True, 
                tries=3,
                refresh_between_tries=True,
                # exp_cond=EC.visibility_of_element_located,
                # wait_time=30
            )
            
        else:
            self.obsrvbl_elmnt = obsrvbl_loc.get_elements(self.driver, single=True)
        time_obs = FlightPageLocators.UPDATED_TIME
        self.updated_time = time_obs.get_end_value(self.driver)
        
        return self.obsrvbl_elmnt

    def listen_for_changes(self, obsrvbl_elmnt=None, listener=None):
        if obsrvbl_elmnt == None:
            obsrvbl_elmnt = self.obsrvbl_elmnt
        if listener is None:
            listener = self.driver
        
        prev_time = self.updated_time
        while prev_time == self.updated_time:
            print('update')
            # print('update', prev_time, self.updated_time)
            WebDriverWait(listener, 
                TIME_INTERVAL
                ).until(EC.staleness_of(obsrvbl_elmnt))
            # time_obs = FlightPageLocators.UPDATED_TIME
            # updated_time = time_obs.get_end_value(listener, single=True)
            self.load_observable()
            print(prev_time, self.updated_time)
            obsrvbl_elmnt = self.obsrvbl_elmnt
        print('table changed')
        prev_time = self.updated_time

    def toggle_flight_update(self, driver=None, button=None):

        if button is None:
            button = self.update_button
        if driver is None:
            driver = self.driver

        button.click(self.driver, tries=3)

    def get_arrival_flights(self, locator=None):
        print('getting arrivals')
        self.driver.refresh()
        self.toggle_flight_update()

        if locator is None:
            locator = FlightPageLocators.ARRIVAL_FLIGHTS_TABLE
        
        arrivals_data = self.get_data(locator)
        print('finished getting arrivals')
        return arrivals_data

    def get_departure_flights(self, locator=None):
        print('getting departures')
        self.driver.refresh()
        self.departure_tab.click(self.driver)
        self.toggle_flight_update()

        if locator is None:
            locator = FlightPageLocators.DEPARTURE_FLIGHTS_TABLE
        
        departures_data = self.get_data(locator, additional='departure')
        print('finished getting departures')
        return departures_data
    
    def get_data(self, locator, additional=None):

        table_element = locator.get_elements(self.driver, single=True)
        self.load_button.load_all_results(self.driver)
        
        fields = [
            'airline',
            'flight',
            'city',
            'terminal',
            'schedule_time',
            'schedule_date',
            'updated_time',
            'status',
        ]
        locators = [
            FlightPageLocators.AIRLINES,
            FlightPageLocators.FLIGHT_NUMBERS,
            FlightPageLocators.FLIGHT_CITIES,
            FlightPageLocators.FLIGHT_TERMINAL,
            FlightPageLocators.FLIGHT_SCH_TIMES,
            FlightPageLocators.FLIGHT_SCH_DATES,
            FlightPageLocators.FLIGHT_CURR_TIME,
            FlightPageLocators.FLIGHT_STATUSES,
        ]
        if additional == 'departure':
            fields.append('checkin_counter')
            locators.append(FlightPageLocators.FLIGHT_COUNTER)

        future_elements, elements = [], []
        with ThreadPoolExecutor(max_workers=9) as elements_pool:
            for loc in locators:
                future_elements.append(elements_pool.submit(loc.get_end_value, table_element))
            # simluate thread pool join
            for fut_ele in future_elements:
                elements.append(fut_ele.result())

        table_values = dict(zip(fields, elements))
        return table_values
