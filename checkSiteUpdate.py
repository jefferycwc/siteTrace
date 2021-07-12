import os
import sys
import requests
import time
import re
import signal
import hashlib
from bs4 import BeautifulSoup
import pandas as pd
from params import id_list,name_dict,url_dict
from manageDataBase import manageDB

path='/Users/jeffery/Desktop/practice/'


def getLastModifiedTime(url):
    ses=requests.Session()
    res=ses.get(url)
    return res.headers['Last-Modified']

def notifyLine():
    headers = {
        "Authorization": "Bearer " + "hOPLFU4uOXqlTDLQf99mQ1WQDpzt9XFqMOvDNcQdhc5",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {"message": "小說已更新"}
    res=requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)
    print(res.status_code)

def evaluateHashValue(timestamp):
    h1=hashlib.md5()
    h1.update(str(timestamp).encode(encoding='utf-8'))
    #print(h1.hexdigest())
    return h1.hexdigest()

def start():
    while(1):
        for id in id_list:
            print(name_dict[id])
            #timestamp=getTimeStamp()
            #print(timestamp)
            dbobject=manageDB()
            hashvalue=dbobject.findData(name_dict[id])
            if hashvalue==None:
                print("insert data to mongoDB")
                timestamp=getLastModifiedTime(url_dict[id])
                hashvalue=evaluateHashValue(timestamp)
                dbobject.insertData(name_dict[id],hashvalue)
            else:
                #ses=requests.Session()
                #res=ses.get(url)
                timestamp=getLastModifiedTime(url_dict[id])
                new_hashvalue=evaluateHashValue(timestamp)
                if(new_hashvalue!=hashvalue):
                    print('modified')
                    notifyLine()
                    dbobject.updateData(name_dict[id],new_hashvalue)
                else:
                    print('not modified')

def kill_process():
    sys.exit(1)

if __name__ == '__main__':
    try:
        start()
        #notify()
        #evaluateHashValue()
    except KeyboardInterrupt:
        kill_process()