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



# adding new users
    def add_user(self, r_user):
        with sqlite3.connect(db_path) as db:
                cur = db.cursor()
                cur.execute("INSERT INTO user (username,full_name,age,country,email,password) VALUES(?,?,?,?,?,?)",(r_user['username'],r_user['fullname'],r_user['age'],r_user['country'],r_user['email'],generate_password_hash(r_user['password'])))
                user_id = cur.execute("SELECT id FROM user WHERE username = ?",(r_user["username"],)).fetchone()[0]
                return user_id


# checking if uesr already exists (username, password)
    def user_exist(self,username,email):
        with sqlite3.connect(db_path) as db:
            cur = db.cursor()
            user =cur.execute("SELECT 1 FROM user WHERE username = ? OR email = ?",(username,email)).fetchone()
            if user is not None:
                return True
            return False

# authenticate users
    def auth_user(self, username,password):

        with sqlite3.connect(db_path) as db:
            db.row_factory = sqlite3.Row
            cur = db.cursor()
            valid_user = cur.execute("SELECT * FROM user WHERE username = ? ", (username,)).fetchone()
            if valid_user is not None:

                print("**********************************")
                if check_password_hash(valid_user["password"],password):
                    print("user_id=>",valid_user["id"])
                    return valid_user["id"]
            print("user is here >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            return False


    def user_data(self,user_id):
        with sqlite3.connect(db_path) as db:
            db.row_factory = sqlite3.Row
            cur = db.cursor()
            user_data = cur.execute("SELECT * FROM user WHERE id = ?",(user_id,)).fetchone()

            return user_data


    def online_users(self):
        with sqlite3.connect(db_path) as db:
            db.row_factory = sqlite3.Row
            cur = db.cursor()
            all_users = cur.execute("SELECT id,username FROM user").fetchall()
            all_u = [dict(row) for row in all_users]
            return all_u

