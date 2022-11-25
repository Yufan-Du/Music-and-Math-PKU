class Info:
    def __init__(self, pitch, rhythm):
        self.pitch = pitch
        self.rhythm = rhythm

class HMM:
    def __init__(self, state, observation, transition_matrix, confusion_matrix):
        self.state = state
        self.observation = observation
        self.transition_matrix = transition_matrix
        self.confusion_matrix = confusion_matrix
class interval:
    def __init__(self, matrix):
        self.matrix = matrix

def normalize_2dim(src_list, dst_list):
    for i in range(len(src_list)):
        sum = 0
        for j in range(len(src_list[0])):
            sum += src_list[i][j]
        for j in range(len(src_list[0])):
            if sum > 0:
                freq = src_list[i][j] / sum
                dst_list[i][j] = freq
    return dst_list


def normalize_3dim(src_list, dst_list):
    for i in range(len(src_list)):
        for j in range(len(src_list[0])):
            sum = 0
            for k in range(len(src_list[0][0])):
                sum += src_list[i][j][k]
            for k in range(len(src_list[0][0])):
                if (sum > 0):
                    freq = src_list[i][j][k] / sum
                    dst_list[i][j][k] = freq
    return dst_list

def normalize_4dim(src_list, dst_list):
    for i in range(len(src_list)):
        for j in range(len(src_list[0])):
            for k in range(len(src_list[0][0])):
                sum=0
                for m in range(len(src_list[0][0][0])):
                    sum+=src_list[i][j][k][m]
                for m in range(len(src_list[0][0][0])):
                    if(sum>0):
                        freq=src_list[i][j][k][m]/sum
                        dst_list[i][j][k][m]=freq
    return dst_list

def norm_matrix(matrix):
    row = len(matrix)
    col = len(matrix[0])

    n_matrix = [[0 for i in range(col)] for i in range(row)]
    for i in range(row):
        sum = 0
        for j in range(col):
            sum = sum + matrix[i][j]
        for j in range(col):
            if sum>0:
                n_matrix[i][j] = matrix[i][j]/sum
            
    return n_matrix

def find_row(k, j, base):  # k，j都有base种可能，输入k，j，输出对应的row
    return k * base + j


dict_yinming = {"0": "0", "1": "C4", "2": "D4", "3": "E4", "4": "F4", "5": "G4", "6": "A4", "7": "B4",
                "+1": "C5", "+2": "D5", "+3": "E5", "+4": "F5", "+5": "G5", "+6": "A5", "+7": "B5",
                "++1": "C6"}
dict_pitch_id = {"0": 0, "C4": 1, "D4": 2, "E4": 3, "F4": 4, "G4": 5, "A4": 6, "B4": 7,
                 "C5": 8, "D5": 9, "E5": 10, "F5": 11, "G5": 12, "A5": 13, "B5": 14,
                 "C6": 15}
dict_rhythm_id = {
    "0.25": 0,
    "0.5": 1,
    "1": 2,
    "1.5": 3,
    "2": 4,
    "2.5": 5,
    "3": 6,
    "3.5": 7,
    "4": 8,
    "5": 9,
    "8.5": 10}

dict_chord_id = {
    "None" : 0,
    "Am": 1,
    "Dm": 2,
    "C": 3,
    "G": 4,
    "F": 5
    }

dict_id_chord = {value: key for key, value in dict_chord_id.items()}

dict_id_rhythm = {value: key for key, value in dict_rhythm_id.items()}

dict_id_pitch = {value: key for key, value in dict_pitch_id.items()}


def trans_1_order(file_list):  # 输入待统计的文件路径列表
    pitch_trans_matrix_num = [[0 for i in range(16)] for i in range(16)]
    pitch_trans_matrix_freq = [[0 for i in range(16)] for i in range(16)]
    rhythm_trans_matrix_num = [[0 for i in range(11)] for i in range(11)]
    rhythm_trans_matrix_freq = [[0 for i in range(11)] for i in range(11)]

    for file_path in file_list:
        # print("onefile")
        file = open(file_path, "r", encoding="utf-8")
        lines = file.readlines()
        i = 0
        pitch_list = []
        rhythm_list = []
        for line in lines:
            if (i >= 1):
                lst = line.split()
                if (i % 2 == 1):
                    pitch_list += lst
                else:
                    rhythm_list += lst
                # print(i,len(lst))
            i += 1
        pitch_length = len(pitch_list)
        rhythm_length = len(rhythm_list)
        # print(pitch_length)
        # print(rhythm_length)
        for i in range(1, pitch_length):
            j = i - 1
            pitch_row = dict_pitch_id[dict_yinming[pitch_list[j]]]
            pitch_col = dict_pitch_id[dict_yinming[pitch_list[i]]]
            pitch_trans_matrix_num[pitch_row][pitch_col] += 1
            rhythm_row = dict_rhythm_id[rhythm_list[j]]
            rhythm_col = dict_rhythm_id[rhythm_list[i]]
            rhythm_trans_matrix_num[rhythm_row][rhythm_col] += 1

    pitch_trans_matrix_freq = normalize_2dim(
        pitch_trans_matrix_num, pitch_trans_matrix_freq)
    rhythm_trans_matrix_freq = normalize_2dim(
        rhythm_trans_matrix_num, rhythm_trans_matrix_freq)
    ret = Info(pitch_trans_matrix_freq, rhythm_trans_matrix_freq)
    # print(pitch_trans_matrix_freq)
    # print(rhythm_trans_matrix_freq)
    return ret


def trans_2_order(file_list):
    pitch_trans_matrix_num = [
        [[0 for i in range(16)] for i in range(16)] for i in range(16)]
    pitch_trans_matrix_freq = [
        [[0 for i in range(16)] for i in range(16)] for i in range(16)]
    rhythm_trans_matrix_num = [
        [[0 for i in range(11)] for i in range(11)] for i in range(11)]
    rhythm_trans_matrix_freq = [
        [[0 for i in range(11)] for i in range(11)] for i in range(11)]

    for file_path in file_list:
        # print("onefile")
        file = open(file_path, "r", encoding="utf-8")
        lines = file.readlines()
        i = 0
        pitch_list = []
        rhythm_list = []
        for line in lines:
            if (i >= 1):
                lst = line.split()
                if (i % 2 == 1):
                    pitch_list += lst
                else:
                    rhythm_list += lst
                # print(i,len(lst))
            i += 1
        pitch_length = len(pitch_list)
        rhythm_length = len(rhythm_list)
        # print(pitch_length)
        # print(rhythm_length)
        for i in range(2, pitch_length):
            j = i - 1
            k = i - 2  # 取前面两个下标k，j
            pitch_k_id = dict_pitch_id[dict_yinming[pitch_list[k]]]
            pitch_j_id = dict_pitch_id[dict_yinming[pitch_list[j]]]
            pitch_col = dict_pitch_id[dict_yinming[pitch_list[i]]]
            pitch_trans_matrix_num[pitch_k_id][pitch_j_id][pitch_col] += 1

            rhythm_k_id = dict_rhythm_id[rhythm_list[k]]
            rhythm_j_id = dict_rhythm_id[rhythm_list[j]]
            rhythm_col = dict_rhythm_id[rhythm_list[i]]
            rhythm_trans_matrix_num[rhythm_k_id][rhythm_j_id][rhythm_col] += 1

    pitch_trans_matrix_freq = normalize_3dim(
        pitch_trans_matrix_num, pitch_trans_matrix_freq)
    rhythm_trans_matrix_freq = normalize_3dim(
        rhythm_trans_matrix_num, rhythm_trans_matrix_freq)
    ret = Info(pitch_trans_matrix_freq, rhythm_trans_matrix_freq)
    # print(pitch_trans_matrix_freq)
    # print(rhythm_trans_matrix_freq)
    return ret

def trans_3_order(file_list):
    pitch_trans_matrix_num = [[[[0 for i in range(16)] for i in range(16)]for i in range(16)]for i in range(16)]
    pitch_trans_matrix_freq = [[[[0 for i in range(16)] for i in range(16)]for i in range(16)]for i in range(16)]
    rhythm_trans_matrix_num = [[[[0 for i in range(11)] for i in range(11)]for i in range(11)]for i in range(11)]
    rhythm_trans_matrix_freq = [[[[0 for i in range(11)] for i in range(11)]for i in range(11)]for i in range(11)]

    for file_path in file_list:
        file = open(file_path, "r", encoding="utf-8")
        lines = file.readlines()
        i = 0
        pitch_list = []
        rhythm_list = []
        for line in lines:
            if (i >= 1):
                lst = line.split()
                if (i % 2 == 1):
                    pitch_list += lst
                else:
                    rhythm_list += lst
            i += 1
        pitch_length = len(pitch_list)
        rhythm_length = len(rhythm_list)
        for i in range(3, pitch_length):
            j = i - 1
            k = i - 2
            m = i - 3  # 取前面三个下标m，k，j
            pitch_m_id = dict_pitch_id[dict_yinming[pitch_list[m]]]
            pitch_k_id = dict_pitch_id[dict_yinming[pitch_list[k]]]
            pitch_j_id = dict_pitch_id[dict_yinming[pitch_list[j]]]
            pitch_col = dict_pitch_id[dict_yinming[pitch_list[i]]]
            pitch_trans_matrix_num[pitch_m_id][pitch_k_id][pitch_j_id][pitch_col] += 1

            rhythm_m_id = dict_rhythm_id[rhythm_list[m]]
            rhythm_k_id = dict_rhythm_id[rhythm_list[k]]
            rhythm_j_id = dict_rhythm_id[rhythm_list[j]]
            rhythm_col = dict_rhythm_id[rhythm_list[i]]
            rhythm_trans_matrix_num[rhythm_m_id][rhythm_k_id][rhythm_j_id][rhythm_col] += 1

    pitch_trans_matrix_freq = normalize_4dim(
        pitch_trans_matrix_num, pitch_trans_matrix_freq)
    rhythm_trans_matrix_freq = normalize_4dim(
        rhythm_trans_matrix_num, rhythm_trans_matrix_freq)
    ret = Info(pitch_trans_matrix_freq, rhythm_trans_matrix_freq)
    return ret


def trans_interval(file_list):
    N = len(dict_pitch_id)
    M = len(dict_rhythm_id)

    transition_matrix = [[0 for i in range(N*M)] for i in range(N*M)]
    for file_path in file_list:
        # print("onefile")
        file = open(file_path, "r", encoding="utf-8")
        lines = file.readlines()
        i = 0
        pitch_list = []
        rhythm_list = []
        for line in lines:
            if (i >= 1):
                lst = line.split()
                if (i % 2 == 1):
                    pitch_list += lst
                else:
                    rhythm_list += lst
            i += 1
        pitch_length = len(pitch_list)

        for i in range(1,pitch_length):
            j = i - 1
            state1 = dict_pitch_id[dict_yinming[pitch_list[j]]]*M + dict_rhythm_id[rhythm_list[j]]
            state2 = dict_pitch_id[dict_yinming[pitch_list[i]]]*M + dict_rhythm_id[rhythm_list[i]]
            transition_matrix[state1][state2] += 1
        transition_matrix = norm_matrix(transition_matrix)
    Interval = interval(transition_matrix)
    return Interval

def state2note(state):
    M = len(dict_rhythm_id)
    pitch = int(state/M)
    rhythm = state - pitch*M
    return pitch,rhythm

def trans_HMM(file_list, state_encoding, observation_encoding):
    # 状态和观测量的编码方式
    state = state_encoding
    observation = observation_encoding
    N = len(state)
    M = len(observation)

    transition_matrix = [[0 for i in range(N)] for i in range(N)]
    confusion_matrix = [[0 for i in range(M)] for i in range(N)]

    for file_path in file_list:
        file = open(file_path, 'r', encoding = "utf-8")
        lines = file.readlines()
        i = 0
        state_list = []
        observation_list = []
        for line in lines:
            if(i>=1):
                lst = line.split()
                if(i%2 == 1):
                    state_list += lst
                else:
                    observation_list += lst
            i = i + 1
        state_length = len(state_list)
        observation_length = len(observation_list)
        
        #状态转移矩阵
        for i in range(1, state_length):
            j = i -1
            state_row = state[dict_yinming[state_list[j]]]
            state_col = state[dict_yinming[state_list[i]]]
            transition_matrix[state_row][state_col] += 1
        transition_matrix = norm_matrix(transition_matrix)

        #混淆矩阵(观测量矩阵)
        for i in range(observation_length):
            state_row = state[dict_yinming[state_list[i]]]
            observation_col = observation[observation_list[i]]
            confusion_matrix[state_row][observation_col] += 1
        confusion_matrix = norm_matrix(confusion_matrix)

    hmm = HMM(state, observation, transition_matrix, confusion_matrix)
    return hmm

# HMM隐马尔可夫生成和弦矩阵
def chord_matrix(filename):
    chord_matrix = [[0 for i in range(6)] for i in range(16)]
    for file_path in filename:
        # print("onefile")
        file = open(file_path, "r", encoding="utf-8")
        lines = file.readlines()
        i = 0
        pitch_list = []
        chord_list = []
        for line in lines:
            if (i >= 1):
                lst = line.split()
                if (i % 2 == 1):
                    pitch_list += lst
                else:
                    chord_list += lst
            i += 1
        pitch_length = len(pitch_list)
        for i in range(pitch_length):
            row = dict_pitch_id[dict_yinming[pitch_list[i]]]
            col = dict_chord_id[chord_list[i]]
            chord_matrix[row][col] += 1
    return norm_matrix(chord_matrix)

'''
file_list = ["D:\\大二上课程\\音乐与数学\\音数大作业\\流行的云.txt", "D:\\大二上课程\\音乐与数学\\音数大作业\\奇迹的山.txt"]
info1 = trans_1_order(file_list)
info2 = trans_2_order(file_list)
for x in info1.pitch:
    print(x)
print()
for x in info1.rhythm:
    print(x)
print()
for x in info2.pitch:
    print(x)
print()
for x in info2.rhythm:
    print(x)
print()
'''
