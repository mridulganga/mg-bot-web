import pymongo
import datetime
import os

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.lmfgk.mongodb.net/bot?retryWrites=true&w=majority")
db = client.main

shop = [
        {"name":"apple", "price":10},
        {"name":"chillpill", "price":20},
        {"name":"house", "price":100000, "max":1},
        {"name":"car", "price":20000, "max":3},
    ]

def init():
    for collection in ["users", "shop", "loans", "helps"]:
        try:
            db.create_collection(collection)
        except pymongo.errors.CollectionInvalid:
            pass

def get_users():
    return db.users.find().sort("wallet",pymongo.DESCENDING)

def get_user(username):
    username = username.lower()
    return db.users.find_one({"username":username})
    

def update_user(new_obj):
    o = db.users.find_one_and_replace({"username":new_obj["username"]},new_obj)

def get_or_create_user(username):
    # get user if exists otherwise create and get
    user = get_user(username)
    if not user:
        user = {
            "username": username,
            "wallet" : 0,
            "bank" : 0,
        }
        db.get_collection("users").insert_one(user)
    return user

def get_shop_items():
    return shop

def get_shop_item(item):
    for i in shop:
        if i["name"] == item:
            return i
    return None