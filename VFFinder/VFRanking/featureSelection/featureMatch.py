

from CVEEntityExtraction.CVEEntity import CVEEntity
from VFRanking.featureSelection.classMatch import clz_match
from VFRanking.featureSelection.vulnerablityMatch.vulnerablityFeatureMatch import vul_feature_match_by_CWE


def feature_match(CVE_entity:CVEEntity, API_entity_list:list, CWE_keywords_dict:dict, rank_opt:dict):
    '''

    :param CVE_entity:
    :param API_entity_list:
    :return:
    '''
    if rank_opt["Class_feature"]:
        clz_matched, clz_not_matched = clz_match(CVE_entity, API_entity_list)
    else:
        clz_matched = []
        clz_not_matched = API_entity_list
    if rank_opt["CWE_feature"]:
        vul_feature_matched, vul_feature_not_matched = vul_feature_match_by_CWE(CVE_entity, clz_not_matched, CWE_keywords_dict)
    else:
        vul_feature_matched = []
        vul_feature_not_matched = clz_not_matched
    return clz_matched, vul_feature_matched, vul_feature_not_matched
    # return clz_matched, clz_not_matched, []