from .classes import *
from .encryption import *
from .settings import *
import ast


class DB:
    db_path = db_path

    @staticmethod
    def execute(commands):
        conn = sqlite3.connect(DB.db_path)
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
            "CREATE TABLE user_name(name text)",
            "INSERT INTO cache values('Bright White')",
            f"INSERT INTO user_data values('{Crypt.en('1')}','{Crypt.en('None')}', '{Crypt.en('0')}')"
        ]
        DB.execute(commands)

    class Cache:

        @staticmethod
        def load():
            conn = sqlite3.connect(DB.db_path)
            c = conn.cursor()
            c.execute("SELECT * FROM cache")
            values = c.fetchall()
            conn.commit()
            conn.close()
            return values[0]

        @staticmethod
        def change_value(field, value, old=None):
            command = "UPDATE cache SET " + field + "= '" + value + "'"
            DB.execute([command])

    @staticmethod
    def save_survival(dumping_dict):
        User_data.save = dumping_dict
        to_dump = str(dumping_dict)
        DB.execute([f"UPDATE user_data set save = '{Crypt.en(to_dump)}'"])

    @staticmethod
    def update_level_progress(n):
        conn = sqlite3.connect(DB.db_path)
        c = conn.cursor()

        c.execute(f"UPDATE user_data SET level = '{Crypt.en(n)}'")
        User_data.current_level = int(n)

        conn.commit()
        conn.close()

    @staticmethod
    def load_user_progress():
        conn = sqlite3.connect(DB.db_path)
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

    @staticmethod
    def check_name():
        to_return = None
        print(DB.db_path)
        conn = sqlite3.connect(DB.db_path)
        c = conn.cursor()

        c.execute("""SELECT * FROM user_name""")
        values = c.fetchall()
        if len(values) == 0:
            to_return = "no name"
        conn.commit()
        conn.close()
        return to_return

    @staticmethod
    def save_name(name):
        conn = sqlite3.connect(DB.db_path)
        c = conn.cursor()

        c.execute(f"""INSERT into user_name values ('{name}')""")

        conn.commit()
        conn.close()

    @staticmethod
    def fetch_name():
        conn = sqlite3.connect(DB.db_path)
        c = conn.cursor()
        c.execute("""SELECT * from user_name""")
        to_return = c.fetchall()[0][0]
        conn.commit()
        conn.close()
        return to_return
