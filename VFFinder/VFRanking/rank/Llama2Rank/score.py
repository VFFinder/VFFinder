
import time
import traceback

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def score_threshold_llama(tgt_word_bag, tgt_word_weight, cddt_word_bag, model, threashold, **kwargs)->float:
    '''
    :param API_entity_list:
    :param CVE_entity:
    :return:
    '''
    if "bert_embed_dict" in kwargs:
        bert_embed_dict = kwargs["bert_embed_dict"]
    else:
        exit(-1)
    total_similarity = 0
    for word1 in tgt_word_bag:
        max_similarity_for_word = -1
        for word2 in cddt_word_bag:
            vec1 = get_llama_embedding(word1.strip(), bert_embed_dict, model)
            vec2 = get_llama_embedding(word2.strip(), bert_embed_dict, model)
            similarity = get_cos_score(vec1, vec2)
            if similarity > max_similarity_for_word:
                max_similarity_for_word = similarity
        if max_similarity_for_word > threashold:
            total_similarity += max_similarity_for_word * tgt_word_weight[word1]
    return total_similarity


def get_llama_embedding(word, bert_dict_obj, model):
    if word in bert_dict_obj:
        return bert_dict_obj.get_dict()[word]
    else:
        vec = model.encode({'text': word}, to_numpy=True)
        bert_dict_obj.bert_dict[word] = vec
        return vec


def get_cos_score(vec1, vec2):
    vec1 = np.reshape(vec1, (1, -1))
    vec2 = np.reshape(vec2, (1, -1))
    return 1 + cosine_similarity(vec1, vec2)
