from pymongo import MongoClient
from bson.objectid import ObjectId #這東西再透過ObjectID去尋找的時候會用到
class manageDB():
    def __init__(self):
        self.conn=MongoClient('127.0.0.1')
        self.db=self.conn.test
        self.collection=self.db.myCollection
    
    def insertData(self,key,hashvalue):
        self.collection.insert_one({'_id':key,'hashvalue':hashvalue})

    def updateData(self,key,hashvalue):
        self.collection.update_one({'_id':key},{'$set':{'hashvalue':hashvalue}})

    def findData(self,key):
        cursor = self.collection.find_one({'_id': key})
        #return cursor.get("hashvalue")
        if cursor==None:
            return None
        else:
            return cursor.get("hashvalue")
        #print(cursor)

"""if __name__ == '__main__':
    test=manageDB()
    test.updateData('劍來','126')
    print(test.findData('劍來'))"""