


from VFRanking.rank.bertRank.score import score_threshold_bert
from VFRanking.rank.nltkRank.score import score_threshold_nltk
from VFRanking.rank.spacyRank.score import score_threshold_spacy
from VFRanking.rank.secureBertRank.score import score_threshold_securebert
from VFRanking.rank.Llama2Rank.score import score_threshold_llama
from VFRanking.rank.bertRank.BertDict import BertDict
from BM25Filtering.utils import get_entity_weight
from VFRanking.featureSelection.classMatch import clz_match
from VFRanking.utils import BERT_PATH, BERT_DICT_PATH, SecureBERT_PATH, SecureBERT_TOKENIZER_PATH, SecureBERT_DICT_PATH, LLAMA_back_bone_model_path, LLAMA_pretrain_adpter_path, LLAMA_embeding_dict
from VFRanking.featureSelection.featureMatch import feature_match
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


def get_cve_entity_weight(query, doc_list):
    # 将查询字符串添加到文档列表中
    # 初始化TF-IDF向量器
    vectorizer = TfidfVectorizer()
    vectorizer.fit(doc_list)

    # 使用训练好的 TfidfVectorizer 来转换待评估文档
    tfidf = vectorizer.transform([query])
    # 获取词汇表
    vocab = vectorizer.get_feature_names_out()
    # 将稀疏矩阵转换为稠密向量
    tfidf_dense = tfidf.todense()

    # 获取每个词的TF-IDF值
    word_importance = {word: tfidf_dense[0, i] for word, i in zip(vocab, range(len(vocab)))}

    # 输出每个词的重要性
    return word_importance


def rank_API_by_model_threashold(CVE_entity, API_entity_list, all_cve_entity, CWE_keywords_dict, model_name, threashold, rank_opt):
    '''
    :param API_entity_list:
    :param CVE_entity:
    :return:
    '''

    clz_matched, feature_matched, feature_not_matched = feature_match(CVE_entity, API_entity_list, CWE_keywords_dict, rank_opt)
    clz_matched_ranked = score_API_by_model_threashold(CVE_entity, all_cve_entity, clz_matched, model_name, threashold, rank_opt)
    feature_matched_ranked = score_API_by_model_threashold(CVE_entity, all_cve_entity, feature_matched, model_name, threashold, rank_opt)
    feature_not_matched_ranked = score_API_by_model_threashold(CVE_entity, all_cve_entity, feature_not_matched, model_name, threashold, rank_opt)
    api_score_list = clz_matched_ranked + feature_matched_ranked + feature_not_matched_ranked
    return api_score_list


def score_API_by_model_threashold(CVE_entity, all_cve_entity, API_entity_list, model_name, threashold, rank_opt):
    '''
    :param model_name:
    :param API_entity_list:
    :param CVE_entity:
    :param threashold:
    :return:
    '''
    if rank_opt["TF_IDF"]:
        cve_entity_weight = get_entity_weight(CVE_entity.CVE_ID, CVE_entity, all_cve_entity, API_entity_list)
    else:
        cve_entity_weight = {entity:1 for entity in CVE_entity.get_all_entity()}

    if not API_entity_list:
        return []
    if model_name == "nltk":
        from nltk.corpus import wordnet
        bert_dict = None
        tokenizer = None
        model = wordnet
        score_api = score_threshold_nltk
    elif model_name == "spacy":
        tokenizer = None
        bert_dict = None
        import spacy
        model = spacy.load('en_core_web_md')
        score_api = score_threshold_spacy
    elif model_name == "bert":
        from sentence_transformers import SentenceTransformer
        dict_path = BERT_DICT_PATH
        with open(BERT_DICT_PATH, "rb") as f:
            dict_ = pickle.load(f)
        bert_dict = BertDict(dict_)
        model = SentenceTransformer(BERT_PATH)
        tokenizer = None
        score_api = score_threshold_bert
    elif model_name == "SecureBERT":
        from transformers import RobertaTokenizer, RobertaModel
        with open(SecureBERT_DICT_PATH, "rb") as f:
            dict_ = pickle.load(f)
        bert_dict = BertDict(dict_)
        tokenizer = RobertaTokenizer.from_pretrained(SecureBERT_TOKENIZER_PATH)
        model = RobertaModel.from_pretrained(SecureBERT_PATH)
        score_api = score_threshold_securebert
    elif model_name == "llama":
        with open(LLAMA_embeding_dict, "rb") as f:
            dict_ = pickle.load(f)
        bert_dict = BertDict(dict_)
        tokenizer = None
        from angle_emb import AnglE, Prompts
        model = AnglE.from_pretrained(LLAMA_back_bone_model_path, pretrained_lora_path=LLAMA_pretrain_adpter_path)
        model.to('cpu')
        model.set_prompt(prompt=Prompts.A)
        score_api = score_threshold_llama
    else:
        raise ValueError("model_name not supported")

    api_score_list = []
    for API_entity in API_entity_list:
        similarity_score = score_api(CVE_entity.get_all_entity(), cve_entity_weight, API_entity.get_cleaned_entity(), model, threashold, bert_embed_dict=bert_dict, tokenizer=tokenizer)
        api_score_list.append((API_entity, similarity_score))
    api_score_list.sort(key=lambda x: x[1], reverse=True)


    return api_score_list