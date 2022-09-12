from scraper import Scraper
import unittest


class TestScraper(unittest.TestCase):
    def setUp(self) -> None:
        self.scraper = Scraper()
    
    def tearDown(self) -> None:
        self.scraper.close()
    
    def test_scraper_on_general_website(self):
        self.scraper.get("http://www.python.org")
        assert "Python" in self.scraper.title

    def test_scraper_on_designated_news_site(self):
        pass


if __name__ == '__main__':
    unittest.main()
