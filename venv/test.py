import requests
from config import *
import json
from random import choice
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import time

headers = [
    {
        'Host': 'www.dianping.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.dianping.com/beijing/ch10/r1465',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': 'navCtgScroll=0; showNav=#nav-tab|0|1; _lxsdk_cuid=161ad130f75c8-099dd9fd58f3c6-32687a04-1fa400-161ad130f76c8; _lxsdk=161ad130f75c8-099dd9fd58f3c6-32687a04-1fa400-161ad130f76c8; _hc.v=015b9cac-41f5-50c9-5b9f-5485f7ac38f0.1519027163; cye=beijing; s_ViewType=10; _dp.ac.v=66165a86-31be-4f3b-a52c-5f6f4be762d8; ua=%E7%99%BD%E7%8C%AB%E5%A4%A7%E4%BE%A0yecc; ctu=ea699dee96a1f9175dbf280cc9dc03d2019db2f32c6c52c19b366f24102e115d; aburl=1; cityid=2; default_ab=citylist%3AA%3A1%7Cshop%3AA%3A1; _lx_utm=utm_source%3Dnull; ctu=e8eab73b92acdb0e3bace69f8b77856bb8ad97a8468543a402bbeadb1cafeb664d2c7baf5fcf521c4da515557d020127; cy=2; _lxsdk_s=161cb5fd264-df2-fe7-d93%7C%7C124'
    },
    {
        'Host': 'www.dianping.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6',
        'Cookie': '_lxsdk_s=161cb6ee454-26b-e83-9c6%7C%7C9; s_ViewType=10; _lx_utm=utm_source%3Dnull; cy=2; cye=beijing; aburl=1; __mta=209106477.1500817881357.1500817881357.1500817883193.2; _lxsdk=15d6fb774eec8-0c4d49418019ee-1d401925-1fa400-15d6fb774efc8; _lxsdk_cuid=15d6fb774eec8-0c4d49418019ee-1d401925-1fa400-15d6fb774efc8; __utma=1.1059343304.1415356861.1415356861.1469973034.2; _hc.v="\"d3cb850a-6efd-43dd-b71e-f737fe7b1adb.1415356780\""',
        'Upgrade-Insecure-Requests': '1'
    }
]

regions = ['r16','r15','r17','r328','r14','r20','r9158','r27615','r5950','r5952','r9157','r5951','r27614','r27616','c434','c435']

area = []

f = open('proxy_txt.txt')
proxying = f.read()
f.close()

proxy = proxying
print(proxy)

def get_index_url(area):
    url = BASE_URL + area
    print(url)
    return url

def get_html(url):
    global proxy
    try:
        proxies = {
            'http': 'http://' + proxy
        }
        r = requests.get(url, headers=choice(headers), allow_redirects=False, proxies=proxies, timeout=10)
        if r.status_code == 200:
            if not proxying == proxy:
                write_to_txt(proxy)
            return r.text
        if r.status_code != 200:
            print(r.status_code)
            proxy = get_proxy()
            print('proxy设置为:', proxy)
            return get_html(url)
    except RequestException as e:
        print('爬虫被识别', e)
        proxy = get_proxy()
        print('proxy设置为:', proxy)
        return get_html(url)

def get_proxy():
    time.sleep(4)
    r = requests.get(PROXY_URL)
    if r.status_code == 200 and r.text:
        json_ip = json.loads(r.text)
        port = str(json_ip['data'][0]['port'])
        return json_ip['data'][0]['ip']+ ':' +port
    else:
        print('PROXY_URL is bad',r.status_code)

def write_to_txt(proxy):
    fw = open('proxy_txt.txt', 'w')
    fw.write(proxy)
    fw.close()

def parse_region(html):
    soup = BeautifulSoup(html, 'lxml')
    if soup.find('div', id='region-nav-sub'):
        Regions = soup.find('div', id='region-nav-sub').find_all('a')
        for Region in Regions:
            area.append(Region.get('href').split('/')[-1])

def main():
    global area
    for region in regions:
        html = get_html(get_index_url(region))
        parse_region(html)
    area = list(set(area))
    print(area)

if __name__ == '__main__':
    main()
