from concurrent.futures import ThreadPoolExecutor

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from web_scraping.sites.IAA.elements import *
from web_scraping.utils import BasePage
from web_scraping.utils import Scraper

MAXIMUM_WAIT_FOR_UPDATE_MINUTES = 30
TIME_INTERVAL = 120


class FlightBoardPage(BasePage):
    def __init__(self, driver=None, headless=True, observer=False):

        self.updated_time = None
        self.observable_element = None
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

    def load_observable(self, observable_locator=None):

        if observable_locator is None:
            observable_locator = FlightPageLocators.AIRLINES
            self.observable_element = observable_locator.get_elements(
                self.driver,
                single=True,
                tries=3,
                refresh_between_tries=True,
                # exp_cond=EC.visibility_of_element_located,
                # wait_time=30
            )

        else:
            self.observable_element = observable_locator.get_elements(self.driver, single=True)
        time_obs = FlightPageLocators.UPDATED_TIME
        self.updated_time = time_obs.get_end_value(self.driver)

        return self.observable_element

    def listen_for_changes(self, observable_element=None, listener=None):
        if observable_element is None:
            observable_element = self.observable_element
        if listener is None:
            listener = self.driver

        prev_time = self.updated_time
        while prev_time == self.updated_time:
            WebDriverWait(listener,
                          TIME_INTERVAL,
                          ).until(EC.staleness_of(observable_element))
            self.load_observable()
            observable_element = self.observable_element
        prev_time = self.updated_time

    def toggle_flight_update(self, driver=None, button=None):

        if button is None:
            button = self.update_button
        if driver is None:
            driver = self.driver

        button.click(self.driver, tries=3)

    def get_arrival_flights(self, locator=None):
        self.driver.refresh()
        self.toggle_flight_update()

        if locator is None:
            locator = FlightPageLocators.ARRIVAL_FLIGHTS_TABLE

        arrivals_data = self.get_data(locator)
        return arrivals_data

    def get_departure_flights(self, locator=None):
        self.driver.refresh()
        self.departure_tab.click(self.driver)
        self.toggle_flight_update()

        if locator is None:
            locator = FlightPageLocators.DEPARTURE_FLIGHTS_TABLE

        departures_data = self.get_data(locator, additional='departure')
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
        ## this calls slow value retrieval method!
        # values = self.get_values_slow(table_element, locators)
        values = self.get_values_fast(locators)

        table_values = dict(zip(fields, values))

        return table_values

    def get_values_fast(self, locators):
        values = []
        for loc in locators:
            query_str = loc.loc_str
            if loc.by == By.CLASS_NAME:
                query_str = '.' + query_str
            values.append(
                self.driver.execute_script(
                    f'return [...document.querySelectorAll("{query_str}")].map(x => x.textContent)'
                )
            )
        return values

    @staticmethod
    def get_values_slow(table_element, locators):
        future_elements, values = [], []
        with ThreadPoolExecutor(max_workers=9) as elements_pool:
            for loc in locators:
                future_elements.append(elements_pool.submit(loc.get_end_value, table_element))
            # simulates thread pool join
            for fut_ele in future_elements:
                values.append(fut_ele.result())
        return values
