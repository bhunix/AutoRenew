import xml.etree.cElementTree as ET
import requests
import json
import hashlib
import time
import urllib

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.already_login_flag = 0

    def __init__(self):
        user_file = open("user", "r")
        self.username = user_file.readline().strip('\n')
        self.password = user_file.readline().strip('\n')
        if len(self.username) == 0 or len(self.password) == 0:
            print("read user info failed")
        self.already_login_flag = 0
        user_file.close()

    def login (self):
        if len(self.username) == 0 or len(self.password) == 0:
            print("username or password is NULL")
            return -1
        login_url='http://www.szlib.org.cn/MyLibrary/readerLoginM.jsp'
        login_header={
            'Host': 'www.szlib.org.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.szlib.org.cn/MyLibrary/Reader-Access.jsp',
            'Connection': 'keep-alive',
        }
        self.session = requests.session()
        password_md5 = hashlib.md5(self.password.encode('utf-8')).hexdigest()
        login_data={
            'username':self.username,
            'password':password_md5
        }
        print(login_data)
        ret = self.session.post(login_url, data=login_data, headers=login_header)
        tree = ET.fromstring(ret.text)
        login_ret = tree.find('message')
        if login_ret.text == 'OK':
            print("login successful")
            self.already_login_flag = 1
            return 0
        else:
            print("login failed:"+login_ret.text)
            self.already_login_flag = 0
            return -1

    def booklist_get(self, filename=''):
        if self.already_login_flag == 0:
            print("pelease login first!")
            return ""
        else:
            booklist_url = 'http://www.szlib.org.cn/MyLibrary/getloanlist.jsp?readerno=461966'
            r = self.session.get(booklist_url)
            if filename != '':
                print("save booklist to file: " + filename)
                f = open (filename, 'w')
                f.write(r.text)
                f.close()
            else:
                print(r.text)
            return r.text

    def book_renew(self):
        booklist = self.booklist_get()
        if len(booklist) == 0:
            print("booklist is null")
        else:
            print(booklist)
            select = []
            tree = ET.fromstring(booklist)
            meta = tree.iter(tag='meta')
            for item in meta:
              renew = item.find('renew')
              if renew.text == '0':
                returndate = int(item.find('returndate').text)
                currentdate = int(time.strftime("%Y%m%d", time.localtime(time.time())))
                if abs(returndate - currentdate) < 2:
                    select.append(item.find('barcode').text)
                    #print(item.find('title').text)
                else:
                    print("query")
                    # query in next time
            url="http://www.szlib.org.cn/MyLibrary/response.jsp"
            renew_url=url+'?'+urllib.parse.urlencode({'v_select':select}, doseq=True)
            renew_header={
                'Host': 'www.szlib.org.cn',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101  Firefox/51.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': 'http://www.szlib.org.cn/MyLibrary/Loan-Status.jsp',
                'Connection': 'keep-alive',
            }
            ret = self.session.post(renew_url, headers=renew_header)
            print(ret.text)

user = User()
user.login()
user.book_renew()
