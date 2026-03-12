import os
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
from error import Error_yee

err_db = Error_yee()

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

                if check_password_hash(valid_user["password"],password):
                    return valid_user["id"]

            return False


    def user_data(self,user_name,owner_id):
        with sqlite3.connect(db_path) as db:
            db.row_factory = sqlite3.Row
            cur = db.cursor()
            user_id= cur.execute("SELECT id FROM user WHERE username = ? AND id != ?",(user_name,owner_id)).fetchone()
            if user_id is not None:


                if not self.request_exist(owner_id, user_id["id"]):
                    user_data = cur.execute("SELECT username,id FROM user WHERE username = ?",(user_name,)).fetchone()
                    user_data_j = dict(user_data)
                    user_data_j["success"]= True
                    return user_data_j

                return err_db.user_already_found

            return err_db.user_not_found

    def user_prof(self, user_id):
            with sqlite3.connect(db_path) as db:
                db.row_factory = sqlite3.Row
                cur = db.cursor()
                print("user_id==>>>>>",user_id)
                user = cur.execute("SELECT * FROM user WHERE id = ?",(user_id,)).fetchone()
                print("user_in_db===>",user)
                if user is not None:
                    return user

                return {"m":"loading"}

    def online_users(self,user_id):
        with sqlite3.connect(db_path) as db:
            db.row_factory = sqlite3.Row
            cur = db.cursor()
            all_users = cur.execute("SELECT id,username FROM user WHERE id != ? And id NOT IN (SELECT sender_id FROM request_messaging WHERE receiver_id = ?) AND id NOT IN ( SELECT receiver_id FROM request_messaging WHERE sender_id = ?) ",(user_id,user_id,user_id)).fetchall()
            all_u = [dict(row) for row in all_users]
            return all_u

    def request_exist(self,send_id, rec_id):
        with sqlite3.connect(db_path) as db:
            cur = db.cursor()
            request = cur.execute("SELECT 1 FROM request_messaging WHERE sender_id = ? AND receiver_id = ?",(send_id,rec_id)).fetchone()

            return request is not None

    def send_request(self,send_id,rec_ic):
        with sqlite3.connect(db_path) as db:
            cur =db.cursor()
            if send_id != rec_ic:
                try:
                    cur.execute("INSERT INTO request_messaging (sender_id,receiver_id) VALUES(?,?)",(send_id,rec_ic))
                    db.commit()

                    return True
                except:
                    return False
            return err_db.user_reverse_req


