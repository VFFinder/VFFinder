

def embed_nltk(CVE_entity, API_entity):
    '''
    :param CVE_entity:
    :param API_entity:
    :return:
    '''
    from VFRanking.rankC import exact_match, fuzz_match
    similarity_sum, CVE_entity, API_entity = exact_match(CVE_entity, API_entity)
    similarity_sum += fuzz_match(CVE_entity, API_entity)
    return similarity_sum


def embed_spacy(CVE_entity, API_entity):
    '''
    :param CVE_entity:
    :param API_entity:
    :return:
    '''
    from noiseRemoval.util import remove_dup_word
    from VFRanking.rankC import exact_match, fuzz_match
    similarity_sum, CVE_entity, API_entity = exact_match(CVE_entity, API_entity)
    similarity_sum += fuzz_match(CVE_entity, API_entity)
    similarity_sum += remove_dup_word(CVE_entity)
    similarity_sum += remove_dup_word(API_entity)
    return similarity_sum


def embed_bert(CVE_entity, API_entity):
    '''
    :param CVE_entity:
    :param API_entity:
    :return:
    '''
    from VFRanking.rankC import exact_match, fuzz_match
    similarity_sum, CVE_entity, API_entity = exact_match(CVE_entity, API_entity)
    similarity_sum += fuzz_match(CVE_entity, API_entity)
    return similarity_sum