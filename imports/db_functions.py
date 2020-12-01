from .classes import *
from .encryption import *
import ast


class DB:
    path = os.path.join('assets', 'data.db')

    @staticmethod
    def execute(commands):
        conn = sqlite3.connect(os.path.join('assets', 'data.db'))
        c = conn.cursor()

        for command in commands:
            c.execute(command)

        conn.commit()
        conn.close()

    @staticmethod
    def make_db():
        commands = [
            "CREATE TABLE user_data(level text, save text, coins text)",
            "CREATE TABLE cache(theme text)",
            "INSERT INTO cache values('Bright White')",
            f"INSERT INTO user_data values('{Crypt.en('1')}','{Crypt.en('None')}', '{Crypt.en('0')}')"
        ]
        DB.execute(commands)

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
            command = "UPDATE cache SET " + field + "= '" + value + "'"
            print(command)
            DB.execute([command])

    @staticmethod
    def save_survival(dumping_dict):
        User_data.save = dumping_dict
        to_dump = str(dumping_dict)
        DB.execute([f"UPDATE user_data set save = '{Crypt.en(to_dump)}'"])

    @staticmethod
    def update_level_progress(n):
        conn = sqlite3.connect(os.path.join('assets', 'data.db'))
        c = conn.cursor()

        c.execute(f"UPDATE user_data SET level = '{Crypt.en(n)}'")
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
        vals[0][0] = Crypt.de(vals[0][0])
        vals[0][-1] = Crypt.de(vals[0][-1])
        vals[0][-2] = Crypt.de(vals[0][-2])
        return vals
