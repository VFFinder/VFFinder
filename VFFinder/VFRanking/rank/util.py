
import numpy as np
import time

def calculate_edit_distance(s1, s2):
    '''
    :param s1:
    :param s2:
    :return:
    '''
    len1 = len(s1)
    len2 = len(s2)
    dp = [[0 for _ in range(len2 + 1)] for _ in range(len1 + 1)]
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j]) + 1
    return dp[len1][len2]


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return 1 + np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def calculate_edit_distance_sum(cddt_word_bag, target_word, editi_distance_threshold: int):
    min_edit_distance_for_word = 999999
    similiarity_score = 0
    for candidate_word in cddt_word_bag:
        ed_dis = calculate_edit_distance(target_word, candidate_word)
        if ed_dis < min_edit_distance_for_word:
            min_edit_distance_for_word = ed_dis
    if min_edit_distance_for_word <= editi_distance_threshold:
        similiarity_score = 1
    return similiarity_score


class TimeDecorator:
    def __init__(self, num=1):
        self.num = num

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"Function '{func.__name__}' run time: {(end_time - start_time) / self.num} units")
            return result
        return wrapper
