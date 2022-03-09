from multiprocessing.spawn import prepare
from operator import le
from pydoc import pager
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

    return {'message':'Product Created'},201




@app.patch('/products/<int:id>')
def patch_base(id):
    data_base=base()
    body_request=request.get_json()
    body_keys_set=set(body_request.keys())
    expected_key={'name','price'}
    invalid_key=body_keys_set-expected_key
    if invalid_key:
        return {'error':'key not allowed','key_denied':list(invalid_key) },404

    for file in data_base:
        file['id']=int(file['id'])
        if id == file['id']:
            fieldnames = ["id", "name", "price"]

            payload = {"id": id, "name": body_request['name'], "price":float(body_request['price'])}
            file.update(payload)

            f = open('FILE_PATH', "w")

            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writerow(file)

            f.close()
            return  file
            
        else:
            message={f"error": f'product id {str(id)} not found'},404

    return message









@app.delete('/products/<int:id>')
def delete_base(id):
    data_base=base()
    for file in data_base:
        file['id']=int(file['id'])
        if id == file['id']:
            fieldnames = ["id", "name", "price"]

            data_base.remove(file)

            f = open('FILE_PATH', "w")

            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writerow(file)

            f.close()
            return  file
            
        else:
            message={f"error": f'product id {str(id)} not found'},404