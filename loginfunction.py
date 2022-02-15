import time
import re
from requests.api import head
from requests.sessions import session
import savestate
import requests
import sys
import hashlib
import json


# 从教务系统登陆界面获取 cookie
def login(username, password):


    request_headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.9',
        'Connection':'keep-alive',
        'Host':'jxglstu.hfut.edu.cn',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'
    }

    srvidresponse = requests.get('http://jxglstu.hfut.edu.cn/eams5-student/login',headers=request_headers)
    result = re.findall(r'SRVID=(.*);',srvidresponse.headers['Set-Cookie'])
    srvid_data = result[0]
    srvidrequest = "SRVID="+srvid_data

    # 获取 loginsalt 及对应的 Session

    request_headers2 = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.9',
        'Connection':'keep-alive',
        'Cookie':srvidrequest,
        'Host':'jxglstu.hfut.edu.cn',
        'Referer':'http://jxglstu.hfut.edu.cn/eams5-student/login',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
        'X-Requested-With':'XMLHttpRequest'
    }
    sessionresponse = requests.get('http://jxglstu.hfut.edu.cn/eams5-student/login-salt',headers=request_headers2)
    loginsalt = sessionresponse.text
    datas = re.findall(r'SESSION=(.*); Path',sessionresponse.headers['Set-Cookie'])
    session_data = datas[0]
    sessionrequest = "SESSION="+session_data
    total_cookie = sessionrequest+'; '+srvidrequest

    # Login 操作

    password_real = str(loginsalt + "-" + password)
    passwordsha = hashlib.sha1(password_real.encode('utf-8')).hexdigest()

    print(passwordsha)

    payloadData = {
        'captcha': '',
        'password': str(passwordsha),
        'username': username
    }

    request_payload = json.dumps(payloadData)
    content_length = len(request_payload)

    print(request_payload)
    print(total_cookie)

    request_headers3 = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.9',
        'Connection':'keep-alive',
        'Content-Length':str(content_length),
        'Content-Type':'application/json',
        'Cookie':total_cookie,
        'Host':'jxglstu.hfut.edu.cn',
        'Origin':'http://jxglstu.hfut.edu.cn',
        'Referer':'http://jxglstu.hfut.edu.cn/eams5-student/login',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
        'X-Requested-With':'XMLHttpRequest'
    }

    rest = requests.post('http://jxglstu.hfut.edu.cn/eams5-student/login',headers=request_headers3,data=request_payload)
    
    data_content = rest.text
    data_json = json.loads(data_content)
    print(data_json)

    if(data_json['result']==False):
        print("用户名或密码错误，请重新来过，或者需要验证码，稍后再试")
        sys.exit(0)


    cookiesdata = {'session':session_data,'srvid':srvid_data}
    #cookie_savefunction(cookiesdata)
    savestate.SaveCookieState(cookiesdata)

    return cookiesdata

