import Recipesdb
import WebCrawler

class JamieOliverRecipesCrawler(object):
    def main(self):
        self.db = Recipesdb.Recipesdb()

        #test connection
        #test_name = "test category"
        #test_parent_category = None
        #self.db.insert_category(test_name, None, "", test_parent_category)
        #self.db.delete_category_byname(test_name)

        self.joCrawler = WebCrawler.WebCrawler()
        starting_url = "https://www.jamieoliver.com/recipes/"
        self.crawl_link(None, starting_url, None)

    #the explanation to arrange details like this is that in categories the category image lives outside the page, in the parent category
    def crawl_link(self, details, url, parent_id):
        fixed_url = url
        if url.find("https") == -1:
            fixed_url = "https://www.jamieoliver.com" + url

        soup = self.joCrawler.get_beautiful_html(fixed_url)

        if soup != None:
            is_recipe, is_category = self.joCrawler.identify_page(soup)
            if is_recipe:
                self.crawl_recipe_page(soup, details, parent_id)
            if is_category:
                new_parent_id = parent_id
                if details != None:
                    new_parent_id = self.db.insert_category(details["name"], parent_id, details["uri"], details["image_url"])
                self.crawl_category_page(soup, details, new_parent_id)
                
    def crawl_recipe_page(self, soup, details, category_id):
        recipe_details = self.joCrawler.get_recipe_info(soup)
        self.db.insert_recipe(details["name"], details["uri"], details["image_url"], recipe_details["makes"], recipe_details["cooks_in"], recipe_details["difficulty"], category_id, recipe_details["ingredient_list"])

    def crawl_category_page(self, soup, details, parent_id):
        item_list = self.joCrawler.get_list_elements(soup)
        for this_item in item_list:
            self.crawl_link(this_item, this_item["url"], parent_id)                

if __name__ == "__main__":
        JamieOliverRecipesCrawler().main()