# YeeChatty

#### Video Demo: `<url here>`

#### Description:


##🌏 What is Yeechatty?

#### Yeechatty is a web based chat application, that enables users to create accounts login with their credeintials, `<br>`find new users, send them message_request, accept request messaging , and exchange messages with those people, also a logged_in user can see their username under the profile icon, and other data inside the profile page


## :electron: Technologies used:
- HTML 5
- CSS
- JS ES2025 / ES2026
- Flask
- eventlet
- python
- Jinja
  
## 🩹 Problem Yeechatty solves:
#### Yeechatty solves the problem of finding a secure and reliable chatting web app. that enables users of finding other potentional users and exchange messages, or even deny the messaging requests, also it solves the problem of bandwith usage for small chat apps since it only loads the last 30 messages if user scrolls up to see old messages it request the secnd after last 30 messages, and so on
## YeeChatty Project has the following structure:


## 🥇 Yeechatty Features:
- it has an instant messaging using socketio from flask
- evry room in the app has it's own encyprtion key for security
- all rooms' encryption keys are encrypted with a global key and that key is stored as an environment variable
- A user can find a specific user if they have that user's username
- A user can send request messageing to all users they can find in the find tab
- A user can accept or deny messaging_requests





## Structure of Yeechatty:
## - /

- README.md
- requirements.txt
- schema.sql
- /backend/
  - app.py
  - auth.py
  - initiate_app.py
  - db.py
  - encyp.py
  - error.py
  - exten.py
  - my_sock.py
- /frontend/
  - static/
    - CSS/
      - chat.css
      - conv.css
      - find.css
      - login.css
      - mainStyle.css
      - profile.css
      - register.css
      - request.css
      - room.css
      - splash.css
    - js/
      - chat.js
      - find.js
      - profile.js
      - request.js
      - room.js
    - media/
      - audio/
        - rec.mp3
      - imgs/
        - chat.png
        - chatBack.jpg
        - find.png
        - myIntro.gif
        - myicon.png
        - mylogo.png
        - profile.png
        - request.png
        - s.jpg
        - send.png
  - templates/
    - layout.html
    - splash.html
    - register.html
    - login.html
    - find.html
    - request.html
    - chats.html
    - room.html

## What files Does Yeechatty have and what does each one do?
# FrontEnd

## templates
 -### layout.html:
    >Holds the template for the whole project especially the header, logo, and the button

  -###splash.html:
    >It is where the user redirect first time , it has introduction about Yeechatty and inside it a user can register or login

  -##login.html:
    >through which a user can login into YeeChatty

  -##Register.html:


