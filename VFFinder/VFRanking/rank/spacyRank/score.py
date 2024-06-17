
from VFRanking.rank.util import calculate_edit_distance_sum
import time

def score_threshold_spacy(tgt_word_bag, cddt_word_bag, nlp, threashold, **kwargs):
    '''
    :param API_entity_list:
    :param CVE_entity:
    :return:
    '''

    similarity_sum = 0
    st_time = time.time()
    for target_word in tgt_word_bag:
        max_similarity_for_word = 0
        if not nlp.vocab.has_vector(target_word):
            similarity_sum += calculate_edit_distance_sum(cddt_word_bag, target_word, 1)
        else:
            syn1 = nlp(target_word)
            for candidate_word in cddt_word_bag:
                # 获取两个词的最相似的义原
                syn2 = nlp(candidate_word)
                similarity = syn1.similarity(syn2)
                if similarity is not None and similarity > max_similarity_for_word:
                    max_similarity_for_word = similarity
            if max_similarity_for_word > threashold:
                similarity_sum += max_similarity_for_word
    ed_time = time.time()
    print("used time:", (ed_time - st_time) / (len(tgt_word_bag) * len(cddt_word_bag)))
    return similarity_sum