from concurrent.futures import ThreadPoolExecutor

from selenium.webdriver.common.by import By

from web_scraping.utils import BasePageLocators, Locator


def get_multi_text(elements):
    try:
        return list(map(lambda ele: ele.get_attribute("textContent"), elements))
    except:
        return [element.text for element in elements]


def get_multi_text_threads(elements):
    try:
        with ThreadPoolExecutor(max_workers=10) as ele_exec:
            return list(ele_exec.map(lambda ele: ele.get_attribute("textContent"), elements))
    except:
        return [element.text for element in elements]


class FlightPageLocators(BasePageLocators):
    # shared between arrivals and departures
    UPDATED_TIME = Locator(By.ID, "lastUpdateTime", lambda ele: ele.text, single=True)
    TABLE_BODY = Locator(By.CSS_SELECTOR, ".tabs-content tbody", single=True)
    UPDATE_BUTTON = Locator(By.ID, "toggleAutoUpdate", single=True)
    LOAD_MORE_BUTTON = Locator(By.ID, "next", single=True)
    CURRENT_RESULTS = Locator(By.ID, 'numOfResults', lambda ele: ele.text, single=True)
    ALL_RESULTS = Locator(By.ID, 'totalItems', lambda ele: ele.text, single=True)

    AIRLINES = Locator(By.CLASS_NAME, "td-airline", get_multi_text)
    FLIGHT_NUMBERS = Locator(By.CLASS_NAME, "td-flight", get_multi_text)
    FLIGHT_CITIES = Locator(By.CLASS_NAME, "td-city", get_multi_text)
    FLIGHT_TERMINAL = Locator(By.CLASS_NAME, "td-terminal", get_multi_text)
    FLIGHT_SCH_TIMES = Locator(By.CSS_SELECTOR, ".td-scheduledTime time strong", get_multi_text)
    FLIGHT_SCH_DATES = Locator(By.CSS_SELECTOR, ".td-scheduledTime time div", get_multi_text)
    FLIGHT_CURR_TIME = Locator(By.CSS_SELECTOR, ".td-updatedTime time", get_multi_text)
    FLIGHT_STATUSES = Locator(By.CSS_SELECTOR, ".td-status div[data-status]", get_multi_text)
    # arrivals
    ARRIVAL_FLIGHTS_TAB = Locator(By.ID, "tab-arrivel_flights-label", single=True)
    ARRIVAL_FLIGHTS_TABLE = Locator(By.ID, "flight_board-arrivel_table", single=True)
    # departurs
    DEPARTURE_FLIGHTS_TAB = Locator(By.ID, "tab--departures_flights-label", single=True)
    DEPARTURE_FLIGHTS_TABLE = Locator(By.ID, "flight_board-departures_table", single=True)
    FLIGHT_COUNTER = Locator(By.CLASS_NAME, "td-counter", get_multi_text)
