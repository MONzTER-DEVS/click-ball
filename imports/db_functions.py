import threading

from .encryption import *
from .settings import *
from .classes import User_data, Music
import sqlite3


class DB:
    db_path = db_path

    @staticmethod
    def execute(commands):
        conn = sqlite3.connect(DB.db_path)
        c = conn.cursor()

        if type(commands) == list:
            for command in commands:
                c.execute(command)
        else:
            c.execute(commands)

        conn.commit()
        conn.close()

    @staticmethod
    def make_db():
        commands = [
            "CREATE TABLE user_data(level text, save text, coins text)",
            "CREATE TABLE cache(theme text)",
            "CREATE TABLE music(state text)",
            "INSERT INTO cache values('Bright White')",
            "INSERT INTO music values('True')",
            f"INSERT INTO user_data values('{Crypt.en('1')}','{Crypt.en('None')}', '{Crypt.en('0')}')"
        ]
        DB.execute(commands)

    class Cache:

        @staticmethod
        def load():
            values = []
            conn = sqlite3.connect(DB.db_path)
            c = conn.cursor()
            c.execute("SELECT * FROM cache")
            values.append(c.fetchall())
            c.execute("SELECT * FROM music")
            values.append(c.fetchall())
            c.execute("SELECT * FROM line")
            values.append(c.fetchall())
            c.execute("SELECT * FROM skins")
            values.append(c.fetchall())
            c.execute("SELECT * FROM skin")
            values.append(c.fetchall())
            conn.commit()

            conn.close()
            return values

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
    def check_tables():
        conn = sqlite3.connect(DB.db_path)
        c = conn.cursor()
        c.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
        tables = c.fetchall()
        checks = {
            'music': ["CREATE TABLE music(state text)",
                      "INSERT INTO music values('True')"],

            'display': ["CREATE TABLE display(size text)",
                        "INSERT INTO display values('standard')"],

            'user_data': ["CREATE TABLE user_data(level text, save text, coins text)",
                          f"INSERT INTO user_data values('{Crypt.en('1')}','{Crypt.en('None')}', '{Crypt.en('0')}')"],

            'cache': ["CREATE TABLE cache(theme text)",
                      "INSERT INTO cache values('Bright White')"],

            'line': ["CREATE TABLE line(type text)",
                     "INSERT INTO line values('new')"],

            'skins': ["CREATE TABLE skins(data text)",
                      f"INSERT INTO skins values('{Crypt.en(str(['00.png', '01.png']))}')"],

            'skin': ["CREATE TABLE skin(data text)",
                      f"INSERT INTO skin values('{Crypt.en('00.png')}')"]

        }

        copy = checks.copy()
        for table in tables:
            for check in checks:
                if table[0] == check:
                    del copy[table[0]]

        checks = copy
        for fail in checks:
            DB.execute(checks[fail])
        conn.commit()
        conn.close()

    @staticmethod
    def make_screen():
        screen_flags = pygame.SCALED | pygame.RESIZABLE
        conn = sqlite3.connect(DB.db_path)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM display")
            val = c.fetchall()[0][0]
            if val == "full":
                screen_flags = pygame.SCALED | pygame.FULLSCREEN | pygame.RESIZABLE
        except Exception as e:
            val = "standard"

        conn.commit()
        conn.close()
        screen = pygame.display.set_mode((WW, WH), screen_flags)
        return screen, val


def toggle_music():
    conn = sqlite3.connect(DB.db_path)
    c = conn.cursor()
    if Music.play:
        to_update = False
        threading.Thread(target=Music.stop_music).start()
    else:
        to_update = True
        threading.Thread(target=Music.play_music).start()

    c.execute(f"UPDATE music SET state = '{to_update}'")
    conn.commit()
    conn.close()


def line_select(state):
    User_data.line = state
    DB.execute([f"UPDATE line SET type = '{state}'"])
