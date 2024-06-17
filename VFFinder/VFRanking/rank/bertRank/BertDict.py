
import pickle

class BertDict(object):
    def __init__(self, bert_dict):
        self.bert_dict = bert_dict

    def get_dict(self):
        return self.bert_dict

    def add_word(self, word, vec):
        self.bert_dict[word] = vec

    def get_word_vec(self, word):
        return self.bert_dict[word]

    def save_dict(self, path):
        with open(path, "wb") as f:
            pickle.dump(self.bert_dict, f)