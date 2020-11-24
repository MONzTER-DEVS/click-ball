import sqlite3, os


class DB:
    path = os.path.join('assets', 'data.db')

    @staticmethod
    def make_db():
        # Connection
        conn = sqlite3.connect(os.path.join('assets', 'data.db'))

        # Cursor
        c = conn.cursor()

        # Create a Table
        c.execute('CREATE TABLE users(name text,password text,level integer)')
        c.execute('CREATE TABLE data(theme text)')
        conn.commit()
        conn.close()

    @staticmethod
    def make_user(name, password):
        conn = sqlite3.connect(os.path.join('assets', 'data.db'))
        c = conn.cursor()
        query = f"INSERT INTO users values('{name}','{password}', 1)"

        c.execute(query)
        conn.commit()
        conn.close()

    @staticmethod
    def retrieve_users():
        conn = sqlite3.connect(os.path.join('assets', 'data.db'))
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        vals = c.fetchall()
        conn.commit()
        conn.close()
        return vals

    @staticmethod
    def load_all_data():
        pass
