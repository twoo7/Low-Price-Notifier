from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TargetScraper:
    def __init__(self):
        """
        Initializes the root path to target and a driver to pull html
        """
        self.root = "https://www.target.com/"
        self.driver = webdriver.Chrome()
    def search(self, search_text):
        """
        Searches for the price on a game by name
        """
        pass
    def get_video_game_deals(self):
        """
        Finds the current video game deals
        """
        # TODO:
        # add the ability to cycle through pages to grab more
        
        # this is the path to the deals (sorted by best sellers first)
        path = "c/video-game-deals/-/N-0snqs?sortBy=bestselling&moveTo=product-list-grid"
        # this is the div class that all the information falls into
        ALL_INFO_HTML_CLASS = "styles__StyledDetailsWrapper-sc-hztu6c-1 TqROS"
        TITLE_HTML_CLASS = "styles_truncate__Eorq7 styles__Truncate-sc-1b75xo0-0 koOpCs"
        PRICE_HTML_TAG = "current-price"
        self.driver.get(self.root + path)
        # gives the content time to generate
        time.sleep(5)
        elements = self.driver.find_elements(By.XPATH, f"//div[@class='{ALL_INFO_HTML_CLASS}']")
        titles = []
        prices = []
        # loops through all product tags
        for element in elements:
            title = element.find_element(By.XPATH, f".//div[@class='{TITLE_HTML_CLASS}']")
            price = element.find_element(By.XPATH, f".//span[@data-test='{PRICE_HTML_TAG}']")
            titles.append(title.get_attribute("title"))
            prices.append(price.text)
        return titles, prices
    
scraper = TargetScraper()
titles, prices = scraper.get_video_game_deals()
print(titles)
print(prices)
