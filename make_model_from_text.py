from gensim.models import word2vec
import pandas as pd

#data = word2vec.Text8Corpus('raw_bible.txt')
#model = word2vec.Word2Vec(data, size=100, window = 5, min_count=5 , workers=2)
## 保存する
#model.save('bible.model')
#
# Word2Vecのインスタンス作成
# sentences : 対象となる分かち書きされているテキスト
# size      : 出力するベクトルの次元数
# min_count : この数値よりも登場回数が少ない単語は無視する
# window    : 一つの単語に対してこの数値分だけ前後をチェックする
filenames = [ 'bhagvadgita','bible','quaran']
for filename in filenames:
    data = word2vec.Text8Corpus('raw_'+filename+'.txt')
    model = word2vec.Word2Vec(data, size=100, window = 5, min_count=10 , workers=2) #学習に使う前後の単語数
# 保存する
    model.save(filename+'.model')

# A more selective model
#model = word2vec.Word2Vec(corpus, size=100, window=20, min_count=500, workers=4)
#tsne_plot(model)
