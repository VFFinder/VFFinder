
from VFRanking.rank.bertRank.storeBertDict import get_description
from transformers import RobertaTokenizer, RobertaModel
import pickle
from tqdm import tqdm


from VFRanking.utils import SecureBERT_PATH, SecureBERT_TOKENIZER_PATH

if __name__ == "__main__":
    all_description = get_description()
    bert_dict = dict()
    tokenizer = RobertaTokenizer.from_pretrained(SecureBERT_TOKENIZER_PATH)
    model = RobertaModel.from_pretrained(SecureBERT_PATH)

    for key, value in tqdm(all_description.items()):
        for word in value.split(" "):
            word = word.strip().strip(".").strip(",").strip("!").strip("?").strip(":").strip(";").strip("\n").strip(
                "\t")
            if word not in bert_dict:
                tokens = tokenizer(word, return_tensors='pt')
                outputs = model(**tokens)
                embedding = outputs.last_hidden_state[:, 0, :]
                bert_dict[word] = embedding

    with open("./bert_dict", "wb") as f:
        pickle.dump(bert_dict, f)