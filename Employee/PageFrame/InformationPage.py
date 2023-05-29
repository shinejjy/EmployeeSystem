import tkinter as tk
from Database.SQL import change_code
from Base.Base import BaseFrame


class InformationPage(BaseFrame):
    def __init__(self, app, window, show):
        super().__init__(app, window, show)

        # 创建信息标签
        self.info_labels = {}

        if show:
            self.show()

    def show(self):
        super(InformationPage, self).show()
        # 展示
        self.show_basic_info()

    def show_basic_info(self):
        # 清除
        self.clear_info_labels()

        # 查询基本信息
        sql = f"""
        SELECT 部门, 姓名, 性别, 职位, 工号, 状态
        FROM [9员工信息表]
        WHERE 工号 = '{self.app.user_info['id']}'
        """
        self.app.db.execute(sql)
        info = self.app.db.cursor.fetchone()

        if info:
            # Convert encoding if necessary
            info = change_code(info)
            info_data = {
                "部门": info[0],
                "姓名": info[1],
                "性别": info[2],
                "职位": info[3],
                "工号": info[4],
                "状态": info[5]
            }
        else:
            info_data = {
                "部门": '',
                "姓名": '',
                "性别": '',
                "职位": '',
                "工号": '',
                "状态": ''
            }

        # Display employee basic information using labels
        row = 0
        for key, value in info_data.items():
            label = tk.Label(self, text=f"{key}: {value}", bg="white")
            label.grid(row=row, column=0, sticky="w")
            self.info_labels[key] = label
            row += 1

    def clear_info_labels(self):
        for label in self.info_labels.values():
            label.grid_forget()
