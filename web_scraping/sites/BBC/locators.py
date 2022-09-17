import re
from copy import copy

from selenium.webdriver.common.by import By

from web_scraping.utils import BasePageLocators, Locator
from web_scraping.utils.locators import ArticlePageLocators


class HomePageLocators(BasePageLocators):
    ARTICLE_ELEMENT = Locator(
        By.CSS_SELECTOR,
        "a.block-link__overlay-link:not([rev*='video'],[rev*='picture'],[href*='/reel/'],[href*='/video/'],"
        "[href*='/av/'])")
    ARTICLE_LINKS = copy(ARTICLE_ELEMENT)
    ARTICLE_LINKS.value_func = lambda article_elements: [ele.get_attribute('href') for ele in article_elements]
    ARTICLE_TITLES = copy(ARTICLE_ELEMENT)
    ARTICLE_TITLES.value_func = lambda article_elements: [ele.text for ele in article_elements]


class NewsPageLocators(ArticlePageLocators):
    ARTICLE_CONTENT = Locator(
        By.CSS_SELECTOR,
        "div[data-component='text-block']",
        lambda article_elements: '\n'.join(ele.text for ele in article_elements)
    )
    ARTICLE_DATE_TIME = Locator(
        By.CSS_SELECTOR,
        "#main-content time[data-testid='timestamp']",
        lambda article_elements: article_elements.get_attribute('datetime')
    )
    ARTICLE_AUTHOR_SOURCE = Locator(By.CSS_SELECTOR, "#main-content header #main-heading + p span")
    ARTICLE_SOURCE = copy(ARTICLE_AUTHOR_SOURCE)
    ARTICLE_SOURCE.value_func = lambda article_element: article_element.text.split('\n')[-1]
    ARTICLE_AUTHOR = copy(ARTICLE_AUTHOR_SOURCE)
    ARTICLE_AUTHOR.loc_str += " strong"
    ARTICLE_AUTHOR.value_func = lambda article_element: re.compile(re.escape('by '), re.IGNORECASE).sub('', article_element.text)
    ARTICLE_TITLE = Locator(By.ID, "main-heading", lambda article_element: article_element.text)


class SportPageLocators(ArticlePageLocators):
    ARTICLE_CONTENT = Locator(
        By.CSS_SELECTOR,
        "div[class='gel-layout__item gel-2/3@l'] h2, div[class='gel-layout__item gel-2/3@l'] \
        h3 div[class='gel-layout__item gel-2/3@l'] h4, div[class='gel-layout__item gel-2/3@l'] p[data-reactid*='$paragraph'",
        lambda artcl_eles: '\n'.join(ele.text for ele in artcl_eles)
    )
    ARTICLE_DATE_TIME = Locator(
        By.CSS_SELECTOR,
        "div[class='gel-layout__item gel-2/3@l'] time[datetime]",
        lambda article_element: article_element.get_attribute('datetime'))
    ARTICLE_AUTHOR_SOURCE = Locator(
        By.CSS_SELECTOR,
        "div[class='gel-layout__item gel-2/3@l'] article header div.story-contributor__body ",
        lambda article_element: article_element.text)
    ARTICLE_SOURCE = copy(ARTICLE_AUTHOR_SOURCE)
    ARTICLE_SOURCE.loc_str += " span.qa-contributor-title"
    ARTICLE_AUTHOR = copy(ARTICLE_AUTHOR_SOURCE)
    ARTICLE_AUTHOR.loc_str += " span.qa-contributor-name"
    ARTICLE_AUTHOR.value_func = lambda article_element: re.compile(re.escape('by '), re.IGNORECASE).sub('', article_element.text)
    ARTICLE_TITLE = Locator(By.ID, "page", lambda article_element: article_element.text)

# TODO: More locators (for each article page type)
# class WorklifePageLocators(BasePageLocators):

#     ARTICLE_CONTENT = Locator(
#         By.CSS_SELECTOR,
#         "div[class='gel-layout__item gel-2/3@l'] h2, div[class='gel-layout__item gel-2/3@l'] \
#         h3 div[class='gel-layout__item gel-2/3@l'] h4, div[class='gel-layout__item gel-2/3@l'] p[data-reactid*='$paragraph'",
#         lambda artcl_ele: artcl_ele.text
#         )
#     ARTICLE_DATE_TIME = Locator(By.CSS_SELECTOR, "div[class='gel-layout__item gel-2/3@l'] time[datetime]")
#     ARTICLE_AUTHOR_SOURCE = Locator(
#         By.CSS_SELECTOR,
#         "div[class='gel-layout__item gel-2/3@l'] article header div.story-contributor__body ",
#         lambda artcl_ele: artcl_ele.text)
#     ARTICLE_SOURCE = copy(ARTICLE_AUTHOR_SOURCE)
#     ARTICLE_SOURCE.loc_str += " span.qa-contributor-title"
#     ARTICLE_AUTHOR = copy(ARTICLE_AUTHOR_SOURCE)
#     ARTICLE_AUTHOR.loc_str += " span.qa-contributor-name"
#     ARTICLE_AUTHOR.value_func = lambda artcl_ele: re.compile(re.escape('by '), re.IGNORECASE).sub('', artcl_ele.text)
#     ARTICLE_TITLE = Locator(By.ID, "page", lambda artcl_ele: artcl_ele.text)
