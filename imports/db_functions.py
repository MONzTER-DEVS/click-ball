from .classes import *
from .encryption import *
import ast


# from cryptography.fernet import *
# class crypt:
#     key = b'E0kGTj9oe68mgUnNZuMwfzosAWO4C1YiO_EIBsaQcTw='
#
#     @staticmethod
#     def de(input_str):
#         return Fernet(crypt.key).decrypt(input_str).decode()
#
#     @staticmethod
#     def en(input_string):
#         return Fernet(crypt.key).encrypt(input_string.encode())


class DB:
    path = os.path.join('assets', 'data.db')

    @staticmethod
    def make_db():
        # Connection
        conn = sqlite3.connect(os.path.join('assets', 'data.db'))

        # Cursor
        c = conn.cursor()

        # Create a few Tables
        c.execute("CREATE TABLE user_data(level text, save text)")
        c.execute("CREATE TABLE cache(theme text)")
        c.execute("INSERT INTO cache values('Bright White')")
        c.execute("INSERT INTO user_data values('1', '" + Crypt.en('None') + "')")
        conn.commit()
        conn.close()

    class Cache:

        @staticmethod
        def load():
            conn = sqlite3.connect(os.path.join('assets', 'data.db'))
            c = conn.cursor()
            c.execute("SELECT * FROM cache")
            values = c.fetchall()
            conn.commit()
            conn.close()
            return values[0]

        @staticmethod
        def change_value(field, value, old=None):
            conn = sqlite3.connect(os.path.join('assets', 'data.db'))
            c = conn.cursor()
            c.execute(f"UPDATE cache SET {field} = '{value}'")

            conn.commit()
            conn.close()

    @staticmethod
    def save_survival(dumping_dict):
        conn = sqlite3.connect(os.path.join('assets', 'data.db'))
        c = conn.cursor()
        User_data.save = dumping_dict
        to_dump = str(dumping_dict)
        c.execute(f"UPDATE user_data set save = '{Crypt.en(to_dump)}'")

        conn.commit()
        conn.close()

    @staticmethod
    def update_level_progress(n):
        conn = sqlite3.connect(os.path.join('assets', 'data.db'))
        c = conn.cursor()

        c.execute(f"UPDATE user_data SET level = '{n}'")
        User_data.current_level = int(n)

        conn.commit()
        conn.close()

    @staticmethod
    def load_user_progress():
        conn = sqlite3.connect(os.path.join('assets', 'data.db'))
        c = conn.cursor()

        c.execute("SELECT * FROM user_data")
        vals = c.fetchall()
        vals[0] = list(vals[0])
        conn.commit()
        conn.close()
        vals[0][-1] = Crypt.de(vals[0][-1])
        return vals
