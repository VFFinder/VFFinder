
import sys
sys.path.append("//data/alan/VFlocation/")
sys.path.append("//data/alan/VFlocation/CVEEntityExtraction/ConceptExtractionRAG/embedDesUtil")

import os
from CVEEntityExtraction.ConceptExtractionRAG.embedDesUtil.treeBuild import tree_build
from stanfordcorenlp import StanfordCoreNLP
import nltk
import hashlib
import pickle
from tqdm import tqdm

basic_component_dir = "../../../../../resource/CVETree/BasicComponent"
tree_dir = "../../../../../resource/CVETree/CVETree"


def embed_and_save():
    CVE_has_componet = [CVE_ID.split("_")[0] for CVE_ID in os.listdir("../../../../../resource/CVETree/BasicComponent")]
    nlp = StanfordCoreNLP(r'//data/alan/stanford-corenlp-4.5.7')
    CVE_description = {}
    with open("../../../../../resource/CVEDescriptionAll", "r") as f:
        for line in f.readlines():
            CVE_ID = line.split(":")[0]
            description = ":".join(line.split(":")[1:])
            CVE_description[CVE_ID] = description

    with open("../../../../../resource/CVE_description", "r") as f:
        for line in f.readlines():
            CVE_ID = line.split(":")[0]
            description = ":".join(line.split(":")[1:])
            CVE_description[CVE_ID] = description

    for CVE_ID in tqdm(CVE_has_componet):
        if CVE_ID not in CVE_description:
            print(CVE_ID)
            continue
        description = CVE_description[CVE_ID]
        for sentence in nltk.sent_tokenize(description):
            sentence_hash = hashlib.md5(description.encode()).hexdigest()
            file_name = CVE_ID + "_" + sentence_hash
            if os.path.exists(os.path.join(tree_dir, file_name)):
                continue

            sentence_tree = tree_build(CVE_ID, sentence, nlp, basic_component_dir)
            with open(os.path.join(tree_dir, file_name), 'wb') as f:
                pickle.dump(sentence_tree, f)


if __name__ == "__main__":
    embed_and_save()




