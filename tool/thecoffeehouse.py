import mysql.connector as mysql
import os
import json
from dotenv import find_dotenv, load_dotenv
from configparser import ConfigParser
load_dotenv()

HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')

class Database:
    def __init__(self, host=HOST, user=USER, password=PASSWORD, database=DATABASE):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.__conn = mysql.connect(
            host = self.host, 
            user = self.user, 
            password = self.password, 
            database = self.database
        )
        if (self.__conn.is_connected()):
            print("Connected")
        else:
            print("Not connected")

    def connect(self):
        return self.__conn
    
    def getCursor(self):
        return self.__conn.cursor()
    
    def execute(self, sql):
        cursor = self.getCursor()
        cursor.execute(sql)
        row = cursor.fetchall()
        return row

def db():
    database = Database(host=HOST, user=USER, database=DATABASE, password=PASSWORD)
    database.connect()
    return database

class Product:
    def __init__(self, id, category_id, name, price, description, image_url):
        self.id = id
        self.category_id = category_id
        self.name = name
        self.price = price
        self.description = description
        self.image_url = image_url
    
    @staticmethod
    def findById(id):
        database = db()
        sql = """
                SELECT * FROM products WHERE id = '{id}'
            """.format(id = id)

        result = database.execute(sql)
        product = Product(
            id = result[0][0],
            category_id = result[0][1],
            name = result[0][2],
            image_url = result[0][3],
            price = result[0][4],
            description = result[0][5]
        )
        return product
    
    def toJson(self):
        template = {
            "id": self.id,
            "category_id": self.category_id,
            "name": self.name,
            "image_url": self.image_url,
            "price": self.price,
            "description": self.description
        }

        return template
    
    @staticmethod
    def listAll():
        database = db()
        sql = """
                SELECT * FROM products
            """

        result = database.execute(sql)
        listProduct = []
        for record in result:
            current = Product(
                id = record[0],
                category_id = record[1],
                name = record[2],
                image_url = record[3],
                price = record[4],
                description = record[5]
            )
            listProduct.append(current)
        return listProduct

class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    @staticmethod
    def findById(id):
        database = db()
        sql = """
                SELECT * FROM categories WHERE id = '{id}'
            """.format(id = id)

        result = database.execute(sql)
        category = Category(
            id = result[0][0],
            name = result[0][1]
        )
        return category