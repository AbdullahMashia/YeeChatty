import os
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
from error import Error_yee

err_db = Error_yee()

base_dir = os.path.dirname(os.path.dirname(__file__))
db_path = os.path.join(base_dir,"data","yeechatty.db")

encryptino_key = 24234231341451

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

                user = cur.execute("SELECT * FROM user WHERE id = ?",(user_id,)).fetchone()

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
            request = cur.execute("SELECT 1 FROM request_messaging WHERE sender_id = ? AND receiver_id = ? OR sender_id =? AND receiver_id =?",(send_id,rec_id,rec_id,send_id)).fetchone()

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


# requests loader
    def all_user_req(self,user_id):
        with sqlite3.connect(db_path) as db:
            db.row_factory = sqlite3.Row
            cur =db.cursor()

            all_req = cur.execute(" select request_id,user_id,type,request_state,request_time,user.username  from (select request_messaging.request_state,request_time,sender_id as user_id ,id as request_id,'incoming' as type  FROM request_messaging where receiver_id = ? union all select request_messaging.request_state,request_time,receiver_id as user_id ,id as request_id,'outgoing' as type  FROM request_messaging where sender_id = ?) as requests join user ON user.id = user_id WHERE request_state =? Group by request_id;",(user_id,user_id,"pending")).fetchall()

            if all_req is not None and len(all_req) > 0:
                all_req = [dict(req) for req in all_req]

                return all_req

            return err_db.not_request_yet


    def accept_request(self,request_id,user_id,type):
        with sqlite3.connect(db_path) as db:
            db.row_factory = sqlite3.Row
            cur =db.cursor()

            print("request_id = ",request_id)
            print("user_id = >",user_id)
            #checking if user is part of the request
            r_req = cur.execute("SELECT *  from request_messaging WHERE id = ? AND receiver_id = ? AND request_state = ?",(request_id,user_id, "pending")).fetchone()
            s_req = cur.execute("SELECT * FROM request_messaging WHERE id = ? AND sender_id = ? AND request_state = ?",(request_id,user_id, "pending")).fetchone()
            print("request === >>>",s_req)
            if r_req is not None:
                if type =="accept":

                        cur.execute("UPDATE  request_messaging SET request_state = 'accepted' WHERE id = ?",(request_id)).fetchone()



                        cur.execute("INSERT  INTO conversations (encryption_key) VALUES (?)",(encryptino_key,))
                        conv_id = cur.lastrowid
                        cur.execute("INSERT  INTO conversations_participants (user_id, conversations_id) VALUES (?,?)", (user_id,conv_id))
                        cur.execute("INSERT  INTO conversations_participants (user_id, conversations_id) VALUES (?,?)",(r_req["sender_id"],conv_id))

                        return {"success":True,"m":"request accepted successfully"}



                elif type == "deny":
                    conv_id =  cur.execute("UPDATE  request_messaging SET request_state = 'denied' WHERE id = ?",(request_id)).fetchone()

                    if cur.rowcount >0:
                        return {"type":"request deny", "m":"request has been successfully denied"}

                    return {"success":False,"m":"failed to deny the request"}


            elif r_req is None and s_req is not None:
                    cur.execute("DELETE FROM request_messaging WHERE id = ?",(request_id,)).fetchone()

                    if cur.rowcount >0:
                        return {"type":"request cancled", "m":"request has been successfully canceld"}

                    return {"success":False,"m":"failed to cancel the request"}

            return err_db.request_not_found




    def user_chats(self, user_id):
        with sqlite3.connect(db_path) as db:
            db.row_factory = sqlite3.Row
            cur =db.cursor()

            chats = cur.execute("""SELECT user.username, s.conversations_id
                                FROM user
                                JOIN conversations_participants as s ON user.id = s.user_id
                                WHERE user_id != ? AND conversations_id IN


                                (SELECT conversations_id FROM conversations_participants WHERE user_id =?) """,(user_id,user_id)).fetchall()

            if len(chats)>0:
                print(chats)
                chats = [dict(r) for r in chats]
                print(chats)
                return chats

            else:
               return  err_db.no_chatsFound




    def load_messages(self,conv_id,user_id):
        with sqlite3.connect(db_path) as db:
            db.row_factory = sqlite3.Row
            cur =db.cursor()

            checking = cur.execute("SELECT * FROM conversations_participants WHERE user_id = ? and conversations_id = ?",(user_id,conv_id)).fetchone()
            if checking is not None:
                messages = cur.execute("""
                                       SELECT u.username, m.content,m.sent_at,m.sender_id FROM user as u
                                       JOIN (SELECT * FROM messages WHERE conversations_id = ?) AS m
                                       ON u.id = m.sender_id""",(conv_id,)).fetchall()

                if len(messages) > 0:
                    messages = [dict(m) for m in messages]
                    for m in messages:
                        if m["sender_id"] == user_id:
                            m["type"] = "sent"
                        else:
                            m["type"] = "rec"
                    return messages

                return err_db.no_messages_yet
            return err_db.conv_not_exist

