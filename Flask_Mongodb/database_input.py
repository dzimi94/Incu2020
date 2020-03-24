import pymongo
from config import url

with pymongo.MongoClient(url) as client:
    db = client.Device_Configuration
    collection = db.Interfaces

    collection.insert_one({
        'Switch_name': 'bru-dna-1',
        'Interface_Name':'int g1/0',
        'Description':'\u0022Connected to the switch2 gi1/2\u0022',
        'State':'up'
    })

    collection.insert_one({
        'Switch_name': 'bru-dna-1',
        'Interface_Name':'int fc1/1/0',
        'Description':'\u0022connected to the storage port 1\u0022',
        'State':'up'
    })

    collection.insert_one({
        'Switch_name': 'mastodon',
        'Interface_Name':'int GigabitEthernet1/0/3',
        'Description':'\u0022Connected to printer CX2\u0022',
        'State':'up'
    })

    collection.insert_one({
        'Switch_name': 'mastodon',
        'Interface_Name':'int GigabitEthernet1/0/5',
        'Description':'\u0022Connected to printer CX4\u0022',
        'State':'down'
    })

    collection.insert_one({
        'Switch_name': 'mastodon',
        'Interface_Name':'int GigabitEthernet1/4/3',
        'Description':'\u0022Connected to server SERV1\u0022',
        'State':'up'
    })

