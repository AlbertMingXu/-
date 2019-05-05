# !/usr/bin/python3
# -*- coding:utf-8 -*-

import io
import os
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics


PATH = '/Users/albert.ming.xu/PycharmProjects/Learning/数据分析实战45讲/test/text_classification'
stop_words = [line.strip().encode('utf-8') for line in io.open('text_classification/stop/stopword.txt')]


def get_documents_labels(path):
    """
    :param path: 文件所在路径
    :return: 目录下所有文件内容的分词列表及标签列表
    """

    documents = list()
    labels = list()

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            word_list = jieba.cut(io.open(os.path.join(dirpath, filename), 'rb').read())
            documents.append(' '.join([''.join(word) for word in word_list]))
            labels.append(os.path.basename(dirpath))

    return documents, labels


def train_fun(train_docs, train_labels, test_docs, test_labels):
    """
    构造模型并计算测试集准确率
    :param train_docs: 训练集数据
    :param train_labels: 训练集标签
    :param test_docs: 测试集数据
    :param test_labels: 测试集标签
    :return: 测试集准确率
    """

    # 计算矩阵
    tt = TfidfVectorizer(stop_words=stop_words, max_df=0.5)
    tf = tt.fit_transform(train_docs)

    # 训练模型
    clf = MultinomialNB(alpha=0.001).fit(tf, train_labels)

    # 模型预测
    test_tf = TfidfVectorizer(stop_words=stop_words, max_df=0.5, vocabulary=tt.vocabulary_)
    test_features = test_tf.fit_transform(test_documents)
    predicted_labels = clf.predict(test_features)

    return metrics.accuracy_score(test_labels, predicted_labels)


if __name__ == '__main__':
    train_documents, train_labels = get_documents_labels(os.path.join(PATH, 'train'))
    test_documents, test_labels = get_documents_labels(os.path.join(PATH, 'test'))
    ratio = train_fun(train_documents, train_labels, test_documents, test_labels)
    print(ratio)
