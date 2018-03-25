# coding=utf-8
from bs4 import BeautifulSoup as BS
import requests
import re

book = 1
sokhanrani = "سخنرانی"
file_couter = 1


def get_main_url():
    global book
    return "http://emam.com/posts/index/sahifeh/" + str(book)


def remove_a_tag(s):
    p = re.sub(r"«[0-9]»", "", s)
    return p


def get_data_from_book():
    global file_couter
    global book
    try:
        # crawl each sahifeh
        html = requests.get(get_main_url())
        soup = BS(html.text, 'html.parser')
        book_index = soup.find(id='bookIndex')
        _a = book_index.find_all('a')
        links = []
        for a in _a:
            if sokhanrani in a.text:
                links.append(a['href'])

        # crawl sokhanrani


        for link in links:
            try:
                url = "http://emam.com" + link
                html = requests.get(url)

                soup = BS(html.text, 'html.parser')
                body = soup.find(id='body')
                text = body.find_all('p')
                with open("imam_khomeini_data/" + str(book) + "_" + str(file_couter), 'w') as f:
                    for p in text:
                        f.write(remove_a_tag(p.get_text('\n').encode('utf8')))
                    f.close()

                file_couter += 1
            except:
                print("Error 1")
    except:
        print("Error 2")


for i in range(21):
    get_data_from_book()
    book += 1
    print("book " + str(book) + " finished")
