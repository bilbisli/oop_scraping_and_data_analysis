from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePageElement(object):
    """
    Base page class that is initialized on every page object class.
    Used for selecting and interacting with page elements.
    """

    def __set__(self, obj, value):
        """Sets the text to the value supplied"""

        driver = obj.driver
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located(self.locator)
        )

        element.clear()
        element.send_keys(value)

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        driver = obj.driver
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located(self.locator)
        )
        # element = WebDriverWait(driver, 100).until(
        #     lambda driver: driver.find_element(*self.locator))
        # element = driver.find_element(*self.locator)
        return element.get_attribute("value")
