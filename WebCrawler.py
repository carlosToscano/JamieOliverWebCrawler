import request
from bs4 import BeautifulSoup
import urllib.parse

class WebCrawler(object):
    def __init__(self):
        r = requests.get('https://www.jamieoliver.com/recipes/')
        r.status_code
        soup = BeautifulSoup(html, 'html.parser')
     
    def identify_page(self, beauty_html):
        #<section id="recipe-single">, recipe-cat-listing, sec-recipe-landing
        #is_recipe, is_category
        section = beauty_html.find_next("section", {"id": "recipe-single"})
        if section != None:
            return True, False
        section = beauty_html.find_next("section", {"id": "recipe-cat-listing"})
        if section != None:
            return False, 
        section = beauty_html.find_next("section", {"id": "sec-recipe-landing"})
        if section != None:
            return False, True
        return False, False

    def get_list_elements(self, beauty_html):
        #<div class="tile-wrapper">
        b_list = beauty_html.find_all("div", {"class": "tile-wrapper"})
        result = []

        if length(b_list) == 0:
            b_list = beauty_html.find_all("div", {"class": "recipe-block"})

        for b_item in b_list:
            item = {}
            item.url = b_item.a["href"]
            parsed = urlparse(item.url)
            item.uri = parsed.path
            item.image_url = b_item.a.findChild("img")["src"]
            item_name_element = b_item.a.findChild("div", {"class": "tile-title"})
            if item_name_element != None:
                item_name_element = b_item.a.findChild("div", {"class": "recipe-title"})
            item_name_element = b_item.a.findChild("div", {"class": "tile-title"})
            item.name = item_name_element.getText()
            result.append(item)    

        return result

    def get_recipe_info(self, beauty_html):
        
        return recipe