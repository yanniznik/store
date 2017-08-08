from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql
connection = pymysql.connect(host='localhost',
                             user='root',
                             password=',Ev1ml_Q',
                             db='store',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
@get("/admin")
def admin_portal():
    return template("pages/admin.html")
@get("/")
def index():
    return template("index.html")
@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')
@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')
@get('/admin')
def admin_portal():
    return template("pages/admin.html")
@post('/admin')
def add_something():
    whattheadminwrote = request.POST.get("content")
    value1 = whattheadminwrote['value1']
    value2 = whattheadminwrote['value2']
    query = "INSERT INTO mytable VALUES ({}, {})".format(value1, value2)
    cursor.execute(query)
    cursor.commit()
@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')
@get('/categories')
def listCategories():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id, name FROM categories"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "CATEGORIES": result, "CODE": 200})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": "Internal error", "CODE": 500})
@get('/category/<id>/products')
def getProducts(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products WHERE category = {}".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result, "CODE": 200})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": "Internal error", "CODE": 500})
@get('/products')
def listProducts():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result, "CODE": 200})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": "Internal error", "CODE": 500})
@get('/product/<id>')
def getProduct(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products WHERE id = {}".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result, "CODE": 200})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": "Internal error", "CODE": 500})
@post('/category')
def addCategory():
    name = request.POST.get("name")
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO categories VALUES (0, '{}')".format(name)
            cursor.execute(sql)
            connection.commit()
            result = cursor.lastrowid
            return json.dumps({"STATUS": "SUCCESS", "CAT_ID": result, "CODE": 201})
    except pymysql.err.IntegrityError as e:
        code, msg = e.args
        if code == 1062:
            return json.dumps({"STATUS": "ERROR", "MSG": msg, "CODE": 500})
@post('/product')
def addProduct():
    isFavorite = 0
    title = request.POST.get("title")
    desc = request.POST.get("desc")
    price = int(request.POST.get("price"))
    img_url = request.POST.get("img_url")
    category = int(request.POST.get("category"))
    favorite = request.POST.get("favorite")
    if favorite:
        isFavorite = 1
    try:
        with connection.cursor() as cursor:
            sql = "insert into products values ({}, '{}', {}, '{}', {}, '{}', 0);".format(category, desc, price, title, isFavorite, img_url)
            cursor.execute(sql)
            connection.commit()
            result = cursor.lastrowid
            return json.dumps({"STATUS": "SUCCESS", "PRODUCT_ID": result, "CODE": 201})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": "Internal error", "CODE": 500})
@delete('/category/<id>')
def deleteCategory(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM categories WHERE id = {}".format(id)
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS", "CODE": 201})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": "Internal error", "CODE": 500})
@delete('/product/<id>')
def deleteProduct(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM products WHERE id = {}".format(id)
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS", "CODE": 201})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": "Internal error", "CODE": 500})
run(host='localhost', port=7000)