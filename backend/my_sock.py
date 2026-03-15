

from exten import my_sock_ob
from flask_socketio import emit,join_room,leave_room,rooms
from flask import session,request,jsonify
from db import MyDataB


import random



username = ''
conv_id = 0
user_id = 0

db_ob = MyDataB()

room = 0


@my_sock_ob.on('join_room')
def joining_room(data):


    room = f"room:{data["conv_id"]}"
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.joined room =>",room)
    user_id_soc = data.get("user_soc_id")
    print("user_id_soc ======>",user_id_soc)
    join_room(room)
    emit('join_room', {"success":True,"m":"joined into room successfully","room":room})


@my_sock_ob.on('send_message')
def sending_message(data):


    print("new_date = >",data["sent_at"])
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>send_messag")


    res = db_ob.send_message(data)
    print(res)
    emit('new_message',data,room=room)


@my_sock_ob.on('connect')
def handle_connect():
    user_id  = session["user_id"]
    username = session["username"]
    conv_id = session["conv_id"]
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>connected")


@my_sock_ob.on('disconnect')
def disc(d):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>dis")
