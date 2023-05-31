import tkinter as tk
from tkinter import ttk

def set_combobox_style():
    # 创建自定义的下拉框样式
    combobox_style = ttk.Style()
    combobox_style.configure('Custom.TCombobox', postoffset=(0, 0, 0, 0),
                             fieldbackground='white', selectbackground='white',
                             selectforeground='black')

    # 创建自定义的listbox样式
    field_style = ttk.Style()
    field_style.configure('Custom.TCombobox.Listbox', justify='center')

    # 将样式应用于下拉框组件
    combobox['style'] = 'Custom.TCombobox'

# 创建主窗口
window = tk.Tk()

# 创建下拉框
combobox = ttk.Combobox(window, values=["Option 1", "Option 2", "Option 3"])

# 设置下拉框样式
set_combobox_style()

# 显示下拉框
combobox.pack()

# 运行主循环
window.mainloop()
