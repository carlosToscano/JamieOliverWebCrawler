import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import time

class WebCrawler(object):
    def __init__(self):
        self.request_count = 0

    def get_beautiful_html(self, starting_url):
        time.sleep(5)
        self.request_count = self.request_count + 1

        #https://www.jamieoliver.com/recipes/
        r = requests.get(starting_url)

        if r.status_code != 200:
            print("died at: ", self.request_count)
            return None

        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def identify_page(self, beautiful_html):
        #<section id="recipe-single">, recipe-cat-listing, sec-recipe-landing
        #is_recipe, is_category
        section = beautiful_html.select("section#recipe-single")
        if len(section) > 0:
            return True, False
        section = beautiful_html.select("div.recipe-row")
        if len(section) > 0:
            return False, True
        section = beautiful_html.select("section#recipe-cat-listing")
        if len(section) > 0:
            return False, True
        section = beautiful_html.select("section#sec-recipe-landing")
        if len(section) > 0:
            return False, True
        section = beautiful_html.select("recipe-subcat-listing")
        if len(section) > 0:
            return False, True
        return False, False

    def get_list_elements(self, beautiful_html):
        #<div class="tile-wrapper">
        b_list = beautiful_html.select("div.tile-wrapper")
        result = []

        if len(b_list) == 0:
            b_list = beautiful_html.select("div.recipe-block")

        for b_item in b_list:   
            url = b_item.a["href"]
            parsed = urllib.parse.urlparse(url)
            uri = parsed.path
            image_url = b_item.a.select("img")[0]["src"]
            item_name_element = b_item.a.select("div.tile-title")
            if len(item_name_element) == 0:
                item_name_element = b_item.a.select("div.recipe-title")
            name = item_name_element[0].getText()
            name = re.sub(' +', ' ', name).strip()

            item = {
                "url": url,
                "uri": uri,
                "image_url": image_url,
                "name": name,
                }

            result.append(item)    

        return result

    def get_recipe_info(self, beautiful_html):
        b_recipe_details_1 = beautiful_html.select("div.recipe-details-col")[0]
        b_makes = b_recipe_details_1.select("div.serves")
        b_cooksin = b_recipe_details_1.select("div.time")
        b_difficulty = b_recipe_details_1.select("div.difficulty")
        
        makes = ""
        cooks_in = ""
        difficulty = ""

        if len(b_makes) > 0:
            makes = b_makes[0].getText().replace("\"", "")
            makes =re.sub(' +', ' ', makes).strip()
        if len(b_cooksin) > 0:
            cooks_in = b_cooksin[0].getText().replace("\"", "")
            cooks_in = re.sub(' +', ' ', cooks_in).strip()
        if len(b_difficulty) > 0:
            difficulty = b_difficulty[0].getText().replace("\"", "")
            difficulty = re.sub(' +', ' ', difficulty).strip()

        b_ingredient_list = beautiful_html.select("ul.ingred-list > li")

        result = {
            "makes": makes,
            "cooks_in": cooks_in,
            "difficulty": difficulty,
            "ingredient_list": []
            }

        for b_item in b_ingredient_list:
            #ingredient.ingredient_text, ingredient.amount, ingredient.ingredient_name
            ingredient_text = b_item.getText().replace("\"", "")
            ingredient_text = re.sub(' +', ' ', ingredient_text).strip()

            indexof = ingredient_text.find(" ")
            amount = ingredient_text[:indexof]
            ingredient_name = ingredient_text[indexof+1:]

            ingredient = {
                "ingredient_text": ingredient_text,
                "amount": amount,
                "ingredient_name": ingredient_name
                }

            result["ingredient_list"].append(ingredient)

        return result