

CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY,
  username VARCHAR (50) unique  not null,
  full_name VARCHAR(50),
  age int,
    country VARCHAR(30),
    email VARCHAR(100) unique,
  password VARCHAR (250) not null,



  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP




);
CREATE TABLE IF NOT EXISTS conversations(
  id INTEGER PRIMARY KEY,
  encryption_key varchar(50) not null,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_message_read INTEGER ,

  FOREIGN KEY (last_message_read)  REFERENCES messages(id)
);

CREATE  TABLE IF NOT EXISTS conversations_participants (
  user_id int not null,
  conversations_id int not null,
  joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   last_message_read INTEGER,
   FOREIGN KEY (last_message_read) REFERENCES messages(id),
  PRIMARY KEY (user_id,conversations_id),
  FOREIGN KEY (user_id) references user(id),
  FOREIGN KEY (conversations_id) references conversations(id)
);

CREATE TABLE IF NOT EXISTS request_messaging(
  id INTEGER PRIMARY KEY,
  sender_id int not null,
  receiver_id int not null,
  request_state VARCHAR(10) default 'pending',
 request_time timestamp default CURRENT_TIMESTAMP,

 FOREIGN KEY (sender_id) references user(id),
 FOREIGN KEY(receiver_id) references user(id)

);
CREATE TABLE IF NOT EXISTS messages(
  id INTEGER PRIMARY KEY,
  conversations_id int not null,
  sender_id int not null,
  content varchar(1024) not null default ' ',
  sent_at timestamp default CURRENT_TIMESTAMP,
  r_type varchar(10) default 'text',
  FOREIGN KEY(conversations_id) references conversations(id),
  FOREIGN KEY (sender_id) references user(id)
);


CREATE unique INDEX IF NOT EXISTS  idx_CP_conversation  ON conversations_participants(user_id, conversations_id) ;
CREATE  INDEX IF NOT EXISTS idx_MG_message ON messages(conversations_id,sent_at) ;
CREATE UNIQUE INDEX  IF NOT EXISTS idx_RM_request ON request_messaging(receiver_id, request_state,sender_id);



