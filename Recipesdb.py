import mysql.connector
import os

class Recipesdb(object):
    def __init__(self):
        self.mydb = mysql.connector.connect(
        host=str(os.environ['ENV_HOST']),
        user=str(os.environ['ENV_USER']),
        passwd=str(os.environ['ENV_PASSWORD']),
        database=str(os.environ['ENV_DATABASE']),
        )

    def insert_category(self, name, parent_id, uri, image_url):
        c=self.mydb.cursor()

        query = "INSERT INTO categories (name, parent_category, uri, image_url) VALUES (%s, %s, %s, %s)"
        c.execute(query,(name, parent_id, uri, image_url,))
        self.mydb.commit()
        categories_id = c.lastrowid

        return categories_id

    def delete_category_byname(self, name):
        c=self.mydb.cursor()

        query = "DELETE FROM categories WHERE name = %s"
        c.execute(query,(name,))

        self.mydb.commit()

    def insert_recipe(self, name, uri, image_url, makes, cooks_in, difficulty, categories_id, ingredient_list):
        c=self.mydb.cursor()

        query = "INSERT INTO recipes (name, uri, image_url, makes, cooks_in, difficulty) VALUES (%s, %s, %s, %s, %s, %s)"
        c.execute(query,(name, uri, image_url, makes, cooks_in, difficulty,))
        recipes_id = c.lastrowid

        query_insert_recipe_category = "INSERT INTO recipes_categories (recipes_id, categories_id) VALUES (%s, %s)"
        c.execute(query_insert_recipe_category,(recipes_id, categories_id,))

        for ingredient in ingredient_list: 
            query_insert_ingredient = "INSERT INTO recipes_ingredients (recipes_id, ingredient_text, amount, ingredient_name) VALUES (%s, %s, %s, %s)"
            c.execute(query_insert_ingredient,(recipes_id, ingredient["ingredient_text"], ingredient["amount"], ingredient["ingredient_name"],))

        self.mydb.commit()
        return recipes_id