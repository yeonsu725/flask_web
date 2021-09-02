from pymongo import MongoClient

client = MongoClient("mongodb+srv://root:1234@cluster0.g4bac.mongodb.net/test?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
db = client.test  

list = db.mydata
list.insert_one({"data":"test123"})