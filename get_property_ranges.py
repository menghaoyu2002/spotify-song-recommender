"""
A Module containing a function to get the ranges of each numeric property of a song in a file.
"""
import csv
import math


def get_property_ranges(songs_file: str) -> dict[str, int]:
    """Returns a dictionary mapping each numeric property of a song to the range of that property
    in the songs_file.

    Preconditions:
        - songs_file is a is the path to a CSV file containing the data for spotify songs.
    """
    n_inf = -math.inf
    inf = math.inf
    dict_values = [[inf, n_inf], [inf, n_inf], [inf, n_inf], [inf, n_inf], [inf, n_inf],
                   [inf, n_inf], [inf, n_inf], [inf, n_inf], [inf, n_inf], [inf, n_inf],
                   [inf, n_inf]]

    with open(songs_file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for line in reader:
            for i in range(11):
                if i == 7 and line[11][1] == ',':
                    val = int(line[11][0] + line[11][2:])
                else:
                    val = int(line[i + 4])

                if val < dict_values[i][0]:
                    dict_values[i][0] = val
                elif val > dict_values[i][1]:
                    dict_values[i][1] = val

    return {
        'year': abs(dict_values[0][0] - dict_values[0][1]),
        'bpm': abs(dict_values[1][0] - dict_values[1][1]),
        'energy': abs(dict_values[2][0] - dict_values[2][1]),
        'danceability': abs(dict_values[3][0] - dict_values[3][1]),
        'loudness': abs(dict_values[4][0] - dict_values[4][1]),
        'liveness': abs(dict_values[5][0] - dict_values[5][1]),
        'valence': abs(dict_values[6][0] - dict_values[6][1]),
        'length': abs(dict_values[7][0] - dict_values[7][1]),
        'acousticness': abs(dict_values[8][0] - dict_values[8][1]),
        'speechiness': abs(dict_values[9][0] - dict_values[9][1]),
        'popularity': abs(dict_values[10][0] - dict_values[10][1])
    }
