import requests
from config_bw import *
import json
from bs4 import BeautifulSoup

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
s = requests.session()
s.headers.update(headers)
ActivityId = []
end = False


def get_index_urls(page_index):
    url = 'https://m.dianping.com/activity/static/list?page=' + str(
        page_index) + '&cityid=&regionParentId=0&regionId=0&type=1&sort=0&filter=0'
    r = s.get(url)
    if r.status_code == 200:
        return r.text
    else:
        print('index页面请求失败', r.status_code)


def parse_urls(html):
    content = json.loads(html)
    PageEnd = content['data']['pageEnd']
    Activitys = content['data']['mobileActivitys']
    for Activity in Activitys:
        if Activity['applyed'] == False:
            ActivityId.append(Activity['offlineActivityId'])
            print('新上架-' + Activity['title'])
    if PageEnd == 'true':
        end = True


def get_payload(activityid):
    headers_bing = {
        'Host': 'm.dianping.com',
        'Connection': 'keep-alive',
        'Content-Length': '533',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://m.dianping.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
        'Content-Type': 'application/json;charset=UTF-8',
        'Referer': 'https://m.dianping.com/mobile/dinendish/apply/209124081?a=1&source=null&utm_source=null',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': '_lxsdk_cuid=161ad130f75c8-099dd9fd58f3c6-32687a04-1fa400-161ad130f76c8; _lxsdk=161ad130f75c8-099dd9fd58f3c6-32687a04-1fa400-161ad130f76c8; _hc.v=015b9cac-41f5-50c9-5b9f-5485f7ac38f0.1519027163; cye=beijing; s_ViewType=10; _dp.ac.v=66165a86-31be-4f3b-a52c-5f6f4be762d8; ua=%E7%99%BD%E7%8C%AB%E5%A4%A7%E4%BE%A0yecc; ctu=ea699dee96a1f9175dbf280cc9dc03d2019db2f32c6c52c19b366f24102e115d; aburl=1; dper=123dcdd604f0b2aabc11ebeae246f2500ea8444c889a8a82bdb485f58953c104; ll=7fd06e815b796be3df069dec7836c3df; cy=2; cityid=2; default_ab=citylist%3AA%3A1; _lxsdk_s=161c846d25c-d89-114-256%7C%7C57; _lx_utm=utm_source%3Dnull',
    }

    payload = {
        'offlineActivityId': activityid, 'babyBirth': None, 'email': None, 'weddingDate': None, 'haveBaby': None,
        'shippingAddress': None, 'comboId': None, 'branchId': None, 'extInfo1': '不愿意', 'extInfo2': None,
        'extInfo3': None, 'extraCount': None, 'passCardNo': None, 'env': 1, 'cx': '',
        'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
        'referer': 'https://m.dianping.com/mobile/dinendish/apply/' + str(activityid) + '?a=1&source=null&utm_source=null',
        'uuid': 0, 'source': 'null'
    }
    r = requests.post(REQUEST_BING_URL, data=json.dumps(payload), headers=headers_bing)
    branch = json.loads(r.text)
    print(r.text)
    if branch['data']['code'] == 402:
        print('----------------------------选择分店--------------------------')
        branchid = get_branchId(activityid)
        payload = {
            'offlineActivityId': activityid, 'babyBirth': None, 'email': None, 'weddingDate': None, 'haveBaby': None,
            'shippingAddress': None, 'comboId': None, 'branchId': branchid, 'extInfo1': '不愿意', 'extInfo2': None,
            'extInfo3': None, 'extraCount': None, 'passCardNo': None, 'env': 1, 'cx': '',
            'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
            'referer': 'https://m.dianping.com/mobile/dinendish/apply/' + str(
                activityid) + '?a=1&source=null&utm_source=null',
            'uuid': 0, 'source': 'null'
        }
        r = requests.post(REQUEST_BING_URL, data=json.dumps(payload), headers=headers_bing)
        print(r.text)

def get_branchId(activityid):
    url = 'https://m.dianping.com/mobile/dinendish/apply/' + str(activityid) + '?a=1&source=null&utm_source=null'
    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    branchid = soup.find('select', attrs={'name': 'branchId'}).find_all('option')[1].get('value')
    return branchid



def main():
    for i in range(1, 10):
        html = get_index_urls(i)
        parse_urls(html)
        if end:
            break
    for activityid in ActivityId:
        print(activityid)
        get_payload(activityid)


if __name__ == '__main__':
    main()
