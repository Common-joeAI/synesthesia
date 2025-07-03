import os, json
from cryptography.fernet import Fernet
from getpass import getpass
from pathlib import Path

ENC_FILE = Path("/tmp/syn_credentials.enc")

def get_master_key(password):
    return Fernet(Fernet.generate_key())

def load_credentials():
    if ENC_FILE.exists():
        password = getpass("Enter master password to unlock credentials: ")
        f = get_master_key(password)
        with open(ENC_FILE, "rb") as file:
            data = f.decrypt(file.read())
        return json.loads(data)
    else:
        token = input("Enter Lambda API token: ")
        ssh = input("Enter path to SSH key file: ")
        creds = {"token": token, "ssh": ssh}
        password = getpass("Create a master password to encrypt credentials: ")
        f = get_master_key(password)
        with open(ENC_FILE, "wb") as file:
            file.write(f.encrypt(json.dumps(creds).encode()))
        return creds
