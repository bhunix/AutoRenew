import xml.etree.cElementTree as ET
import requests
import json
s=requests.session()
url='http://www.szlib.org.cn/MyLibrary/readerLoginM.jsp'
login_header={
    'Host': 'www.szlib.org.cn',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.szlib.org.cn/MyLibrary/Reader-Access.jsp',
    'Connection': 'keep-alive',
    #'Content-Type': 'application/x-www-form-urlencoded',
    #'X-Requested-With': 'XMLHttpRequest'
}

login_data={
    'username':'lopht',
    'password':'36e1a5072c78359066ed7715f5ff3da8'
}

r=s.post(url, data=login_data, headers=login_header)
tree = ET.fromstring(r.text)
login_ret = tree.find('message')
print("login: " + login_ret.text);
#print(r.headers)
#if "OK" in r.text:
#  print("login: %s", r.text)
#else:
#    print("login failed!")

render_header={
    'Host': 'www.szlib.org.cn',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.szlib.org.cn/MyLibrary/Loan-Status.jsp',
    'Connection': 'keep-alive',
    #'Content-Type': 'application/x-www-form-urlencoded',
    #'X-Requested-With': 'XMLHttpRequest'
}
#render_url="http://www.szlib.org.cn/MyLibrary/response.jsp?v_select=04400510945835&v_select=04400511505781&v_select=04400510609364&v_select=04400510945835&v_select=04400511505781&v_select=04400510609364&v_select=04400510945835&v_select=04400511505781&v_select=04400510609364&"

get_booklist_url='http://www.szlib.org.cn/MyLibrary/getloanlist.jsp?readerno=461966'
r=s.get(get_booklist_url)
f=open ("booklist.xml", 'w')
f.write(r.text)
f.close()
#print(r.headers)
#print(r.text)

barcode = []
select = []
tree = ET.fromstring(r.text)
meta = tree.iter(tag='meta')
for item in meta:
  renew = item.find('renew')
  #print(renew.text)
  if renew.text == '0':
    barcode.append(item.find('barcode').text)
    #print(item.find('title').text)

for item in barcode:
  select.append("v_select:"+item)

rend_data = json.dumps(select)
#print(json.dumps(select))
print(rend_data)

rend_url="http://www.szlib.org.cn/MyLibrary/response.jsp"
#rend_data={
#        'v_select':'04400611190075',
#        'v_select':'04400510737871',
#        'v_select':'F4401001308328',
#        'v_select':'04400810233132'
#}
#r=s.post(rend_url, data=rend_data)
#print(r.text)
