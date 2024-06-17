


import sys
sys.path.append("../CVEEntityExtraction/")
from VFRanking.InspectResultUtil import get_GT_index
from VFRanking.InspectResultUtil import get_top_precision
from VFRanking.InspectResultUtil import inspect_cases_GT_json
from VFRanking.opt import get_opt_dependent, get_opt_independent, CVE_extraction_opt, API_extraction_opt, ranking_opt
from VFRanking.utils import get_CVE_entity_dir, get_API_entity_dir, get_ranking_result_dir
from CommonUtils.FileUtils import construct_opt_dir, recreate_directory

CVE_description_dir = '../resource/CVE_description_mess'
bad_CVE_JSON_base_dir = '../result/CVEGTresult'
CVE_GAV_mapping_dir = '../resource/CVE_jar'
CVE_entity_base_dir = '../resource/CVEEntity/CVEEntity'
API_entity_base_dir = '../resource/APIEntity/APIEntity'
CVE_API_ranking_dict_dir_base = '../result/CVEAPIRankingDict'
CWE_keywords = '../resource/CWE_keywords_count.pk'
CVE_API_GT_dir = "../resource/CVE_API"

model_name_opt = "model_name"
threshold_opt = "threshold"
CWE_feature = "CWE_feature"
Class_feature = "Class_feature"
TF_IDF = "TF_IDF"

ranking_opt_dict = {
    model_name_opt: "llama",
    threshold_opt: 1.4,
    CWE_feature: False,
    Class_feature: True,
    TF_IDF:True
}


if __name__ == "__main__":
    running_opt_dict = get_opt_independent(ranking_opt_dict)
    CVE_entity_dir = get_CVE_entity_dir(CVE_entity_base_dir, running_opt_dict[CVE_extraction_opt])
    API_entity_dir = get_API_entity_dir(API_entity_base_dir, running_opt_dict[API_extraction_opt])
    #CVE_API_ranking_dict_dir = get_ranking_result_dir(CVE_API_ranking_dict_dir_base, running_opt_dict)
    CVE_API_ranking_dict_dir = "//data/alan/VFlocation/result/whole_tf_1_2/CVEAPIRankingDict_RCAV_TMP_treesequence_1_1_1_0_0_1_1_llama_1.4_0_1_1"
    # CVE_API_ranking_dict_dir = "//data/alan/VFlocation/result/whole_tf_1_2/CVEAPIRankingDict_RCAV_TMP_treesequence_1_1_1_0_0_1_1_llama_1.4_0_1_1"
    bad_CVE_JSON_dir = bad_CVE_JSON_base_dir + construct_opt_dir("", running_opt_dict[CVE_extraction_opt]) + construct_opt_dir("", running_opt_dict[API_extraction_opt]) + construct_opt_dir("", running_opt_dict[ranking_opt])
    recreate_directory(bad_CVE_JSON_dir)


    gt_index_dict = get_GT_index(CVE_API_ranking_dict_dir, CVE_API_GT_dir)
    get_top_precision(CVE_API_ranking_dict_dir, CVE_API_GT_dir)

    bad_CVE = [CVE for CVE, index in gt_index_dict.items() if index <=2]
    for CVE_ID in bad_CVE:
        inspect_cases_GT_json(CVE_API_ranking_dict_dir, CVE_API_GT_dir, CVE_entity_dir, CVE_description_dir, CVE_ID, [1, 2, 3, 5, 10, 20, 50], bad_CVE_JSON_dir + "/" + CVE_ID + ".json")

