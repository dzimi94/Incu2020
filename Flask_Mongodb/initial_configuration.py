import pymongo

admin_username = input("Enter your mongodb admin username: ")
admin_password = input("Enter your mongodb admin password: ")
if admin_username == '' and admin_password == '':
    url = "mongodb://localhost:27017/"
else:
    url="mongodb://" + admin_username + ":" + admin_password + "@localhost:27017/"

try:
    with pymongo.MongoClient(url) as client:
        mydb = client["Device_Configuration"]
        client.mydb.add_user('svetlana', 'cisco123', roles=[{'role': 'readWrite', 'db': 'Device_Configuration'}])
except:
    print('Error, check your username and password')
