import abc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException


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

    def get_elements(
        self, 
        driver, 
        single=None, 
        wait_time=10, 
        exp_cond=None, 
        tries=1, 
        refresh_between_tries=False,
    ):
        
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
        
        for i in range(tries, 0, -1):
            try:
                return WebDriverWait(driver,
                    wait_time, 
                    ignored_exceptions=ignored_exceptions).until(get_func)
            except TimeoutException:
                if i - 1 == 0:
                    raise
                print(f'Element retrieval failed - tries left: {i - 1}')
                if refresh_between_tries:
                    driver.refresh()

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
