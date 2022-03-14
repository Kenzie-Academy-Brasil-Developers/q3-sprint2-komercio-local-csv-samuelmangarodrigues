from itertools import product
from math import prod
from urllib import response
from app.products import base
from flask import Flask,jsonify,request
import csv
import os

file_test=os.getenv('FILE_PATH')

app=Flask(__name__)



@app.get('/products')
def get_products():
    data_base=base()
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 3))
    products_paginated = data_base[(page-1)*per_page:page*per_page]

    
    for file in data_base:
        file['id']=int(file['id'])
        file['price']=float(file['price'])  
    return jsonify(products_paginated)
    

@app.get('/products/<int:id>')
def get_prod_id(id):
    data_base=base()
    new_product=[]
    for file in data_base:
        file['id']=int(file['id'])
        if file['id']==id:
            new_product.append(file)
            return jsonify(new_product),200
        else:
            message = {'message':'Product not find'},404
    return message
   


    
@app.post('/products')
def create_products():
    expected_keys={'name','price'}
    data_base=base()
    body_request=request.get_json() 
    body_keys_set=set(body_request.keys())
    invalid_keys=body_keys_set-expected_keys

    if invalid_keys:
        return {'error':'key not allowed','keys_denied':list(invalid_keys) },404

    new_id=data_base[-1]
    new_id=int(new_id['id'])+1
    fieldnames = ["id","name", "price"]

    payload = {"id":int(new_id),"name":body_request['name'], "price":body_request['price']}

    f = open(file_test,"a")

    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writerow(payload)

    f.close()

    return payload,201




@app.patch('/products/<int:id>')
def patch_base(id):
    data_base=base()
    body_request=request.get_json()
    body_keys_set=set(body_request.keys())
    expected_key={'name','price'}
    invalid_key=body_keys_set-expected_key
    reponse=[]
    if invalid_key:
        return {'error':'key not allowed','key_denied':list(invalid_key) },404

    product = [product for product in data_base if id == int(product["id"])]
    if len(product) == 0:
        return {"error": f"product id {id} not found"}

    for product in data_base:
        product["id"]=int(product["id"])
        if product["id"] == id:
            product["name"] = body_request.get("name", product["name"])
            product["price"] = body_request.get("price", product["price"])
            reponse=product

    fieldnames = ["id", "name", "price"]
    file = open(file_test, "w")
    result = csv.DictWriter(file, fieldnames=fieldnames)
    result.writeheader()
    result.writerows(data_base)
    file.close()

    return reponse, 200


@app.delete('/products/<int:id>')
def delete_base(id):
    data_base=base()
    response=[]

    product=[product for product in data_base if id == int(product["id"])]
    if len(product)==0:
        return {"error": f"product id {id} not found"}

    for product in data_base:
        product["id"]=int(product["id"])
        if product["id"]==id:
            data_base.remove(product)
            response=product

    fieldnames = ["id", "name", "price"]
    file = open(file_test, "w")
    result = csv.DictWriter(file, fieldnames=fieldnames)
    result.writeheader()
    result.writerows(data_base)
    file.close()

    return response    