#https://developers.eure.jp/tech/pairs-word2vec-svm-community-classification/

# -*- coding: utf-8 -*-

import numpy
from gensim.models.keyedvectors import KeyedVectors

def main():
    model = KeyedVectors.load_word2vec_format('./vectors.bin', binary=True, unicode_errors='ignore')

    f = open('./community.owakati', 'r')
    for line in f:
        community_words = line.rstrip().split(' ')
        community_name = ''.join(community_words)
        try:
            community_vec = text_to_vec(community_words, model)
            community_vec = normalize(community_vec)
            numpy.savetxt('./vec/' + community_name, community_vec)
        except:
            pass

def text_to_vec(words, model):
    word_vecs = []
    for word in words:
        try:
            word_vecs.append(model[word])
        except:
            pass

    if len(word_vecs) == 0:
        return None

    text_vec = numpy.zeros(word_vecs[0].shape, dtype = word_vecs[0].dtype)
    for word_vec in word_vecs:
        text_vec = text_vec + word_vec

    return text_vec

def normalize(vec):
    return vec / numpy.linalg.norm(vec)

if __name__ == '__main__':
    main()






from sklearn.cross_validation import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
 
# トレーニングデータ:テストデータ を 9:1 に分割
data_train, data_test, label_train, label_test = train_test_split(features, labels, test_size=0.1, random_state=1)
 
# トレーニングデータから分類器を作成 (Linear SVM)
estimator = LinearSVC(C=1.0)
estimator.fit(data_train, label_train)
 
# テストデータを分類器に入れる
label_predict = estimator.predict(data_test)
 
# Accuracy
print accuracy_score(label_test, label_predict)
