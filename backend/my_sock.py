
#used Deep seek here to explain the library and how it's used
from exten import my_sock_ob
from flask_socketio import emit,join_room,leave_room,rooms
from flask import session,request,jsonify
from db import MyDataB



import random

user_data = dict()



db_ob = MyDataB()

room = 0


@my_sock_ob.on('join_room')
def joining_room(data):



    room = f"room:{data["conv_id"]}"

    user_id_soc = data.get("user_soc_id")

    join_room(room)
    emit('join_room', {"success":True,"m":"joined into room successfully","room":room})


@my_sock_ob.on('send_message')
def sending_message(data):





    res = db_ob.send_message(data)

    emit('new_message',data,room=room)


@my_sock_ob.on('connect')
def handle_connect():
    user_data["id"] = session["user_id"]
    user_data["username"] = session["username"]
    user_data["cur_room_id"]= session["conv_id"]




@my_sock_ob.on('disconnect')
def disc(d):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>disconnected")



