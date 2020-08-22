from pymongo import MongoClient
from pymongo.collection import ObjectId
from flask import Flask, request
app = Flask(__name__)
import json
import uuid

from flask_cors import CORS
client = MongoClient("mongodb+srv://user:pwd@cluster0.g1zv3.mongodb.net/<dbname>?retryWrites=true&w=majority")

db = client.get_database("data")

x = db.workers
y = db.clothes

CORS(app)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
    
def register_worker(name, country, bio, youtube):
    wid = str(uuid.uuid1())
    x.insert_one({"name":name, "country":country, "bio":bio, "youtube":youtube, "id":wid})
    return {"status":"success"}

def get_worker_data(id):
    return x.find_one({"id":id})

def register_clothes(country, higgs, workers):
    wid = str(uuid.uuid1())
    y.insert_one({"id":wid, "country":country, "higgs":higgs, "workers":workers})
    return {"status":"success"}

def get_clothes_data(id):
    return y.find_one({"id":id})


@app.route('/register-worker', methods=["GET", "POST"])
def register_worker_endpoint():
    data = request.json

    return register_worker(data["name"], data["country"], data["bio"], data["youtube"])

@app.route('/get-worker', methods=["GET", "POST"])
def get_worker_endpoint():
    data = request.json

    return JSONEncoder().encode(get_worker_data(data["id"]))

@app.route('/register-clothes', methods=["GET", "POST"])
def register_clothes_endpoint():
    data = request.json

    return register_clothes(data["country"], data["higgs"], data["workers"])

@app.route('/get-clothes', methods=["GET", "POST"])
def get_clothes_endpoint():
    data = request.json

    return JSONEncoder().encode(get_clothes_data(data["id"]))


if __name__ == "__main__":
    app.run()
