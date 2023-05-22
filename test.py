# coding=utf-8  #settng设置全局为utf—8格式
# 导包
import pymssql
import pandas as pd
from frame import easy_sql as es

# 创建连接字符串  （sqlserver默认端口为1433）
conn = pymssql.connect(host='localhost',  # 这里的host='_'可以用本机ip或ip+端口号
                       server="127.0.0.1",  # 本地服务器
                       port="1433",  # TCP端口
                       user="sa", password="12345",
                       database="Company",
                       charset="UTF-8",  # 这里设置全局的GBK，如果设置的是UTF—8需要将数据库默认的GBK转化成UTF-8
                       autocommit=True
                       )
if conn:
    print('连接数据库成功!')  # 测试是否连接上

cursor = conn.cursor()

# cursor.execute(
#     "INSERT INTO lan VALUES(22, 33)"
# )
#
# cursor.execute('SELECT * FROM lan ')

df = pd.read_excel(
    io='辅料销售涉及主要表格例/1药用辅料产品规格编码设置表-2022.08.18.xlsx',
    sheet_name=0,
    usecols="A:G",
    skiprows=2,
    nrows=154,
    na_values=['——', '---']
)

value = 'nan'
for index, row in df.iterrows():
    if pd.isna(row['品名']):
        row['品名'] = value
    else:
        value = row['品名']

if es.isExist(cursor, 'MedicinalIngredients'):
    print("The MedicinalIngredients already exists!")
else:
    cursor.execute(
        """
        CREATE TABLE MedicinalIngredients (
        Category VARCHAR(255),
        Product_Name VARCHAR(255),
        Specification VARCHAR(255),
        Specification_Features VARCHAR(255),
        Requirements VARCHAR(255),
        Label_Top_Right_Corner VARCHAR(255),
        Sales_Department_Code VARCHAR(255)
        )
        """
    )

    for index, row in df.iterrows():
        sql = f"""
        insert into MedicinalIngredients(Category, Product_Name, Specification, Specification_Features, Requirements, Label_Top_Right_Corner, Sales_Department_Code)
            VALUES('{row['类别']}', '{row['品名']}', '{row['规格']}',
            '{row['规格特点']}', '{row['要求']}', '{row['标签右上角体现']}', '{row['销售部编码']}')
        """
        cursor.execute(sql)
