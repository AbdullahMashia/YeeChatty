from flask import Flask, render_template,jsonify,request, redirect,session
from db import MyDataB
from error import Error_yee
from flask_session import Session
from auth import login_required

import os
project_root = os.path.dirname(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(project_root , "frontend/templates") ,   static_folder= os.path.join(project_root, "frontend/static"))

db_ob = MyDataB()

err_con = Error_yee()
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
@app.route("/")
def splash():
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
            return redirect("/chat")
        return jsonify(err_con.wrong_creden)


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

            return redirect("/chat")


    return render_template("register.html")


@app.route("/chat")
@login_required
def chat():
    print(session)
    return render_template("chats.html")


@login_required
@app.route("/chat/1")
def conv():
    return render_template("conversation.html")


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
    user_data = db_ob.user_data(session["user_id"])
    return render_template("profile.html",user_dataT=user_data)


#/apis

@app.route("/api/users/find")
@login_required
def find_users():
    users_f = [dict(row) for row in db_ob.online_users() if row['id'] != session["user_id"]]



    print(users_f)
    return (jsonify(users_f))



@app.route("/api/requests",methods=["POST","GET"])
@login_required
def requests_handler():
    data_s = request.get_json(force=True)


    return jsonify(reso)

