import base64
import requests
import rsa
import binascii
import re
import json
import time
import random
'''用rsa对明文密码进行加密，加密规则通过阅读js代码得知'''
class WeiBoLogIn():
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.encode_su()
        self.session = requests.session()#建立一个连续访问
        self.loginurl = 'https://login.sina.com.cn/signup/signin.php'
        self.session.get(self.loginurl)#目标登录地址
    #加密su
    def encode_su(self):
        self.su = base64.b64encode(self.username.encode('utf-8'))

    def pre_log(self):
        #访问一波拿到各种东西
        url = 'https://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su={uname}&rsakt=mod&client=ssologin.js(v1.4.15)&_={tstamp}'.format(uname = self.username,tstamp = time.time() * 1000)

        try:
            res = self.session.get(url).text
            res = re.findall("{.*}",res)[0]###
            self.res = json.loads(res)
            #print(self.res)
            self.nonce = self.res["nonce"]
            self.pubkey = self.res["pubkey"]
            self.rsakv = self.res["rsakv"]
            self.servertime = self.res["servertime"]

            #self.nonce = 
        except:
            print('failed')

    def get_sp(self):
        publickey = rsa.PublicKey(int(self.pubkey,16),int('10001',16))
        keycode = str(self.servertime) + '\t' + str(self.nonce) + '\n' + str(self.password)
        self.sp = rsa.encrypt(keycode.encode(), publickey)
        self.spcode = binascii.b2a_hex(self.sp)
        print(self.spcode)

    def login(self):
        self.pre_log()
        self.get_sp()
        data = {
            'entry': 'sso',
            'gateway': '1',
            'from': 'null',
            'savestate': '30',
            'useticket': '0',
            'pagerefer': 'https://login.sina.com.cn/sso/login.php?client=ssologin.js',
            'vsnf': '1',
            'su': self.su,
            'service': 'sso',
            'servertime': self.servertime,
            'nonce': self.nonce,
            'pwencode': 'rsa2',
            'rsakv': self.rsakv,
            'sp': self.spcode, 
            'sr': '1500*1000',#分辨率吧应该是，r是resolution
            'encoding': 'UTF-8',
            'cdult': '3',
            'domain': 'sina.com.cn',
            'prelt': random.randint(1,100),
            'returntype': 'TEXT'
        }

        url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js'
        j_content = self.session.post(url,data=data).json()
        print(j_content)
        # time.sleep(10)
        # j_content = self.session.post(url,data=data).json()
        # print(j_content)


weibo = WeiBoLogIn('****不给看***','*****真的不给看哦***')
#weibo.pre_log()
weibo.login()
