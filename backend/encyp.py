import os
from dotenv import load_dotenv
load_dotenv()
from cryptography.fernet import Fernet



key = os.environ.get('ENCRYPTION_KEY')

print("first key ==== > ",key)
if key is None:

    raise RuntimeError("Encryption_key enviroment variable not set")


cypher = Fernet(key.encode())




class MyEnc:


    def __init__(self):
        self.room_key = None
        self.room_obj = None

    def key_init(self,en_key):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>key initiaed")

        self.room_key =  cypher.decrypt(en_key.encode()).decode()


        self.room_obj = Fernet(self.room_key.encode())



    def generate_room_key(self):
        key = cypher.encrypt(Fernet.generate_key()).decode()


        return key


    def encrypt_message(self,message):





        message  = self.room_obj.encrypt(message.encode()).decode()



        return message



    def decrypt_all_messages(self,messages) :



        for m in messages:

            m["content"] = self.decrypt_per_message(m["content"])



        return messages




    def decrypt_per_message(self,message):

        decrypted_message = self.room_obj.decrypt(message.encode()).decode()



        return decrypted_message







