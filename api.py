import urllib
import json
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
    if urls:
        return urls[0].get("url")
