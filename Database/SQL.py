import pymssql
from pandas._libs.tslibs.timestamps import Timestamp
from pymssql import OperationalError


class EasySql:
    def __init__(self,
                 host='localhost',
                 server="127.0.0.1",
                 port="1433",
                 user="sa",
                 password="12345",
                 database="Company",
                 charset="UTF-8",
                 autocommit=True):
        # Establish a connection to the SQL Server
        try:
            conn = pymssql.connect(host=host,
                                   server=server,
                                   port=port,
                                   user=user,
                                   password=password,
                                   database=database,
                                   charset=charset,
                                   autocommit=autocommit)
        except OperationalError:
            conn = None

        if conn:
            print('Connected to the database successfully!')
            # Get the cursor object
            self.cursor = conn.cursor()
        else:
            print('Failed to connect to the database!')

    def createTable(self, table_name, type_dic):
        # Check if the table already exists
        if self.tableExist(table_name):
            print('Table already exists!')
            return
        # Construct the CREATE TABLE SQL statement
        columns = ', '.join([f"{column} {data_type}" for column, data_type in type_dic.items()])
        sql = f"CREATE TABLE {table_name} ({columns})"

        # Execute the SQL statement
        self.cursor.execute(sql)
        if self.cursor:
            print('Successfully create Table!')

    def tableExist(self, table_name):
        # Check if the table exists in the database
        query = f"SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        return bool(result)

    def insertData(self, table_name, variable_list):
        value_list = []
        for value in variable_list:
            if isinstance(value, str) and value != 'null' or isinstance(value, Timestamp):
                value = str(value).replace("'", "''").replace(' 00:00:00', '')
                value_list.append(f"'{value}'")
            else:
                value_list.append(str(value))

        values = ', '.join(value_list)

        # Construct the INSERT INTO SQL statement
        sql = f"INSERT INTO {table_name} VALUES ({values})"
        print(sql)

        # Execute the SQL statement
        self.cursor.execute(sql)

        if self.cursor:
            print('Insert data Successfully!')

    def execute(self, sql):
        # Execute custom SQL statements
        self.cursor.execute(sql)

    def queryData(self, table_name, columns=None, condition=None):
        # Construct the SELECT SQL statement
        if columns:
            columns_str = ', '.join(columns)
        else:
            columns_str = "*"

        sql = f"SELECT {columns_str} FROM {table_name}"

        if condition:
            sql += f" WHERE {condition}"

        # Execute the SQL statement
        self.cursor.execute(sql)

        # Fetch all the rows
        rows = self.cursor.fetchall()

        return rows

    def alterColumnType(self, table_name, column_type_dict):
        for column_name, new_data_type in column_type_dict.items():
            # Construct the ALTER TABLE SQL statement for each column
            sql = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} {new_data_type}"

            # Execute the SQL statement
            self.cursor.execute(sql)
