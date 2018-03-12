import requests
import json
from bs4 import BeautifulSoup

offlineActivityId = '1110275384'
headers = {
    'Accept': 'application/json, text/javascript',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'cy=2; cye=beijing; _lxsdk_cuid=161c5833a08c8-01effa25717221-326a7d04-13c680-161c5833a09c8; _lxsdk=161c5833a08c8-01effa25717221-326a7d04-13c680-161c5833a09c8; _hc.v=b03e110a-3a63-63bb-9cc7-b4f281bcc057.1519437168; dper=1657d6b1bc2812d25046a4911dc7c7829cb81b190ffc14aaf3d924bceccbdf9d; ll=7fd06e815b796be3df069dec7836c3df; ua=%E7%99%BD%E7%8C%AB%E5%A4%A7%E4%BE%A0yecc; ctu=ea699dee96a1f9175dbf280cc9dc03d29c3387333a91cd8cea05f785d0fa67b6; msource=default; default_ab=citylist%3AA%3A1; cityid=2; _lx_utm=utm_source%3DmShare; _lxsdk_s=161c5833a0c-8b-b5c-143%7C%7C112',
    'Host': 'm.dianping.com',
    'Origin': 'https://h5.dianping.com',
    'Referer': 'https://h5.dianping.com/app/app-community-free-meal/index.html?from=city_hot',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Mobile Safari/537.36'
}
url = 'https://m.dianping.com/mobile/dinendish/apply/' + offlineActivityId + '?a=1&source=null&utm_source=null'
r = requests.get(url, headers=headers)
html = r.text
soup = BeautifulSoup(html, 'lxml')
branchid = soup.find('select', attrs={'name': 'branchId'}).find_all('option')[1].get('value')
print(branchid)