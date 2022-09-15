from typing import Any
from web_scraping.utils import BasePageLocators, Locator
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class FlightPageLocators(BasePageLocators):
    # shared between arrivals and departures
    UPDATE_BUTTON = Locator(By.ID, "toggleAutoUpdate", single=True)
    LOAD_MORE_BUTTON = Locator(By.ID, "next", single=True)
    CURRENT_RESULTS = Locator(By.ID, 'numOfResults', lambda ele: ele.text, single=True)
    ALL_RESULTS = Locator(By.ID, 'totalItems', lambda ele: ele.text, single=True)
    AIRLINES = Locator(By.CLASS_NAME, "td-airline", lambda eles: [ele.text for ele in eles])
    FLIGHT_NUMBERS = Locator(By.CLASS_NAME, "td-flight", lambda eles: [ele.text for ele in eles])
    FLIGHT_CITIES = Locator(By.CLASS_NAME, "td-city", lambda eles: [ele.text for ele in eles])
    FLIGHT_TERMINAL = Locator(By.CLASS_NAME, "td-terminal", lambda eles: [ele.text for ele in eles])
    FLIGHT_SCH_TIMES = Locator(By.CSS_SELECTOR, ".td-scheduledTime time strong", lambda eles: [ele.text for ele in eles])
    FLIGHT_SCH_DATES = Locator(By.CSS_SELECTOR, ".td-scheduledTime time div", lambda eles: [ele.text for ele in eles])
    FLIGHT_CURR_TIME = Locator(By.CSS_SELECTOR, ".td-updatedTime time", lambda eles: [ele.text for ele in eles])
    FLIGHT_STATUSES = Locator(By.CSS_SELECTOR, ".td-status [data-status]", lambda eles: [ele.get_attribute("textContent") for ele in eles])
    # arrivals
    ARRIVAL_FLIGHTS_TAB = Locator(By.ID, "tab-arrivel_flights-label", single=True)
    ARRIVAL_FLIGHTS_TABLE = Locator(By.ID, "flight_board-arrivel_table", single=True)
    # departurs
    DEPARTURE_FLIGHTS_TAB = Locator(By.ID, "tab--departures_flights-label", single=True)
    DEPARTURE_FLIGHTS_TABLE = Locator(By.ID, "flight_board-departures_table", single=True)

