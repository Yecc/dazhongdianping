#coding = utf-8
import requests
from config import *
from random import choice
from bs4 import BeautifulSoup
import time
import json
import pymongo
from requests.exceptions import RequestException

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]

f = open('proxy_txt.txt')
proxying = f.read()
f.close()

proxy = proxying
print(proxy)

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

def get_index_url(area, page):
    url = BASE_URL + area + page
    return url

def get_index_html(url):
    global proxy
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            r = requests.get(url, headers=choice(headers), allow_redirects=False, proxies=proxies, timeout=10)
            if r.status_code == 200:
                if not proxying == proxy:
                    write_to_txt(proxy)
                return r.text
            if r.status_code != 200:
                proxy = get_proxy()
                print('proxy设置为:', proxy)
                return get_index_html(url)
        else:
            r = requests.get(url, headers=choice(headers), allow_redirects=False)
            if r.status_code == 200:
                if not proxying == proxy:
                    write_to_txt(proxy)
                return r.text
            if r.status_code != 200:
                proxy = get_proxy()
                print('proxy设置为:', proxy)
                return get_index_html(url)
    except RequestException as e:
        print('爬虫被识别', e)
        proxy = get_proxy()
        print('proxy设置为:', proxy)
        return get_index_html(url)

def write_to_txt(proxy):
    fw = open('proxy_txt.txt', 'w')
    fw.write(proxy)
    fw.close()

def parse_index_url(html):
    end = False
    content_list = []
    soup = BeautifulSoup(html,'lxml')
    shop_list = soup.find('div', id='shop-all-list')
    shop_urls = shop_list.find_all('a', attrs={'data-click-name': 'shop_title_click'})
    shop_stars = shop_list.find_all('span', class_='sml-rank-stars')
    shop_reviewcount = shop_list.find_all('div', class_='comment')
    shop_pricetitle = shop_list.find_all('a', class_='mean-price')
    shop_score = shop_list.find_all('div', class_='txt')
    shop_address = shop_list.find_all('div', class_='tag-addr')
    page_index = soup.find('div', class_='content-wrap').find('div', class_='page')
    for i in range(len(shop_urls)):
        if shop_score[i].find('span', class_='comment-list'):
            content = {
                'Url': shop_urls[i].get('href'),
                'Name': shop_urls[i].get('title'),
                'Star': float(shop_stars[i].get('class')[1].split('r')[1])/10,
                'ReviewCount': int(shop_reviewcount[i].a.b.get_text()) if shop_reviewcount[i].a.b else None,
                'Pricetitle': float(shop_pricetitle[i].b.get_text().split('￥')[1]) if shop_pricetitle[i].b else None,
                'Taste': float(shop_score[i].find('span', class_='comment-list').span.b.get_text()) if shop_score[i].find('span', class_='comment-list').span.b else None,
                'Environment': float(shop_score[i].find('span', class_='comment-list').find_all('span')[1].b.get_text()) if shop_score[i].find('span', class_='comment-list').find_all('span')[1].b else None,
                'Services': float(shop_score[i].find('span', class_='comment-list').find_all('span')[2].b.get_text()) if shop_score[i].find('span', class_='comment-list').find_all('span')[2].b else None,
                'Style': shop_address[i].span.get_text(),
                'Trading Area': shop_address[i].find_all('span')[1].get_text(),
                'Address': shop_address[i].find_all('span')[2].get_text()
            }
            content_list.append(content)
        else:
            content = {
                'Url': shop_urls[i].get('href'),
                'Name': shop_urls[i].get('title'),
                'Star': float(shop_stars[i].get('class')[1].split('r')[1]) / 10,
                'ReviewCount': int(shop_reviewcount[i].a.b.get_text()) if shop_reviewcount[i].a.b else None,
                'Pricetitle': float(shop_pricetitle[i].b.get_text().split('￥')[1]) if shop_pricetitle[i].b else None,
                'Taste': None,
                'Environment': None,
                'Services': None,
                'Style': shop_address[i].span.get_text(),
                'Trading Area': shop_address[i].find_all('span')[1].get_text(),
                'Address': shop_address[i].find_all('span')[2].get_text()
            }
            content_list.append(content)
    if page_index:
        if page_index.find_all('a')[-1].get('class')[0] == 'cur':
            end = True
    else:
        end = True
    return content_list, end


def get_proxy():
    time.sleep(4)
    r = requests.get(PROXY_URL)
    if r.status_code == 200 and r.text:
        json_ip = json.loads(r.text)
        port = str(json_ip['data'][0]['port'])
        return json_ip['data'][0]['ip']+ ':' +port
    else:
        print('PROXY_URL is bad',r.status_code)


def save_to_mongo(data):
    for item in data:
        if db[AREA_NAME].update({'Name': item['Name']}, {'$set': item}, True):
            print('Saved to Mongo', item['Name'])
        else:
            print('Saved to Mongo Failed', len(data))

def main(area):
    for page in range(1,51):
        url = get_index_url(area, 'p' + str(page))
        html = get_index_html(url)
        data, end = parse_index_url(html)
        save_to_mongo(data)
        if end:
            print('-----------------------------------------------')
            break


if __name__ == '__main__':
    for area in AREA:
        print(area)
        main(area)
