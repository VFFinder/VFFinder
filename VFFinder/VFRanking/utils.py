
import os.path
import os
import pickle
from CommonUtils.codeUtils import get_para_type_list
from CommonUtils.FileUtils import construct_opt_dir
from VFRanking.opt import CVE_extraction_opt, API_extraction_opt, ranking_opt


BERT_PATH = "//data/alan/BERT/multi-qa-mpnet-base-dot-v1/"
BERT_DICT_PATH = "//data/alan/VFlocation/VFRanking/rank/bertRank/bert_dict"
SecureBERT_PATH = "//data/alan/BERT/SecureBERT"
SecureBERT_TOKENIZER_PATH = "//data/alan/BERT/tokenizer/SecureBERTTokenizer"
SecureBERT_DICT_PATH = "//data/alan/VFlocation/VFRanking/rank/secureBertRank/bert_dict"
LLAMA_back_bone_model_path = "//data/alan/model/Llama-2-7b-hf"
LLAMA_pretrain_adpter_path = "//data/alan/model/angle-llama-7b-nli-20231027"
LLAMA_embeding_dict = "//data/alan/VFlocation/VFRanking/rank/Llama2Rank/CVE_API_bert_dict"


def get_CVE_jar_mapping():
    pass

def get_CVE_entity_dict(CVE_entity_dir:str):
    '''

    :param CVE_entity_dir:
    :return:
    '''
    CVE_entity_file_list = os.listdir(CVE_entity_dir)
    CVE_entity_dict = {}
    for CVE_entity_file in CVE_entity_file_list:
        with open(os.path.join(CVE_entity_dir, CVE_entity_file), "rb") as f:
            CVE_entity_dict[CVE_entity_file] = pickle.load(f)
    return CVE_entity_dict


def get_GAV_API_dict(GAV_API_entity_dir:str):
    '''


    :return:
    '''
    GAV_list = os.listdir(GAV_API_entity_dir)
    GAV_API_dict = {}
    for GAV in GAV_list:
        with open(os.path.join(GAV_API_entity_dir, GAV), "rb") as f:
            GAV_API_dict[GAV] = pickle.load(f)
    return GAV_API_dict


def form_para_str(para_type_list:list):
    '''

    :param para_type_list:
    :return:
    '''
    para_str = ":".join(para_type_list)
    return para_str


def calculate_spacy_similarity(spacy_model, str1, str2):
    '''

    :param str1:
    :param str2:
    :return:
    '''
    doc1 = spacy_model(str1)
    doc2 = spacy_model(str2)
    return doc1.similarity(doc2)


def get_API_entity_dir(API_entity_base_dir:str, API_entity_extraction_opt:dict):
    '''

    :param API_entity_dir:
    :return:
    '''
    API_entity_dir = construct_opt_dir(API_entity_base_dir, API_entity_extraction_opt)
    return API_entity_dir


def get_CVE_entity_dir(CVE_entity_base_dir:str, CVE_entity_extraction_opt:dict):
    '''

    :param CVE_entity_dir:
    :return:
    '''
    CVE_entity_dir = construct_opt_dir(CVE_entity_base_dir, CVE_entity_extraction_opt)
    return CVE_entity_dir



def get_ranking_result_dir(CVE_API_ranking_dict_dir_base:str, running_opt_dict:dict):
    '''

    :param CVE_API_ranking_dict_dir_base:
    :param running_opt_dict:
    :return:
    '''
    CVE_entity_opt = construct_opt_dir("", running_opt_dict[CVE_extraction_opt])
    API_entity_opt = construct_opt_dir("", running_opt_dict[API_extraction_opt])
    base_dir = CVE_API_ranking_dict_dir_base + CVE_entity_opt + API_entity_opt
    ranking_result_opt = construct_opt_dir(base_dir, running_opt_dict[ranking_opt])
    return ranking_result_opt


def normalize_rank(rank_list):
    '''
    :param rank_list:
    :return:
    '''
    n = len(rank_list)
    normalized_rank_list = []
    i = 0

    while i < n:
        func_name, vulnerability_degree = rank_list[i]
        # Find all elements with the same vulnerability degree
        same_rank_funcs = [(func_name, vulnerability_degree)]
        while i + 1 < n and rank_list[i + 1][1] == vulnerability_degree:
            i += 1
            same_rank_funcs.append(rank_list[i])

        # Assign the same score to all functions with the same rank
        score = 1 - i / (n - 1) if n > 1 else 1
        for func_name, _ in same_rank_funcs:
            normalized_rank_list.append((func_name, score))

        i += 1

    return normalized_rank_list
