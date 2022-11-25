import DataProcess as DP
import GenerateList as GL
import GenerateMusic as GM
import matplotlib.pyplot as plt
import numpy as np
file_list_similar = ['奇迹的山.txt', '流行的云.txt']
file_list_diff=['奇迹的山.txt', '流行的云.txt','卡农.txt']
chord_file_list = ['流行的云 和弦对应.txt']
output_file_list = ['马尔科夫\order_1_similar.mid', '马尔科夫\order_2_similar.mid', '马尔科夫\order_3_similar.mid',
                    '马尔科夫\order_1_diff.mid', '马尔科夫\order_2_diff.mid', '马尔科夫\order_3_diff.mid',

                    '马尔科夫\HMM.mid', '马尔科夫\interval.mid', 
                    '马尔科夫 - 多声部\combination(2).mid', '马尔科夫 - 多声部\combination(3).mid', '马尔科夫 - 多声部\combination(4).mid', 
                    
                    '马尔科夫 - 时值对齐\order_1_aligned.mid', '马尔科夫 - 时值对齐\order_2_aligned.mid', 
                    '马尔科夫 - 时值对齐\HMM_aligned.mid', '马尔科夫 - 时值对齐\interval_aligned.mid', 
                    '马尔科夫 - 时值对齐\combination(2).aligned.mid', '马尔科夫 - 时值对齐\combination(3).aligned.mid','马尔科夫 - 时值对齐\combination(4).aligned.mid',
                    '马尔科夫 - 自动和弦\HMM_auto_acmp.mid','马尔科夫 - 自动和弦\interval_auto_acmp.mid','马尔科夫 - 自动和弦\combination(3).auto_acmp.mid']
#-------------------------------采用相似乐曲------------------------------------#

# 生成一阶音高和节奏的矩阵
Info1 = DP.trans_1_order(file_list_similar)

# 生成二阶音高和节奏的矩阵
Info2 = DP.trans_2_order(file_list_similar)

# 生成三阶音高和节奏的矩阵
Info3 = DP.trans_3_order(file_list_similar)

# 生成和弦的马尔科夫矩阵
Chord_matrix = DP.chord_matrix(chord_file_list)


# 生成一阶音高列表
Pitch_List1 = GL.list_generate_1(Info1.pitch, 100)

# 生成一阶节奏列表
Rhythm_List1 = [DP.dict_id_rhythm[i]
                for i in GL.list_generate_1(Info1.rhythm, 100)]

# 生成一阶随机音乐mid文件
GM.MusicGen(Pitch_List1, Rhythm_List1,
            output_file_list[0], chord_name=['None'], base_num=[0], bpm=90, beat=4)


# 生成二阶音高列表
Pitch_List2 = GL.list_generate_2(Info2.pitch, 100, [])
print(Info2.pitch)
x=np.arange(0,16,1)

y=np.arange(0,16,1)
#z=Info2.pitch[x][y]
z=np.sin(x+y)
plt.plot(x,y,z)

# 生成二阶节奏列表
Rhythm_List2 = [DP.dict_id_rhythm[i]
                for i in GL.list_generate_2(Info2.rhythm, 100, [])]

# 生成二阶随机音乐mid文件
GM.MusicGen(Pitch_List2, Rhythm_List2, output_file_list[1],
            chord_name=['None'], base_num=[0], bpm=90, beat=4)


# 生成三阶音高列表
Pitch_List3 = GL.list_generate_3(Info3.pitch, 100, [])

# 生成三阶节奏列表
Rhythm_List3 = [DP.dict_id_rhythm[i]
                for i in GL.list_generate_3(Info3.rhythm, 100, [])]

# 生成三阶随机音乐mid文件
GM.MusicGen(Pitch_List3, Rhythm_List3, output_file_list[2],
            chord_name=['None'], base_num=[0], bpm=90, beat=4)

#-------------------------------采用差异较大的乐曲------------------------------------#


# 生成一阶音高和节奏的矩阵
Info4 = DP.trans_1_order(file_list_diff)

# 生成二阶音高和节奏的矩阵
Info5 = DP.trans_2_order(file_list_diff)

# 生成三阶音高和节奏的矩阵
Info6 = DP.trans_3_order(file_list_diff)


# 生成一阶音高列表
Pitch_List4 = GL.list_generate_1(Info4.pitch, 100)

# 生成一阶节奏列表
Rhythm_List4 = [DP.dict_id_rhythm[i]
                for i in GL.list_generate_1(Info4.rhythm, 100)]

# 生成一阶随机音乐mid文件
GM.MusicGen(Pitch_List4, Rhythm_List4,
            output_file_list[3], chord_name=['None'], base_num=[0], bpm=90, beat=4)


# 生成二阶音高列表
Pitch_List5 = GL.list_generate_2(Info5.pitch, 100, [])

# 生成二阶节奏列表
Rhythm_List5 = [DP.dict_id_rhythm[i]
                for i in GL.list_generate_2(Info5.rhythm, 100, [])]

# 生成二阶随机音乐mid文件
GM.MusicGen(Pitch_List5, Rhythm_List5, output_file_list[4],
            chord_name=['None'], base_num=[0], bpm=90, beat=4)


# 生成三阶音高列表
Pitch_List6 = GL.list_generate_3(Info6.pitch, 100, [])

# 生成三阶节奏列表
Rhythm_List6 = [DP.dict_id_rhythm[i]
                for i in GL.list_generate_3(Info6.rhythm, 100, [])]

# 生成三阶随机音乐mid文件
GM.MusicGen(Pitch_List6, Rhythm_List6, output_file_list[5],
            chord_name=['None'], base_num=[0], bpm=90, beat=4)


#-----------------------------------------------------------------------------------------------

# HMM生成音乐
hmm = DP.trans_HMM(file_list_similar, DP.dict_pitch_id, DP.dict_rhythm_id)
Pitch_list_hmm, Rhythm_list_hmm_id = GL.list_generate_HMM(hmm, 100)
Rhythm_list_hmm = [DP.dict_id_rhythm[i] for i in Rhythm_list_hmm_id]
GM.MusicGen(Pitch_list_hmm, Rhythm_list_hmm,
            output_file_list[6], chord_name=['None'], base_num=[0], bpm=90, beat=4)


# 音高时值束定生成音乐
Interval = DP.trans_interval(file_list_similar)
Pitch_list_interval, Rhythm_list_interval_id = GL.list_generate_interval(
    Interval.matrix, 100)
Rhythm_list_interval = [DP.dict_id_rhythm[i] for i in Rhythm_list_interval_id]

GM.MusicGen(Pitch_list_interval, Rhythm_list_interval,
            output_file_list[7], chord_name=['None'], base_num=[0], bpm=90, beat=4)

# 多声部
# chord_name 各个和弦名 ; base_num 各个声部高低八度偏置 ; Tonality 主音 ; bpm 节拍每分 ; beat 几拍一小节（强弱控制）
GM.MusicGen(Pitch_list_interval, Rhythm_list_interval, output_file_list[8],
            Pitch_List2=Pitch_list_hmm, Rhythm_List2=Rhythm_list_hmm,
            chord_name=['Octave', 'Octave'], base_num=[-1, -2], bpm=100, beat=4)
GM.MusicGen(Pitch_list_hmm, Rhythm_list_hmm, output_file_list[9],
            Pitch_List2=Pitch_list_interval, Rhythm_List2=Rhythm_list_interval,
            Pitch_List3=Pitch_List1,         Rhythm_List3=Rhythm_List1,
            chord_name=['Octave', 'Octave', 'None'], base_num=[-1, -2, -2], bpm=100, beat=4)
GM.MusicGen(Pitch_list_hmm, Rhythm_list_hmm, output_file_list[10],
            Pitch_List2=Pitch_list_interval, Rhythm_List2=Rhythm_list_interval,
            Pitch_List3=Pitch_List1,         Rhythm_List3=Rhythm_List1,
            Pitch_List4=Pitch_List2,         Rhythm_List4=Rhythm_List2,
            chord_name=['Octave', 'Octave', 'Octave', 'None'], base_num=[-1, -2, -3, -3], bpm=100, beat=4)

#对齐
Pitch_List1_aligned, Rhythm_List1_aligned = GL.align_note(
    Pitch_List1, Rhythm_List1, beat=4, Tonality='C5')
Pitch_List2_aligned, Rhythm_List2_aligned = GL.align_note(
    Pitch_List2, Rhythm_List2, beat=4, Tonality='C5')
Pitch_list_interval_aligned, Rhythm_list_interval_aligned = GL.align_note(
    Pitch_list_interval, Rhythm_list_interval, beat=4, Tonality='C5')
Pitch_list_hmm_aligned, Rhythm_list_hmm_aligned = GL.align_note(
    Pitch_list_hmm, Rhythm_list_hmm, beat=4, Tonality='C5')

GM.MusicGen(Pitch_List1_aligned, Rhythm_List1_aligned,
            output_file_list[11], chord_name=['None'], base_num=[0], bpm=100, beat=4)
GM.MusicGen(Pitch_List2_aligned, Rhythm_List2_aligned, 
            output_file_list[12], chord_name=['None'], base_num=[0], bpm=100, beat=4)
GM.MusicGen(Pitch_list_hmm_aligned, Rhythm_list_hmm_aligned,
            output_file_list[13], chord_name=['None'], base_num=[0], bpm=100, beat=4)
GM.MusicGen(Pitch_list_interval_aligned, Rhythm_list_interval_aligned,
            output_file_list[14], chord_name=['None'], base_num=[0], bpm=100, beat=4)
# 各声部内部对齐的多声部
GM.MusicGen(Pitch_list_interval_aligned, Rhythm_list_interval_aligned, output_file_list[15],
            Pitch_List2=Pitch_list_hmm_aligned, Rhythm_List2=Rhythm_list_hmm_aligned,
            chord_name=['Octave', 'Octave'], base_num=[-1, -2], 
            tensity=[100,80], bpm=100, beat=4)
GM.MusicGen(Pitch_list_hmm_aligned, Rhythm_list_hmm_aligned, output_file_list[16],
            Pitch_List2=Pitch_list_interval_aligned, Rhythm_List2=Rhythm_list_interval_aligned,
            Pitch_List3=Pitch_List1_aligned,         Rhythm_List3=Rhythm_List1_aligned,
            chord_name=['Octave', 'Octave', 'Octave'], base_num=[-1, -2, -3],
            tensity=[100,80,80], bpm=100, beat=4)
GM.MusicGen(Pitch_list_hmm_aligned, Rhythm_list_hmm_aligned, output_file_list[17],
            Pitch_List2=Pitch_list_interval_aligned, Rhythm_List2=Rhythm_list_interval_aligned,
            Pitch_List3=Pitch_List1_aligned,         Rhythm_List3=Rhythm_List1_aligned,
            Pitch_List4=Pitch_List2_aligned,         Rhythm_List4=Rhythm_List2_aligned,
            chord_name=['Octave', 'Octave', 'Octave', 'Octave'], base_num=[-1, -2, -3, -4],
            tensity=[100,80,60,60], bpm=100, beat=4)

#自动伴奏
hmm_pitch_acmp,hmm_rhythm_acmp=GL.AcmpnyGen(Pitch_list_hmm_aligned,Rhythm_list_hmm_aligned,Chord_matrix,Tonality='C5',beat=4)
print(Pitch_list_hmm_aligned , "\n",Rhythm_list_hmm_aligned)
for i in range(len(Rhythm_list_hmm_aligned)):
    print(DP.dict_id_pitch[Pitch_list_hmm_aligned[i]],Rhythm_list_hmm_aligned[i])
print("\n")
print(hmm_pitch_acmp)
GM.MusicGen(Pitch_list_hmm_aligned, Rhythm_list_hmm_aligned, output_file_list[18],
            Pitch_list_chord=hmm_pitch_acmp, Rhythm_list_chord=hmm_rhythm_acmp,
            chord_name=['Octave'], base_num=[-1, 0,0,0,-2], 
            tensity=[100,0,0,0,50], bpm=100, beat=4)

interval_pitch_acmp,interval_rhythm_acmp=GL.AcmpnyGen(Pitch_list_interval,Rhythm_list_interval,Chord_matrix,Tonality='C5',beat=4)
GM.MusicGen(Pitch_list_interval_aligned, Rhythm_list_interval_aligned, output_file_list[19],
            Pitch_list_chord=interval_pitch_acmp, Rhythm_list_chord=interval_rhythm_acmp,
            chord_name=['Octave'], base_num=[-1, 0,0,0,-2], 
            tensity=[100,0,0,0,50], bpm=100, beat=4)

GM.MusicGen(Pitch_list_hmm_aligned, Rhythm_list_hmm_aligned, output_file_list[20],
            Pitch_List2=Pitch_list_interval_aligned, Rhythm_List2=Rhythm_list_interval_aligned,
            Pitch_list_chord=hmm_pitch_acmp,         Rhythm_list_chord=hmm_rhythm_acmp,
            chord_name=['Octave', 'Octave'], base_num=[-1, -2, 0,0,-2],
            tensity=[100,80,0,0,50], bpm=100, beat=4)