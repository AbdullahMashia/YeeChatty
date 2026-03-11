from flask import Flask, render_template,jsonify,request, redirect
from flask_login import login_required
from db import MyDataB
from error import Error_yee

import os
project_root = os.path.dirname(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(project_root , "frontend/templates") ,   static_folder= os.path.join(project_root, "frontend/static"))

db_ob = MyDataB()
err_con = Error_yee()

@app.route("/")
def splash():
    return render_template("splash.html")


@app.route("/login", methods=["POST","GET"])
def login():
    if  request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if db_ob.auth_user(username,password):
            return redirect("/chat")
        return jsonify(err_con.wrong_creden)


    return render_template("login.html")

@app.route("/register",methods=["POST","GET"])
def register():
    if request.method == "POST":
        print(".....................uername=")

        username = request.form.get("username")

        email = request.form.get("email")

        if not db_ob.user_exist(username,email):
            password = request.form.get("password")
            cp =request.form.get("Cpassword")

            if password != cp :
                return jsonify(err_con.password_match)
            r_user = {
                "username":username,
                "fullname":request.form.get("fullname"),
                "age":request.form.get("age"),
                "country":request.form.get("country"),
                "email": email,
                "password":password
            }
            db_ob.add_user(r_user)


    return render_template("register.html")


@login_required
@app.route("/chat")
def chat():
    return render_template("chats.html")


@login_required
@app.route("/chat/1")
def conv():
    return render_template("conversation.html")

@login_required
@app.route("/request")
def request_f():
    return render_template("request.html")


@login_required
@app.route("/find")
def find():
    return render_template("find.html")