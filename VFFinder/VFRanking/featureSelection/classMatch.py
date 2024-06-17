
from CVEEntityExtraction.CVEEntity import CVEEntity
from CommonUtils.FileUtils import filepath2filename


def clz_match(CVE_entity:CVEEntity, API_entity_list:list):
    '''
    match clz name in API_entity_list with clz name in CVE_entity
    :param API_entity_list:
    :param CVE_entity:
    :return:
    '''
    matched_api = []
    no_matched_api = []
    CVE_clz_name_list = CVE_entity.get_clz_name()
    for API_entity in API_entity_list:
        api_clz_name = filepath2filename(API_entity.get_clz_name())
        if api_clz_name in CVE_clz_name_list:
            matched_api.append(API_entity)
        else:
            no_matched_api.append(API_entity)

    return matched_api, no_matched_api