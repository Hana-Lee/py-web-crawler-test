# -*- coding: utf-8 -*-
import urllib
import urllib2
import MySQLdb
import requests
from bs4 import BeautifulSoup

db = MySQLdb.connect('localhost', 'temp', 'temp', 'temp')
cursor = db.cursor()

url = 'https://www.kata.or.kr/search/02_search.asp'
source_code = requests.get(url)
plain_text = source_code.text
soup = BeautifulSoup(plain_text, 'lxml')
for td in soup.findAll('td', attrs={'width': '201'}):
    memberId = int(td.find('a')['href'].replace('javascript:content_go(', '').replace(')', ''))
    print(memberId)
    cursor.execute('INSERT INTO temp.member (`mem_id`) VALUES (%s)', (memberId,))
    db.commit()

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/50.0.2661.94 Safari/537.36'

gotopage = 2
block = 0
while gotopage < 109:
    try:
        values = {'gotopage': gotopage, 'block': block}
        source_code = requests.post(url, data=values)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')

        for td in soup.findAll('td', attrs={'width': '201'}):
            memberId = int(td.find('a')['href'].replace('javascript:content_go(', '').replace(')', ''))
            print('member id : %d' % memberId)
            cursor.execute('INSERT INTO temp.member (`mem_id`) VALUES (%s)', (memberId,))
            db.commit()

        gotopage += 1

        if (gotopage - 1) % 10 == 0:
            block += 1

        print('gotopage : %d' % gotopage)

    except urllib2.HTTPError, e:
        print e.reason
    except urllib2.URLError, e:
        print e.reason
