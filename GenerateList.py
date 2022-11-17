import DataProcess
import random
import numpy as np


# 一阶生成：
# 输入：
# matrix：二层list N*N的马尔科夫矩阵，
# list_len：希望得到的音符列表长度
# start_note：初始列表,-1为随机
def list_generate_1(matrix, list_len, start_note=-1):
    mat_size = len(matrix)
    if start_note >= mat_size or start_note < 0:
        cur_note = random.randint(0, list_len - 1) % mat_size
    else:
        cur_note = start_note
    note_list = [cur_note]
    for i in range(1, list_len):
        if sum(matrix[cur_note]) != 0:
            cur_note = np.random.choice(range(mat_size), 1, p=matrix[cur_note])[0]
        else:
            cur_note = np.random.choice(range(mat_size), 1)[0]
        note_list.append(cur_note)
    return note_list


# 二阶生成：
# 输入：
# matrix：三层list N*N*N的马尔科夫矩阵，
# list_len：希望得到的列表长度
# start_note：初始列表,留空为随机
def list_generate_2(matrix, list_len, start_note_list):
    mat_size = len(matrix)
    while len(start_note_list) < 2:
        start_note_list.insert(0, random.randint(0, mat_size - 1))
    note_list = start_note_list
    for i in range(1, list_len):
        if sum(matrix[note_list[-2]][note_list[-1]]) != 0:
            cur_note = np.random.choice(range(mat_size), 1, p=matrix[note_list[-2]][note_list[-1]])[0]
        else:
            cur_note = np.random.choice(range(mat_size), 1)[0]
        note_list.append(cur_note)
    return note_list
