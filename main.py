from _email import email_Sender ,email_status
from req import *
import requests
import time,datetime
from urllib import request
import urllib
import socket
socket.setdefaulttimeout(5.0) 
import threading
import streamlink

import sys

import traceback
from api import is_live,get_stream_url

def record(url, file_name):
    if not url:
        return

    res = None
    output_file = None

    try:
        headers = dict()
        headers['Accept-Encoding'] = 'identity'
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'
        #headers['Referer'] = re.findall(r'(https://.*\/).*\.flv', url)[0]
        #res = requests.get(url, stream=True, headers=headers)
        #res = request.urlopen(url, timeout=100000,headers=headers)
        r = urllib.request.Request(url,headers=headers)
        res = urllib.request.urlopen(r)
        with open(file_name, 'wb') as f:
        
            
            print('starting download from:\n%s\nto:\n%s' % (url, file_name))

            size = 0
            _buffer = res.read(1024 * 256)
            n = 0
            while n <10 :
                if len( _buffer) == 0:
                    n+=1
                else:
                    n = 0
                    #print(len(_buffer))
                    f.write(_buffer)
                    size += len(_buffer)
                    print('{:<4.2f} MB downloaded'.format(size/1024/1024),datetime.datetime.now(),end="\r")
                    sys.stdout.flush()
                    _buffer = res.read(1024 * 256)
    except Exception as e:
        print(e)
    
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
    
    # try:
    #     streams = streamlink.streams(_url)
    # except Exception as e:
    #     time.sleep(11)
    #     #print(e)
    #     traceback.print_exc()
    #     print("[%s]"%n)
    #     continue
    # link = streams.keys()
    # l = ['source_alt', 'source_alt2', 'source']
    # #l = ["source"]
    # n+=1
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
        if email_status == 1:
            email_Sender.send("开播了")              
        now = datetime.datetime.now()
        # real_url = None
        # for k,v in streams.items():
        #     source = k

        #     url = v.url
        #     try:
        #         headers = dict()
        #         headers['Accept-Encoding'] = 'identity'
        #         headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'
       
        #         r = urllib.request.Request(url,headers=headers)
        #         res = urllib.request.urlopen(r)
        #         if res.code == 200:
        #             real_url  = url
        #             break
        #     except Exception as e:
        #         print(e)
        #         pass
        real_url = get_stream_url(_id)
        if real_url == None:
            print("开播了但是没有源")
            now  = datetime.datetime.now()
            # if email_status ==1:               
            #     email_Sender.send("开播了但是没有源")
            
            continue

        filename =_path+ _name +now.strftime("_%Y_%m_%d_%H_%M_%S_%f_"+"_.flv")

        #print("开始下载\n"+real_url)
        record(real_url,filename)
            

        print("$$$$$$$$$$$allend")