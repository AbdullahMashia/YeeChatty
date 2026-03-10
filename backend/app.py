from flask import Flask, render_template
import os
project_root = os.path.dirname(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(project_root , "frontend/templates") ,   static_folder= os.path.join(project_root, "frontend/static"))


@app.route("/")
def splash():
    return render_template("splash.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/chat")
def chat():
    return render_template("chats.html")

@app.route("/chat/1")
def conv():
    return render_template("conversation.html")