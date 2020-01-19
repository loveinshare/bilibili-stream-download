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


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
_user = "3146464900@qq.com"
_pwd  = "kygatiugzsijdgcc"
_to   = "657688572@qq.com"

class aEmail():
    def __init__(self):
        self._user = "3146464900@qq.com"
        self._pwd  = "kygatiugzsijdgcc"
        self._to   = "657688572@qq.com"
        self.s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        self.s.login(self._user,self._pwd)
    def send(self,text,subject="auto"):
        msg = MIMEText(text)
        msg["Subject"] =subject
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
if __name__ == "__main__" :

    eml = aEmail()                
    eml.send("test")
#text = '1t'
#subject = '2t'
#a = SendEmail(text,subject)
#a.send()