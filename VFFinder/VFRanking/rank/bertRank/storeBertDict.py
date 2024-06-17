
import sys
sys.path.append("../../../")

from VFRanking.utils import BERT_PATH
import pickle
from tqdm import tqdm
import os
import multiprocessing

def get_description():
    all_description = dict()
    need_ID = []
    with open("../../../resource/CVE_API", "r") as f:
        for line in f.readlines():
            CVE_ID, description = line.split(":")[0], ":".join(line.split(":")[1:]).strip("\n")
            need_ID.append(CVE_ID)

    with open("../../../resource/CVE_description_mess", "r") as f:
        for line in f.readlines():
            CVE_ID, description = line.split(":")[0], ":".join(line.split(":")[1:]).strip("\n")
            if CVE_ID in need_ID:
                all_description[CVE_ID] = description
    return all_description


def split_dict_equally(input_dict, chunks):
    "Splits dict by keys. Returns a list of dictionaries."
    # prep with empty dicts
    return_list = [dict() for idx in range(chunks)]
    idx = 0
    for k,v in input_dict.items():
        return_list[idx][k] = v
        if idx < chunks-1:  # indexes start at 0
            idx += 1
        else:
            idx = 0
    return return_list


def process_sub_dict(model, sub_dict, pid):
    bert_dict = dict()


    for key, value in tqdm(sub_dict.items(), desc=f"Process {pid}"):
        for word in value.split(" "):
            if word not in bert_dict:
                bert_dict[word] = model.encode(word)

        with open(f"../../../resource/bert_dict/{key}", "wb") as f:
            pickle.dump(bert_dict, f)


if __name__ == "__main__":
    # all_description = get_description()
    # num_processes = 10  # get the number of cores

    # split the dictionary into sub-dictionaries for each process
    # sub_dicts = split_dict_equally(all_description, num_processes)
    # sub_dicts = [sub_dict for sub_dict in sub_dicts if sub_dict]  # remove empty dicts
    # for index, dict_ in enumerate(sub_dicts):
    #     with open("bert_dict_" + str(index), "wb") as f:
    #         pickle.dump(dict_, f)

    index = 9
    with open("bert_dict_" + str(index), "rb") as f:
        description_dict = pickle.load(f)

    done_list = os.listdir("../../../resource/bert_dict")
    bert_dict = dict()
    model = SentenceTransformer(BERT_PATH)
    for key, value in tqdm(description_dict.items()):
        # if key in done_list:
        #     continue
        for word in value.split(" "):
            word = word.strip().strip(".").strip(",").strip("!").strip("?").strip(":").strip(";").strip("\n").strip("\t")
            if word not in bert_dict:
                bert_dict[word] = model.encode(word)

        with open("../../../resource/bert_dict/" + key, "wb") as f:
            pickle.dump(bert_dict, f)

    # processes = []
    # model = SentenceTransformer(BERT_PATH)
    # for i in range(num_processes):
    #     p = multiprocessing.Process(target=process_sub_dict, args=(model, sub_dicts[i], i))
    #     processes.append(p)
    #     p.start()
    #
    # for p in processes:
    #     p.join()
    #
    #
    #
    # bert_dict = dict()
    # model = SentenceTransformer(BERT_PATH)
    # all_description = get_description()
    # for key, value in tqdm(all_description.items()):
    #     for word in value.split(" "):
    #         if word not in bert_dict:
    #             bert_dict[word] = model.encode(word)
    #
    #     with open("../../../resource/bert_dict/" + key, "wb") as f:
    #         pickle.dump(bert_dict, f)