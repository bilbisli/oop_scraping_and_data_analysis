
from collections import defaultdict
from web_scraping.utils import BasePage
from web_scraping.utils import Scraper
from web_scraping.sites.IAA.locators import FlightPageLocators
from web_scraping.sites.IAA.elements import UpdateButton, LoadMoreButton
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FlightBoardPage(BasePage):
    def __init__(self, driver=None):
        options = Scraper.get_options()
        options.headless = False
        super().__init__(driver, options=options)

        self.base_url = 'https://www.iaa.gov.il/airports/ben-gurion/flight-board'
        self.driver.get(self.base_url)
        self.update_button = UpdateButton()
        self.load_button = LoadMoreButton()

    def get_flights(self):
        flights = dict()
        # self.toggle_flight_update()
        flights['arrivial_flights'] = self.get_arrival_flights()
        flights['departure_flights'] = self.get_departure_flights()
        # self.toggle_flight_update()

        return flights

    def toggle_flight_update(self, button=None):

        if button is None:
            button = self.update_button

        button.click(self.driver)

        # WebDriverWait(wd, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"))).click()
        # button = WebDriverWait(self.driver, 10).until(
        #     lambda driver: driver.find_element(By.ID, "toggleAutoUpdate"))
        # self.driver.execute_script("arguments[0].click();", button)
    
    def get_arrival_flights(self, locator=None):
        
        if locator is None:
            locator = FlightPageLocators.ARRIVAL_FLIGHTS_TABLE
        
        arrivals_data = self.get_shared_data(locator)

        return arrivals_data

    def get_departure_flights(self, locator=None):
        pass
    
    def get_shared_data(self, locator):

        # numOfResults = WebDriverWait(self.driver, 10).until(
        #     EC.visibility_of_element_located((By.CSS_SELECTOR, "#numOfResults")))
        # print('numOfResults', numOfResults)
        # print('value', numOfResults.text, '<--')
        # exit()
        

        

        while True:
            self.toggle_flight_update()
            table_element = locator.get_elements(self.driver, single=True)

            self.load_button.load_all_results(self.driver)
            
            old_element = FlightPageLocators.AIRLINES.get_elements(self.driver, single=True)
            
            table_values = defaultdict(list)
            print('1')
            table_values['airlines'] = FlightPageLocators.AIRLINES.get_end_value(table_element)
            print('2')
            table_values['flights'] = FlightPageLocators.FLIGHT_NUMBERS.get_end_value(table_element)
            # print('3')
            # table_values['cities'] = FlightPageLocators.FLIGHT_CITIES.get_end_value(table_element)
            # print('4')
            # table_values['terminals'] = FlightPageLocators.FLIGHT_TERMINAL.get_end_value(table_element)
            # print('5')
            # table_values['schedule_time'] = FlightPageLocators.FLIGHT_SCH_TIMES.get_end_value(table_element)
            # print('6')
            # table_values['schedule_date'] = FlightPageLocators.FLIGHT_SCH_DATES.get_end_value(table_element)
            # print('7')
            # table_values['updated_time'] = FlightPageLocators.FLIGHT_CURR_TIME.get_end_value(table_element)
            # print('8')
            # table_values['status'] = FlightPageLocators.FLIGHT_STATUSES.get_end_value(table_element)
            print('done')
            self.toggle_flight_update()
            WebDriverWait(self.driver, 120).until(EC.staleness_of(old_element))

        # # print(table.text)
        # # table_ele = self.driver.find_elements(By.CSS_SELECTOR, ".td-airline")
        # print(self.driver.page_source)
        # # button = WebDriverWait(self.driver, 10).until(
        # #     lambda driver: driver.find_element(By.ID, "toggleAutoUpdate"))
        # # self.driver.execute_script("arguments[0].click();", button)
        # element = WebDriverWait(self.driver, 10).until(
        #     lambda driver: driver.find_elements(By.CSS_SELECTOR, "#flight_board-arrivel_table tbody>tr"))
        return table_values

    def construct_json(self):
        json_dict = dict()
        pass

    def save_json(self, element):
        pass

with FlightBoardPage() as page:
    res = page.get_flights()
    print(res)
    print(len(res['arrivial_flights']['airlines']))
    # print(res[0].page_source)
    # print('\n'.join(r.text for r in res))
