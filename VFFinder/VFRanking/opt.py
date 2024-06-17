


########CVE extraction opt key##########

from CVEEntityExtraction.main import CoT
from CVEEntityExtraction.main import TF_IDF
from CVEEntityExtraction.main import percentage
from CVEEntityExtraction.main import min_words

########CVE extraction opt##########

########API extraction opt##########

from APIEntityExtraction.main import APIName, APIClz, APIVar, APIParaName, APIParaType, APIString, APIInline

########All opt##########

CVE_extraction_opt = "CVE_extraction_opt"
API_extraction_opt = "API_extraction_opt"
ranking_opt = "ranking_opt"
running_opt = {
    CVE_extraction_opt:{},
    API_extraction_opt:{},
    ranking_opt:{},
}

#########All opt##########


def get_opt_dependent(ranking_dict:dict):
    '''
    Get the running opt from other component
    :param ranking_dict:
    :return:
    '''
    from CVEEntityExtraction.main import CVE_entity_extraction_dict
    from APIEntityExtraction.main import extraction_opt_dict
    running_opt[CVE_extraction_opt] = CVE_entity_extraction_dict
    running_opt[API_extraction_opt] = extraction_opt_dict
    running_opt[ranking_opt] = ranking_dict
    return running_opt


def get_opt_independent(ranking_dict:dict):
    '''
    Get the running opt independently
    :param ranking_dict:
    :return:
    '''
    CoT = "CoT"
    TF_IDF = "TF_IDF"
    percentage = "percentage"
    min_words = "min_words"
    embed_mode = "embed_mode"

    CVE_entity_extraction_dict = {
        CoT: "RCAV_TMP",
        embed_mode: "treesequence",
    }

    API_extraction_opt_dict = {
        APIName: True,
        APIClz: True,
        APIVar: True,
        APIParaName: False,
        APIParaType: False,
        APIString: True,
        APIInline: True
    }

    running_opt[CVE_extraction_opt] = CVE_entity_extraction_dict
    running_opt[API_extraction_opt] = API_extraction_opt_dict
    running_opt[ranking_opt] = ranking_dict
    return running_opt