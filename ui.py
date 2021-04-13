"""
A Module which is responsible for managing the User Interface
"""
import tkinter as tk
from graphs import SongGraph
import Pages as pg
from typing import Optional


class UserInterface:
    """A class representing the main user interface"""
    mainframe: tk.Tk
    search_variable: tk.StringVar
    graph: SongGraph
    home_page: pg.HomePage
    results_page: pg.ResultsPage
    recommend_page: pg.RecommendationsPage

    _current_page: Optional[pg.Page]

    def __init__(self, root: tk.Tk, graph: SongGraph) -> None:
        """Initialize the user interface"""
        self.mainframe = root
        self.mainframe.title('Spotify Song Recommender')
        self.graph = graph

        # Initializing the pages
        self.search_variable = tk.StringVar()
        self.home_page = pg.HomePage(self.mainframe, self, self.search_variable)
        self.results_page = pg.ResultsPage(self.mainframe, self, self.search_variable)
        self.recommend_page = pg.RecommendationsPage(self.mainframe, self)

        self._current_page = self.home_page
        self._current_page.show_page(True)

    def change_current_page(self, page: pg.Page) -> None:
        """Change the current page to <page> and display it"""
        self._current_page.show_page(False)
        self._current_page = page
        self._current_page.show_page(True)


if __name__ == '__main__':
    # Constants
    BG_COLOUR = 'gray10'
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 600

    root = tk.Tk()
    root.configure(background=BG_COLOUR)

    root.resizable(width=False, height=False)
    root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

    from graphs import build_graph
    graph = build_graph('data/data.csv')

    UserInterface(root, graph)
    root.mainloop()