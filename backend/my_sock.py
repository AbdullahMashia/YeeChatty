
#used Deep seek here to explain the library and how it's used
from exten import my_sock_ob
from flask_socketio import emit,join_room,leave_room,rooms
from flask import session,request,jsonify
from db import MyDataB



import random





db_ob = MyDataB()



@my_sock_ob.on('join_room')
def joining_room(data):







    join_room( session["cur_room"])
    emit('join_room', {"success":True,"m":"joined into room successfully","room": session["cur_room"]})


@my_sock_ob.on('send_message')
def sending_message(data):





    res = db_ob.send_message(data)

    emit('new_message',data,room= session["cur_room"])


@my_sock_ob.on('connect')
def handle_connect():
    session["cur_room"]= session["conv_id"]




@my_sock_ob.on('disconnect')
def disc():
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>disconnected")



