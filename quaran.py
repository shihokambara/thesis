# -*- coding: utf-8 -*-

# 単語だけ取り出す。

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

stop_words = ['thing','thee', 'that', 'it','thou','thy','which', 'thee','thou', 'shalt', 'hast', 'thereof', 'i', 'o', 'thereof', 'once','where', 'twice','third', 'fourth','fifth','sixth','seventh','eighth','nine','four','five','six','seven','eight','nine','ten','eleven','twelve', 'twenty','not','more','here','first','second','fifty','forty','one','let','thus','also','have', 'therefore','such','ever', 'surely','then','certainly','many','other','others','yet','there','too','only','who','else','much','certain','indeed','now','nothing','best','everything','despise','better','worse','hath','unto','take','say','make','come','number','him','his','her','see','know','give','take','chapter','I','IV','even']
#NNP: 固有名詞

noun_tags = ['NN', 'NNPS','NNS','NNP','NNPS']
verb_tags =  ['VBP', 'VS', 'VB','VBD','VBG','VBN','VBP','VBZ']

acceptable_tags = ['RB','RBR','RBS', 'JJ','JJR','JJS', 'VBP', 'VS', 'VB','VBD','VBG','VBN','VBP','VBZ','NN', 'NNPS','NNS','NNP','NNPS']
 
def _sentence2bow(line):
  """
  文を形態素解析してBagOfWordsに変換
  @param sentence: text
    自然言語の文
  @return bag: list
    語形変化が修正された単語のリスト
  """
  bag = []
  #print('line', line)
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

f = open('quaran.txt')
data = f.read()  # ファイル終端まで全て読んだデータを返す
f.close()

lines = data.split('\n') 
line_count = 0
word_count = 0



# 見出し語化
lemmatizer = nltk.WordNetLemmatizer()

number_pattern=r'([+-]?[0-9]+\.?[0-9]*)'

texts = []

new_file = open('raw_quaran.txt', 'w')

for line in lines:
    acceptable_words = _sentence2bow(line)
    texts.append(acceptable_words)
    word_count += len(acceptable_words)
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
dictionary.filter_extremes(no_below=10, no_above=0.4, keep_n=None)
# no_berow: 使われてる文章がno_berow個以下の単語無視
# no_above: 使われてる文章の割合がno_above以上の場合無視

# バイナリで保存
dictionary.save('quaran.dict')
# バイナリではなくテキストとして保存する
dictionary.save_as_text('quaran_readable.dict')

# 読むとき
# dictionary = corpora.Dictionary.load_from_text('livedoordic.txt')


#dictionary.token2id

# コーパス ＝ *.mmファイル(Matrix Marketファイル)
# dictionaryを元にして、解析したい文章を変換したもの。コーパスを見れば、解析したい文章にどの単語が何回出現するのかが分かります。

corpus =  [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('quaran.mm', corpus)

