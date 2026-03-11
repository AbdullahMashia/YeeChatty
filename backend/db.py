import os
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash

base_dir = os.path.dirname(os.path.dirname(__file__))
db_path = os.path.join(base_dir,"data","yeechatty.db")



class MyDataB:




    def __init__(self):
        admin_password = generate_password_hash("admin")
        with sqlite3.connect(db_path) as db:
            with open(os.path.join(base_dir,"schema.sql")) as schema:
                db.executescript(schema.read())
                db.cursor().execute("INSERT OR IGNORE INTO user (username,full_name,age,country,email,password) VALUES(?,?,?,?,?,?)",("admin","aw",0,"none","admin@yeechatty.com",admin_password))




    def add_user(self, user):
        with sqlite3.connect(db_path) as db:
                cur = db.cursor()
                cur.execute("INSERT INTO user (username,full_name,age,country,email,password) VALUES(?,?,?,?,?,?)",(user.username,user.full_name,user.age,user.country,user.email,user.password))

    def user_exist(self,username,email):
        with sqlite3.connect(db_path) as db:
            cur = db.cursor()
            user =cur.execute("SELECT username FROM user WHERE username = ? OR email = ?",(username,email)).fetchone()
            if user:
                return True
            return False

    def auth_user(self, username,password):

        with sqlite3.connect(db_path) as db:
            cur = db.cursor()
            valid_user = cur.execute("SELECT * FROM user WHERE username = ? ", (username,)).fetchone()
            if check_password_hash(valid_user[5],password):

                return valid_user[0]
            return False

