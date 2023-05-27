import tkinter as tk


class BaseFrame(tk.Frame):
    def __init__(self, app, window, show=True, *args, **kwargs):
        super().__init__(window, *args, **kwargs)
        self.app = app
        self.window = window
        self.configure(bg="white")
        if not show:
            self.hide()

    def show(self):
        self.pack()

    def hide(self):
        self.pack_forget()

