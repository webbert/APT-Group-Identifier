import sqlite3
import pandas as pd


class SQL_Conn():
    def conn(self, df, DB_name, sql_filename=None):
        column_names = df.columns
        if sql_filename is None:
            sql_filename = "temp_.db"
        conn = sqlite3.connect(sql_filename)
        df.to_sql(DB_name, conn, if_exists='replace')
        print(pd.read_sql_query(f"select * from {DB_name};", conn))
