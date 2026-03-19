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
  ### layout.html:
    >Holds the template for the whole project especially the header, logo, and the button

  ###splash.html:
    >It is where the user redirect first time , it has introduction about Yeechatty and inside it a user can register or login

  ###login.html:
    >through which a user can login into YeeChatty

  ###Register.html:
    >Where user can create their account for the first time

  ###find.html:
    > A user can find all users who are using this app , and if they can use search for finding a specific user

  ###request.html:
    > all request resides here both incoming and outgoing, here a user can accept or deny a request
  ### chats.html:
   > all chat rooms are listed here for users that share a conversation room with the user

  ### room.html:
   > Here is where the user can send and reseive messages live with a specific user

##Media
  ##css:
  > contains the style for all html pages

  ## js:
  ### chat.js:
  >  here we have a asynch functions to load all chat rooms as json files and display them in chat.html

  ### find.js:
  > find.js has two functions for fetching data , the first one is for fetching all users, the second one is for fetching a single user info as json

  ###request.js:
    > contains asynch functions for fetching request data and sending them when accepting or denying
  ### room.js:
  > is the most complex js file here, since it handles the websockets that enables the user to send and receive messages live, and build the ui for the user based on the returned data


## Backend
  ###initiate_app.py
    > where the app object is created and returned to app.py (to avoid import loop )
  ### eten.py:
   > Where socketio object is created before initialized in app.py
 ### error.py:
   > prepeared error respones resides here
 ### encyp.py:
   > Here key generation for each room, encrypting, decrypting keys, and messages are done here
 ###auth.py:
 > Here the app makes sure only authorized people can access the resouces (@login_required)

### db.py:
> db.py is the brain of Yeechatty, it has all the logic for yeechatty database interactions such as :
> - creating new accounts
> - login
> - send requests
> - accepted or deny requests
> - search for user
> - create the default admin user
> - create the perwritten tables and indexes from file schema.sql

 ### my_sock.py:
   > holds the logic for webSockets from flask_socketio library in flask:
> - holds the events for:
>    - connection
>    - disconnect
>    - join_room
>    - send_message
 ### app.py:
   > here all the mechanical parts are joined to build a functioning web App:
> All routes are done here
> All api/ endpoints are here
> user experience sequance is built here
> 

## requirements.txt:
> where all dependencies are listed

  


