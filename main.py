"""
The module responsible for executing the program
"""
import tkinter as tk
from ui import UserInterface, WINDOW_HEIGHT, WINDOW_WIDTH, BG_COLOUR
from graphs import build_graph


def run_program() -> None:
    """Run the program"""
    root = tk.Tk()
    root.configure(background=BG_COLOUR)

    root.resizable(width=False, height=False)
    root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

    # graph = build_graph('data/data_large.csv')
    graph = build_graph('data/data_small.csv')

    UserInterface(root, graph)
    root.mainloop()


if __name__ == '__main__':
    run_program()
    