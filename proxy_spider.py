#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-14 13:46:10
# @Author  : Awrrays
# @Link    : http://cnblogs.com/Awrrays
# @Version : 1.0


import requests
from bs4 import BeautifulSoup
import re
import sys
from requests.packages import urllib3
import time
import getopt


# 获取免费代理，每页为100个代理ip
def proxy_spider():
	headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
	}

	for i in range(int(PAGES)):
		url = 'https://www.xicidaili.com/wt/' + str(i + 1)
		html = requests.get(url, headers=headers, verify=False).text

		soup = BeautifulSoup(html, 'html.parser')
		datas = soup.find_all(name='tr', attrs={'class':re.compile('|odd')})

		for data in datas:
			soup_proxy = BeautifulSoup(str(data), 'html.parser')
			proxy = soup_proxy.find_all(name='td')
			ip = str(proxy[1].string)
			port = str(proxy[2].string)

			proxy_check(ip, port)


# 测试代理ip是否可用，可用ip会输出到文件
def proxy_check(ip, port):
	proxy = {
		'http': 'http://%s:%s' % (ip, port)
	}
	try:
		check_resp = requests.get('http://httpbin.org/get', proxies=proxy, timeout=(2, 5)).text
		proxy_pat = '"origin": "(.*?)",'
		proxy_data = re.findall(proxy_pat, check_resp)[0]

		if proxy_data == ip:
			print("[*] %s:%s is usable." % (ip, port))
			print("http://%s:%s" % (ip, port), file=open(OUTPUT_FILE, 'a'))
		else:
			print("[*] %s:%s is unavailable." % (ip, port))
	except:
		pass


if __name__ == '__main__':
	urllib3.disable_warnings()

	shortargs = '-h-o:-p:'
	longargs = ['help', 'output_file=', 'page=']
	opts, args = getopt.getopt(sys.argv[1:], shortargs, longargs)

	for key, value in opts:
		if key in ('-h', '--help'):
			print("[-] python3 proxy_spider.py -p 10 -o result.txt")
			sys.exit()
		if key in ('-o', '--output_file'):
			OUTPUT_FILE = value
		else:
			OUTPUT_FILE = time.strftime('%Y-%m-%d') + '.txt'
		if key in ('-p', '--pages'):
			PAGES = value
		else:
			PAGES = 5

	proxy_spider()