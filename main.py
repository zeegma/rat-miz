import tkinter as tk
from gui.window import Maze


def main():
    root = tk.Tk()
    Maze(root)
    root.mainloop()


if __name__ == "__main__":
    main()
