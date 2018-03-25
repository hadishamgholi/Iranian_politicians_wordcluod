# coding=utf-8
from bs4 import BeautifulSoup as BS
import requests
import re

year = 1387

sokhanrani = 'بیانات'
file_counter = 1


def normalizing(s):
    s = re.sub(r"\([۱۲۳۴۵۶۷۸۹]+\)", "", s)
    s = re.sub(r"[۰۱۲۳۴۵۶۷۸۹]+\..+", "", s)
    return s


def get_content_of_year():
    global file_counter
    url = "http://farsi.khamenei.ir/speech?nt=2&year=" + str(year)
    html = requests.get(url)
    soup = BS(html.text, 'html.parser')
    content = soup.find_all('div', class_="Content")
    h2s = content[0].find_all('h2')
    links = []
    for h in h2s:
        if sokhanrani in h.a.text:
            links.append(h.a['href'])

    for link in links:
        url = "http://farsi.khamenei.ir/" + link
        html = requests.get(url)
        soup = BS(html.text, 'html.parser')
        content = soup.find('div', class_='Content')
        try:
            if len(content.div.text) >= 150:
                content = content.div
            elif len(content.p.text) >= 150:
                content = content.p

            if len(content.text) < 150:
                continue

            content = normalizing(content.get_text())
            file_name = str(year) + '_' + str(file_counter)
            with open('imam_khamenei_data/' + file_name, 'w') as f:
                f.write(content)
                f.close()
                print("file {name} created".format(name=file_name))

            file_counter += 1
        except:
            print("Error 1")


for i in range(1):
    year -= 1
    get_content_of_year()
    file_counter = 1

print(year)
