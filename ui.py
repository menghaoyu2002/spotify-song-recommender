from __future__ import annotations
import tkinter as tk
from tkinter.constants import BOTTOM, W
from tkinter.font import BOLD
from graphs import SongGraph, build_graph

# Constants
BG_COLOUR = 'gray10'
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

class Page:
    """ an abstract class representing a single page in the application"""
    _frame: tk.Tk
    _ui: UserInterface

    def __init__(self, frame: tk.Tk, user_interface: UserInterface) -> None:
        self._frame = frame
        self._ui = user_interface

    def show_page(self, truth: bool) -> None:
        """Make the current page visible or invisible based on truth

        the page is visible if and only if truth == true
        """
        NotImplementedError


class HomePage(Page):
    """A class representing the Homepage of the application"""

    # Private Instance Attributes:
    _frame: tk.Tk
    _ui: UserInterface
    _search_variable: tk.StringVar
    _text: tk.Label
    _search_field: tk.Entry
    _submit_button: tk.Button
    _error_message: tk.Label

    def __init__(self, frame: tk.Tk, user_interface: UserInterface, search_variable: tk.StringVar) -> None:
        """Initialize the homepage object"""
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

        self._search_field = tk.Entry(self._frame, textvariable=self._search_variable, font=('Verdana', 50), bg='gray95')
        self._error_message = tk.Label(self._frame,
                              text='Sorry, that song is not in our database\n Try Again',
                              bg=BG_COLOUR,
                              fg='Red',
                              font=('arialnarrow', 38))

    def _search(self) -> None:
        """Search for the song name represented by self._search_variable in the song graph"""
        song_name = self._search_variable.get()
        artist_list = self._ui.graph.get_artists_by_song(song_name)

        if artist_list == []:
            self._text.place_forget()
            self._error_message.place(x=(WINDOW_WIDTH) // 2, y=(WINDOW_HEIGHT) // 4, anchor='center')
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

            self._submit_button.place(x=(WINDOW_WIDTH)//2,
                                      y=WINDOW_HEIGHT//1.25,
                                      anchor='center',
                                      width=WINDOW_WIDTH//4,
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
    _frame: tk.Tk
    _ui: UserInterface
    _search_variable: tk.StringVar
    _submit_button: tk.Button
    _home_button: tk.Button
    _search_results: SearchResults
    _artist_variable: tk.StringVar

    def __init__(self, frame: tk.Tk, user_interface: UserInterface, search_variable: tk.StringVar) -> None:
        """Initialize the Search results page"""
        Page.__init__(self, frame, user_interface)
        self._search_variable = search_variable
        self._search_results = SearchResults(self._frame, user_interface)

        # Page Elements
        self._search_field = tk.Entry(self._frame, textvariable=self._search_variable, font=('Verdana', 20), bg='gray95')

        self._submit_button = tk.Button(self._frame, text='Submit', command=self._show_results,
                                       font=('arialnarrow', 15), bg='forest green', fg='white')

        self._home_button = tk.Button(self._frame,
                                      text='Home',
                                      command=lambda: self._ui.change_current_page(self._ui.home_page),
                                      font=('arialnarrow', 15),
                                      bg='gray60',
                                      fg='white')

    def _show_results(self):
        song_name = self._search_variable.get()
        artist_list = self._ui.graph.get_artists_by_song(song_name)
        self._search_results.update_search(artist_list, song_name)
        self._search_results.show_artists(True)


    def show_page(self, truth: bool) -> None:
        if truth:
            self._search_field.place(x=WINDOW_WIDTH // 2, y=(WINDOW_HEIGHT // 15),
                                     width=WINDOW_WIDTH * 0.75, height=50, anchor='center')

            self._submit_button.place(x=WINDOW_WIDTH - 10, y=(WINDOW_HEIGHT //15),
                                      width=WINDOW_WIDTH//10, height=50, anchor='e',)

            self._home_button.place(x=10, y=WINDOW_HEIGHT // 15,
                                    width=WINDOW_WIDTH // 10, height=50, anchor='w')
            self._show_results()
        else:
            self._search_field.place_forget()
            self._submit_button.place_forget()
            self._home_button.place_forget()
            self._search_results.show_artists(False)


class RecommendationsPage(Page):
    """A class respresenting a page which will display the song recommendations from graph"""
    _home_button: tk.Button
    _back_button: tk.Button
    _recommendations: list[tuple[str, str]]
    _recommendation1: tk.Label
    _recommendation2: tk.Label
    _recommendation3: tk.Label
    _recommendation4: tk.Label
    _recommendation5: tk.Label

    def __init__(self, frame: tk.Tk, user_interface: UserInterface) -> None:
        Page.__init__(self, frame, user_interface)

        # initializing the recommendations
        self._recommendation1 = tk.Label(self._frame, bg=BG_COLOUR, fg='white', font=('Verdana', 20), pady=10)
        self._recommendation2 = tk.Label(self._frame, bg=BG_COLOUR, fg='white', font=('Verdana', 20), pady=10)
        self._recommendation3 = tk.Label(self._frame, bg=BG_COLOUR, fg='white', font=('Verdana', 20), pady=10)
        self._recommendation4 = tk.Label(self._frame, bg=BG_COLOUR, fg='white', font=('Verdana', 20), pady=10)
        self._recommendation5 = tk.Label(self._frame, bg=BG_COLOUR, fg='white', font=('Verdana', 20), pady=10)

        self._title = tk.Label(self._frame,
                               text= 'We Recommend Listening To ',
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
                                      command= lambda: self._ui.change_current_page(self._ui.home_page))

        self._back_button = tk.Button(self._frame,
                                      text='Back',
                                      font=('verdana', 20),
                                      fg='white',
                                      bg='gray60',
                                      width=20,
                                      height=5,
                                      command= lambda: self._ui.change_current_page(self._ui.results_page))

    def update_recommended(self, song_name: str, song_artist: str) -> None:
        self._recommendations = self._ui.graph.get_recommendations(song_name, song_artist, 5, 80)

        recommendation_count = len(self._recommendations)

        label_list = [self._recommendation1,
                      self._recommendation2,
                      self._recommendation3,
                      self._recommendation4,
                      self._recommendation5]

        if recommendation_count < 5:
            rest = label_list[recommendation_count:]
            for text in rest:
                text.config(text='')

        # configuring each label
        for i in range(recommendation_count):
            label = label_list[i]
            recommended_name, recommended_artist = self._recommendations[i]
            label.config(text=f'{recommended_name} by {recommended_artist}')

    def show_page(self, truth: bool) -> None:
        if truth:
            self._title.pack(side='top')
            self._recommendation1.pack(side='top')
            self._recommendation2.pack(side='top')
            self._recommendation3.pack(side='top')
            self._recommendation4.pack(side='top')
            self._recommendation5.pack(side='top')
            self._home_button.place(x=30, y=WINDOW_HEIGHT - 130, width=200, height=100)
            self._back_button.place(x=WINDOW_WIDTH - 230, y=WINDOW_HEIGHT - 130, width=200, height=100)
        else:
            self._title.pack_forget()
            self._recommendation1.pack_forget()
            self._recommendation2.pack_forget()
            self._recommendation3.pack_forget()
            self._recommendation4.pack_forget()
            self._recommendation5.pack_forget()
            self._home_button.place_forget()
            self._back_button.place_forget()


class SearchResults:
    _frame: tk.Tk
    _ui: UserInterface
    _artist_list: list[str]
    _artist_listbox: tk.Listbox
    _song_info: tk.Label
    _error_message: tk.Label
    _confrim_button: tk.Button
    _song_name: str

    def __init__(self, frame: tk.Tk, user_interface: UserInterface) -> None:
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

    def update_search(self, artist_list: list[str], song_name: str) -> None:
        self._artist_list = artist_list
        self._song_name = song_name
        self._artist_variable.set(artist_list)
        self._song_info.config(text=f'{song_name} by')

    def _update_recommendedpage(self) -> None:
        selection = self._artist_listbox.curselection()
        if selection != ():
            self._ui.recommend_page.update_recommended(self._song_name, self._artist_list[selection[0]])
            self._ui.change_current_page(self._ui.recommend_page)

    def show_artists(self, truth) -> None:
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


class UserInterface:
    """A class representing the main user interface"""
    mainframe: tk.Tk
    search_variable: tk.StringVar
    graph: SongGraph
    home_page: HomePage
    results_page: ResultsPage
    recommend_page: RecommendationsPage

    _current_page: Optional[Page]

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



if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background=BG_COLOUR)

    root.resizable(width=False, height=False)
    root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

    from graphs import build_graph
    graph = build_graph('data/data.csv')

    UserInterface(root, graph)
    root.mainloop()