import tkinter as tk
from tkinter import ttk

class MyApp(tk.Tk):
    def __init__(self, menu_names):
        super().__init__()

        self.menu_frame = ttk.Frame(self)
        self.menu_frame.pack(side=tk.TOP, fill=tk.X)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # 创建菜单选项卡
        self.menu_buttons = []
        for name in menu_names:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=name)

            button = ttk.Button(self.menu_frame, text=name, command=lambda n=name: self.switch_page(n))
            button.pack(side=tk.LEFT, padx=5, pady=5)
            self.menu_buttons.append(button)

    def switch_page(self, name):
        # 切换到相应的选项卡
        for i, button in enumerate(self.menu_buttons):
            if button.cget("text") == name:
                self.notebook.select(i)
                break

menu_names = ["Menu 1", "Menu 2", "Menu 3", "Menu 4", "Menu 5", "Menu 6", "Menu 7"]

app = MyApp(menu_names)
app.mainloop()
