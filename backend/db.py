import os
import sqlite3

base_dir = os.path.dirname(os.path.dirname(__file__))
db_path = os.path.join(base_dir,"data","yeechatty.db")



class db:

    def start_db(self):
        with sqlite3.connect(db_path) as db:
            with open(os.path.join(base_dir,"schema.sql")) as schema:
                db.executescript(schema.read())

    def add_user(self, user):
        with sqlite3.connect(db_path) as db:
                cur = db.cursor()
                cur.execute("INSERT INTO user (username,full_name,age,country,email,password) VALUES(?,?,?,?,?,?,?)",(user.username,user.full_name,user.age,user.country,user.email,user.password))

    def exist(self,username,email):
        with sqlite3.connect(db_path) as db:
            cur = db.cursor()
            user =cur.execute("SELECT username FROM user WHERE username = ? OR email = ?",(username,email)).fetchone()
            if user:
                return True
            return False

    def auth_user(self, username,password):
        with sqlite3.connect(db_path) as db:
            cur = db.cursor()
            valid_user = cur.execute("SELECT user_id FROM user WHERE username = ? AND password= ?", (username,password)).fetchone()
            return valid_user is not None