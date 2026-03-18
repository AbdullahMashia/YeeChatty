import os
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
from error import Error_yee
from encyp import MyEnc
from datetime import date, time,datetime




dd = datetime.now()


en_key = os.environ.get('ENCRYPTION_KEY')

err_db = Error_yee()

base_dir = os.path.dirname(os.path.dirname(__file__))
db_path = os.path.join(base_dir,"data","yeechatty.db")


en_ob = MyEnc()

class MyDataB:

    user_info= dict()


    def __init__(self):
        admin_password = generate_password_hash("admin")
        with sqlite3.connect(db_path) as db:
            with open(os.path.join(base_dir,"schema.sql")) as schema:
                db.executescript(schema.read())
                db.cursor().execute("INSERT OR IGNORE INTO user (username,full_name,age,country,email,password) VALUES(?,?,?,?,?,?)",("admin","aw",0,"none","admin@yeechatty.com",admin_password))

        self.user_info["username"] = None
        self.user_info["cur_room"] = None
        self.user_info["last_message"] = None
        self.user_info["page_reloaded"] = False
        self.user_info["reload_old"] = False

        self.user_info["room_key"] = None

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
                    self.user_info["username"] = username
                    return valid_user["id"]

            return False


    def user_data(self,user_name,owner_id):
        with sqlite3.connect(db_path) as db:
            db.row_factory = sqlite3.Row
            cur = db.cursor()
            user_id= cur.execute("SELECT id FROM user WHERE username = ? ",(user_name,)).fetchone()
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


            #checking if user is part of the request
            r_req = cur.execute("SELECT *  from request_messaging WHERE id = ? AND receiver_id = ? AND request_state = ?",(request_id,user_id, "pending")).fetchone()
            s_req = cur.execute("SELECT * FROM request_messaging WHERE id = ? AND sender_id = ? AND request_state = ?",(request_id,user_id, "pending")).fetchone()

            if r_req is not None:
                if type =="accept":


                        room_en_key = en_ob.generate_room_key()


                        cur.execute("UPDATE  request_messaging SET request_state = 'accepted' WHERE id = ?",(request_id,)).fetchone()



                        cur.execute("INSERT  INTO conversations (encryption_key) VALUES (?)",(room_en_key,))
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

                chats = [dict(r) for r in chats]

                return chats

            else:
               return  err_db.no_chatsFound




    def load_messages(self,conv_id,user_id):
        with sqlite3.connect(db_path) as db:
            db.row_factory = sqlite3.Row
            cur =db.cursor()



            checking = cur.execute("SELECT 1 FROM conversations_participants WHERE user_id = ? and conversations_id = ?",(user_id,conv_id)).fetchone()
            if checking is not None:
                username = cur.execute("select username from user where id = ?",(user_id,)).fetchone()["username"]
                self.user_info["cur_room"]= conv_id



                if self.user_info["page_reloaded"]:
                    self.user_info["last_message"] = cur.execute("Select id from messages Where conversations_id = ? order by id desc limit 1",(conv_id,)).fetchone()["id"]
                    self.user_info["page_reloaded"] = False
                    self.user_info['reload_old'] = False

                print("Before ====================>",self.user_info["last_message"])
                messages = cur.execute("""
                                       SELECT u.username, m.content,m.sent_at,m.sender_id, m.id FROM user as u
                                       JOIN (SELECT * FROM messages WHERE conversations_id = ?  ) AS m
                                       ON u.id = m.sender_id WHERE m.id < ? order by sent_at desc limit 20""",(conv_id,self.user_info["last_message"],)).fetchall()




# Initiating the key and encryption object
                key = cur.execute("SELECT encryption_key FROM conversations WHERE id = ?",(conv_id,)).fetchone()
                en_ob.key_init(key["encryption_key"])

                if messages is None:
                    return err_db.no_messages_left
                room_members = cur.execute("SELECT COUNT(user_id) as members,user_id FROM conversations_participants WHERE conversations_id = ? AND user_id != ?",(conv_id,user_id)).fetchone()
                room_user = cur.execute("SELECT * FROM user WHERE id = ?",(room_members["user_id"],)).fetchone()["username"]

                # for future room naming
                if room_members["members"] > 1:
                    room_name = db.room_name()


                else:
                    room_user = cur.execute("SELECT * FROM user WHERE id = ?",(room_members["user_id"],)).fetchone()["username"]
                    room_name = room_user

                if len(messages) > 0:
                    messages = [dict(m) for m in messages]
                    self.user_info["last_message"]  = messages[-1]["id"]


#checking if there is still messages:
                    m_left = cur.execute("Select 1 FROM messages WHERE conversations_id = ? AND  id <?",(conv_id,self.user_info["last_message"]),).fetchone()
                    if m_left is not None:
                        messages_left = True
                    else:
                        messages_left = False




                    self.user_info["room_key"] = key


                    decrypted_messages = en_ob.decrypt_all_messages(messages)



                    messages.insert(0,{"conv_id":conv_id,"myusername":username,'room_name':room_name,"status":"load",'still':messages_left,'reload_old':self.user_info["reload_old"]})

                    self.user_info['reload_old'] = True


                    return decrypted_messages

                # if empty
                res = err_db.no_messages_yet
                res["conv_id"] = conv_id
                res["myusername"] = username
                res["room_name"] = room_name
                return res
            return err_db.conv_not_exist




    def send_message(self,m_data):
            with sqlite3.connect(db_path) as db:
                db.row_factory = sqlite3.Row
                cur =db.cursor()
                user_id = cur.execute("Select id from user where username = ?",(m_data["username"],)).fetchone()["id"]

                checking = cur.execute("SELECT 1 FROM conversations_participants WHERE user_id = ? and conversations_id = ?",(user_id,m_data["conv_id"])).fetchone()
                if checking is not None:

                    key = cur.execute("SELECT encryption_key FROM conversations WHERE id = ?",(m_data["conv_id"],)).fetchone()
                    if key is not None:
                        key = key["encryption_key"]
                    encrypted_m = en_ob.encrypt_message(m_data["content"])
                    cur.execute("INSERT INTO messages (conversations_id,sender_id,content,sent_at) VALUES(?,?,?,?)",(m_data["conv_id"],user_id,encrypted_m,m_data["sent_at"]))
                    return {"success":True,"m":"message saved successfully"}
                return err_db.conv_not_exist


    def room_name(self,conv_id):
            with sqlite3.connect(db_path) as db:
                db.row_factory = sqlite3.Row
                cur =db.cursor()

