
import os
import json
import base64
import getpass
from cryptography.fernet import Fernet

SECRETS_FILE = "secrets.enc"

def generate_key(master_password: str) -> bytes:
    return base64.urlsafe_b64encode(master_password.encode("utf-8").ljust(32)[:32])

def encrypt_secrets(secrets: dict, master_password: str):
    key = generate_key(master_password)
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(json.dumps(secrets).encode())
    with open(SECRETS_FILE, "wb") as file:
        file.write(encrypted_data)
    print("🔐 Secrets saved and encrypted.")

def decrypt_secrets(master_password: str) -> dict:
    key = generate_key(master_password)
    fernet = Fernet(key)
    if not os.path.exists(SECRETS_FILE):
        raise FileNotFoundError("Secrets file not found.")
    with open(SECRETS_FILE, "rb") as file:
        encrypted_data = file.read()
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
    except Exception:
        raise ValueError("Invalid master password or corrupted secrets file.")

def setup_secrets():
    print("🛡️ First-time setup: enter your secrets.")
    lambda_api = input("Lambda API Token: ").strip()
    ssh_key = input("Path to SSH private key file: ").strip()
    ssh_user = input("SSH username: ").strip()
    master_pwd = getpass.getpass("Create master password to protect your secrets: ")
    encrypt_secrets({
        "lambda_api_key": lambda_api,
        "ssh_key_path": ssh_key,
        "ssh_user": ssh_user
    }, master_pwd)

def load_secrets():
    if not os.path.exists(SECRETS_FILE):
        print("Secrets not found. Run setup_secrets() first.")
        return None
    master_pwd = getpass.getpass("Enter master password to unlock secrets: ")
    try:
        return decrypt_secrets(master_pwd)
    except ValueError as e:
        print(f"❌ Error: {e}")
        return None
