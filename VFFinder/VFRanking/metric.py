

CVE_API_ranking_dict_dir = '../result/CVE_API_ranking_dict/'


def get_topk_precision(GT_list, ranked_api_list, k):
    """
    :param GT_list:
    :param ranked_list:
    :param k:
    :return:
    """
    count = 0
    for index, ranked_api in enumerate(ranked_api_list):
        topk_ranked_api = ranked_api[:k]
        GT = GT_list[index]
        if GT in topk_ranked_api:
            count += 1
    return count / len(ranked_api_list)

