from mido import Message, MidiFile, MidiTrack
import DataProcess as DP
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

dict_chord_play = {
    "None":[0,"None","None"],
    "Am": [13,"A4","Minor3"],
    "Dm": [9,"D4","Minor3"],
    "C": [8,"C4","Major3"],
    "G": [12,"G4","Major3"],
    "F": [11,"F4","Major3"]
    }

def get_chord(name):
    chord = {
        "None": [0],  # 单音
        "Octave": [0, 12],  # 八度
        'Pentatonic': [0, 6, 12],  # 五度
        'Quartet': [0, 5, 12],  # 四度
        "Major3": [0, 4, 7, 12],  # 大三和弦
        "Minor3": [0, 3, 7, 12],  # 小三和弦
        "Augmented3": [0, 4, 8, 12],  # 增三和弦
        "Diminished3": [0, 3, 6, 12],  # 减三和弦

        "M7": [0, 4, 7, 11, 12],  # 大七和弦
        "Mm7": [0, 4, 7, 10, 12],  # 属七和弦
        "m7": [0, 3, 7, 10, 12],  # 小七和弦
        "mM7": [0, 3, 7, 12]  # 大小七和弦
        # To be added......
    }
    return chord[name]


def play_note(note, length, track, bpm, chord_name='None', base_num=0, delay=0, velocity=1.0, channel=0):
    meta_time = 60 / bpm * 1000  # 一拍毫秒数
    base_note = 60  # C4偏置值
    for i in get_chord(chord_name):
        note1 = note + i
        # print(num2name[note1])
        if note != 0:
            track.append(Message('note_on', note=base_note + base_num*12 + note1,
                         velocity=round(64*velocity-10+2*i), time=round(meta_time*delay), channel=channel))
    if note != 0:
        track.append(Message('note_off', note=base_note + base_num*12 + note1,
                             velocity=round(64*velocity), time=round(meta_time*length), channel=channel))
    else:  # 休止符
        track.append(Message('note_off', time=round(
            meta_time*length), note=0, channel=channel))


def MusicGen(Pitch_List, Rythm_List, filename, Pitch_list_chord=[],Rhythm_list_chord=[],
Pitch_List4=[], Rhythm_List4=[], Pitch_List3=[], Rhythm_List3=[], Pitch_List2=[], Rhythm_List2=[], 
chord_name=['None'], base_num=[0], tensity=[100,80,80,80,80], bpm=60, beat=4):
    # print(Rythm_List)
    mid = MidiFile()
    track = MidiTrack()
    track2 = MidiTrack()
    track3 = MidiTrack()
    track4 = MidiTrack()
    track5 = MidiTrack()
    length = len(Pitch_List)
    length2 = len(Pitch_List2)
    length3 = len(Pitch_List3)
    length4 = len(Pitch_List4)
    length5 = len(Pitch_list_chord)
    """Track_chord"""
    for i in range(length5):
        play_note(name2num[DP.dict_id_pitch[dict_chord_play[Pitch_list_chord[i]][0]]], float(
            Rhythm_list_chord[i]), track5, bpm, velocity=tensity[4]/100, chord_name=dict_chord_play[Pitch_list_chord[i]][2], base_num=base_num[4])

    total_length = float(0)
    """Track4"""
    for i in range(length4):
        index = 1
        """节拍强弱控制"""
        if total_length % beat == 2 and beat % 4 == 0:
            index = 1.11
        elif total_length % beat == (beat/2):
            index = 1.11
        elif total_length % beat == 0:
            index = 1.25
        else:
            index = 0.8
        total_length += float(Rhythm_List4[i])
        play_note(name2num[DP.dict_id_pitch[Pitch_List4[i]]], float(
            Rhythm_List4[i]), track4, bpm, velocity=tensity[3]*index/100, chord_name=chord_name[3], base_num=base_num[3])
    """Track3"""
    total_length = float(0)
    for i in range(length3):
        index = 1
        """节拍强弱控制"""
        if total_length % beat == 2 and beat % 4 == 0:
            index = 1.11
        elif total_length % beat == (beat/2):
            index = 1.11
        elif total_length % beat == 0:
            index = 1.25
        else:
            index = 0.8
        total_length += float(Rhythm_List3[i])
        play_note(name2num[DP.dict_id_pitch[Pitch_List3[i]]], float(
            Rhythm_List3[i]), track3, bpm, velocity=tensity[2]*index/100, chord_name=chord_name[2], base_num=base_num[2])
    """Track2"""
    total_length = float(0)
    for i in range(length2):
        index = 1
        """节拍强弱控制"""
        if total_length % beat == 2 and beat % 4 == 0:
            index = 1.11
        elif total_length % beat == (beat/2):
            index = 1.11
        elif total_length % beat == 0:
            index = 1.25
        else:
            index = 0.8
        total_length += float(Rhythm_List2[i])
        play_note(name2num[DP.dict_id_pitch[Pitch_List2[i]]], float(
            Rhythm_List2[i]), track2, bpm, velocity=tensity[1]*index/100, chord_name=chord_name[1], base_num=base_num[1])
    """Track1"""
    total_length = float(0)
    tensity = float(tensity[0])
    for i in range(length):
        # print(DP.dict_id_pitch[Pitch_List[i]])
        """节拍强弱控制"""
        if total_length % beat == 2 and beat % 4 == 0:
            index = 1.11
        elif total_length % beat == (beat/2):
            index = 1.11
        elif total_length % beat == 0:
            index = 1.25
        else:
            index = 0.8
        total_length += float(Rythm_List[i])
        play_note(name2num[DP.dict_id_pitch[Pitch_List[i]]], float(
            Rythm_List[i]), track, bpm, velocity=tensity*index/100, chord_name=chord_name[0], base_num=base_num[0])

    mid.tracks.append(track)
    if length2:
        mid.tracks.append(track2)
    if length3:
        mid.tracks.append(track3)
    if length4:
        mid.tracks.append(track4)
    if length5:
        mid.tracks.append(track5)
    mid.save(filename)
