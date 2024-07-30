from module_study.SQlite3.DbManager  import DbManager

class DbManagerTest:
    def __init__(self ):
        self.db = DbManager('db.sqlite3')

    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS employees (
               id integer PRIMARY KEY,
               name text NOT NULL,
               salary real
           );
        """
        self.db.create_table(create_table_sql)
    def insert_data(self):
        self.db.insert_data("employees", (3, "John Wang", 50000))
        self.db.insert_data("employees", (4, "John KU", 30000))
    def select_data(self,table_name):
        return self.db.select_data(table_name)
    def update_data(self,table_name, data, condition):
        self.db.update_data(table_name,data, condition)

    def close_conn(self):
        self.db.close_connection()

if __name__ == "__main__":
     dbTest = DbManagerTest()
     dbTest.create_table()
     # dbTest.insert_data()
     dbTest.update_data('employees',{'salary':40800},'id=1')
     print(dbTest.select_data('employees'))
     dbTest.close_conn()

