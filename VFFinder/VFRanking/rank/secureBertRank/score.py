

from torch.nn.functional import cosine_similarity


def score_threshold_securebert(tgt_word_bag, tgt_word_weight, cddt_word_bag, model, threashold, **kwargs)->float:
    '''
    :param API_entity_list:
    :param CVE_entity:
    :return:
    '''
    if "bert_embed_dict" not in kwargs:
        exit(-1)

    if "tokenizer" not in kwargs:
        exit(-1)

    bert_embed_dict = kwargs["bert_embed_dict"]
    tokenizer = kwargs["tokenizer"]

    total_similarity = 0
    for word1 in tgt_word_bag:
        max_similarity_for_word = -1
        for word2 in cddt_word_bag:
            vec1 = get_bert_embedding(word1, bert_embed_dict, model, tokenizer)
            vec2 = get_bert_embedding(word2, bert_embed_dict, model, tokenizer)
            similarity = 1 + cosine_similarity(vec1, vec2)
            if similarity > max_similarity_for_word:
                max_similarity_for_word = similarity
        if max_similarity_for_word > threashold:
            total_similarity += max_similarity_for_word
    return total_similarity


def get_bert_embedding(word, bert_dict_obj, model, tokenizer):
    if word in bert_dict_obj.get_dict():
        return bert_dict_obj.get_dict()[word]
    else:
        tokens = tokenizer(word, return_tensors='pt')
        outputs = model(**tokens)
        embedding = outputs.last_hidden_state[:, 0, :]
        bert_dict_obj.bert_dict[word] = embedding
        return embedding