import requests

product_name = "Enterprise-wide scalable collaboration"
requestURL = "http://127.0.0.1:5000/contact/products"
PARAMS = {'product_name': product_name}

data = requests.get(url=requestURL, params=PARAMS)
print(data)
