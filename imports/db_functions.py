import os
import sqlite3
import ast

class crypt:
    key = "}>CX[JAnpm8)H[rKEvrt/kse1G'j{Pd\jxfTNCxU/b4i0MeeV9A(FusO9zd9bM\m"
    splitter = "z"

    @staticmethod
    def de(inputed_str):
        decrypted = ""
        encrypted_list = inputed_str[:-1].split(crypt.splitter)

        index = 0
        for num in encrypted_list:
            try:
                decrypted += chr(int(int(num) / ord(crypt.key[index])))
            except IndexError:
                decrypted += chr(int(int(num) / ord(crypt.key[index % 64])))
            finally:
                index += 1

        return decrypted

    @staticmethod
    def en(string):
        index = 0
        encrypted = ""
        for alpha in string:
            try:
                encrypted += str(ord(alpha) * ord(crypt.key[index])) + crypt.splitter
            except IndexError:
                encrypted += str(ord(alpha) * ord(crypt.key[index % 64])) + crypt.splitter
            finally:
                index += 1
        return encrypted


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
    def load_all_data():
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
        values = ast.literal_eval(crypt.de(c.fetchall()[0][0])) # the complex Decryption alg
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
