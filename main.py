import tkinter as tk
from gui import NanoCardApp

def main():
    root = tk.Tk()
    app = NanoCardApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()