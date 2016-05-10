# -*- coding: utf-8 -*-
import MySQLdb
import requests
from bs4 import BeautifulSoup

db = MySQLdb.connect('localhost', 'temp', 'temp', 'temp')
cursor = db.cursor()

cursor.execute('SELECT mem_id FROM temp.member')
allData = cursor.fetchall()

for mem_id in allData:
    param = mem_id[0]

    url = 'https://www.kata.or.kr/search/02_search_pop.asp?i_no=%s'
    source_code = requests.get(url % param)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    count = 0
    tds = soup.find_all('td', 'padding_bbs')

    textList = []
    for i in range(1, 20, 2):
        textList.append(tds[i].text)

    # print(tuple(textList))
    # print(tds[1].text)
    # print(tds[3].text)
    # print(tds[5].text)
    # print(tds[7].text)
    # print(tds[9].text)
    # print(tds[11].text)
    # print(tds[13].text)
    # print(tds[15].text)
    # print(tds[17].text)
    # print(tds[19].text)
    #
    # print(soup.select('td[bgcolor="e7eff5"]')[0].text)

    textList.append(soup.select('td[bgcolor="e7eff5"]')[0].text)
    textList.append(param)

    tupleData = tuple(textList)
    print(tupleData)
    query = "UPDATE temp.member SET `name` = %s, `ceo` = %s, `gubun` = %s, `addr` = %s, " \
            "`tel` = %s, `fax` = %s, `period` = %s, `homepage` = %s, `email` = %s, `focus` = %s, `intro` = %s " \
            "WHERE `mem_id` = %s"

    cursor.execute(query, tupleData)
