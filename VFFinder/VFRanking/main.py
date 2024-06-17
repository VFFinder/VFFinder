
import copy
import os.path
import sys
sys.path.append("../CVEEntityExtraction/")
sys.path.append("../")
from tqdm import tqdm
import pickle

from CommonUtils.FileUtils import get_CVE_GAV_mapping, recreate_directory
from CommonUtils.textUtils import get_groundTruth
from VFRanking.rank.rank import rank_API_by_model_threashold
from VFRanking.utils import get_CVE_entity_dict, get_GAV_API_dict, get_API_entity_dir, get_CVE_entity_dir, get_ranking_result_dir
from VFRanking.opt import get_opt_independent, CVE_extraction_opt, API_extraction_opt, ranking_opt


CVE_GAV_mapping_dir = '../resource/CVE_jar'
CVE_entity_base_dir = '../resource/CVEEntity/CVEEntity'
API_entity_base_dir = '../resource/APIEntity/APIEntity'
CVE_API_ranking_dict_dir_base = '../result/CVEAPIRankingDict'
CWE_keywords = '../resource/CWE_keywords_count.pk'
CVE_API_GT_dir = "../resource/CVE_API"

############Option for Ranking################
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


############Option for Ranking################
def main():
    CVE_GAV_mapping = get_CVE_GAV_mapping(CVE_GAV_mapping_dir)
    running_opt_dict = get_opt_independent(ranking_opt_dict)


    for running_opt_dict in [running_opt_dict]:
        API_entity_dir = get_API_entity_dir(API_entity_base_dir, running_opt_dict[API_extraction_opt])
        CVE_entity_dir = get_CVE_entity_dir(CVE_entity_base_dir, running_opt_dict[CVE_extraction_opt])

        CVE_entity_dict = get_CVE_entity_dict(CVE_entity_dir)
        jar_API_entity_dict = get_GAV_API_dict(API_entity_dir)
        GT_dict = get_groundTruth(CVE_API_GT_dir)
        with open(CWE_keywords, "rb") as f:
            CWE_keywords_dict = pickle.load(f)
        model_name = running_opt_dict[ranking_opt][model_name_opt]
        threashold = running_opt_dict[ranking_opt][threshold_opt]

        print("Start ranking..." + model_name + " " + str(threashold))
        CVE_API_ranking_dict_dir = get_ranking_result_dir(CVE_API_ranking_dict_dir_base, running_opt_dict)
        recreate_directory(CVE_API_ranking_dict_dir)

        all_cve_entity_list = [" ".join(i.get_all_entity()) for i in CVE_entity_dict.values()]

        for CVE_ID, CVE_eneity_bag in tqdm(CVE_entity_dict.items()):
            if CVE_ID not in CVE_GAV_mapping or CVE_GAV_mapping[CVE_ID] not in jar_API_entity_dict or CVE_ID in os.listdir(CVE_API_ranking_dict_dir):
                continue
            GAV = CVE_GAV_mapping[CVE_ID]
            CVE_API_name_list = [i.get_name_signature() for i in jar_API_entity_dict[GAV]]
            GT = GT_dict[CVE_ID]
            if GT not in CVE_API_name_list:
                continue
            ranked_API_list = rank_API_by_model_threashold(CVE_eneity_bag, jar_API_entity_dict[GAV], all_cve_entity_list, CWE_keywords_dict, model_name, threashold, running_opt_dict["ranking_opt"])
            with open(os.path.join(CVE_API_ranking_dict_dir, CVE_ID), "wb") as f:
                pickle.dump(ranked_API_list, f)


if __name__ == "__main__":
    main()