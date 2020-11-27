import os
import sqlite3
import ast
from cryptography.fernet import *


class crypt:
    key = b'E0kGTj9oe68mgUnNZuMwfzosAWO4C1YiO_EIBsaQcTw='

    @staticmethod
    def de(input_str):
        return Fernet(crypt.key).decrypt(input_str).decode()

    @staticmethod
    def en(input_string):
        return Fernet(crypt.key).encrypt(input_string.encode())

class DB:
    path = os.path.join('assets', 'data.db')

    @staticmethod
    def make_db():
        # Connection
        conn = sqlite3.connect(os.path.join('assets', 'data.db'))

        # Cursor
        c = conn.cursor()

        # Create a Table
        c.execute("CREATE TABLE users(name text,password text)")
        c.execute("CREATE TABLE cache(theme text)")
        c.execute("CREATE TABLE saves(data text)")
        c.execute("INSERT INTO cache values('Bright White')")
        conn.commit()
        conn.close()

    @staticmethod
    def load_cache_data():
        conn = sqlite3.connect(os.path.join('assets', 'data.db'))
        c = conn.cursor()
        c.execute("SELECT * FROM cache")
        values = c.fetchall()
        conn.commit()
        conn.close()
        return values[0]

    @staticmethod
    def level_save(dumping_dict):
        conn = sqlite3.connect(os.path.join('assets', 'data.db'))
        c = conn.cursor()
        to_dump = crypt.en(str(dumping_dict))
        c.execute("DROP TABLE saves")
        c.execute("CREATE TABLE saves(data text)")
        c.execute(f"INSERT INTO saves values('{to_dump}')")
        conn.commit()
        conn.close()

    @staticmethod
    def load_save():
        conn = sqlite3.connect(os.path.join('assets', 'data.db'))
        c = conn.cursor()

        c.execute("SELECT * FROM saves")
        values = ast.literal_eval(crypt.de(c.fetchall()[0][0]))  # the complex Decryption alg
        conn.commit()
        conn.close()
        return values

    @staticmethod
    def change_cache_value(field, value, old):
        conn = sqlite3.connect(os.path.join('assets', 'data.db'))
        c = conn.cursor()
        c.execute(f"UPDATE cache SET {field} = '{value}'")

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
