from web_scraping.utils import BasePageLocators, Locator
from selenium.webdriver.common.by import By


class FlightPageLocators(BasePageLocators):
    ARRIVAL_FLIGHTS = Locator(By.ID, "tab-arrivel_flights-label", lambda ele: ele.text)
    DEPARTURE_FLIGHTS = Locator(By.ID, "tab--departures_flights-label", lambda ele: ele.text)
    ARRIVAL_FLIGHTS = Locator(By.CSS_SELECTOR, "#flight_board-arrivel_table")
    
