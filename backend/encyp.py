import os
from dotenv import load_dotenv
load_dotenv()
from cryptography.fernet import Fernet

key = os.environ.get('ENCRYPTION_KEY')

if key is None:

    raise RuntimeError("Encryption_key enviroment variable not set")


cypher = Fernet(key.encode())



class MyEnc:


    def generate_room_key(self):
        key = cypher.encrypt(Fernet.generate_key()).decode()


        return key


    def encrypt_messages(self,key,message):
        room_key = Fernet(cypher.decrypt(key.encode()))





        message["content"]  = room_key.encrypt(message["content"].encode()).decode()



        return message



    def decrypt_messages(self, key,messages):
        room_key = Fernet(cypher.decrypt(key.encode()))

        for m in messages:
            m["content"] = room_key.decrypt(m["content"].encode()).decode()



        return messages







