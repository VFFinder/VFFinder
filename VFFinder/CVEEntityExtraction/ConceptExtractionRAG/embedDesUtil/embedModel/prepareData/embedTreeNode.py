
import os
import pickle
from gensim.models import FastText

def get_labels(root):
    if root is None:
        return []
    labels = [root.label]  # 获取当前节点的标签
    for child in root.children:  # 遍历每个子节点
        labels.extend(get_labels(child))  # 递归获取子节点的标签
    return labels


def fasttext_embed():
    all_tree = os.listdir("../../../../../resource/CVETree/CVETree")
    all_label = []
    for tree in all_tree:
        with open("../../../../../resource/CVETree/CVETree/" + tree, 'rb') as f:
            tree = pickle.load(f)
        tree_label_list = get_labels(tree)
        all_label.extend(tree_label_list)
    all_label = list(set(all_label))
    all_sepreat_label = []
    for label in all_label:
        all_sepreat_label.append([label])
    model = FastText(all_sepreat_label, vector_size=64, window=5, min_count=1, workers=4)
    model.save("../model/textEmbed/fasttext.bin")


if __name__ == "__main__":
    fasttext_embed()



