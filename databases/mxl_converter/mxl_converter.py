from music21 import *
from pathlib import *
import csv


def convert_mxl(path):

    # Parse the incoming Music XML file.
    global chord_to_use
    c = converter.parse(path)

    # Find all instrumental parts for the file.
    parts = c.parts
    res = [["bar", "beat", "chord", "note", "duration"]]

    for part in parts:

        try:
            # Obtain a list of all measures in a bar.
            measures = [x for x in part if isinstance(x, stream.Measure)]
            for measure in measures:
                chords = [x for x in measure.elements if isinstance(x, harmony.ChordSymbol)]
                if len(chords) > 0:
                    chord_to_use = chords[0]
                if not(isinstance(chord_to_use, harmony.ChordSymbol)):
                    chord_to_use = harmony.ChordSymbol()
                notes = [x for x in measure.elements if isinstance(x, note.Note)]
                for n in notes:
                    toAppend = [str(n.measureNumber), str(n.offset),
                        str(chord_to_use.figure), str(n.nameWithOctave),
                        str(n.duration.quarterLength)]
                    res.append(toAppend)

            # print(res)

            with open('csv_files/' + path.stem + '.csv', 'w') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerows(res)

            csvFile.close()

        except:
            c.show('text')

                # print(str(n.measureNumber) + "," + str(n.beat) + "," + str(chord_to_use.figure) + "," + str(n.nameWithOctave) + "," + str(n.duration))

    # print(part.elements)
    # print(part[0].elements)
    # measures = [x for x in part[0] if isinstance(x, stream.Measure)]
    # print(measures)
    # measure = measures[0]
    # print(measure.elements)
    # has_chord = False
    # for element in measure.elements:
    #     if (isinstance(element, harmony.ChordSymbol) and not(has_chord)):
    #         print(element)
    #         has_chord = True
    #     if (isinstance(element, note.Note)):
    #         print(element.name,element.measureNumber, element.beat - 1)


path_in = Path('mxl_files')
mxl_list = [x for x in path_in.iterdir() if x.suffix == '.mxl']
for mxl_file in mxl_list:
    convert_mxl(mxl_file)