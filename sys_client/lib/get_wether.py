# !/user/bin/python3
# -*- coding: utf-8 -*-
# Author: Wu Yan Jun

"""
模块功能：获取用户当前所在城市、天气、温度区间
实现思路：
    思路1：查询本机IP所在城市，查询城市当前天气
    思路2：百度搜索天气，在结果中选择第一个链接，点开后即显示当前所在城市天气，抓取需要信息
    选择：果断思路2，为什么??---因为稳定，容易实现
"""

import requests
from bs4 import BeautifulSoup


def get_link():
    """
    获取百度搜索天气后的第一个链接
    """
    # 百度请求头
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'ispeed=1; ispeed_lsm=3; PSTM=1527840724; BIDUPSID=03A7565DE4B2DBFF9612B39C407CEED6; '
                  'BD_UPN=1a314353; '
                  'BAIDUID=B08FC8997B2986BDF8BA84F9A8C46ABD:FG=1; '
                  'BDSFRCVID=LFtsJeC6261HnjR7XTxvtW9ZS2KaIROTH6aoa10mTSn-vyUU1BXoEG0PDM8g0Kub_NkZogKKBeOTHn3P; '
                  'H_BDCLCKID_SF=tR-f_ILhtK_3fP36q6_2D-3Hhf_sWU5J-2Q-5KL-JDj1DRc'
                  '-jp7x2bK33NrzQ5jiKm5N2MbdJJjoHDDxhqO6hCuB2JoPJxjva2TxoUJgBCnJhhvG-lnFMpIebPRi3tQ9QgbXoMtLK-oj'
                  '-D_9ejtK3e; BD_CK_SAM=1; PSINO=2; rsv_jmp_slow=1528788183520; B64_BOT=1; BDRCVFR['
                  'S_ukKV6dOkf]=mk3SLVN4HKm; BDRCVFR[EaNsStaiD7m]=mk3SLVN4HKm; BD_HOME=0; '
                  'H_PS_PSSID=26524_1432_21084_18559_26350_26431_26577_20928; '
                  'H_PS_645EC=a894KA5NK9YkQ7SafjSwjuyQ2OMXIbquV9nGiiCQFhJ5k4zEyDgBw%2BGmMJI; '
                  'BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSVRTM=192; WWW_ST=1528791312145',
        'Host': 'www.baidu.com',
        'is_pbs': '%E5%A4%A9%E6%B0%94',
        'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E5%A4%A9%E6%B0%94&oq=%25E5'
                   '%25A4'
                   '%25A9%25E6%25B0%2594&rsv_pq=f2b51e2600048502&rsv_t'
                   '=a894KA5NK9YkQ7SafjSwjuyQ2OMXIbquV9nGiiCQFhJ5k4zEyDgBw%2BGmMJI&rqlang=cn&rsv_enter=0&rsv_sug=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.26Safari/537.36 Core/1.63.5467.400 '
                      'QQBrowser/10.1.1503.400X-Requested-With:XMLHttpRequest'

    }
    url = 'https://www.baidu.com/s?ie=utf8&oe=utf8&wd=%E5%A4%A9%E6%B0%94&tn=98012088_6_dg&ch=9'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    # 找到对应连接
    link = soup.select(r'#1 > h3 > a')[0].get('href')
    return link


# 解析连接
def get(url):
    """
    获取当天天气信息
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.26Safari/537.36 Core/1.63.5467.400 '
                      'QQBrowser/10.1.1503.400X-Requested-With:XMLHttpRequest'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    location = soup.select(r'div.crumbs.fl > a')[1].contents[0]
    weather = soup.select(r'ul.t.clearfix > li > p.wea')[0].contents[0]
    highest_temp = soup.select(r'ul.t.clearfix > li > p.tem > span')[0].contents[0]
    lowest_temp = soup.select(r'ul.t.clearfix > li > p.tem > i')[0].contents[0]
    info_list = [location, weather, highest_temp, lowest_temp]
    return info_list


def main():
    return get(get_link())


if __name__ == '__main__':
    print(main())
