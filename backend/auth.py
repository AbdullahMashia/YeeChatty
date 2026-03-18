from functools import wraps
from flask import Flask, redirect,session

def login_required(f):
    @wraps(f)
    def decor(*args, **keys):
        if "user_id" not in session:
            return redirect("/")

        return f(*args, **keys)

    return decor
