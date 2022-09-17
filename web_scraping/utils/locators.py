import abc

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class BasePageLocators(object):
    """
    Base class to pack web page element locators together
    """
    pass


class ArticlePageLocators(BasePageLocators, metaclass=abc.ABCMeta):
    """
    This class is a base class for article web pages containing basic article properties
    """

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
    """
    This class represents a locator object to locate elements in a web page
    """
    def __init__(self, by, loc_str, value_func=None, single=False, exp_cond=None) -> None:
        """
        Args:
            by (By): see By<selenium.webdriver.common.by.By>
            loc_str (str): string that identifies the element in the web page (xpath / css / etc.)
            value_func (function): function used to extract the desired data from the web page element
            single (bool): whether to try to locate a single result or multiple
            exp_cond (:mod:`EC`): see EC<selenium.webdriver.support.expected_conditions>
        """
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
            refresh_between_tries=False):
        """
        This method tries to locate and retrieve the elements from the web page using `by` and `loc_str`
        Args:
            driver: driver of the web page
            single (bool): whether to try to locate a single result or multiple
            wait_time (float|int): time to wait for element retrieval
            exp_cond (:mod:`EC`): see EC<selenium.webdriver.support.expected_conditions>
            tries (int): number of tries upon failure to retrieve element
            refresh_between_tries (bool): whether to refresh the web page between tries or not

        Returns:
            the elements extracted
        """
        if single is None:
            single = self.single
        if single:
            find_method = 'find_element'
        else:
            find_method = 'find_elements'
        if exp_cond is None:
            exp_cond = self.exp_cond
        # ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
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
        """
        This method extracts the value from the web page elements
        Args:
            elements: the web elements to extract the value from
            value_func (function): the function used to extract the value from the web element

        Returns:
            the value extracted
        """
        if value_func is None:
            value_func = self.value_func
        if value_func is None:
            raise AttributeError("value_func is not set and wasn't specified.")

        return value_func(elements)

    def get_end_value(self, driver, value_func=None, single=None, wait_time=10, exp_cond=None):
        """
        This method uses `get_elements` and `get_value` to retrieve the final value by calling them sequentially
        Args:
            driver: driver of the web page
            value_func (function): the function used to extract the value from the web element
            single (bool): whether to try to locate a single result or multiple
            wait_time (float|int): time to wait for element retrieval
            exp_cond (:mod:`EC`): see EC<selenium.webdriver.support.expected_conditions>

        Returns:
            the final value
        """
        elements = self.get_elements(
            driver=driver,
            single=single,
            wait_time=wait_time,
            exp_cond=exp_cond)
        value = self.get_value(elements, value_func)

        return value
