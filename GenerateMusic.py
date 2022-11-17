from mido import Message, MidiFile, MidiTrack
import DataProcess as DP
import random
name2num = {
    '0': 0,
    '#C3': 1,
    'bD3': 1,
    'D3': 2,
    '#D3': 3,
    'bE3': 3,
    'E3': 4,
    'F3': 5,
    '#F3': 6,
    'bG3': 6,
    'G3': 7,
    '#G3': 8,
    'bA3': 8,
    'A3': 9,
    '#A3': 10,
    'bB3': 10,
    'B3': 11,
    'C4': 12,
    '#C4': 13,
    'bD4': 13,
    'D4': 14,
    '#D4': 15,
    'bE4': 15,
    'E4': 16,
    'F4': 17,
    '#F4': 18,
    'bG4': 18,
    'G4': 19,
    '#G4': 20,
    'bA4': 20,
    'A4': 21,
    '#A4': 22,
    'bB4': 22,
    'B4': 23,
    'C5': 24,
    '#C5': 25,
    'bD5': 25,
    'D5': 26,
    '#D5': 27,
    'bE5': 27,
    'E5': 28,
    'F5': 29,
    '#F5': 30,
    'bG5': 30,
    'G5': 31,
    '#G5': 32,
    'bA5': 32,
    'A5': 33,
    '#A5': 34,
    'bB5': 34,
    'B5': 35,
    'C6': 36,
    '#C6': 37,
    'bD6': 37,
    'D6': 38,
    '#D6': 39,
    'bE6': 39,
    'E6': 40,
    'F6': 41,
    '#F6': 42,
    'bG6': 42,
    'G6': 43,
    '#G6': 44,
    'bA6': 44,
    'A6': 45,
    '#A6': 46,
    'bB6': 46,
    'B6': 47,
    'C7': 48
}
num2name = {num: name for name, num in name2num.items()}


def get_chord(name):
    chord = {
        "None": [0],  # 单音
        "Octave": [0, 12],  # 八度
        'Pentatonic': [0, 6],  # 五度
        'Quartet': [0, 5],  # 四度
        "Major3": [0, 4, 7, 12],  # 大三和弦
        "Minor3": [0, 3, 7, 12],  # 小三和弦
        "Augmented3": [0, 4, 8, 12],  # 增三和弦
        "Diminished3": [0, 3, 6, 12],  # 减三和弦

        "M7": [0, 4, 7, 11],  # 大七和弦
        "Mm7": [0, 4, 7, 10],  # 属七和弦
        "m7": [0, 3, 7, 10],  # 小七和弦
        "mM7": [0, 3, 7, 12]  # 大小七和弦
        # To be added......
    }
    return chord[name]


def play_note(note, length, track, bpm, chord_name='None', base_num=0, delay=0, velocity=1.0, channel=0):
    meta_time = 60 / bpm * 1000  # 一拍毫秒数
    base_note = 60  # C4偏置值
    for i in get_chord(chord_name):
        note1 = note + i
        print(num2name[note1])
        if note != 0:
            track.append(Message('note_on', note=base_note + base_num*12 + note1,
                         velocity=round(64*velocity-15+2*i), time=round(meta_time*delay), channel=channel))
    if note != 0:
        track.append(Message('note_off', note=base_note + base_num*12 + note1,
                             velocity=round(64*velocity), time=round(meta_time*length), channel=channel))
    else:  # 休止符
        track.append(Message('note_off', time=round(
            meta_time*length), note=0, channel=channel))


def MusicGen(Pitch_List, Rythm_List, filename, chord_name='None', base_num=0, Tonality='C5', bpm=60, beat=4):
    print(Rythm_List)
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    length = len(Pitch_List)
    total_length = float(0)
    tensity = float(80)
    for i in range(length):
        print(DP.dict_id_pitch[Pitch_List[i]])
        if i < tensity * 0.25:
            tensity += 0.9
        elif i < tensity * 0.5:
            tensity -= 0.8
        elif i < tensity * 0.77:
            tensity += 1
        else:
            tensity -= 0.8

        index = 1
        ini_grp = total_length//beat
        if total_length % beat == 2 and beat % 4 == 0:
            index = 1.08
        elif total_length % beat == (beat/2):
            index = 1.12
        elif total_length % beat == 0:
            index = 1.23
        else:
            index = 0.75
        new_grp = total_length//beat

        total_length += float(Rythm_List[i])
        """跨小节的音与后方音高相同直接连上"""
        if (i < length-1) and (int(new_grp) == int(ini_grp)+1) and (Pitch_List[i] == Pitch_List[i+1]):
            total_length += float(Rythm_List[i+1])
            play_note(name2num[DP.dict_id_pitch[Pitch_List[i]]], float(
                Rythm_List[i])+float(Rythm_List[i+1]), track, bpm, chord_name=chord_name, base_num=base_num, velocity=tensity*index/100)
            i += 1
            """跨小节的音与后方不同，用主音先补成一小节,后方的音顺延"""
        elif (i < length-1) and (int(new_grp) == int(ini_grp)+1) and (Pitch_List[i] != Pitch_List[i+1]) and (abs(name2num[DP.dict_id_pitch[Pitch_List[i]]]-name2num[Tonality]) < random.randint(0, 8)):
            play_note(name2num[DP.dict_id_pitch[Pitch_List[i]]], float(
                Rythm_List[i]), track, bpm, velocity=tensity*index/100, chord_name=chord_name, base_num=base_num)
            play_note(name2num[Tonality], float(new_grp*beat) + beat -
                      float(total_length), track, bpm, velocity=tensity*0.8/100, chord_name=chord_name, base_num=base_num)
            """正常情况"""
        else:
            play_note(name2num[DP.dict_id_pitch[Pitch_List[i]]], float(
                Rythm_List[i]), track, bpm, velocity=tensity*index/100, chord_name=chord_name, base_num=base_num)
    play_note(name2num[Tonality], float(beat), track, bpm,
              chord_name=chord_name, base_num=base_num)
    mid.save(filename)
