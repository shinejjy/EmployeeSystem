# GUI界面编程

#  界面包
from tkinter import *
from tkinter import simpledialog
from tkinter.ttk import Treeview
from tkinter import messagebox as message
from manager.recordManager import RecordManager
from pojo.record import Record

manager=RecordManager()

# 新建一个窗口
window=Tk()
# 设置标题
window.title('险种管理')
# 设置大小  widthxheightt+x+y
window.geometry('400x400+200+200')


# 增加
def add():
    id=simpledialog.askstring('提示','输入编号')
    name=simpledialog.askstring('提示','输入名称')
    money=simpledialog.askstring('提示','输入金额')
    type=simpledialog.askstring('提示','输入类型')
    r=Record(id,name,money,type)
    manager.add_record(r)
    load()


# 删除
def delete():
    # message.showinfo('提示','删除成功')
    if message.askyesno('提示','是否删除'):
        # pass
        # 获取被选中的行
        if len(table.selection())>0:
            # 获取当前这行数据
            # table.item(table.selection()[0])获得字典对象
            # ["values"]获取字典的值
            id=table.item(table.selection()[0])["values"][0]
            manager.delete_record(str(id))
            table.delete(table.selection()[0])


#加载
def load():
    #1.获得所有元素
    for i in table.get_children():
        # 2.清空元素
        print(i)
        table.delete(i)
    for r in manager.records:
        assert isinstance(r,Record)
        table.insert('',END,value=(r.record_id,r.record_name,r.record_money,r.record_type))
# END是一个常量

def save():
    manager.save_record()


# 编写控件Treeview
table = Treeview(columns=('id','name','money','type'),show='headings')
table.column('id',width=100)
table.column('name',width=100)
table.column('money',width=100)
table.column('type',width=100)
table.heading('id',text='记录编号')
table.heading('name',text='缴费者')
table.heading('money',text='缴费金额')
table.heading('type',text='缴费类型')
# 让控件显示
table.pack()

# command指令。调用方法
Button(text='增加',command=add).pack()
Button(text='删除',command=delete).pack()
Button(text='加载',command=load).pack()
Button(text='保存',command=save).pack()

# 让窗口运行
window.mainloop()


