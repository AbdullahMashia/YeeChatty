from flask import Flask, render_template,jsonify,request, redirect,session
from db import MyDataB
from error import Error_yee
from flask_session import Session
from auth import login_required
from response import Response
import os
from exten import my_sock_ob
from flask_socketio import SocketIO
from config import ini_app
import my_sock






app = ini_app()

my_sock_ob.init_app(app, cors_allowed_origins="*")
#initializing socket ob


#objects:
db_ob = MyDataB()

err_con = Error_yee()
res_ob = Response()





app.config["SESSION_TYPE"] = "filesystem"









@app.route("/")
def splash():
    session.clear()
    return render_template("splash.html")


@app.route("/login", methods=["POST","GET"])
def login():
    if  request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_id = db_ob.auth_user(username,password)
        if user_id:

            session["username"] = username

            session["user_id"]  = user_id
            return redirect("/chats")
        return jsonify(err_con.wrong_creden)

    session.clear()
    return render_template("login.html")

@app.route("/register",methods=["POST","GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")

        email = request.form.get("email")

        if not db_ob.user_exist(username,email):
            password = request.form.get("password")
            cp =request.form.get("cpassword")

            if password != cp :

                return jsonify(err_con.password_match)
            r_user = {
                'username':username,
                "fullname":request.form.get("fullname"),
                "age":request.form.get("age"),
                "country":request.form.get("country"),
                "email": email,
                "password":password
            }
            user_id = db_ob.add_user(r_user)
           # adding the session keys
            session["username"] = username
            session["user_id"]  =user_id


            return redirect("/chats")

    session.clear()
    return render_template("register.html")


#chat page
@app.route("/chats")
@login_required
def chat():

    return render_template("chats.html",user_nameT=session["username"])



@app.route("/room",methods=["POST","GET"])
@login_required
def room():
    if request.method =="POST":
        session["conv_id"] = request.get_json(force=True)["conv_id"]


        return jsonify({"type":"open_room","m":"opened successfully"})

    db_ob.user_info["page_reloaded"] = True


    return render_template("room.html")


@app.route("/request")
@login_required
def request_f():
    return render_template("request.html")



@app.route("/find")
@login_required
def find():
    return render_template("find.html")



@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


@app.route("/profile")
@login_required
def profile():
    user_data = db_ob.user_prof(session["user_id"])
    print(user_data)
    return render_template("profile.html",user_dataT=user_data)


#/apis

@app.route("/api/users/find",methods = ["POST","GET"])
@login_required
def find_users():
    if request.method== "GET":
        users_f = [dict(row) for row in db_ob.online_users(session["user_id"]) if row['id'] != session["user_id"]]
        return (jsonify(users_f))

    else:
        data_f = request.get_json(force=True)
        user_f = db_ob.user_data(data_f["username"], session["user_id"])


        return jsonify(user_f)








#sending requests in find page
@app.route("/api/requests/send",methods=["POST","GET"])
@login_required
def requests_sender():
    data_s = request.get_json(force=True)


    if not db_ob.request_exist(session["user_id"], data_s["rec_id"]):
        db_ob.send_request(session["user_id"],data_s["rec_id"])
        return jsonify(res_ob.request_sent)

    return err_con.request_sent

# returns all requests

@app.route("/api/requests",)
@login_required
def load_requests():
    all_request = db_ob.all_user_req(session["user_id"])
    print("reqqqqq === >>", all_request)
    return jsonify(all_request)




# handles the actions of requests
@app.route("/api/request/handler", methods=["POST","GET"])
@login_required
def request_hanlder():
    req = request.get_json()
    type = req["type"]


    res = db_ob.accept_request(req["request_id"],session["user_id"],type)

    return jsonify(res)



#chats content
#returns all rooms
@app.route("/api/chats")
@login_required
def load_chats():
    chats = db_ob.user_chats(session["user_id"])

    return jsonify(chats)




@app.route("/api/chats/room")
@login_required
def load_messages():

    messages = db_ob.load_messages(session["conv_id"],session["user_id"])




    return jsonify(messages)






if __name__ == "__main__":
    print('strarted debugging')
    my_sock_ob.run(app,debug=True)
