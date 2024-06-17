
from CVEEntityExtraction.ConceptExtractionRAG.embedDesUtil.treeBuild import draw_tree


def find_no_split_NP_subtree(root):
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node.label == 'NP':
            result.append(node)
        stack.extend([i for i in node.children])

    killed_result = []
    for node in result:
        if check_indivision_subtree(node, 'NP'):
            killed_result.append(node)

    return killed_result


def check_indivision_subtree(root, label):
    stack = [i for i in root.children]
    while stack:
        node = stack.pop()
        if node.label == label or node.label == 'VUL' or node.label == 'AGENT' or node.label == 'COMP' or node.label == 'VPV':
            return False
        else:
            stack.extend([i for i in node.children])
    return True


def find_pure_NP_tree(root):
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node.label == 'NP':
            result.append(node)
        stack.extend([i for i in node.children])

    killed_result = []
    for node in result:
        if check_pure_NP_tree(node):
            killed_result.append(node)

    return killed_result


def check_pure_NP_tree(root):
    if root.label != 'NP':
        return False

    for child in root.children:
        if not check_pure_NP_tree(child):
            return False
    return True


def remove_NP_children(root, label="NP"):
    all_indivsion_NP_node = find_no_split_NP_subtree(root)
    for node in all_indivsion_NP_node:
        node.children = []
    all_pure_NP_node = find_pure_NP_tree(root)
    for node in all_pure_NP_node:
        node.children = []


def remove_leaves_except(root, labels):
    if root is None:
        return

    root.children = [child for child in root.children if not (len(child.children) == 0 and child.label not in labels)]

    for child in root.children:
        remove_leaves_except(child, labels)


def get_leaf_nodes(root):
    if root is None:
        return []

    if len(root.children) == 0:
        return [root]

    leaf_nodes = []
    for child in root.children:
        leaf_nodes.extend(get_leaf_nodes(child))

    return leaf_nodes


def get_leaf_node_sequence(root):
    leaf_nodes = get_leaf_nodes(root)
    labels = [node.label for node in leaf_nodes]
    return labels


def transferTree2Seq(description_tree):
    """
    Transfer the tree to the sequence
    :param tree: the tree of the description
    :return: the sequence of the tree
    """
    draw_tree(description_tree, "origin_tree.png")
    remove_NP_children(description_tree, 'NP')
    draw_tree(description_tree, "remove_NP.png")
    remove_leaves_except(description_tree, ['NP', 'VPV', 'COMP', 'VUL', 'AGENT'])
    draw_tree(description_tree, "remove_levef.png")
    leaf_sequence = get_leaf_node_sequence(description_tree)
    return leaf_sequence


def embed_treesequence(description_tree, embed_model):
    """
    Embed the sequence of the tree
    :param sequence: the sequence of the tree
    :return: the embedded sequence
    """
    sequence = transferTree2Seq(description_tree)
    # print(sequence)
    embedded_sequence = embed_model.encode(" ".join(sequence))
    return embedded_sequence

