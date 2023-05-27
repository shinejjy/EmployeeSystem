import tkinter as tk


class BaseNewWindow(tk.Toplevel):
    def __init__(self, downsideWindow):
        super(BaseNewWindow, self).__init__(downsideWindow)

    def run(self):
        self.mainloop()

    def destroy(self):
        self.destroy()
