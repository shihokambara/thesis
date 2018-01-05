# -*- coding: utf-8 -*-
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import re
import nltk
import seaborn as sns

from gensim.models import word2vec

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

#model = word2vec.Word2Vec(corpus, size=100, window=20, min_count=200, workers=4)

sns.set(style="darkgrid")
sns.palplot(sns.color_palette("Set2", 10))



def tsne_plot(model, word, filename):
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []
    counts = []

    # プロットする単語を選択
    sim_words = similar_words([word])
    if sim_words:
        for similar_word in sim_words:
            tokens.append(model[similar_word])
            labels.append(similar_word)
            counts.append(model.wv.vocab[similar_word].count)
    
        tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
        new_values = tsne_model.fit_transform(tokens)
    
        x = []
        y = []
        for value in new_values:
            x.append(value[0])
            y.append(value[1])
    
        plt.figure(figsize=(16, 16))
    
        for i in range(len(x)):
            plt.scatter(x[i],y[i], s=3*(counts[i]), alpha=0.7)
            plt.annotate(labels[i],
                         xy=(x[i], y[i]),
                         xytext=(5, 2),
                         textcoords='offset points',
                         ha='right',
                         va='bottom')
        plt.title('similar words of '+ word + ' in ' + filename, fontsize=35)
        plt.show()
        plt.savefig('./images/co_words/'+ filename+ '/' + word + '_in_' + filename)
    
def similar_words(posi, nega=[], n=30):
    # similar_words([word])
    # 学習済みモデルからcos距離が最も近い単語n個(topn個)を表示する
    results = []

    try:
        results = model.most_similar(positive = posi, topn = n)
    except KeyError as e:
        print(posi)
        print(e)

    words = []
    for result in results:
        # r[0] 単語
        # r[1] 類似度
        words.append(result[0])
    return words 


font = {'sans-serif': 'Times New Roman',
        'weight': '300',
        'size': '22' 
        }
plt.rc('font', **font)

bible_words = ['die','sin','spirit','fear','poor','answer','god','christ','hell','lord','speak','soul','enemy','judah','beauty','reign','angel','man','law', 'devil', 'evil', 'jacob','paul','solomon', 'moses','adam','cain','noah', 'woman', 'king','luke', 'young','david','joseph','egypt', 'daughter', 'exodus','ezekiel','earth','heart','jesus','joshua','fire','job','judge','know','priest','servant','water']
quaran_owrds = ['destiny']

co_words = ['lie','punishment','dog','woman','moses','man','people','water','lord','son','daughter','kill','god','grace','promise','grow','joseph','truth','israel','heart','enjoy','law','work','poor','female','blood','believe','fire','create','worship','kind','angel','mercy','give','prophet','strength','enemy','adam','faith','word','child','wrong','love','war','priest','art','wearth','think','truth','time','success','wish','death','body','drink','ear','destroy','spoil','spirit','desire','eye','mouth','face','hand']
extra = ['calling' ]
filenames = [ 'bhagvadgita','bible','quaran']
for word in co_words:
    for filename in filenames:
        model = word2vec.Word2Vec.load(filename + ".model")
        try:
            tsne_plot(model, word, filename)
        except KeyError as e:
            print(word)
            print(e)
