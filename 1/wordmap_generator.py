import re
import os
import time
import numpy as np
from wordcloud import WordCloud
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from PIL import Image


def load_data(name: str, limit_file_num: int):
    global stopwords
    if name != 'khomeini' and name != 'khamenei':
        raise Exception('name should be "khamenei" or "khomeini"')

    current_dir = os.getcwd()
    _words = []
    folder_name = current_dir + '/imam_' + name + '_data'
    files = os.listdir(folder_name)
    for i, file in enumerate(files):
        if i < limit_file_num:
            file_path = os.path.join(folder_name, file)
            with open(file_path, 'r', encoding='utf-8') as fin:
                _words = _words + re.findall(r"\w[\w']+", fin.read())
                fin.close()
        else:
            break
    _words = remove_stopwords(_words, stopwords)
    big_text = get_display(reshape(' '.join(_words)))
    return big_text


def remove_stopwords(words: list, stopwords: list):
    for stop in stopwords:
        if stop in words:
            words = list(filter(lambda a: a != stop, words))
    return words


def load_persian_stopwords():
    stopwords = []
    with open('persian-stopwords.txt', 'r', encoding='utf-8') as fin:
        for line in fin:
            stopwords.append(line[:-1])
        fin.close()

    return stopwords[2:]


t1 = time.time()

khomeini_mask = np.array(Image.open(os.path.join(os.getcwd(), "khomeini_mask.png")))
khamenei_mask = np.array(Image.open(os.path.join(os.getcwd(), "khamenei_mask.png")))
stopwords = load_persian_stopwords()
khomeini_words = load_data('khomeini', 1000)
khamenei_words = load_data('khamenei', 580)

khomeini_wordcloud = WordCloud(
    width=400,
    height=400,
    background_color='white',
    max_words=1000,
    max_font_size=100,
    stopwords=set(stopwords),
    random_state=42,
    mask=khomeini_mask,
    font_path=os.getcwd() + '/BNazanin.ttf'
).generate(khomeini_words)
khomeini_wordcloud.to_file('khomeini_wordmap.png')

khamenei_wordcloud = WordCloud(
    width=400,
    height=400,
    background_color='white',
    max_words=1000,
    max_font_size=100,
    stopwords=set(stopwords),
    random_state=42,
    mask=khamenei_mask,
    font_path=os.getcwd() + '/BNazanin.ttf'
).generate(khamenei_words)
khamenei_wordcloud.to_file('khamenei_wordmap.png')

# khamenei_dict = khamenei_wordcloud.words
# khomeini_dict = khomeini_wordcloud.words


print(time.time() - t1)
