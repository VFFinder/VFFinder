
import networkx as nx
from gensim.models import Word2Vec
import random
import numpy as np

def random_walk(G, node, length):
    walk = [(node, G.nodes[node]['label'])]
    for _ in range(length - 1):
        neighbors = list(G.neighbors(walk[-1][0]))
        if len(neighbors) > 0:
            next_node = random.choice(neighbors)
            walk.append((next_node, G.nodes[next_node]['label']))
        else:
            break
    walk = [path[1] for path in walk]
    return walk


def deepwalk_embed(G:nx.DiGraph):
    walks = []
    for node in G.nodes:
        for _ in range(7):  # 每个节点进行10次随机游走
            walk = random_walk(G, node, 5)  # 每次游走的长度为5
            walks.append(walk)

    model = Word2Vec(walks, vector_size=32, window=2, min_count=0, sg=1, workers=4)

    all_node_embeddings = [model.wv[G.nodes[node]['label']] for node in G.nodes]
    # 使用平均池化获取整个图的embedding
    graph_embedding = np.mean(all_node_embeddings, axis=0)
    return graph_embedding