# blinker needs to be version < 1.8.0 for seleniumwire to work
from seleniumwire import webdriver, utils
from selenium.webdriver.common.by import By

import time
import json

class GameStopScraper:
    def __init__(self):
        """
        Initializes the root path to target and a driver to pull html
        """
        self.root = "https://www.gamestop.com/"
        self.driver = webdriver.Chrome()
    def search(self, search_text):
        """
        Searches for the price on a game by name
        """
        pass
    def get_all_video_game_deals(self, maxItems = 20):
        """
        Finds the current video game deals
        """
        # set total to 20 as default to not overflow results
        resultTotal = 20
        page = 0
        itemsPerPage = 20
        items = []
        recommendedItems = set()
        while (page * itemsPerPage < resultTotal and page * itemsPerPage < maxItems):
          # this is the path to the deals (sorted by best sellers first)
          path = "deals/video-games?view=new&hybrid=true&srule=top-sellers&start=" + str(itemsPerPage * page) + "&sz=20"
          
          # get details from webpage
          self.driver.get(self.root + path)

          # gives the content time to generate
          time.sleep(5)

          # for the first iteration, retrieve total number of items available in deals
          if page == 0:
            searchResult = self.driver.find_element(By.CSS_SELECTOR, ".pageResults.product-search-count")
            if(searchResult.text):
              searchResultString = searchResult.text
              resultTotal = [int(s) for s in searchResultString.split() if s.isdigit()][0]
          
          # iterate through all requests related the product details and add to items list
          for request in self.driver.requests:
            response, url = request.response, request.url
            if response:  
              # filter out items that aren't video games. Requests are also sent out for recommended items (can be games or consoles)
              if "products-in-all-categories-PLP" in url:
                body = utils.decode(response.body, response.headers.get('Content-Encoding', 'identity'))
                body = body.decode("utf8")
                
               
                body = (body[body.index("{"):body.rindex("}") + 1])
                obj = json.loads(body)
                print(obj)
                for rec in obj["products-in-all-categories-PLP"]["recs"]:
                   recommendedItems.add(rec["id"])


              if "Tile-ShowJSON" in url:
                body = utils.decode(response.body, response.headers.get('Content-Encoding', 'identity'))
                body = body.decode("utf8")
                obj = json.loads(body)
                id = obj['product']['id']
                if(id not in recommendedItems):
                  items.append({
                    "id": obj['product']['id'],
                    "name": obj['product']['name'],
                    "price": obj['product']['price']
                  })
                  if(len(items) >= maxItems):
                    return items
          
          page +=1
        return items
    
scraper = GameStopScraper()
items = scraper.get_all_video_game_deals()
print(items)
