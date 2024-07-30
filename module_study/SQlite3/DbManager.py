import sqlite3
from sqlite3 import Error


class DbManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.create_connection()

    def create_connection(self):
        """ 创建一个与SQLite数据库的连接，'self.db_name' 是我们命名的一个数据库
            首次运行会在工作目录中创建一个名为“self.db_name”的新文件
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def close_connection(self):
        """ 关闭与SQLite数据库的连接 """
        if self.conn:
            self.conn.close()

    def create_table(self, create_table_sql):
        """ 根据create_table_sql 参数创建一个数据表"""
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
    def delete_table(self, table_name):
        """ 删除表 """
        try:
            c = self.conn.cursor()
            c.execute(f"DROP TABLE IF EXISTS {table_name}")
        except Error as e:
            print(e)

    def insert_data(self, table_name, data):
        """ 插入数据到指定的表中
        table_name：表名
        data：元祖类型，例子：(1, "John Doe", 50000)
         """
        try:
            placeholders = ', '.join(['?'] * len(data))
            c = self.conn.cursor()
            c.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", data)
            self.conn.commit()
        except Error as e:
            print(e)

    def update_data(self, table_name, data, condition):
        """ 更新数据到指定的表中
        table_name：表名
        data：字典类型的更新数据
        condition：查询条件
        """
        try:
            set_clause = ', '.join([f'{key} = ?' for key in data.keys()])
            c = self.conn.cursor()
            c.execute(f"UPDATE {table_name} SET {set_clause} WHERE {condition}", list(data.values()))
            self.conn.commit()
        except Error as e:
            print(e)

    def delete_data(self, table_name, condition):
        """ 从指定表中删除数据
        table_name ： 表名
        condition ： 查询条件
        """
        try:
            c = self.conn.cursor()
            c.execute(f"DELETE FROM {table_name} WHERE {condition}")
            self.conn.commit()
        except Error as e:
            print(e)

    def select_data(self, table_name, columns="*", condition=None):
        """ 从指定表中查询数据
        table_name：表名
        columns：待查询的字段
        condition：查询条件
        """
        try:
            c = self.conn.cursor()
            query = f"SELECT {columns} FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"
            print('query sql：{}'.format(query))
            c.execute(query)
            return c.fetchall()
        except Error as e:
            print(e)


    def select_data_free(self, select_sql):
        """ 自由的查询数据
        select_sql：查询语句
        """
        try:
            c = self.conn.cursor()
            if select_sql:
                c.execute(select_sql)
                return c.fetchall()
            else :
                return ''
        except Error as e:
            print(e)
