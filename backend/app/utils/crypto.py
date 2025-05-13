from cryptography.fernet import Fernet
import os

# It's crucial to set FERNET_KEY in your environment variables.
# You can generate a key using:
# python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
# FERNET_KEY will be fetched dynamically in encrypt/decrypt functions

def get_fernet_instance():
    """Creates a Fernet instance using the current FERNET_KEY environment variable."""
    fernet_key_env = os.getenv("FERNET_KEY")
    if not fernet_key_env:
        raise ValueError("FERNET_KEY environment variable not set. Please generate and set a Fernet key.")
    return Fernet(fernet_key_env.encode()) # Ensure the key is bytes

def encrypt_message(msg: str) -> str:
    """Encrypts a message string."""
    if not isinstance(msg, str):
        raise TypeError("Message to encrypt must be a string.")
    fernet = get_fernet_instance()
    return fernet.encrypt(msg.encode()).decode()

def decrypt_message(token: str) -> str:
    """Decrypts an encrypted message token string."""
    if not isinstance(token, str):
        raise TypeError("Token to decrypt must be a string.")
    fernet = get_fernet_instance()
    return fernet.decrypt(token.encode()).decode()