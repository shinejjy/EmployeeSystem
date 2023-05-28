import pymssql

# 连接数据库
conn = pymssql.connect(server='your_server', user='your_username', password='your_password', database='your_database')

# 创建研发客户档案模板表
create_table_sql = '''
CREATE TABLE CustomerTemplate (
    [Description] VARCHAR(255),
    [Column 1] VARCHAR(255),
    [Column 2] VARCHAR(255),
    [Column 3] VARCHAR(255),
    [Column 4] VARCHAR(255),
    [Column 5] VARCHAR(255),
    [Column 6] VARCHAR(255),
    [Column 7] VARCHAR(255),
    [Column 8] VARCHAR(255),
    [Column 9] VARCHAR(255),
    [Column 10] VARCHAR(255),
    [Column 11] VARCHAR(255),
    [Column 12] VARCHAR(255),
    [Column 13] VARCHAR(255),
    [Column 14] VARCHAR(255),
    [Column 15] VARCHAR(255),
    [Column 16] VARCHAR(255),
    [Column 17] VARCHAR(255),
    [Column 18] VARCHAR(255),
    [Column 19] VARCHAR(255),
    [Column 20] VARCHAR(255),
    [Column 21] VARCHAR(255),
    [Column 22] VARCHAR(255),
    [Column 23] VARCHAR(255),
    [Column 24] VARCHAR(255),
    [Column 25] VARCHAR(255),
    [Column 26] VARCHAR(255)
)
'''
with conn.cursor() as cursor:
    cursor.execute(create_table_sql)
    conn.commit()

# 读取研发客户档案模板
select_data_sql = 'SELECT * FROM CustomerTemplate'
with conn.cursor(as_dict=True) as cursor:
    cursor.execute(select_data_sql)
    rows = cursor.fetchall()

    for row in rows:
        print(row)

# 关闭数据库连接
conn.close()
