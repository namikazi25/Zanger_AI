import unittest
import os
from cryptography.fernet import InvalidToken
from backend.app.utils.crypto import encrypt_message, decrypt_message

class TestCryptoUtils(unittest.TestCase):

    def setUp(self):
        # Ensure FERNET_KEY is available for tests, similar to how crypto.py checks
        if not os.getenv("FERNET_KEY"):
            raise ValueError("FERNET_KEY environment variable not set. Cannot run crypto tests.")
        self.sample_message = "This is a secret message!"
        self.non_string_input = 12345

    def test_encrypt_decrypt_successful(self):
        """Test successful encryption and decryption of a message."""
        encrypted_token = encrypt_message(self.sample_message)
        self.assertIsInstance(encrypted_token, str)
        self.assertNotEqual(encrypted_token, self.sample_message)
        
        decrypted_message_text = decrypt_message(encrypted_token)
        self.assertEqual(decrypted_message_text, self.sample_message)

    def test_encrypt_message_type_error(self):
        """Test encrypt_message raises TypeError for non-string input."""
        with self.assertRaisesRegex(TypeError, "Message to encrypt must be a string."):
            encrypt_message(self.non_string_input)

    def test_decrypt_message_type_error(self):
        """Test decrypt_message raises TypeError for non-string input."""
        with self.assertRaisesRegex(TypeError, "Token to decrypt must be a string."):
            decrypt_message(self.non_string_input)

    def test_decrypt_invalid_token(self):
        """Test decrypt_message raises InvalidToken for a malformed/invalid token."""
        invalid_token = "this_is_not_a_valid_fernet_token"
        with self.assertRaises(InvalidToken):
            decrypt_message(invalid_token)

    def test_decrypt_empty_string_token(self):
        """Test decrypt_message with an empty string token (should raise error)."""
        # Fernet tokens are base64 encoded and have a structure; an empty string is invalid.
        with self.assertRaises(InvalidToken):
            decrypt_message("")

    def test_encrypt_empty_string(self):
        """Test encryption and decryption of an empty string."""
        encrypted_token = encrypt_message("")
        self.assertIsInstance(encrypted_token, str)
        decrypted_message_text = decrypt_message(encrypted_token)
        self.assertEqual(decrypted_message_text, "")

if __name__ == '__main__':
    # This allows running the tests directly from this file
    # For a real project, you'd use a test runner like pytest
    if not os.getenv("FERNET_KEY"):
        print("WARNING: FERNET_KEY is not set. Crypto tests might fail or use a default if crypto.py has one.")
        print("Please set FERNET_KEY in your environment or .env file.")
        # For local testing convenience, you might temporarily set it here, but this is not best practice for shared code.
        # os.environ["FERNET_KEY"] = Fernet.generate_key().decode() # Example: Generate a temporary key
    
    unittest.main()