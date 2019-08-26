from keras.models import Model, Sequential
from keras.layers import Input, LSTM, Dense, Dropout, Activation, TimeDistributed
from keras.optimizers import Adam
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

from PSCA.chord_wrangling import handle_chord

chords = 'C Cm Caug Cdim Csus C# C#m C#aug C#dim C#sus D Dm Daug Ddim Dsus D# D#m D#aug D#dim D#sus E Em Eaug Edim Esus F Fm Faug Fdim Fsus F# F#m F#aug F#dim F#sus G Gm Gaug Gdim Gsus G# G#m G#aug G#dim G#sus A Am Aaug Adim Asus A# A#m A#aug A#dim A#sus B Bm Baug Bdim Bsus'.split()


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

batch_size = 16
epochs = 8
lstm_units = 64
dropout = 0.2
sequence_length = 4

chord_note_df = pd.read_pickle("~/comp2560/PSCA/chord_note_df.pkl")

unique_chord_dict = dict()

for count, chord in enumerate(chords):
    unique_chord_dict[chord] = int(count)

x = np.zeros((len(chord_note_df), sequence_length, 12), dtype='float32')
y = np.zeros((len(chord_note_df), sequence_length, len(chords)), dtype='int')

for i in range(0, len(chord_note_df) - sequence_length):

    x[i][0] = np.array(chord_note_df.iloc[i, 1:])
    matrix_index = unique_chord_dict[handle_chord(chord_note_df.iloc[i, 0])]
    y[i][0][matrix_index] = 1

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.33, random_state=42
)

print(x_train)
print(y_train)

model = Sequential()

model.add(LSTM(lstm_units, input_shape=(sequence_length, 12), return_sequences=True))
model.add(Dropout(dropout))
model.add(LSTM(lstm_units, go_backwards=True, return_sequences=True))
model.add(Dropout(dropout))
model.add(LSTM(lstm_units, return_sequences=True))
model.add(Dropout(dropout))
model.add(LSTM(lstm_units, go_backwards=True, return_sequences=True))
model.add(Dropout(dropout))
model.add(TimeDistributed(Dense(len(chords))))
model.add(Activation('softmax'))

optimizer = Adam()
model.compile(loss='categorical_crossentropy', optimizer=optimizer,metrics=['acc'])

history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=[x_test, y_test])

# plot the data from history.history['loss', 'acc'].

model.save('cc_draft.h5')

score = model.evaluate(x_test, y_test)
print("SCORE: ", score)

# SCORES:
#
# Mean Squared Error Basic LSTM: 140,000 (roundabouts) loss, very low accuracy
#
# Categorical Crossentropy Basic LSTM: loss 3.483, accuracy 0.231 (better!)
#
# Categorical Crossentropy 10-Epoch LSTM (as opposed to 5 epochs):
#       loss 3.342, accuracy 0.255 (even better - seems like 8 epochs was the plateau though)
#
# Categorical Crossentropy 64-Layer LSTM (as opposed to 32 layers):
#       loss 3.340, accuracy 0.256 (the best so far - not sure whether perfect fit of layers lies
#       within (32, 64] or somewhere higher)
#
# Categorical Crossentropy 8-Epoch 64-Layer LSTM:
#       loss 3.217, accuracy 0.278 (such an improvement!!)

