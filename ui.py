import tkinter as tk
from tkinter import ttk
from typing import Optional

BG_COLOUR = 'gray10'
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

class Page:
    frame: ttk.Frame

    """ an abstract class representing a single page in the application"""
    def __init__(self, frame) -> None:
        self.frame = frame

    def show_page(self, truth: bool) -> None:
        """Make the current page visible or invisible based on truth

        the page is visible in the main window if and only if truth == true
        """
        NotImplementedError


class SearchField(Page):
    """A class representing the search field"""
    _search_variable: tk.StringVar
    _frame: ttk.Frame
    _text: Optional[tk.Label]
    _field: Optional[tk.Entry]

    def __init__(self, frame: tk.Tk, search_variable: tk.StringVar) -> None:
        Page.__init__(self, frame)
        self._search_variable = search_variable
        self.show_page(True)

    def place_text(self) -> None:
        """Place "Search" label on the screen"""
        self._text = tk.Label(self.frame, text='Search for a Song!', bg=BG_COLOUR, fg='gray95', font=('arialnarrow', 50))
        self._text.pack()

        self.frame.update()
        text_height = self._text.winfo_height()
        text_width = self._text.winfo_width()

        self._text.place(x=(WINDOW_WIDTH - text_width)//2, y=(WINDOW_HEIGHT - text_height)//4)

    def place_entryfield(self) -> None:
        """Dispaly the "Search" field on the screen"""
        self._field = tk.Entry(self.frame, textvariable=self._search_variable, font=('Verdana', 50), bg='gray95')
        self._field.pack()

        text_ypos = self._text.winfo_rooty()
        self._field.place(x=(WINDOW_WIDTH)//2, y=((WINDOW_HEIGHT + text_ypos)//2.5),
                         width=WINDOW_WIDTH * 0.75, height=100, anchor='center')


    def show_page(self, truth: bool) -> None:
        """Make the current page visible or invisible based on truth"""
        if truth:
            self.place_text()
            self.place_entryfield()
        else:
            self._text.destroy()
            self._field.destroy()


class UserInterface:
    """A class representing the user interface"""
    mainframe: tk.Tk
    search_variable: tk.StringVar
    search_field: SearchField
    submit_button: tk.Button
    graph: ...

    def __init__(self, root: tk.Tk, graph=None) -> None:
        """Initialize the user interface"""
        root.title('Spotify Song Recommender')
        self.mainframe = root

        # Placing the search field
        self.search_variable = tk.StringVar()
        self.search_field = SearchField(self.mainframe, self.search_variable)
        self.place_submit_button()

    def place_submit_button(self) -> None:
        self.submit_button = tk.Button(self.mainframe, text='Submit', command=self.search,
                                       font=('arialnarrow', 20), bg='forest green', fg='white')
        self.submit_button.pack()
        self.submit_button.place(x=(WINDOW_WIDTH)//2, y=WINDOW_HEIGHT//1.25, anchor='center',
                                 width=WINDOW_WIDTH//4, height=100)

    def search(self) -> None:
        """Search for the song name represented by self._search_variable in the song graph"""
        song_name = self.search_variable.get()
        print(song_name)
        # if song_name in graph:
        #     pass # do something
        # else:
        #     pass



if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background=BG_COLOUR)

    root.resizable(width=False, height=False)
    root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

    UserInterface(root)
    root.mainloop()