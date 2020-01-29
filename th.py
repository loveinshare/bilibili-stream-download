import threading
from _email import *
import streamlink
import requests
import time,datetime
from urllib import request
import urllib

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
        output_file = open(file_name, 'wb')
        print('starting download from:\n%s\nto:\n%s' % (url, file_name))

        size = 0
        _buffer = res.read(1024 * 256)
        while len(_buffer) != 0 :
            output_file.write(_buffer)
            size += len(_buffer)
            print('{:<4.2f} MB downloaded'.format(size/1024/1024),end="\r")
            #sys.stdout.flush()
            _buffer = res.read(1024 * 256)
    finally:
        print("finnally")
        eml = aEmail()                
        eml.send("finish"+file_name)
        if res:
            res.close()
            print("res.close()")
        if output_file:
            output_file.close()
            print("output_file.close()")

        if os.path.isfile(file_name) and os.path.getsize(file_name) == 0:
            os.remove(file_name)
            print("os.remove(file_name)")



rid = 281

streams = streamlink.streams("https://live.bilibili.com/"+str(rid))
l = ['source_alt', 'source_alt2', 'source']

for i in l:
    print(streams[i].url)
    t = threading.Thread(target = record,args=(streams[i].url,i+".flv"))
    t.setDaemon(True)
    t.start()
    
    
import time
while 1:
    time.sleep(20)
print("finished")
