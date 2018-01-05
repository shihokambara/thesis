# -*- coding: utf-8 -*-

import logging
import os
import pickle
import gensim
import nltk
from gensim import corpora
import re
import string

number_pattern=r'([+-]?[0-9]+\.?[0-9]*)'


# lemmatize text
#from nltk import word_tokenize, pos_tag
#from nltk.stem import WordNetLemmatizer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
TOPIC_NUM = 30

stop_words = ['thing','thee', 'that', 'it','thou','thy','which', 'thee','thou', 'shalt', 'hast', 'thereof', 'i', 'o', 'thereof', 'once','where', 'twice','third', 'fourth','fifth','sixth','seventh','eighth','nine','four','five','six','seven','eight','nine','ten','eleven','twelve', 'twenty','not','more','here','first','second','fifty','forty','one','let','thus','also','have', 'therefore','such','ever', 'surely','then','certainly','many','other','others','yet','there','too','only','who','else','much','certain','indeed','now','nothing','best','everything','despise','better','worse','hath','unto','take','say','make','come','number','him','his','her','see','know','give','take','chapter','I','IV','even']
noun_tags = ['NN', 'NNPS','NNS','NNP','NNPS']
verb_tags =  ['VBP', 'VS', 'VB','VBD','VBG','VBN','VBP','VBZ']
acceptable_tags = ['RB','RBR','RBS', 'JJ','JJR','JJS', 'VBP', 'VS', 'VB','VBD','VBG','VBN','VBP','VBZ','NN', 'NNPS','NNS','NNP','NNPS']
 

# 見出し語化
lemmatizer = nltk.WordNetLemmatizer()



def _sentence2bow(line):
    bag = []
    print(line)
    line = line.split('\t')[-1] # 章の始まりとかを削除
    print(line)
    sentence = []
    tokens = nltk.word_tokenize(line)
    tagged = nltk.pos_tag(tokens)
    for tag in tagged:
      if tag[1] in acceptable_tags:
        word = tag[0]
        word = word.replace(',','')  #句読点を除く
        word = word.replace('.','')  #句読点を除く
        word = word.replace('!','')  #句読点を除く
        word = word.replace(':','')  #句読点を除く
        word = word.replace(';','')  #句読点を除く
        word = word.replace('´','')
        word = word.replace('`','')

        word = re.sub(number_pattern, "", word)
        word = word.lower() # 小文字
    
        if tag[1] in verb_tags: #動詞なら
            word = lemmatizer.lemmatize(word, 'v') # 見出し語化
        elif tag[1] in noun_tags and (tag[1] not in ['NNPS', 'NNP']): #名詞かつ固有名詞でないなら
            word = lemmatizer.lemmatize(word) # 見出し語化
    
        if word not in stop_words:
          if len(word) > 2:
            bag.append(word)

    return bag 
    
f = open('bible.txt')
data = f.read()  # ファイル終端まで全て読んだデータを返す
f.close()
lines = data.split('\n') 
word_count = 0
line_count = 0
new_file = open('raw_bible.txt', 'w')
texts = []
acceptable_words = []

for line in lines:
    acceptable_words = _sentence2bow(line)
    word_count += len(acceptable_words)
    texts.append(acceptable_words)
    #　アウトプットファイルに1センテンスぶん書き込む。
    flat_sentence = ' '.join(acceptable_words)
    print(flat_sentence)
    print(flat_sentence, file=new_file)
    line_count +=1

new_file.close()

# 単語数と行の数
print('-----------------------------')
print('line:', line_count)
print('word:', word_count)
print('-----------------------------')


# dictionary: 最初に用意した大きな文章データから各単語の出現回数を計算しておいたもの
dictionary = gensim.corpora.Dictionary(texts)
dictionary.filter_extremes(no_below=1, no_above=0.6, keep_n=None)

# バイナリで保存
dictionary.save('../dicts/bible.dict')

#dictionary.token2id
# コーパス ＝ *.mmファイル(Matrix Marketファイル)
# dictionaryを元にして、解析したい文章を変換したもの。コーパスを見れば、解析したい文章にどの単語が何回出現するのかが分かります。

corpus =  [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('../corpus/bible.mm', corpus)
