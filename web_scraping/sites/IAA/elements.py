
from web_scraping.utils import BasePageElement
from web_scraping.sites.IAA.locators import FlightPageLocators


class UpdateButton(BasePageElement):
    locator = FlightPageLocators.UPDATE_BUTTON


class LoadMoreButton(BasePageElement):
    locator = FlightPageLocators.LOAD_MORE_BUTTON

    def load_all_results(self, driver):
        
        while True:
            curr_results_loc = FlightPageLocators.CURRENT_RESULTS.get_end_value(driver, single=True)
            all_results_loc = FlightPageLocators.ALL_RESULTS.get_end_value(driver, single=True)
            # print(curr_results_loc, '/', all_results_loc)
            if curr_results_loc == all_results_loc:
                break
            self.click(driver)
