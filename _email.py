# -*- coding: utf-8 -*-
"""
data = pd.read_csv('JM1809.csv',index_col =0)
data.index = pd.DatetimeIndex(data.index)
"""
#from dateutil import parser
import re,os,time,random,datetime,traceback


#import tensorflow as 
#from WindPy import w
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
import time 
import json

import os

emial_status = 0

if not os.path.exists("_email_config.json"):
    print("把email_config.json改名为_email_config.json并填写相关信息\n退出")
    raise "erro"

conf = json.load(open("_email_config.json"))
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
_user = conf["_user"]
_pwd  = conf["_pwd"]
_to   = conf["_to"]
_subject = conf["_subject"]

class aEmail():
    def __init__(self,_user,_pwd,_to,_subject):
        self._user = _user
        self._pwd  = _pwd
        self._to   = _to
        self._subject = _subject
        
    def send(self,text):
        try_num = 0
        while try_num <20:
            try:
                try_num +=1
                self.s = smtplib.SMTP_SSL("smtp.qq.com", 465)
                self.s.login(self._user,self._pwd)
                msg = MIMEText(text)
                msg["Subject"] =self._subject
                msg['From'] = _format_addr('智障助手 <%s>' %self._user)
                msg['To'] = _format_addr('管理员 <%s>' % self._to)
                for i in range(20):
                    try:
                        self.s.sendmail(self._user, self._to, msg.as_string())
                        # s.quit()
                        #print("Email Sent")
                        break
                    except :
                        try:
                            self.s = smtplib.SMTP_SSL("smtp.qq.com", 465)
                            self.s.login(self._user,self._pwd)
                            #print("重新登陆成功")
                        except:
                            traceback.print_exc()
                            print("email登陆失败")
                            traceback.print_exc()
                            print ("%s times Falied,retrying......" %i)
                            time.sleep(2)
                return
            except Exception as e :
                print(e)
                time.sleep(5)
if _user == "":
    email_Sender = None
    email_status = 0 
else:
    email_Sender = aEmail(_user,_pwd,_to,_subject)
    email_status = 1
if __name__ == "__main__" :

    pass
#text = '1t'
#subject = '2t'
#a = SendEmail(text,subject)
#a.send()