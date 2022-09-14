import chromedriver_autoinstaller as browser_installer
from selenium.webdriver import Chrome as Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
import re


def scrape_bbc():
    browser_installer.install()

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    driver = Driver(options=options)

    # base_page_url = 'https://www.bbc.com/'
    # driver.get(base_page_url)

    # article_link_tag = 'a'
    # article_link_class = 'block-link__overlay-link'

    url_test = 'https://www.bbc.com/news/business-62745767'
    driver.get(url_test)
    locator = (By.CSS_SELECTOR, "div[data-component='text-block']")

    # try:
    ignored_exceptions=(NoSuchElementException, StaleElementReferenceException,)

    content_elements = WebDriverWait(driver, 100, ignored_exceptions=ignored_exceptions).until(
        lambda driver: driver.find_elements(*locator))

    content = ''
    for content_block in content_elements:
        content += content_block.text + '\n'
    
    print(content)

    locator = (By.CSS_SELECTOR, "#main-content time[data-testid='timestamp']")

    date_time = WebDriverWait(driver, 100, ignored_exceptions=ignored_exceptions).until(
        lambda driver: driver.find_element(*locator))

        # article_link_elements = driver.find_elements(By.XPATH, f"(//{article_link_tag}[@class='{article_link_class}'])")
        # for link_element in article_link_elements:
        #     print(link_element.get_attribute('href'))
    # except:
    #     driver.quit()
    print(date_time.get_attribute('datetime'))

    locator = (By.CSS_SELECTOR, "#main-content header #main-heading + p span")
    find_func = 'find_element'
    author_source = WebDriverWait(driver, 100, ignored_exceptions=ignored_exceptions).until(
        lambda driver: getattr(driver, find_func)(*locator)).text.split('\n')
    remove_by = re.compile(re.escape('by '), re.IGNORECASE)
    author = remove_by.sub('', author_source[0])
    source = author_source[-1]

    print(author)
    print(source)
    


if __name__ == '__main__':
    scrape_bbc()