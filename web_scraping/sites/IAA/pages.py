
from web_scraping.utils import BasePage
from web_scraping.utils import Scraper
from web_scraping.sites.IAA.locators import FlightPageLocators
from web_scraping.sites.IAA.elements import ArrivalTab, DepartureTab, UpdateButton, LoadMoreButton
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
# from concurrent.futures import ProcessPoolExecutor
# from pathos.multiprocessing import ProcessingPool

# import dill as pickle
# import copyreg
# import types


class FlightBoardPage(BasePage):
    def __init__(self, driver=None, headless=True, observer=True):

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
            self.obsrvbl_elmnt = FlightPageLocators.FLIGHT_NUMBERS.get_elements(
                self.driver, 
                single=True, 
                # exp_cond=EC.visibility_of_element_located
                )
        else:
            self.obsrvbl_elmnt = obsrvbl_loc.get_elements(self.driver, single=True)

        return self.obsrvbl_elmnt

    # def get_flights_when_updated(self, timer=None, exec_num=None, obsrvbl_loc=None):
    #     listener = self.driver

    #     if obsrvbl_loc is None:
    #         obsrvbl_elmnt = FlightPageLocators.AIRLINES.get_elements(listener, single=True)
    #     else:
    #         obsrvbl_elmnt = obsrvbl_loc.get_elements(listener, single=True)

    #     self.arrival_drive.get(self.base_url)
    #     self.departure_drive.get(self.base_url)

    #     with ThreadPoolExecutor(max_workers=2) as retrieval:
    #         while True:                                                # TODO: timer & exec_num
    #             self.listen_for_changes(obsrvbl_elmnt, listener)
    #             future_arrivals_file = retrieval.submit(self.get_arrival_flights)
    #             future_departure_file = retrieval.submit(self.get_departure_flights)

    def listen_for_changes(self, obsrvbl_elmnt=None, listener=None):
        if obsrvbl_elmnt == None:
            obsrvbl_elmnt = self.obsrvbl_elmnt
        if listener is None:
            listener = self.driver
        WebDriverWait(listener, 120).until(EC.staleness_of(obsrvbl_elmnt))
        self.load_observable()
        return

    def toggle_flight_update(self, driver=None, button=None):

        if button is None:
            button = self.update_button
        if driver is None:
            driver = self.driver

        button.click(self.driver)

        # WebDriverWait(wd, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"))).click()
        # button = WebDriverWait(self.driver, 10).until(
        #     lambda driver: driver.find_element(By.ID, "toggleAutoUpdate"))
        # self.driver.execute_script("arguments[0].click();", button)
    
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

        # numOfResults = WebDriverWait(self.driver, 10).until(
        #     EC.visibility_of_element_located((By.CSS_SELECTOR, "#numOfResults")))
        # print('numOfResults', numOfResults)
        # print('value', numOfResults.text, '<--')
        # exit()
        

        
        # for i in range(3):
        # while True:
        # self.toggle_flight_update()
        table_element = locator.get_elements(self.driver, single=True)

        self.load_button.load_all_results(table_element)
        
        # old_element = FlightPageLocators.AIRLINES.get_elements(self.driver, single=True)
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
        future_values, values = [], []
        with ThreadPoolExecutor(max_workers=len(fields)) as elements_pool:
            for loc in locators:
                future_elements.append(elements_pool.submit(loc.get_end_value, self.driver))
            # simluate thread pool join
            for fut_ele in future_elements:
                elements.append(fut_ele.result())

        
        table_values = dict(zip(fields, elements))



        # print('1')
        # table_values['airline'] = FlightPageLocators.AIRLINES.get_elements
        # print('2')
        # table_values['flight'] = FlightPageLocators.FLIGHT_NUMBERS.get_elements
        # print('3')
        # table_values['city'] = FlightPageLocators.FLIGHT_CITIES.get_elements
        # print('4')
        # table_values['terminal'] = FlightPageLocators.FLIGHT_TERMINAL.get_elements
        # print('5')
        # table_values['schedule_time'] = FlightPageLocators.FLIGHT_SCH_TIMES.get_elements
        # print('6')
        # table_values['schedule_date'] = FlightPageLocators.FLIGHT_SCH_DATES.get_elements
        # print('7')
        # table_values['updated_time'] = FlightPageLocators.FLIGHT_CURR_TIME.get_elements
        # print('8')
        # table_values['status'] = FlightPageLocators.FLIGHT_STATUSES.get_elements
        # if additional == 'departure':
        #     print('9')
        #     table_values['check_in_counter'] = FlightPageLocators.FLIGHT_COUNTER.get_end_value
        
        # with ThreadPoolExecutor(max_workers=len(table_values)) as get_end_values_exec:
        #     for field, func in table_values.items():
        #         table_values[field] = get_end_values_exec.submit(func, table_element)
        #     print('got elements - getting values')
        #     for field, ele in table_values.items():
        #         table_values[field] = get_end_values_exec.submit(
        #             lambda eles: 
        #                 ele.result().get_value
        #             )
        #     print('got values')
        #     # simulate a join for threadpool
        #     for field, func in table_values.items():
        #         table_values[field] = table_values[field].result()
        
        print('done')
        return table_values



        # self.toggle_flight_update()
        # WebDriverWait(self.driver, 120).until(EC.staleness_of(old_element))

        # # print(table.text)
        # # table_ele = self.driver.find_elements(By.CSS_SELECTOR, ".td-airline")
        # print(self.driver.page_source)
        # # button = WebDriverWait(self.driver, 10).until(
        # #     lambda driver: driver.find_element(By.ID, "toggleAutoUpdate"))
        # # self.driver.execute_script("arguments[0].click();", button)
        # element = WebDriverWait(self.driver, 10).until(
        #     lambda driver: driver.find_elements(By.CSS_SELECTOR, "#flight_board-arrivel_table tbody>tr"))
        

    # def get_flights(self):
    #     flights = dict()
    #     # self.toggle_flight_update()
    #     flights['arrivial_flights'] = self.get_arrival_flights()
    #     flights['departure_flights'] = self.get_departure_flights()
    #     # self.toggle_flight_update()

    #     return flights

    # def construct_json(self):
    #     json_dict = dict()
    #     pass

    # def save_json(self, element):
    #     pass


# with FlightBoardPage() as page:
#     res = page.get_flights()
#     print(res)
#     print(len(res['arrivial_flights']['airlines']))
#     # print(res[0].page_source)
#     # print('\n'.join(r.text for r in res))
