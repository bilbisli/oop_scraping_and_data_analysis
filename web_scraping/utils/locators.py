from collections import defaultdict
from selenium.webdriver.common.by import By


class BasePageLocators(object):
    """A base class for page locators. All page locators should come here"""

    default_value = (By.ID, str)

    def __init__(self) -> None:
        self.locators = defaultdict(lambda: BasePageLocators.default_value)

    def __setitem__(self, locator_name: str, value):
        """Sets the desired locator"""
        if locator_name not in self.locators and hasattr(self, locator_name):
            raise ValueError(f"{locator_name} is an attribute of '{self.__class__.__name__}' and can't be a locator.")
        self.locators[locator_name] = value

    def __getitem__(self, locator_name: str):
        """Gets the desired locator (packed)"""
        res = self.locators.get(locator_name)
        if not res:
            raise KeyError(f"No such locator as '{locator_name}'")
        return res

    def __getattr__(self, attr):
        try:
            object.__getattribute__(self, attr)
        except Exception as e:
            res = self.locators.get(attr)
            if not res:
                raise e
            return res
