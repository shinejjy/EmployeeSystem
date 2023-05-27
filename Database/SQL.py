import pymssql


class EasySql:
    def __init__(self,
                 host='localhost',
                 server="127.0.0.1",
                 port="1433",
                 user="sa",
                 password="12345",
                 database="Company",
                 charset="UTF-8",
                 autocommit=True
                 ):
        # 建立与 SQL Server 的连接
        conn = pymssql.connect(host=host,
                               server=server,
                               port=port,
                               user=user,
                               password=password,
                               database=database,
                               charset=charset,
                               autocommit=autocommit
                               )

        self.cursor = None
        if conn:
            print('连接数据库成功！')
            # 获取游标对象
            self.cursor = conn.cursor()
        else:
            print('连接数据库失败！')

    def creatTable(self, table_name, type_dic):
        # 检查表是否已存在
        if self.tableExist(table_name):
            print('表格已存在')
            return
        type_str = ''
        for key, value in type_dic.items():
            type_str += f"{key} {value},"

        # 构造创建表格的 SQL 语句
        sql = f"""
        CREATE TABLE {table_name}(
        {type_str}
        )
        """

        # 执行 SQL 语句
        self.cursor.execute(sql)

    def tableExist(self, table_name):
        # 查询表是否存在的 SQL 语句
        query = f"SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if result:
            return True
        else:
            return False

    def insertTable(self, table_name, variable_list):
        variable_str = ''
        for i, value in enumerate(variable_list):
            if i > 0:
                variable_str += f",{value}"
            else:
                variable_str += f"{value}"

        # 构造插入数据的 SQL 语句
        sql = f"INSERT INTO {table_name} VALUES ({variable_str})"

        print(sql)

        # 执行 SQL 语句
        self.cursor.execute(sql)

    def execute(self, sql):
        # 执行自定义的 SQL 语句
        self.cursor.execute(sql)


def change_code(info):
    return tuple(
        item.encode('latin1').decode('gbk') if isinstance(item, str) else item for item in info
    )
