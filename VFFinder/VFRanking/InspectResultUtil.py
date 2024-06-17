
import os
import pickle
from CommonUtils.textUtils import get_groundTruth
from VFRanking.metric import get_topk_precision
from CommonUtils.FileUtils import get_CVE_description
from APIEntityExtraction.APIEntity import APIEntity
from CommonUtils.FileUtils import get_CVE_GAV_mapping
from VFRanking.utils import get_CVE_entity_dict, get_GAV_API_dict
# from VFRanking.rankC import rank_API_beta
import matplotlib.pyplot as plt
import json


def print_case_entity_detail(api_entity:APIEntity):
    print(f"API name: {api_entity.get_name()}")
    print(f"API all clean entity: {api_entity.get_cleaned_entity()}")
    print(f"API code entity: {api_entity.get_code_entity()}")
    print(f"API class entity: {api_entity.get_clz_entity()}")
    print(f"API name entity: {api_entity.get_name_entity()}")


def inspect_cases_GT(CVE_API_ranking_dict_dir:str, CVE_API_GT_dir:str, CVE_entity_dir:str, CVE_description_dir:str, CVE_ID:str, case_list):
    GT_dict = get_groundTruth(CVE_API_GT_dir)
    CVE_entity_dict = get_CVE_entity_dict(CVE_entity_dir)
    CVE_description_dict = get_CVE_description(CVE_description_dir)
    with open(os.path.join(CVE_API_ranking_dict_dir, CVE_ID), "rb") as f:
        CVE_API_ranking_list = pickle.load(f)

    GT = GT_dict[CVE_ID]
    CVE_API_name_list = [i.get_name_signature() for i in CVE_API_ranking_list]
    try:
        GT_index = CVE_API_name_list.index(GT)
    except ValueError:
        print(f"GT index of {CVE_ID} is not found")
        return


    print("CVE ID:" + CVE_ID)
    print("CVE description:" + CVE_description_dict[CVE_ID])
    print("CVE entity:" + ",".join(CVE_entity_dict[CVE_ID]))
    print("=============================")
    print("GT index:" + str(GT_index) + " GT score:" + str(CVE_API_ranking_list[GT_index][1]))
    print_case_entity_detail(CVE_API_ranking_list[GT_index][0])

    for case in case_list:
        print("=============================")
        print("Case" + str(case) + "(score:" + str(CVE_API_ranking_list[case][1]) + "):")
        print_case_entity_detail(CVE_API_ranking_list[case][0])


def get_GT_index(CVE_API_ranking_dict_dir, CVE_API_GT_dir):
    """
    :param GT_dict:
    :param CVE_API_list:
    :param k:
    :return:
    """
    GT_dict = get_groundTruth(CVE_API_GT_dir)
    all_CVE_ranking = os.listdir(CVE_API_ranking_dict_dir)
    gt_index_list = []
    gt_index_dict = {}
    for CVE in all_CVE_ranking:
        with open(os.path.join(CVE_API_ranking_dict_dir, CVE), "rb") as f:
            CVE_API_ranking_list = pickle.load(f)
            CVE_API_name_list = [i[0].get_name_signature() for i in CVE_API_ranking_list]
            GT = GT_dict[CVE]
            try:
                gt_index = CVE_API_name_list.index(GT)
                gt_index_list.append(gt_index)
                gt_index_dict[CVE] = gt_index
            except ValueError:
                print(f"GT index of {CVE} is not found")
                continue
            with open("//data/alan/VFranklst/" + CVE, "wb") as f:
                pickle.dump(CVE_API_name_list, f)
            if CVE_API_ranking_list[gt_index][1]:
                print(f"GT index of {CVE} is {gt_index} score:{CVE_API_ranking_list[gt_index][1].item()}")
            else:
                print(f"GT index of {CVE} is {gt_index} score:{CVE_API_ranking_list[gt_index][1]}")
    # plt.hist(gt_index_list, bins=range(min(gt_index_list), max(gt_index_list) + 2), align='left', color='g', alpha=0.7)
    # plt.xlabel('Value')
    # plt.ylabel('Frequency')
    # plt.title('Frequency Distribution Histogram')
    # plt.show()
    return gt_index_dict


def get_all_topk_precision(CVE_API_ranking_dict, CVE_API_GT_dir, k):
    """
    :param GT_dict:
    :param CVE_API_list:
    :param k:
    :return:
    """
    GT_dict = get_groundTruth(CVE_API_GT_dir)
    GT_list = []
    CVE_API_list = []
    for CVE, CVE_API_ranking_list in CVE_API_ranking_dict.items():
        GT = GT_dict[CVE]
        jar_API_list = [i[0].get_name_signature() for i in CVE_API_ranking_list]
        if GT not in jar_API_list:
            continue
        else:
            GT_list.append(GT_dict[CVE])
            CVE_API_list.append(jar_API_list)

    precision =  get_topk_precision(GT_list, CVE_API_list, k)
    return precision


def get_top_precision(CVE_API_ranking_dict_dir, CVE_API_GT_dir):
    """
    :param GT_list:
    :param ranked_list:
    :param k:
    :return:
    """
    all_CVE_ranking = os.listdir(CVE_API_ranking_dict_dir)
    GT_dict = get_groundTruth(CVE_API_GT_dir)
    GT_list = []
    CVE_API_list = []
    for CVE in all_CVE_ranking:
        with open(os.path.join(CVE_API_ranking_dict_dir, CVE), "rb") as f:
            CVE_API_ranking_list = pickle.load(f)
            GT_mtd = GT_dict[CVE]
            jar_API_list = [i[0].get_name_signature() for i in CVE_API_ranking_list]
            with open("./rankedAPIName/" + CVE, "wb") as f:
                pickle.dump(jar_API_list, f)
            if GT_mtd not in jar_API_list:
                continue
            else:
                GT_list.append(GT_dict[CVE])
                CVE_API_list.append(jar_API_list)

    for k in [1, 2, 3, 4, 5, 10, 30, 50, 100]:
        print(f"Top-{k} precision: {get_topk_precision(GT_list, CVE_API_list, k)}")

    # k_list = []
    # for k in range(100):
    #     k_list.append(get_topk_precision(GT_list, CVE_API_list, k))
    # with open("../RQanalysis/RQ4/whole", "wb") as f:
    #     pickle.dump(k_list, f)
    print("MRR:", cal_MRR(GT_list, CVE_API_list))


def cal_MRR(GT_list, CVE_API_list):
    def mrr_score(target, predictions):
        """
        target : target value
        predictions : list - sorted predictions
        """
        try:
            return 1 / (predictions.index(target) + 1)
        except ValueError:
            return 0

    mrr_list = []
    for index, GT in enumerate(GT_list):
        mrr_list.append(mrr_score(GT, CVE_API_list[index]))
    return sum(mrr_list) / len(mrr_list)


def inspect_cases_GT_json(CVE_API_ranking_dict_dir:str, CVE_API_GT_dir:str, CVE_entity_dir:str, CVE_description_dir:str, CVE_ID:str, case_list:list, json_file_path:str):
    GT_dict = get_groundTruth(CVE_API_GT_dir)
    CVE_entity_dict = get_CVE_entity_dict(CVE_entity_dir)
    CVE_description_dict = get_CVE_description(CVE_description_dir)
    with open(os.path.join(CVE_API_ranking_dict_dir, CVE_ID), "rb") as f:
        CVE_API_ranking_list = pickle.load(f)

    # with open(os.path.join(CVE_API_func_ranking_dict_dir, CVE_ID), "rb") as f:
    #     CVE_API_func_ranking_list = pickle.load(f)

    GT = GT_dict[CVE_ID]
    CVE_API_name_list = [i[0].get_name_signature() for i in CVE_API_ranking_list]
    # CVE_API_name_list_func = [i[0].get_name_signature() for i in CVE_API_func_ranking_list]
    try:
        # GT_index = CVE_API_name_list_func.index(GT)
        element_GT_index = CVE_API_name_list.index(GT)
    except ValueError:
        print(f"GT index of {CVE_ID} is not found")
        return

    output = {}
    output["CVE ID"] = CVE_ID
    output["CVE description"] = CVE_description_dict[CVE_ID]
    output["CVE entity"] = ",".join(CVE_entity_dict[CVE_ID].get_all_entity())
    output["CVE AV"] = CVE_entity_dict[CVE_ID].AV
    output["CVE IM"] = CVE_entity_dict[CVE_ID].IM
    output["CVE RC"] = CVE_entity_dict[CVE_ID].RC
    output["CVE clz"] = CVE_entity_dict[CVE_ID].get_clz_name()
    output["GT element index"] = element_GT_index
    output["GT score"] = CVE_API_ranking_list[element_GT_index][1].item()
    # output["GT functionality"] = CVE_API_func_ranking_list[GT_index][0].get_functionality()
    output["GT case entity detail"] = get_case_entity_detail(CVE_API_ranking_list[element_GT_index][0])
    output["cases"] = []

    for case in case_list:
        if case > len(CVE_API_name_list):
            continue
        case_detail = {}
        case_detail["Case"] = case
        try:
            case_detail["score"] = CVE_API_ranking_list[case][1].item()
        except AttributeError:
            case_detail["score"] = CVE_API_ranking_list[case][1]
        # case_detail["case functionality"] = CVE_API_func_ranking_list[case][0].get_functionality()
        case_detail["case entity detail"] = get_case_entity_detail(CVE_API_ranking_list[case][0])

        output["cases"].append(case_detail)

    json_output = json.dumps(output, indent=4)
    with open(json_file_path, "w") as f:
        f.write(json_output)


def get_case_entity_detail(api_entity:APIEntity):
    case_detail = {}
    case_detail["API name"] = api_entity.get_name()
    case_detail["API all clean entity"] = api_entity.get_cleaned_entity()
    case_detail["API code entity"] = api_entity.get_code_entity()
    case_detail["API class entity"] = api_entity.get_clz_entity()
    case_detail["API name entity"] = api_entity.get_name_entity()
    case_detail["API code"] = api_entity.get_src_code().split("\n")
    case_detail["API description"] = api_entity.get_description().split("\n")
    return case_detail