
import time

from VFRanking.rank.util import cosine_similarity


def score_threshold_bert(tgt_word_bag, tgt_word_weight, cddt_word_bag, model, threashold, **kwargs)->float:
    '''
    :param API_entity_list:
    :param CVE_entity:
    :return:
    '''
    if "bert_embed_dict" in kwargs:
        bert_embed_dict = kwargs["bert_embed_dict"]
    total_similarity = 0
    for word1 in tgt_word_bag:
        max_similarity_for_word = -1
        for word2 in cddt_word_bag:
            vec1 = get_bert_embedding(word1, bert_embed_dict, model)
            vec2 = get_bert_embedding(word2, bert_embed_dict, model)
            similarity = cosine_similarity(vec1, vec2)
            if similarity > max_similarity_for_word:
                max_similarity_for_word = similarity
        if max_similarity_for_word > threashold:
            total_similarity += max_similarity_for_word * tgt_word_weight[word1]
    return total_similarity


def get_bert_embedding(word, bert_dict_obj, model):
    if word in bert_dict_obj.get_dict():
        return bert_dict_obj.get_dict()[word]
    else:
        vec = model.encode(word)
        bert_dict_obj.bert_dict[word] = vec
        return vec

