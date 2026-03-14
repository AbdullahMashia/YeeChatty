

# from app import my_soc
# from flask_socketio import emit,join_room,leave_room
# from db import MyDataB

# db_ob = MyDataB()




# @my_soc.on('join_room')
# def joining_room(data):
#     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.joined")
#     room = f"conversation:{conv_id}"
#     # join_room(room)


# @my_soc.on('send_message')
# def sending_message(data):
#     content = data.get('m')
#     username = data.get('username')
#     room = f"conversation:{conv_id}"
#     emit('new_message',{'username':username,'m':content},room=room)

# @socketio.on('connect')
# def handle_connect():
#     print(f'Client {request.sid} connected')


from app import my_soc
from flask_socketio import emit, join_room, leave_room
from flask import request
from db import MyDataB

db_ob = MyDataB()

@my_soc.on('join_room')
def joining_room(data):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> joined")
    conv_id = data.get('conversation_id')          # get from client data
    if not conv_id:
        emit('error', {'message': 'Missing conversation_id'})
        return
    room = f"conversation:{conv_id}"
    join_room(room)
    emit('joined', {'room': room}, room=room)      # optional confirmation

@my_soc.on('send_message')
def sending_message(data):
    conv_id = data.get('conversation_id')
    content = data.get('content')
    sender_id = data.get('user_id')   # or get from current_user if using Flask-Login

    if not conv_id or not content:
        emit('error', {'message': 'Missing data'})
        return

    # Save message to database
    message_id = db_ob.save_message(conv_id, sender_id, content)

    # Prepare broadcast data
    room = f"conversation:{conv_id}"
    emit('new_message', {
        'id': message_id,
        'sender_id': sender_id,
        'content': content,
        'sent_at': datetime.utcnow().isoformat()
    }, room=room)

@my_soc.on('connect')
def handle_connect():
    print(f'Client {request.sid} connected')