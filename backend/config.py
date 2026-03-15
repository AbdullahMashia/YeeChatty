from flask import Flask , session,request,render_template,redirect,url_for
from flask_socketio import SocketIO,join_room,leave_room,emit
import os

def ini_app():
    project_root = os.path.dirname(os.path.dirname(__file__))

    app = Flask(__name__, template_folder=os.path.join(project_root , "frontend/templates") ,   static_folder= os.path.join(project_root, "frontend/static"))
    app.config["SECRET_KEY"] = "hellowolrd"
    app.config["SESSION_TYPE"] = "filesystem"

    return app