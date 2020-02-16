from _email import email_Sender ,email_status
import requests
import time,datetime
from urllib import request
import urllib
import socket
socket.setdefaulttimeout(5.0) 
import threading
import streamlink
import re
import sys

import traceback
from api import is_live,get_stream_url

def record(url, file_name,headers):
    if not url:
        return
    res = None
    output_file = None
    retry_num = 0
    r = urllib.request.Request(url,headers=headers)
    print(url)
    while retry_num <10 :
        try :
            res = urllib.request.urlopen(r)
            break
        except Exception as e:
            print(retry_num,"=============================")
            print(e)
            print("=============================")
            retry_num +=1
            time.sleep(2)
    if not res:
        return        
    try:
        with open(file_name, 'wb') as f:    
            print('starting download from:\n%s\nto:\n%s' % (url, file_name))
            size = 0
            _buffer = res.read(1024 *256)
            n = 0
            while n<50 :
                if len(_buffer) == 0:
                    n+=1
                    time.sleep(0.2)
                else:
                    n = 0
                    #print(len(_buffer))
                    f.write(_buffer)
                    size += len(_buffer)
                    print('{:<4.2f} MB downloaded'.format(size/1024/1024),datetime.datetime.now(),end="\r")
                    #sys.stdout.flush()
                    _buffer = res.read(1024 * 32)
    except Exception as e:
        print("=============================")
        print(e)
        print("=============================")
    finally:
        print("finnally")
        if res:
            res.close()
            print("res.close()")
        

        if os.path.isfile(file_name) and os.path.getsize(file_name) == 0:
            os.remove(file_name)
            print("os.remove(file_name)")

import json ,os
if os.path.exists("_config.json") == None:
    print("将config.json改名为 _config.json 并填写相关配置内容")
    raise "erro"
conf = json.load(open("_config.json"))
_id = conf["_id"]
_name = conf["_name"]
_path = conf["_path"]

if not  os.path.exists(_path):
    raise "path not exists" 

while 1 :
    try:
        live_status = is_live(_id)
    except Exception as e:
        print(e)
        continue

    if live_status == False:
        
        print("[%s]未开播"%_id,datetime.datetime.now(),end = "\r")
        time.sleep(5)
        pass
    else:                   
        now = datetime.datetime.now()
        real_url,headers = get_stream_url(_id)
        if real_url == None:
            print("开播了但是没有源")
            now  = datetime.datetime.now()
            # if email_status ==1:               
            #     email_Sender.send("开播了但是没有源")
            
            continue

        filename =_path+ _name +now.strftime("_%Y_%m_%d_%H_%M_%S_%f_"+"_.flv")
        if email_status == 1:
            email_Sender.send("开播了")   
        record(real_url,filename,headers)