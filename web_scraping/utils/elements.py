from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import abc


class BasePageElement(object, metaclass=abc.ABCMeta):
    """
    Base page class that is initialized on every page object class.
    Used for selecting and interacting with page elements.
    """

    @classmethod
    @property
    @abc.abstractmethod
    def locator(cls):
        """throws a NotImplementedError"""
        raise NotImplementedError('Add locator to element.')

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
            EC.presence_of_element_located(self.locator.by, self.locator.loc_str)
        )
        
        return element.get_attribute("value")

    def click(self, 
        driver, 
        wait_time=20,
        exp_cond=EC.element_to_be_clickable, 
        tries=1, 
        refresh_between_tries=False,
    ):
        button = self.locator.get_elements(
            driver=driver, 
            wait_time=wait_time, 
            exp_cond=exp_cond,
            tries=tries,
            refresh_between_tries=refresh_between_tries,
            single=True
        )
        
        driver.execute_script("arguments[0].click();", button)
