# -*- coding: utf-8 -*-

# make csv of raw text

import logging
import os
import pickle
import gensim
import nltk
from gensim import corpora
import re
import string

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
TOPIC_NUM = 30


filenames = ['quaran', 'bible']
for filename in filenames:

    f = open('raw_'+filename+'.txt')
    data = f.read()  # ファイル終端まで全て読んだデータを返す
    lines = data.split('\n') 

    new_file = open('raw_'+filename+'.csv', 'w')
    for line in lines:
        line = line.replace(' ',',')  #空白を句読点に
        print(line, file=new_file)

    new_file.close()





