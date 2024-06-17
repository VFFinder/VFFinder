
import pickle
from CommonUtils.textUtils import get_groundTruth
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from typing import List
import math
import random



def get_all_description():
    all_description = dict()
    with open("../resource/CVEDescriptionAll", "r") as f:
        for line in f.readlines():
            CVE_ID, description = line.split(":")[0], ":".join(line.split(":")[1:]).strip("\n")
            all_description[CVE_ID] = description
    return all_description


def get_caddt_description():
    caddt_description = dict()
    with open("../resource/CVE_description_mess", "r") as f:
        for line in f.readlines():
            CVE_ID, description = line.split(":")[0], ":".join(line.split(":")[1:]).strip("\n")
            caddt_description[CVE_ID] = description
    return caddt_description


def intersect_two_dict(dict1, dict2):
    '''
    Merge two dictionary
    :param dict1:
    :param dict2:
    :return:
    '''
    new_dict = dict()
    for key, value in dict1.items():
        if key in dict2:
            continue
        else:
            new_dict[key] = value
    return new_dict


def merge_two_dict(dict1, dict2):
    '''
    Merge two dictionary
    :param dict1:
    :param dict2:
    :return:
    '''
    new_dict = dict()
    for key, value in dict1.items():
        new_dict[key] = value
    for key, value in dict2.items():
        new_dict[key] = value
    return new_dict


def make_vectorizer(texts):
    vectorizer = TfidfVectorizer()
    vectorizer.fit_transform(texts)
    return vectorizer


def select_words(vectorizer, text, words, ratio=0.5, min_words=3):
    # 使用vectorizer转化输入的文本
    tfidf_matrix = vectorizer.transform([text])

    # 找到待选词在vectorizer的词汇表中的索引
    indices = [vectorizer.vocabulary_.get(word) for word in words]

    # 获取待选词的tf-idf值
    tfidf_values = tfidf_matrix[0, indices].toarray()[0]

    # 对tf-idf值进行排序，并获取排序后的索引
    sorted_indices = np.argsort(tfidf_values)[::-1]

    # 计算需要删除的词的数量
    num_words = len(words)
    num_remove = int(num_words * ratio)

    # 保证剩余的词至少有min_words个
    if num_words - num_remove < min_words:
        num_remove = num_words - min_words

    # 删除一部分词
    selected_indices = sorted_indices[:-num_remove] if num_remove > 0 else sorted_indices
    selected_words = [words[i] for i in selected_indices]

    return selected_words


def compute_tfidf(texts: list, text_id: int) -> dict:
    # 创建TfidfVectorizer对象
    tfidf = TfidfVectorizer()
    # 将输入的文本列表转化为TF-IDF矩阵
    tfidf_matrix = tfidf.fit_transform(texts)
    # 获取所有的特征名（单词）
    feature_names = tfidf.get_feature_names_out()
    # 获取输入2对应的文本的TF-IDF向量
    tfidf_vector = tfidf_matrix.toarray()[text_id]
    # 将特征名和TF-IDF值配对起来，形成一个字典
    tfidf_dict = {feature_names[i]: tfidf_vector[i] for i in range(len(feature_names))}

    return tfidf_dict


def select_top_words(tfidf_dict: dict, candidate_words: list, percentage: float = 0.9, min_words: int = 7) -> list:
    # 在TF-IDF字典中找到候选词的TF-IDF值
    candidate_tfidf = {word: tfidf_dict[word] for word in candidate_words if word in tfidf_dict}
    # 对候选词进行排序
    sorted_words = sorted(candidate_tfidf, key=candidate_tfidf.get, reverse=True)
    # 计算需要选出的词的数量
    num_words = max(int(len(sorted_words) * percentage), min_words)
    # 选出排名前80%的词，但保证数量大于3
    selected_words = sorted_words[:num_words]
    return selected_words


def remove_words(description, entity_list, extaction_opt_dict: dict):
    description_dict = get_all_description()
    caddt_descrption_dict = get_caddt_description()
    description_dict = merge_two_dict(description_dict, caddt_descrption_dict)
    texts = [i for i in description_dict.values()]
    tfidf_dict = compute_tf_idf_mannual(texts, description)
    words = select_top_words(tfidf_dict, entity_list, percentage=extaction_opt_dict["TF_IDF"]["percentage"], min_words=extaction_opt_dict["TF_IDF"]["min_words"])
    return words


def compute_tf_idf_mannual(corpus: List[str], doc: str) -> dict:
    # 将文档分割为词
    words = doc.split()
    clean_words = []
    for word in words:
        clean_words.append(word.strip(".,?!'`\"\'"))

    words = list(set(words + clean_words))
    # 计算TF
    tf = Counter(words)
    for word in tf:
        tf[word] = tf[word] / len(words)
    # 计算IDF
    idf = {}
    for word in set(words):
        idf[word] = math.log(len(corpus) / sum(word in doc for doc in corpus))
    # 计算TF-IDF
    tf_idf = {word: tf[word] * idf[word] for word in tf}
    return tf_idf


def get_entity_weight(CVE_ID, CVE_entity, all_cve_entity, API_entity_list):
    # 获取CVE的描述

    entity_weight = compute_tf_idf_mannual(all_cve_entity, " ".join(CVE_entity.get_all_entity()))
    return entity_weight


def select_top_words_mannual(tf_idf_dict, candidate_words, ratio=0.8, min_words=3):
    # 从TF-IDF字典中获取候选词的TF-IDF值，并按照从大到小的顺序排序
    candidate_scores = [(word, tf_idf_dict.get(word, 0)) for word in candidate_words]
    candidate_scores.sort(key=lambda x: x[1], reverse=True)

    # 计算需要选出的词的数量
    num_to_select = max(int(len(candidate_scores) * ratio), min_words)

    # 选出排名前num_to_select的词
    selected_words = [word for word, _ in candidate_scores[:num_to_select]]

    return selected_words