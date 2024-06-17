


def vul_feature_match_by_CWE(CVE_entity, API_entity_list, CWE_keywords_dict:dict):
    '''
    match the API list with the keywords of CWE
    :param CVE_keywords_dict: dict
    :param API_list: list
    :return: list, list
    '''
    matched = []
    not_matched = []
    CWE_ID = CVE_entity.get_CWE_ID()
    if CWE_ID not in CWE_keywords_dict:
        return matched, API_entity_list
    keywords = [i[0] for i in CWE_keywords_dict[CWE_ID][:3]]
    for api_entity in API_entity_list:
        if set(api_entity.get_cleaned_entity()).intersection(keywords):
            matched.append(api_entity)
        else:
            not_matched.append(api_entity)
    return matched, not_matched