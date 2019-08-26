import random

chords = 'C Cm Caug Cdim Csus C# C#m C#aug C#dim C#sus D Dm Daug Ddim Dsus D# D#m D#aug D#dim D#sus E Em Eaug Edim Esus F Fm Faug Fdim Fsus F# F#m F#aug F#dim F#sus G Gm Gaug Gdim Gsus G# G#m G#aug G#dim G#sus A Am Aaug Adim Asus A# A#m A#aug A#dim A#sus B Bm Baug Bdim Bsus ENDTOKEN'.split()

note_dict = {'A': 0,
             'A#': 1,
             'B': 2,
             'C': 3,
             'C#': 4,
             'D': 5,
             'D#': 6,
             'E': 7,
             'F': 8,
             'F#': 9,
             'G': 10,
             'G#': 11
             }


def trim_chord(chord: str, input_string: str, offset: int, to_add: str):
    #print("Handling string ", input_string, " in chord ", chord)
    if input_string in chord:
        index = chord.find(input_string)
        return chord[:index + offset] + to_add
    else:
        return chord


def handle_chord(chord : str):
    length = len(chord)

    if length <= 1: # can only be a major chord
        return chord

    for input_string in ['/', 'power', 'pedal', ' add', 'maj', '6', '9', '11', '13', ' alter']:
        chord = trim_chord(chord, input_string, 0, '')

    if '-' in chord:
        entry = int(note_dict[chord[0]])
        entry -= 1
        if (entry < 0):
            entry += 12
        out = list(note_dict.keys())[entry]
        chord = out + chord[2:]

    chord = trim_chord(chord, 'dim', 3, '')
    chord = trim_chord(chord, 'o', 0, 'dim')
    chord = trim_chord(chord, '7+', 0, 'aug')
    chord = trim_chord(chord, '7', 0, '')
    chord = trim_chord(chord, '+', 0, 'aug')
    chord = trim_chord(chord, 'M', 0, '')
    chord = trim_chord(chord, '2', 0, '')
    chord = trim_chord(chord, '4', 0, '')

    if 'b' in chord:
        entry = int(note_dict[chord[0]])
        entry -= 1
        if (entry < 0):
            entry += 12
        out = list(note_dict.keys())[entry]
        chord = out + chord[2:]

    if '#' in chord and '-' in chord:
        chord = chord[:2]

    if chord == 'N.C.' or len(chord) == 0:
        chord = chords[random.randint(0, len(chords))]

    return chord


# with open("unique_chords.txt", "r") as uc:
#     reader = uc.read()
#     unique_chords = reader.split(",")
#     unique_set = set([handle_chord(chord) for chord in unique_chords if not handle_chord(chord) == 'N.C.' and len(handle_chord(chord)) > 0])
#     print(unique_set)