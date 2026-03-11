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
    if  request.method == "post":
        username = request.form.get("username")
        password = request.form.get("password")
        if db_ob.auth_user(username,password):
            return redirect("/chat")
        return jsonify(err_con.wrong_creden)


    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@login_required
@app.route("/chat")
def chat():
    return render_template("chats.html")

@app.route("/chat/1")
def conv():
    return render_template("conversation.html")


@app.route("/request")
def request_f():
    return render_template("request.html")


@app.route("/find")
def find():
    return render_template("find.html")