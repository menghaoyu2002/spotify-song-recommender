from __future__ import annotations
import tkinter as tk
from typing import Optional

BG_COLOUR = 'gray10'
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

class Page:
    """ an abstract class representing a single page in the application"""
    _frame: tk.Tk
    _user_interface: UserInterface

    def __init__(self, frame: tk.Tk, user_interface: UserInterface) -> None:
        self._frame = frame
        self._user_interface = user_interface

    def show_page(self, truth: bool) -> None:
        """Make the current page visible or invisible based on truth

        the page is visible if and only if truth == true
        """
        NotImplementedError


class HomePage(Page):
    """A class representing the Homepage of the application"""

    # Private Instance Attributes:
    _search_variable: tk.StringVar
    _frame: tk.Tk
    _text: Optional[tk.Label]
    _search_field: Optional[tk.Entry]
    _submit_button: Optional[tk.Button]
    _user_interface: UserInterface
    _error_message: Optional[tk.Label]

    def __init__(self, frame: tk.Tk, user_interface: UserInterface, search_variable: tk.StringVar) -> None:
        """Initialize the homepage object"""
        Page.__init__(self, frame, user_interface)
        self._search_variable = search_variable

    def _place_text(self) -> None:
        """Place the "Search" label on the screen"""
        self._text = tk.Label(self._frame, text='Search for a Song!', bg=BG_COLOUR, fg='gray95', font=('arialnarrow', 50))
        self._text.pack()
        self._text.place(x=(WINDOW_WIDTH) // 2, y=(WINDOW_HEIGHT) // 4, anchor='center')

    def _place_searchfield(self) -> None:
        """Dispaly the "Search" field on the screen"""
        self._search_field = tk.Entry(self._frame, textvariable=self._search_variable, font=('Verdana', 50), bg='gray95')
        self._search_field.pack()


        self._search_field.place(x=WINDOW_WIDTH // 2, y=(WINDOW_HEIGHT // 2),
                          width=WINDOW_WIDTH * 0.75, height=100, anchor='center')

    def _place_submit_button(self) -> None:
        """Place the submit button on the user interface"""
        self._submit_button = tk.Button(self._frame, text='Submit', command=self._search,
                                       font=('arialnarrow', 20), bg='forest green', fg='white')
        self._submit_button.pack()
        self._submit_button.place(x=(WINDOW_WIDTH)//2, y=WINDOW_HEIGHT//1.25, anchor='center',
                                  width=WINDOW_WIDTH//4, height=100)

    def _show_error_message(self) -> None:
        pass

    def _search(self) -> None:
        """Search for the song name represented by self._search_variable in the song graph"""
        song_name = self._search_variable.get()
        search_page = ResultsPage(self._frame, self._user_interface, self._search_variable, self)
        self._user_interface.change_current_page(search_page)

        # if song_name in graph:
        #     pass # do something
        # else:
        #     pass

    def show_page(self, truth: bool) -> None:
        """Make the current page visible or invisible based on truth"""
        if truth:
            self._place_text()
            self._place_searchfield()
            self._place_submit_button()
        else:
            self._text.destroy()
            self._search_field.destroy()
            self._submit_button.destroy()
            self._error_message.destroy()


class ResultsPage(Page):
    """A page representing the search results page in the application from the give graph

    This page is responsible for providing a graphical interface which displays the search results
    """
    # Private Instance Attributes:
    _frame: tk.Tk
    _user_interface: UserInterface
    _search_variable: tk.StringVar
    _submit_button: Optional[tk.Button]
    _home_button: Optional[tk.Button]
    _home_page: HomePage
    _search_results: SearchResults
    _error_message: Optional[tk.Label]

    def __init__(self, frame: tk.Tk, user_interface: UserInterface, search_variable: tk.StringVar, home_page: HomePage) -> None:
        """Initialize the Search results page"""
        Page.__init__(self, frame, user_interface)
        self._search_variable = search_variable
        self._home_page = home_page

    def _place_searchfield(self):
        """Display a search field on the current page"""
        self._search_field = tk.Entry(self._frame, textvariable=self._search_variable, font=('Verdana', 20), bg='gray95')
        self._search_field.pack()


        self._search_field.place(x=WINDOW_WIDTH // 2, y=(WINDOW_HEIGHT // 15),
                          width=WINDOW_WIDTH * 0.75, height=50, anchor='center')

    def _place_submit_button(self) -> None:
        """Display the submit button on the user interface"""
        self._submit_button = tk.Button(self._frame, text='Submit', command=self._search,
                                       font=('arialnarrow', 15), bg='forest green', fg='white')
        self._submit_button.pack()
        self._submit_button.place(x=WINDOW_WIDTH - 10, y=(WINDOW_HEIGHT //15),
                                  width=WINDOW_WIDTH//10, height=50, anchor='e',)

    def _place_home_button(self):
        """Display the home button on the current page"""
        self._home_button = tk.Button(self._frame,
                                      text='Home',
                                      command= lambda: self._user_interface.change_current_page(self._home_page),
                                      font=('arialnarrow', 15),
                                      bg='gray60',
                                      fg='white')

        self._home_button.pack()

        self._home_button.place(x=10, y=(WINDOW_HEIGHT //15),
                                  width=WINDOW_WIDTH//10, height=50, anchor='w',)

    def _show_error_message(self, truth: bool) -> None:
        pass

    def _show_results(self):
        self._search_results = SearchResults()

    def _search(self) -> None:
        """Search for the song name represented by self._search_variable in the song graph"""
        song_name = self._search_variable.get()
        print(song_name)

        # if song_name in graph:
        #     pass # do something
        # else:
        #     pass

    def show_page(self, truth: bool) -> None:
        if truth:
            self._place_searchfield()
            self._place_submit_button()
            self._place_home_button()
            self._show_results()
        else:
            self._search_field.destroy()
            self._submit_button.destroy()
            self._home_button.destroy()
            self._error_message.destroy()


class SongRecommendations(Page):
    """A class respresenting a page which will display the song recommendations from graph"""
    _prev_page: ResultsPage
    _home_page: HomePage

    def __init__(self, frame: tk.Tk, user_interface: UserInterface, graph, prev_page: ResultsPage, home_page: HomePage) -> None:
        Page.__init__(self, frame, user_interface)
        self._prev_page = prev_page
        self._home_page = home_page


class SearchResults:
    pass

class UserInterface:
    """A class representing the main user interface"""
    mainframe: tk.Tk
    search_variable: tk.StringVar
    graph: ...

    _current_page: Optional[Page]

    def __init__(self, root: tk.Tk, graph=None) -> None:
        """Initialize the user interface"""
        root.title('Spotify Song Recommender')
        self.mainframe = root

        # Initializing the home page
        self.search_variable = tk.StringVar()
        self._current_page = HomePage(self.mainframe, self, self.search_variable)
        self._current_page.show_page(True)

    def change_current_page(self, page: Page) -> None:
        """Change the current page to <page> and display it"""
        # make the current page invisible
        self._current_page.show_page(False)

        # update the current page and make it visible
        self._current_page = page
        self._current_page.show_page(True)



if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background=BG_COLOUR)

    root.resizable(width=False, height=False)
    root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

    UserInterface(root)
    root.mainloop()