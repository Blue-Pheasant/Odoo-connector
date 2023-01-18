from thecoffeehouse import *
import requests
from requests.auth import HTTPBasicAuth

HOST = "https://odoo.hoctapkethop.com/api-docs"
TIME_OUT = 10
ENDPOINT =  "https://odoo.hoctapkethop.com/sync_product_api/v1/sync_product/"
SEARCH = "https://odoo.hoctapkethop.com/sync_pydantic_product_api/v1/sync_product_pydantic/search"
APIKEY = "968eeaa2-9d5e-4947-a9eb-4a0d5e5903fb"
LOGIN = "https://odoo.hoctapkethop.com/web/session/authenticate"

data = {
    "jsonrpc": "2.0",
    "params": {
        "login": "long.vo2k1@hcmut.edu.vn",
        "password": "0979172290Aa",
        "db": "erp"
    }
}

sess = requests.session()
print("Login to Odoo")
res = sess.post(LOGIN, json=data)

def check_health():
    try:
        response = requests.get(HOST, timeout = TIME_OUT)
    except requests.exceptions.Timeout:
        message = "System is timed out"
        status = 400
    else:
        message = "System is running"
        status = response.status_code

    print(message)
    return status == 200 
    
def get_template(name, type, category, list_price, description):
    template = {
        "name": name,
        "sale_ok": True,
        "can_be_expensed": True,
        "purchase_ok": True,
        "type": type,
        "category": category,
        "list_price": list_price,
        "description": description,
        "to_weight": True,
        "store_id": "1"
    }

    return template

def sync_product():
    products = Product.listAll()
    for product in products:
        category = Category.findById(product.category_id)
        template = get_template(
            name = product.name,
            type = "Đồ uống",
            category = category.name,
            list_price = product.price,
            description = product.description
        )
        print(template)
        print("Syncing product: " + product.name)
        result = sess.post(url = ENDPOINT, json = template)
        if (result.status_code == 500 or result.status_code == 403):
            print("Sync product: " + product.name + "Status: fail")
        else:
            print("Sync product: " + product.name + "Status: success")
        
        print(result.status_code)

def __main__():
    health = check_health()
    if (health):
        print("Syncing product to Odoo ...")
        sync_product()
        print("Done")
    else:
        print("Can/'t not sync")

__main__()




