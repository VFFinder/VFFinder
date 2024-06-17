
from VFRanking.rank.util import calculate_edit_distance_sum
import time

def score_threshold_nltk(tgt_word_bag, cddt_word_bag, wordnet, threashold, **kwargs):
    '''
    :param API_entity_list:
    :param CVE_entity:
    :return:
    '''
    similarity_sum = 0
    for target_word in tgt_word_bag:
        max_similarity_for_word = 0
        syn1 = wordnet.synsets(target_word)
        if not syn1:
            similarity_sum += calculate_edit_distance_sum(cddt_word_bag, target_word, 1)
        else:
            for candidate_word in cddt_word_bag:
                # 获取两个词的最相似的义原
                syn2 = wordnet.synsets(candidate_word)
                if syn2:
                    similarity = syn1[0].path_similarity(syn2[0])
                    if similarity is not None and similarity > max_similarity_for_word:
                        max_similarity_for_word = similarity
            if max_similarity_for_word > threashold:
                similarity_sum += max_similarity_for_word
    return similarity_sum


