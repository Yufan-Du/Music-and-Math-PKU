import DataProcess as DP
import random
import numpy as np
import GenerateMusic as GM

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

# 三阶生成：
# 输入：
# matrix：四层list N*N*N*N的马尔科夫矩阵，
# list_len：希望得到的列表长度
# start_note：初始列表,留空为随机
def list_generate_3(matrix, list_len, start_note_list):
    mat_size = len(matrix)
    while len(start_note_list) < 3:
        start_note_list.insert(0, random.randint(0, mat_size - 1))
    note_list = start_note_list
    for i in range(1, list_len):
        if sum(matrix[note_list[-3]][note_list[-2]][note_list[-1]]) != 0:
            cur_note = np.random.choice(range(mat_size), 1, p=matrix[note_list[-3]][note_list[-2]][note_list[-1]])[0]
        else:
            cur_note = np.random.choice(range(mat_size), 1)[0]
        note_list.append(cur_note)
    return note_list

# 音阶时值绑定生成：
# 输入：
# matrix：NM*NM的状态转移矩阵
# list_len：希望得到的列表长度
# start_state：初始列表，-1为随机
def list_generate_interval(matrix, list_len, start_state = -1):
    mat_size = len(matrix)
    if start_state >= mat_size or start_state < 0:
        cur_state = random.randint(0, list_len - 1) % mat_size
    else:
        cur_state = start_state
    state_list = [cur_state]
    pitch, rhythm = DP.state2note(cur_state)
    pitch_list = [pitch]
    rhythm_list = [rhythm]
    for i in range(1, list_len):
        if sum(matrix[cur_state]) != 0:
            cur_state = np.random.choice(range(mat_size), 1, p=matrix[cur_state])[0]
        else:
            cur_state = np.random.choice(range(mat_size), 1)[0]
        state_list.append(cur_state)
        pitch, rhythm = DP.state2note(cur_state)
        pitch_list.append(pitch)
        rhythm_list.append(rhythm)

    return pitch_list, rhythm_list

# HMM
# 输入：
# hmm: 隐含马尔可夫模型模型
# list_len: 希望得到的列表长度
# start_note: 初始列表，-1为随机
def list_generate_HMM(hmm, list_len, start_note = -1):
    trans = hmm.transition_matrix
    conf = hmm.confusion_matrix

    N = len(trans) #总状态数
    M = len(conf[0]) #总观测量数

    if start_note >= N or start_note < 0:
        cur_note = random.randint(0, list_len - 1) % len(trans)
    else:
        cur_note = start_note
    cur_duration = np.random.choice(range(M),1, p = conf[cur_note])[0]
    
    note_list = [cur_note]
    duration_list = [cur_duration]

    for i in range(1, list_len):
        if sum(trans[cur_note]) != 0:
            cur_note = np.random.choice(range(N), 1, p=trans[cur_note])[0]
        else:
            cur_note = np.random.choice(range(N), 1)[0]
        note_list.append(cur_note)

        if sum(conf[cur_note]) != 0:
            cur_duration = np.random.choice(range(M), 1, p = conf[cur_note])[0]
        else:
            cur_duration = np.random.choice(range(M),1)[0]
        duration_list.append(cur_duration)
        
    return note_list, duration_list

def align_note(Pitch_List_,Rythm_List_,beat=4,Tonality='C5'):
    Pitch_List=Pitch_List_.copy()
    Rythm_List=Rythm_List_.copy()
    length = len(Pitch_List)
    total_length = float(0)
    note_list_aligned=[]
    rhythm_list_aligned=[]
    i=0
    while i<length:
        ini_grp = total_length//beat
        total_length += float(Rythm_List[i])
        new_grp = total_length//beat

        """跨小节的音与后方音高相同直接连上"""
        if (i < length-1) and (int(new_grp) == int(ini_grp)+1) and (Pitch_List[i] == Pitch_List[i+1]):
            #print("case1",end=" ")
            total_length += float(Rythm_List[i+1])
            note_list_aligned.append(Pitch_List[i])
            rhythm_list_aligned.append(str(float(Rythm_List[i]) + float(Rythm_List[i+1])))
            i += 1
            """跨小节的音与后方不同，用主音先补成一小节,后方的音顺延"""
        elif (i < length-1) and (int(new_grp) == int(ini_grp)+1) and (Pitch_List[i] != Pitch_List[i+1]) and\
        (abs(GM.name2num[DP.dict_id_pitch[Pitch_List[i]]]-GM.name2num[Tonality]) + \
        abs(GM.name2num[DP.dict_id_pitch[Pitch_List[i+1]]]-GM.name2num[Tonality])) < random.randint(0,12):
            #print("case2",end=" ")
            note_list_aligned.append(Pitch_List[i])
            rhythm_list_aligned.append(Rythm_List[i])
            note_list_aligned.append(DP.dict_pitch_id[Tonality])
            rhythm_list_aligned.append(str(float(new_grp*beat) + beat -float(total_length)))
            total_length=new_grp*beat + beat
            """正常情况"""
        else:
            #print("case3",end=" ")
            note_list_aligned.append(Pitch_List[i])
            rhythm_list_aligned.append(Rythm_List[i])
        i+=1
    """结尾主音"""
    note_list_aligned.append(DP.dict_pitch_id[Tonality])
    rhythm_list_aligned.append(str(beat))
    return note_list_aligned, rhythm_list_aligned

#根据和弦矩阵自动生成副声部和弦，若不存在已有的信息，则根据小节第一个音来生成
def AcmpnyGen(Pitch_List,Rythm_List,chord_matrix,Tonality='C5',beat=4):
    length=len(Pitch_List)
    i=0
    acmp_pitch_list=[]
    acmp_rhythm_list=[]
    pitch_layout=[]
    chord_num=len(chord_matrix[0])
    while i<length:
        for j in range(int(float(Rythm_List[i])*4)):
            pitch_layout.append(Pitch_List[i])
        i+=1
    grp=0
    last_grp=(sum(float(x) for x in Rythm_List)-1)//beat -1 
    while grp<=last_grp:
        cur_pitch=pitch_layout[grp*2*beat]
        if sum(chord_matrix[cur_pitch]) != 0:
            cur_chord = np.random.choice(range(chord_num), 1, p=chord_matrix[cur_pitch])[0]
        else:
            cur_chord = np.random.choice(range(chord_num), 1)[0] if random.randint(1, 100)<50 else 0
        acmp_pitch_list.append(DP.dict_id_chord[cur_chord])
        acmp_rhythm_list.append(str(beat))
        grp+=1
    return acmp_pitch_list,acmp_rhythm_list