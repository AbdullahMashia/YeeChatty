from flask import Flask, render_template
import os
project_root = os.path.dirname(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(project_root , "frontend/templates") ,   static_folder= os.path.join(project_root, "frontend/static"))


@app.route("/")
def splash():
    return render_template("splash.html")

