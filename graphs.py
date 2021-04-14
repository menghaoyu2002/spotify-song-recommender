"""
Module for Song Graph
"""

from __future__ import annotations
import csv
from typing import Union
from get_property_ranges import get_property_ranges

# CONSTANT VALUES
PROPERTY_RANGES = get_property_ranges('data/20k_data.csv')


class _Song:
    """A class to represent a song containing attributes based on its qualities.

    Instance Attributes:
        - attributes: A dictionary mapping the name of the property of a song to its value.
        It must be in the form of
        attributes = {
                'name': str,
                'artist': str,
                'genre': str,
                'year': float,
                'bpm': float,
                'energy': float,
                'danceability': float(,
                'loudness': float,
                'liveness': float,
                'valence': float,
                'length': float,
                'acousticness': float,
                'speechiness': float,
                'popularity': float
            }
        - neighbors: a dictionary mapping songs that are adjacent to self to their respective
        similarity

    Representation Invariants:
        - self.attributes are in the format described in the docstring
        - self not in self.neighbors
        - all(self in v.neighbors for v in self._neighbours)
    """
    attributes: dict[str, Union[str, float]]
    neighbors: dict[_Song, float]

    def __init__(self, attributes: dict[str, Union[str, float]]):
        """Initialize a song."""
        self.attributes = attributes
        self.neighbors = {}

    def is_adjacent(self, other: _Song) -> bool:
        """Returns whether other is adjacent to self."""
        return other in self.neighbors

    def get_similarity(self, other: _Song) -> float:
        """Returns a number representing the similarity between self and other.

        Similarity is a percentage representing how similar of a song self is to other.
        It is calculated using a special algorithm.
        """
        sum_similarity = 0

        for p in self.attributes:
            if p != 'name' and p != 'artist' and p != 'genre':
                original_num = self.attributes[p]
                new_num = other.attributes[p]

                diff = abs(original_num - new_num)
                percent_diff = diff / PROPERTY_RANGES[p] * 100
                sum_similarity += 100 - percent_diff
            elif p == 'artist' or p == 'genre':
                sum_similarity += 100

        similarity = sum_similarity / (len(self.attributes) - 1)

        return similarity


class SongGraph:
    """A class to represent a graph of songs."""
    # Private Instance Attributes:
    #   - _vertices: a dictionary mapping a tuple of a song's name and artist to the _Song instance

    _vertices: dict[tuple[str, str], _Song]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, attributes: dict[str, Union[str, float]]) -> None:
        """Add a vertex to the graph. Do nothing if the song is already in the graph."""
        song = (attributes['name'], attributes['artist'])
        if song not in self._vertices:
            self._vertices[song] = _Song(attributes)

    def add_edge(self, song1: _Song, song2: _Song, similarity) -> None:
        """Add an edge between the two songs in this graph.

        Preconditions:
            - song1 != song2
            - song1 in self._vertices.values() and song2 in self._vertices.values()
        """
        song1.neighbors[song2] = similarity
        song2.neighbors[song1] = similarity

    def get_artists_by_song(self, name: str) -> list:
        """Returns a list of artist that have the song titled <name> in the graph."""
        return [artist for title, artist in self._vertices if name == title]

    def get_recommendations(self,
                            name: str,
                            artist: str,
                            num_songs: float,
                            similarity_threshold: float) -> list[tuple[str, str]]:
        """Returns a list of song/artist names that are similar to the given song.

        Each tuple of strings in the list represents a song. The first string is the song name, the
        second string is the song artist. The size of the list is <= to num_songs. All songs in
        the list must have a similarity score >= similarity_threshold. The songs in the list are
        sorted in descending order of similarity.

        Preconditions:
            - 0 <= similarity_threshold
            - 0 <= num_songs
        """
        if artist not in self.get_artists_by_song(name):
            return []

        lst_so_far = []
        x = 0
        for other in self._vertices.values():
            print(x)
            x += 1
            song = self._vertices[(name, artist)]
            if other == song:
                continue
            elif song.is_adjacent(other):
                similarity = song.neighbors[other]
            else:
                similarity = song.get_similarity(other)
                self.add_edge(song, other, similarity)

            _insert_song(lst_so_far, other, similarity)

        return _get_reformatted_songs(lst_so_far, num_songs, similarity_threshold)


def build_graph(songs_file: str) -> SongGraph:
    """Return a SongGraph with all the songs in song_file. Each vertex is a song
    represented by the _Song class.

    Preconditions:
        - songs_file is a is the path to a CSV file containing the data for spotify songs.
    """
    song_graph = SongGraph()

    with open(songs_file, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for line in reader:
            length = line[11]
            if length[1] == ',':
                length = length[0] + length[2:]

            attributes = {
                'name': line[1].lower(),
                'artist': line[2].lower(),
                'genre': line[3].lower(),
                'year': float(line[4]),
                'bpm': float(line[5]),
                'energy': float(line[6]),
                'danceability': float(line[7]),
                'loudness': float(line[8]),
                'liveness': float(line[9]),
                'valence': float(line[10]),
                'length': float(length),
                'acousticness': float(line[12]),
                'speechiness': float(line[13]),
                'popularity': float(line[14])
            }

            song_graph.add_vertex(attributes)

    return song_graph


def _insert_song(lst: list, other: _Song, similarity: float) -> None:
    """Mutate lst by inserting other so that all items are sorted in descending order by their
    similarity."""
    name = other.attributes['name']
    artist = other.attributes['artist']

    for i in range(0, len(lst)):
        if lst[i][1] < similarity:
            lst.insert(i, ((name, artist), similarity))
            return

    lst.append(((name, artist), similarity))


def _get_reformatted_songs(lst: list, num_songs: float, similarity_threshold) -> list[tuple[str, str]]:
    """Return a list of up to the first num_songs songs in lst. If the similarity is 0, then the
    song is not included in the list."""
    lst_so_far = []
    for song, similarity in lst:
        if similarity >= similarity_threshold:
            lst_so_far.append(song)
        if len(lst_so_far) == num_songs:
            return lst_so_far

    return lst_so_far
