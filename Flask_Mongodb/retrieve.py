import pymongo
from config import url


with pymongo.MongoClient(url) as client:
    db = client.Device_Configuration
    collection = db.Interfaces

    # cursor = collection.find({'Switch_name':'mastodon', 'Interface_Name':'int GigabitEthernet1/0/5' })
    cursor = collection.find({'Switch_name': 'mastodon'})

    for result in cursor:
        for key, value in result.items():
            print(f'{key}:{value}')

        print('')