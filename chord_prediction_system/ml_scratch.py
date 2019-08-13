from keras.models import Model
from keras.layers import Input, LSTM, Dense
import pandas as pd

latent_dim = 256
big_database = pd.read_pickle("the_big_dataframe.pkl")
chord_note_df = pd.read_pickle("chord_note_df.pkl")

with open("unique_chords.txt", "r") as uc:
    unique_chords = uc.read().split(",")

testing_length = len(big_database) - len(big_database) / 10

encoder_inputs = Input()
encoder = LSTM(return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)

encoder_states = [state_h, state_c]

decoder_inputs = Input()
