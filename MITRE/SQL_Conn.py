import sqlalchemy


class SQL_Conn():
    def __init__(self, db_name, server_hostname, server_port, username,
                 password):
        self.conn(db_name, server_hostname, server_port, username,
                  password)

    def conn(self, db_name, server_hostname, server_port, username,
             password):
        self.db_name = db_name
        create_db_engine = sqlalchemy.create_engine(
            f'mysql://{username}:{password}@{server_hostname}:\
                {server_port}')
        create_db_engine.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        self.server_hostname = server_hostname
        self.server_port = server_port
        self.username = username
        self.password = password
        self.engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.username}:{self.password}@\
                    {self.server_hostname}/{self.db_name}?\
                        host={self.server_hostname}?\
                        port={str(self.server_port)}")
        self.engine.execute(f"CREATE DATABASE {db_name}")

    def create_new_table(self, df, table_name):
        longest_char = df.index.str.len().max()
        df.to_sql(table_name, self.engine, if_exists='replace', dtype={
                  'Name': sqlalchemy.VARCHAR(length=longest_char)})

    def append_table():
        pass
