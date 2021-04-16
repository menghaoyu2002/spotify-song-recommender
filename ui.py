"""
A Module which is responsible for the user interface
"""
from __future__ import annotations
import tkinter as tk
from tkinter.font import BOLD
from graphs import SongGraph

# Constants
BG_COLOUR = 'gray10'
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600


class Page:
    """ an abstract class representing a single page in the application"""

    # Private Instance Attributes:
    #   - _frame: the object which the page will be displayed on
    #   - _ui: the user interface object which will be mutated by the page

    _frame: tk.Tk
    _ui: UserInterface

    def __init__(self, frame: tk.Tk, user_interface: UserInterface) -> None:
        """Initialize the page"""
        self._frame = frame
        self._ui = user_interface

    def show_page(self, truth: bool) -> None:
        """Make the current page visible or invisible based on truth

        the page is visible if and only if truth == true
        """
        raise NotImplementedError


class UserInterface:
    """A class representing the main user interface

    Instance Attributes:
    '   - mainframe: the main frame which all graphical elements will be displayed on
        - search_variable: the StringVar object representing the name of the song being
                           searched for
        - graph: the SongGraph which will be used to search for the songs and
                 get recommendations
        - home_page: the homepage of the user interface
        - results_page: the page which will display the results of the search
        - recommend_page: the page which is responsible for displaying the recommendations
                          for the given song and artist combination
    """
    mainframe: tk.Tk
    search_variable: tk.StringVar
    graph: SongGraph
    home_page: HomePage
    results_page: ResultsPage
    recommend_page: RecommendationsPage

    # Private Attributes:
    #   -_current_page: the current page which is being displayed
    _current_page: Page

    def __init__(self, root: tk.Tk, graph: SongGraph) -> None:
        """Initialize the user interface"""
        self.mainframe = root
        self.mainframe.title('Spotify Song Recommender')
        self.graph = graph

        # Initializing the pages
        self.search_variable = tk.StringVar()
        self.home_page = HomePage(self.mainframe, self, self.search_variable)
        self.results_page = ResultsPage(self.mainframe, self, self.search_variable)
        self.recommend_page = RecommendationsPage(self.mainframe, self)

        self._current_page = self.home_page
        self._current_page.show_page(True)

    def change_current_page(self, page: Page) -> None:
        """Change the current page to <page> and display it"""
        self._current_page.show_page(False)
        self._current_page = page
        self._current_page.show_page(True)

        
class HomePage(Page):
    """A class representing the Homepage of the application"""

    # Private Instance Attributes:
    #   - _frame: the object which the page will be displayed on
    #   - _ui: the user interface object which will be mutated by the page
    #   -_search_variable: a tk.StringVar representing the name of the song
    #   -_text: a element of the page which displays the main text
    #   -_search_field: a element of the page which allows the user
    #                   to enter song names
    #   - _submit_button: a button on the page which allows the user to submit
    #                     their song name
    #   -_error_message: an error message which will be displayed when the
    #                    song is not found

    _frame: tk.Tk
    _ui: UserInterface
    _search_variable: tk.StringVar
    _text: tk.Label
    _search_field: tk.Entry
    _submit_button: tk.Button
    _error_message: tk.Label

    def __init__(self,
                 frame: tk.Tk,
                 user_interface: UserInterface,
                 search_variable: tk.StringVar) -> None:
        """Initialize the homepage and all it's elements"""
        Page.__init__(self, frame, user_interface)
        self._search_variable = search_variable

        # Page Elements
        self._text = tk.Label(self._frame,
                              text='Search for a Song!',
                              bg=BG_COLOUR,
                              fg='gray95',
                              font=('arialnarrow', 50))

        self._submit_button = tk.Button(self._frame,
                                        text='Submit',
                                        command=self._search,
                                        font=('arialnarrow', 20),
                                        bg='forest green',
                                        fg='white')

        self._search_field = tk.Entry(self._frame,
                                      textvariable=self._search_variable,
                                      font=('Verdana', 50),
                                      bg='gray95')

        self._error_message = tk.Label(self._frame,
                                       text='Sorry, that song is not in our database\n Try Again',
                                       bg=BG_COLOUR,
                                       fg='Red',
                                       font=('arialnarrow', 38))

    def _search(self) -> None:
        """Search for the song name represented by self._search_variable in the song graph

        If the song is not in graph, display an error message
        """
        song_name = self._search_variable.get()
        artist_list = self._ui.graph.get_artists_by_song(song_name.lower())

        if artist_list == []:
            self._text.place_forget()
            self._error_message.place(x=WINDOW_WIDTH // 2,
                                      y=WINDOW_HEIGHT // 4,
                                      anchor='center')
        else:
            self._ui.change_current_page(self._ui.results_page)

    def show_page(self, truth: bool) -> None:
        """Make the current page visible or invisible based on truth"""
        if truth:
            self._text.place(x=(WINDOW_WIDTH) // 2, y=(WINDOW_HEIGHT) // 4, anchor='center')

            self._search_field.place(x=WINDOW_WIDTH // 2,
                                     y=WINDOW_HEIGHT // 2,
                                     width=WINDOW_WIDTH * 0.75,
                                     height=100,
                                     anchor='center')

            self._submit_button.place(x=WINDOW_WIDTH // 2,
                                      y=WINDOW_HEIGHT // 1.25,
                                      anchor='center',
                                      width=WINDOW_WIDTH // 4,
                                      height=100)
        else:
            self._text.place_forget()
            self._search_field.place_forget()
            self._submit_button.place_forget()
            self._error_message.place_forget()


class ResultsPage(Page):
    """A page representing the search results page in the application from the give graph

    This page is responsible for providing a graphical interface which displays the search results
    """
    # Private Instance Attributes:
    #   - _frame: the object which the page will be displayed on
    #   - _ui: the user interface object which will be mutated by the page
    #   -_search_variable: a tk.StringVar representing the name of the song
    #   -_search_field: a element of the page which allows the user
    #                   to enter song names
    #   - _submit_button: a button on the page which allows the user to submit
    #                     their song name
    #   -_home_button: a button that allows the user to return to the homepage
    #   -_search_results: an instance of SearchResults which is responsible for displaying
    #                     all the artists which the song could be by

    _frame: tk.Tk
    _ui: UserInterface
    _search_variable: tk.StringVar
    _search_field: tk.Entry
    _submit_button: tk.Button
    _home_button: tk.Button
    _search_results: SearchResults

    def __init__(self,
                 frame: tk.Tk,
                 user_interface: UserInterface,
                 search_variable: tk.StringVar) -> None:
        """Initialize the Search results page and all it's elements"""
        Page.__init__(self, frame, user_interface)
        self._search_variable = search_variable
        self._search_results = SearchResults(self._frame, user_interface)

        # Page Elements
        self._search_field = tk.Entry(self._frame,
                                      textvariable=self._search_variable,
                                      font=('Verdana', 20),
                                      bg='gray95')

        self._submit_button = tk.Button(self._frame,
                                        text='Submit',
                                        command=self._show_results,
                                        font=('arialnarrow', 15),
                                        bg='forest green',
                                        fg='white')

        self._home_button = tk.Button(self._frame,
                                      text='Home',
                                      command=lambda:
                                      self._ui.change_current_page(self._ui.home_page),
                                      font=('arialnarrow', 15),
                                      bg='gray60',
                                      fg='white')

    def _show_results(self) -> None:
        """Show the results of the search on the page

        That is, display all the names of the artists which the song could be by
        """
        song_name = self._search_variable.get()
        artist_list = self._ui.graph.get_artists_by_song(song_name.lower())
        self._search_results.update_search(artist_list, song_name.lower())
        self._search_results.show_artists(True)

    def show_page(self, truth: bool) -> None:
        """Make the current page visible/invisble based on truth

        If truth is true then make the page visible, otherwise, make it invisible
        """
        if truth:
            self._search_field.place(x=WINDOW_WIDTH // 2,
                                     y=(WINDOW_HEIGHT // 15),
                                     width=WINDOW_WIDTH * 0.75,
                                     height=50, anchor='center')

            self._submit_button.place(x=WINDOW_WIDTH - 10,
                                      y=WINDOW_HEIGHT // 15,
                                      width=WINDOW_WIDTH // 10,
                                      height=50, anchor='e',)

            self._home_button.place(x=10,
                                    y=WINDOW_HEIGHT // 15,
                                    width=WINDOW_WIDTH // 10,
                                    height=50, anchor='w')
            self._show_results()
        else:
            self._search_field.place_forget()
            self._submit_button.place_forget()
            self._home_button.place_forget()
            self._search_results.show_artists(False)


class RecommendationsPage(Page):
    """A class respresenting a page which will display the song recommendations from graph"""

    # Private Attributes:
    #   - _frame: the object which the page will be displayed on
    #   - _ui: the user interface object which will be mutated by the page
    #   -_home_button: a button which will change the current page to the homepage
    #   -_back_button: a button which will change the current page to the previous page
    #   -_recommendation_labels: a list of Label objects which will display the recommendations
    #                            on the page
    #   -_title: a Label object responsible for displaying the 'We Recommend Listening To' message

    _frame: tk.Tk
    _ui: UserInterface
    _home_button: tk.Button
    _back_button: tk.Button
    _recommendation_labels: list[tk.Label]
    _title: tk.Label

    def __init__(self, frame: tk.Tk, user_interface: UserInterface) -> None:
        """Initialize the RecommendationsPage and all it's graphical elements"""
        Page.__init__(self, frame, user_interface)

        # initializing the recommendations
        recommendation1 = tk.Label(self._frame,
                                   bg=BG_COLOUR,
                                   fg='white',
                                   font=('Verdana', 18),
                                   pady=10)

        recommendation2 = tk.Label(self._frame,
                                   bg=BG_COLOUR,
                                   fg='white',
                                   font=('Verdana', 18),
                                   pady=10)

        recommendation3 = tk.Label(self._frame,
                                   bg=BG_COLOUR,
                                   fg='white',
                                   font=('Verdana', 18),
                                   pady=10)

        recommendation4 = tk.Label(self._frame,
                                   bg=BG_COLOUR,
                                   fg='white',
                                   font=('Verdana', 18),
                                   pady=10)

        recommendation5 = tk.Label(self._frame,
                                   bg=BG_COLOUR,
                                   fg='white',
                                   font=('Verdana', 18),
                                   pady=10)

        self._recommendation_labels = [recommendation1,
                                       recommendation2,
                                       recommendation3,
                                       recommendation4,
                                       recommendation5]

        self._title = tk.Label(self._frame,
                               text='We Recommend Listening To',
                               font=('Verdana', 40, BOLD),
                               bg=BG_COLOUR,
                               fg='deep sky blue',
                               pady=30)

        self._home_button = tk.Button(self._frame,
                                      text='Home',
                                      font=('verdana', 20),
                                      fg='white',
                                      bg='gray60',
                                      width=20,
                                      height=5,
                                      command=lambda:
                                      self._ui.change_current_page(self._ui.home_page))

        self._back_button = tk.Button(self._frame,
                                      text='Back',
                                      font=('verdana', 20),
                                      fg='white',
                                      bg='gray60',
                                      width=20,
                                      height=5,
                                      command=lambda:
                                      self._ui.change_current_page(self._ui.results_page))

    def update_recommended(self, song_name: str, song_artist: str) -> None:
        """Update the recommendations based on the CURRENT song name and artist"""
        recommendations_list = self._ui.graph.get_recommendations(song_name, song_artist, 5, 80)

        recommendation_count = len(recommendations_list)

        if recommendation_count < 5:
            rest = self._recommendation_labels[recommendation_count:]
            for text in rest:
                text.config(text='')

        for i in range(recommendation_count):
            label = self._recommendation_labels[i]
            recommended_name, recommended_artist = recommendations_list[i]
            label.config(text=f'{recommended_name.title()} by {recommended_artist.title()}')

    def show_page(self, truth: bool) -> None:
        """Make the current page visible/invisble based on the value of truth"""
        if truth:
            self._title.pack(side='top')

            for recommendation in self._recommendation_labels:
                recommendation.pack(side='top')

            self._home_button.place(x=30, y=WINDOW_HEIGHT - 130,
                                    width=200,
                                    height=100)

            self._back_button.place(x=WINDOW_WIDTH - 230,
                                    y=WINDOW_HEIGHT - 130,
                                    width=200,
                                    height=100)
        else:
            self._title.pack_forget()

            for recommendation in self._recommendation_labels:
                recommendation.pack_forget()

            self._home_button.place_forget()
            self._back_button.place_forget()


class SearchResults:
    """A class respresenting the search result element of a page

    This class is responsible for displaying the search results on the ResultsPage
    as well as the artist selection
    """
    # Private Attributes:
    #   - _frame: the object which the page will be displayed on
    #   - _ui: the user interface object which will be mutated by the page
    #   -_artist_list: a list of all the artist which the song searched for
    #                  could be by
    #   -_artist_listbox: a Listbox object which is responsible for displaying all
    #                     the artists which the current song could be by
    #   -_artist_variable: a StringVar object which will be passed into _artist_listbox which
    #                      represents all the plausible artists the song could be by
    #   -_song_info: a Label object which will display the song name
    #   -_song_name: the name of the song being searched for
    #   -_confirm_button: a button which will allow the user to confirm their selection of artist
    #   -_error_message: an error message which will inform the user that the song being searched
    #                    for was not found
    #   -_empty_selection: an error message which will inform the user that they have not selected
    #                      an artist yet

    _frame: tk.Tk
    _ui: UserInterface
    _artist_list: list[str]
    _artist_listbox: tk.Listbox
    _artist_variable: tk.StringVar
    _song_info: tk.Label
    _song_name: str
    _confrim_button: tk.Button
    _error_message: tk.Label
    _empty_selection: tk.Label

    def __init__(self, frame: tk.Tk, user_interface: UserInterface) -> None:
        """Initialize the Search results and all it's graphical elements"""
        self._frame = frame
        self._ui = user_interface
        self._artist_list = []
        self._song_name = ''
        self._artist_variable = tk.StringVar()

        self._artist_listbox = tk.Listbox(self._frame,
                                          listvariable=self._artist_variable,
                                          height=3,
                                          width=WINDOW_WIDTH - 100,
                                          bg=BG_COLOUR,
                                          fg='white',
                                          borderwidth=0,
                                          font=('arialnarrow', 40),
                                          relief='flat',
                                          selectmode='SINGLE',
                                          highlightthickness=0,
                                          activestyle='none')
        self._artist_listbox.configure(justify='center')

        self._song_info = tk.Label(self._frame,
                                   text='',
                                   font=('arialnarrow', 20),
                                   bg=BG_COLOUR,
                                   fg='white')

        self._error_message = tk.Label(self._frame,
                                       text="No Songs Found\nTry Again",
                                       fg='red',
                                       bg=BG_COLOUR,
                                       font=('arialnarrow', 38))

        self._confrim_button = tk.Button(self._frame,
                                         text='Confirm Selection',
                                         bg='forest green',
                                         fg='white',
                                         font=('arial narrow', 20),
                                         command=self._update_recommendedpage)

        self._empty_selection = tk.Label(self._frame,
                                         text='No Artist Was Selected',
                                         font=('arialnarrow', 20),
                                         bg=BG_COLOUR,
                                         fg='red')

    def update_search(self, artist_list: list[str], song_name: str) -> None:
        """Update the old song name and artists being displayed to the CURRENT song"""
        self._empty_selection.place_forget()
        self._artist_list = artist_list
        self._song_name = song_name
        self._artist_variable.set([artist.title() for artist in artist_list])
        self._song_info.config(text=f'{song_name.title()} by')

    def _update_recommendedpage(self) -> None:
        """Update the current page to display recommendations for the CURRENT
        song and artist

        Display the empty_selection error message if user has no selected an artist
        """
        selection = self._artist_listbox.curselection()
        if selection != ():
            song_name = self._song_name
            artist = self._artist_list[selection[0]]
            self._ui.recommend_page.update_recommended(song_name, artist)
            self._ui.change_current_page(self._ui.recommend_page)
        else:
            self._empty_selection.place(x=WINDOW_WIDTH // 2,
                                        y=WINDOW_HEIGHT - 100,
                                        anchor='center')

    def show_artists(self, truth: bool) -> None:
        """Display all the artists which the song could be by based on truth

        make the SearchResults visible if and only if truth == True
        """
        if truth:
            self._artist_listbox.place(x=WINDOW_WIDTH // 2,
                                       y=WINDOW_HEIGHT // 2,
                                       anchor='center',
                                       width=WINDOW_WIDTH - 50,
                                       height=200)

            if len(self._artist_list) == 0:
                self._song_info.place_forget()
                self._confrim_button.place_forget()
                self._error_message.place(x=WINDOW_WIDTH // 2,
                                          y=WINDOW_HEIGHT // 2,
                                          anchor='center')
            else:
                self._error_message.place_forget()
                self._song_info.place(x=WINDOW_WIDTH // 2,
                                      y=WINDOW_HEIGHT // 4,
                                      anchor='center')

                self._confrim_button.place(x=WINDOW_WIDTH // 2,
                                           y=WINDOW_HEIGHT - 50,
                                           anchor='center')
        else:
            self._artist_listbox.place_forget()
            self._error_message.place_forget()
            self._song_info.place_forget()
            self._confrim_button.place_forget()
            self._empty_selection.place_forget()


if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background=BG_COLOUR)

    root.resizable(width=False, height=False)
    root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

    from graphs import build_graph
    graph = build_graph('data/data_large.csv')

    UserInterface(root, graph)
    root.mainloop()

    # import python_ta
    # python_ta.check_all(config={
    # 'extra-imports': [],  # the names (strs) of imported modules
    # 'allowed-io': [],     # the names (strs) of functions that call print/open/input
    # 'max-line-length': 100,
    # 'disable': ['E1136']
    # })
