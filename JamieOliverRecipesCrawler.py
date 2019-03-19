import Recipesdb

class JamieOliverRecipesCrawler(object):
    def main(self):
        self.db = Recipesdb.Recipesdb()

        #test connection
        #test_name = "test category"
        #test_parent_category = None
        #self.db.insert_category(test_name, test_parent_category)
        #self.db.delete_category_byname(test_name)

if __name__ == "__main__":
        JamieOliverRecipesCrawler().main()