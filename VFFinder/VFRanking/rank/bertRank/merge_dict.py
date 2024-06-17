
import os
import pickle

if __name__ == "__main__":
    all_CVE = os.listdir("//data/alan/VFlocation/resource/bert_dict")
    large_dict = {}
    for cve in all_CVE:
        with open(os.path.join("//data/alan/VFlocation/resource/bert_dict", cve), "rb") as f:
            bert_dict = pickle.load(f)
        for key, value in bert_dict.items():
            large_dict[key] = value

    with open("./bert_dict", "wb") as f:
        pickle.dump(large_dict, f)