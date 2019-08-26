import pandas as pd
import numpy as np

from pathlib import *

note_dict = {'A-': 11,
             'A': 0,
             'A#': 1,
             'B-': 1,
             'B': 2,
             'B#': 3,
             'C-': 2,
             'C': 3,
             'C#': 4,
             'D-': 4,
             'D': 5,
             'D#': 6,
             'E-': 6,
             'E': 7,
             'E#': 8,
             'F-': 7,
             'F': 8,
             'F#': 9,
             'G-': 9,
             'G': 10,
             'G#': 11}

global big_database
global unique_chords_global


def get_big_database():

    # Find the directory with all of the CSV files and extract the CSV files
    path = Path("../databases/EWLD/csv_files")
    csv_files = [x for x in path.iterdir() if x.suffix == '.csv']

    # Two data structures being defined here:
    #   1. The huge training set for our ML algorithm
    #   2. A set containing all the unique chords within this database.

    frames = []
    unique_chords = set([])

    for csv_file in csv_files:

        # Read the CSV file and append it to the big list.
        pd_csv = pd.read_csv(str(csv_file))
        frames.append(pd_csv)

        for chord in pd_csv["chord"]:

            # `unique_chords` is a set, so we're guaranteed that this method won't
            # add duplicates.

            unique_chords.add(chord)

    df = pd.concat(frames)
    df.to_pickle("the_big_dataframe.pkl")

    with open("unique_chords.txt", 'w') as toWrite:
        for x in unique_chords:

            toWrite.write(x + ",")

    return pd.concat(frames), unique_chords


def get_pitched_arrays():

    # Get the big pandas dataframe and initialise the dataframe to return.
    tup = get_big_database()
    database = tup[0]
    unique_chords = tup[1]
    chord_note_df = pd.DataFrame([], columns=['chord','A','A#','B','C','C#','D','D#','E','F','F#','G','G#'])

    # Create the template for each individual entry in our training dataset.
    to_add = []
    bar_count = 1
    note_count = 0
    chord_vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    empty_chord_vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for x in range(len(database) - 1):

        # Get the row from the big pandas dataframe.
        row = database.iloc[x]

        # Initialise `to_add`.
        if x == 0:
            to_add = [row['chord']]

        # If it's a new bar we reset.
        if row['bar'] != bar_count:

            if note_count > 0:
                for i, x in enumerate(chord_vector):
                    chord_vector[i] /= note_count

            to_add.extend(chord_vector)
            note_count = 0
            chord_vector = empty_chord_vector
            chord_note_df = chord_note_df.append\
                (pd.DataFrame([to_add], columns=['chord','A','A#','B','C','C#','D','D#','E','F','F#','G','G#']))
            bar_count = row['bar']
            to_add = [row['chord']]

        if len(row['note']) > 2:
            note = row['note'][0:2]
        else:
            note = row['note'][0:1]

        index = note_dict[note]
        chord_vector[index] += 1
        note_count += 1

    chord_note_df.to_pickle("chord_note_df.pkl")

    return(chord_note_df)


get_pitched_arrays()