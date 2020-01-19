from _email import *
from req import *
import requests
import time,datetime
from urllib import request
import urllib
def record( record_url, output_filename):
    try:
        print( '√ 正在录制...')
        headers = dict()
        headers['Accept-Encoding'] = 'identity'
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'
        headers['Referer'] = re.findall(r'(https://.*\/).*\.flv', record_url)[0]
        resp = requests.get(record_url, stream=True, headers=headers)
        with open(output_filename, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024):
                f.write(chunk) if chunk else None
    except Exception as e:
        import traceback
        traceback.print_exc()
        #print( 'Error while recording:' + str(e))
        time.sleep(10)
def record2(url, file_name):
    if not url:
        return

    res = None
    output_file = None

    try:
        headers = dict()
        headers['Accept-Encoding'] = 'identity'
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'
        headers['Referer'] = re.findall(r'(https://.*\/).*\.flv', url)[0]
        #res = requests.get(url, stream=True, headers=headers)
        #res = request.urlopen(url, timeout=100000,headers=headers)
        r = urllib.request.Request(url,headers=headers)
        res = urllib.request.urlopen(r)
        output_file = open(file_name, 'wb')
        print('starting download from:\n%s\nto:\n%s' % (url, file_name))

        size = 0
        _buffer = res.read(1024 * 256)
        while _buffer:
            output_file.write(_buffer)
            size += len(_buffer)
            print('{:<4.2f} MB downloaded'.format(size/1024/1024),end="\r")
            #sys.stdout.flush()
            _buffer = res.read(1024 * 256)
    finally:
        print("finnally")
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
#rid = 660

alive = False
while True:
    try:
        live_status, room_id = get_real_rid(rid)
    except:
        print ("bug:",datetime.datetime.now())
        time.sleep(10)
    if alive == False:
        if live_status == 0:
            print("未开播",end = "\r")
        else:
            alive = True
            print("开播",datetime.datetime.now())
            eml = aEmail()                
            eml.send("开播了")
            real_url = get_real_url(rid)
            print(real_url)
            now = datetime.datetime.now()
            filename ="videos/"+ "kushui"+now.strftime("_%Y_%m_%d_%H_%M_%S_%f_")+".flv"
            record2(real_url,filename)
            
    elif alive == True:
        if live_status == 0:
            print("下播",datetime.datetime.now())
            eml = aEmail()                
            eml.send("下播了")
            alive = False
        else:
            alive = True
            print("直播中",end = "\r")
            
    time.sleep(10)
    
