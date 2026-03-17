import os
from cryptography.fernet import Fernet

# Load the key from environment (string)
key_str = os.environ.get('ENCRYPTION_KEY')
if key_str is None:
    raise ValueError("ENCRYPTION_KEY environment variable not set")

# Create Fernet cipher instance
cipher = Fernet(key_str.encode())


print(key_str)