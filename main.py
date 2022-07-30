#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import datetime
from calendar import isleap

from bs4 import BeautifulSoup
from icalendar import Calendar, Event, vCalAddress, vText
import requests


class BirthDay:
    def __init__(self, name, date):
        self.name = name
        self.date = date


url = 'https://wikiwiki.jp/kirara/%E8%AA%95%E7%94%9F%E6%97%A5'

r = requests.get(url)
html = r.content

soup = BeautifulSoup(html, 'lxml')

today = datetime.date.today()

birthdays = []


def fetch_birthdays(n):
    h_scrollable = soup.select('.h-scrollable')[n]
    for i, tr in enumerate(
            h_scrollable.select(f'table > tbody > tr')):
        for j, td in enumerate(tr.select('td')):
            # iはヘッダの部分で余分にループが回るので+1されている
            month = 6*n + j+1
            date = i

            # 今年が閏年でない場合2/29は飛ばす
            if not isleap(today.year) and month == 2 and date == 29:
                continue

            # その他不正な日付は飛ばす
            try:
                date = datetime.date(today.year, month, date)
            except ValueError:
                continue

            names = td.get_text(separator='\t').split('\t')
            # ※で始まるものは除く
            names = [name for name in names if not name.startswith("※")]

            # スペースの場合やブランクは飛ばす
            if names[0] == '\u3000\u3000\u3000\u3000\u3000' or names[0] == '':
                continue
            print(date)
            print(names)
            for name in names:
                birthdays.append(BirthDay(name, date))


fetch_birthdays(0)
fetch_birthdays(1)

cal = Calendar()
cal.add('prodid', '-//kaki_xxx//kirara_cal//ja')
cal.add('version', '1.0')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'REQUEST')
cal.add('x-wr-calname', 'きらら誕生日カレンダー')

for birthday in birthdays:
    event = Event()
    event.add('summary', birthday.name)
    event.add('dtstart', birthday.date)
    event.add('dtend', birthday.date)
    event.add('description', birthday.name + "の誕生日")
    cal.add_component(event)

with open('test.ics', 'wb') as f:
    f.write(cal.to_ical())
