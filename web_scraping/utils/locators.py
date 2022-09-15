import abc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


class BasePageLocators(object):
    """
    Base class to pack element locators together
    """
    pass


class ArticlePageLocators(BasePageLocators, metaclass=abc.ABCMeta):

    @classmethod
    @property
    @abc.abstractmethod
    def ARTICLE_TITLE(cls):
        """throws a NotImplementedError"""
        raise NotImplementedError('Add this locator.')
    @classmethod
    @property
    @abc.abstractmethod
    def ARTICLE_CONTENT(cls):
        """throws a NotImplementedError"""
        raise NotImplementedError('Add this locator.')
    @classmethod
    @property
    @abc.abstractmethod
    def ARTICLE_AUTHOR(cls):
        """throws a NotImplementedError"""
        raise NotImplementedError('Add this locator.')
    @classmethod
    @property
    @abc.abstractmethod
    def ARTICLE_SOURCE(cls):
        """throws a NotImplementedError"""
        raise NotImplementedError('Add this locator.')
    @classmethod
    @property
    @abc.abstractmethod
    def ARTICLE_DATE_TIME(cls):
        """throws a NotImplementedError"""
        raise NotImplementedError('Add this locator.')


class Locator(object):
    def __init__(self, by, loc_str, value_func=None, single=False, exp_cond=None) -> None:
        self.by = by
        self.loc_str = loc_str
        self.value_func = value_func
        self.single = single
        self.exp_cond = exp_cond

    def get_elements(self, driver, single=None, wait_time=10, exp_cond=None):
        if single is None:
            single = self.single
        if single == True:
            find_method = 'find_element'
        else:
            find_method = 'find_elements'
        if exp_cond is None:
            exp_cond = self.exp_cond
        ignored_exceptions=(NoSuchElementException, StaleElementReferenceException,)
        ignored_exceptions = None
        if exp_cond is None:
            get_func = lambda driver: getattr(driver, find_method)(self.by, self.loc_str)
        else:
            get_func = exp_cond((self.by, self.loc_str))
        
        return WebDriverWait(driver, wait_time, ignored_exceptions=ignored_exceptions).until(get_func)

    def get_value(self, elements, value_func=None):
        if value_func is None:
            value_func = self.value_func
        if value_func is None:
            raise AttributeError("value_func is not set and wasn't specified.")
        return value_func(elements)

    def get_end_value(self, driver, value_func=None, single=None, wait_time=10, exp_cond=None):
        elements = self.get_elements(
            driver=driver, 
            single=single, 
            wait_time=wait_time, 
            exp_cond=exp_cond)
        value = self.get_value(elements, value_func)

        return value





############################################
# second option for BasePageLocators - object based instead of class based
############################################
# class BasePageLocators(object):
#     """A base class for page locators. All page locators should come here"""

#     default_value = (By.ID, str)
    
    
#     def __init__(self, locators=None) -> None:
#         self.locators = defaultdict(lambda: BasePageLocators.default_value)

#         if locators:
#             for locator in locators:
#                 self.add_locator(locator)


#     def __setitem__(self, locator_name: str, value):
#         """Sets the desired locator"""
#         if locator_name not in self.locators and hasattr(self, locator_name):
#             raise ValueError(f"{locator_name} is an attribute of '{self.__class__.__name__}' and can't be a locator.")
#         self.locators[locator_name] = value

#     def __getitem__(self, locator_name: str):
#         """Gets the desired locator (packed)"""
#         res = self.locators.get(locator_name)
#         if not res:
#             raise KeyError(f"No such locator as '{locator_name}'")
#         return res

#     def __getattr__(self, attr):
#         try:
#             object.__getattribute__(self, attr)
#         except Exception as e:
#             res = self.locators.get(attr)
#             if not res:
#                 raise e
#             return res

#     def add_locator(self, name: str, by: By, value: str) -> None:
#         self.locators[name] = (by, value)

#     def remove_locator(self, name: str):
#         del self.locators[name]
