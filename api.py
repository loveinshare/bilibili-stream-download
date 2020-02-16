import urllib
import json
import re
import time
uid = "9999"
live_api = "https://api.live.bilibili.com/room/v1/Room/room_init?id=%s"%uid
stream_api = "https://api.live.bilibili.com/room/v1/Room/playUrl?cid=%s&quality=4&platform=web"%uid
def my_request(url):
    headers = dict()
    headers['Accept-Encoding'] = 'identity'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'
    
    req = urllib.request.Request(url,headers=headers)
    res = urllib.request.urlopen(req)
    content = res.read()
    return json.loads(content.decode())

def is_live(uid):
    live_api = "https://api.live.bilibili.com/room/v1/Room/room_init?id=%s"%str(uid)
    rtn = my_request(live_api)
    live_status = rtn["data"]["live_status"]
    #print(rtn)
    if live_status == 0:
        return False
    elif live_status == 1:
        return True


def get_stream_url(uid):
    stream_api = "https://api.live.bilibili.com/room/v1/Room/playUrl?cid=%s&quality=4&platform=web"%uid
    
    rtn = my_request(stream_api)
    urls = rtn.get("data").get("durl")
    #print(urls)
    retry_time= 0
    if urls:
        while 1:
            for i in urls:
                for referer in [True,False]:
                    try :
                        if retry_time >20:
                            return None ,None
                        retry_time+=1
                        url = i.get("url")
                        headers = dict()
                        headers['Accept-Encoding'] = 'identity'
                        # headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'
                        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 " 
                        if referer == True:
                            headers['Referer'] = re.findall(r'(https://.*\/).*\.flv', url)[0]
                        req = urllib.request.Request(url,headers=headers)
                        res = urllib.request.urlopen(req)
                        
                        return i.get("url"),headers

                    except Exception as e :
                        time.sleep(1)
                        print("retry",retry_time,"]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")
                        print(url)
                        print(e)
                        retry_time+=1
                        pass
            
        
