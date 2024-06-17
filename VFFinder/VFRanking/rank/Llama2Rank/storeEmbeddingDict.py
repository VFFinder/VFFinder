
import sys
sys.path.append("../../../")
from angle_emb import AnglE, Prompts
from tqdm import tqdm
import pickle
from VFRanking.rank.bertRank.storeBertDict import get_description
from VFRanking.utils import get_GAV_API_dict

back_bone_model_path = "//data/alan/model/Llama-2-7b-hf"
pretrain_adpter_path = "//data/alan/model/angle-llama-7b-nli-20231027"
#API_entity_dir = '//data/alan/VFlocation/resource/APIEntity/APIEntity_1_1_1_1_1_1_1/'

API_entity_dir_list = [
'//data/alan/VFlocation/resource/APIEntity/APIEntity_1_1_1_1_1_1_1/',
'//data/alan/VFlocation/resource/APIEntity/APIEntity_0_1_1_1_1_1_1/',
'//data/alan/VFlocation/resource/APIEntity/APIEntity_1_0_1_1_1_1_1/',
'//data/alan/VFlocation/resource/APIEntity/APIEntity_1_1_0_1_1_1_1/',
'//data/alan/VFlocation/resource/APIEntity/APIEntity_1_1_1_0_1_1_1/',
'//data/alan/VFlocation/resource/APIEntity/APIEntity_1_1_1_1_0_1_1/',
'//data/alan/VFlocation/resource/APIEntity/APIEntity_1_1_1_1_1_0_1/',
]

if __name__ == "__main__":
    all_description = get_description()

    # with open("./CVE_API_bert_dict", "rb") as f:
    #     bert_dict = pickle.load(f)
    angle = AnglE.from_pretrained(back_bone_model_path, pretrained_lora_path=pretrain_adpter_path)
    angle.set_prompt(prompt=Prompts.A)
    print('prompt:', angle.prompt)

    # for key, value in tqdm(all_description.items()):
    #     for word in value.split(" "):
    #         word = word.strip(".,!?:;\n\t([{<>\"'`")
    word = 'S2'
    angle.to('cpu')
    vec = angle.encode({'text': word}, to_numpy=True)
    # if word not in bert_dict:
    #     vec = angle.encode({'text': word}, to_numpy=True)
    #     bert_dict[word] = vec
    #
    #     with open("./CVE_API_bert_dict", "wb") as f:
    #         pickle.dump(bert_dict, f)
    #     with open("./CVE_API_bert_dict", "rb") as f:
    #         bert_dict = pickle.load(f)
    #
    # for API_entity_dir in API_entity_dir_list:
    #     API_entity_list = get_GAV_API_dict(API_entity_dir)
    #     for GAV, API_entity_bag in tqdm(API_entity_list.items()):
    #         for API_entity in API_entity_bag:
    #             for API_entity_element in API_entity.get_cleaned_entity():
    #                 word = API_entity_element.strip(".,!?:;\n\t([{<\"'`")
    #                 if word not in bert_dict:
    #                     vec = angle.encode({'text': word}, to_numpy=True)
    #                     bert_dict[word] = vec
    #         with open("./CVE_API_bert_dict", "wb") as f:
    #             pickle.dump(bert_dict, f)
    #
    #         with open("./CVE_API_bert_dict", "rb") as f:
    #             bert_dict = pickle.load(f)
    #
