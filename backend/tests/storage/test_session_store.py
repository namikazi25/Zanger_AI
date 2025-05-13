import unittest
from unittest.mock import patch, MagicMock, call
import os
import json

# Temporarily adjust path for imports if tests are run directly and backend is a module
import sys
if os.path.join(os.getcwd(), 'backend') not in sys.path and os.path.join(os.getcwd(), '..', 'backend') not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app.storage.session_store import SupabaseSessionStore
from backend.app.utils.crypto import encrypt_message, decrypt_message # Used by the class, ensure FERNET_KEY is available
from cryptography.fernet import InvalidToken

# Define a test Fernet key - ensure this matches what crypto.py would expect if FERNET_KEY is set
TEST_FERNET_KEY = ""
TEST_SUPABASE_URL = "http://test.supabase.co"
TEST_SUPABASE_API_KEY = "test_supabase_api_key"

class TestSupabaseSessionStore(unittest.TestCase):

    @patch.dict(os.environ, {
        "SUPABASE_URL": TEST_SUPABASE_URL,
        "SUPABASE_API_KEY": TEST_SUPABASE_API_KEY,
        "FERNET_KEY": TEST_FERNET_KEY
    })
    @patch('backend.app.storage.session_store.create_client')
    def setUp(self, mock_create_client):
        # Ensure crypto module uses the test key if it re-initializes fernet based on os.getenv
        # This is a bit tricky as crypto.py initializes fernet on import.
        # For robust testing, crypto.py might need a way to reconfigure its key or be patched itself.
        # However, since FERNET_KEY is set in environ, crypto.py *should* pick it up.
        
        self.mock_supabase_client = MagicMock()
        mock_create_client.return_value = self.mock_supabase_client
        self.store = SupabaseSessionStore()
        mock_create_client.assert_called_once_with(TEST_SUPABASE_URL, TEST_SUPABASE_API_KEY)

    def _get_mock_response(self, data, error=None):
        mock_response = MagicMock()
        mock_response.data = data
        mock_response.error = error
        return mock_response

    def test_get_session_exists_with_messages(self):
        """Test retrieving an existing session with messages."""
        session_id = "test-session-1"
        raw_messages = [
            {"role": "user", "text": "Hello", "timestamp": "ts1"},
            {"role": "agent", "text": "Hi there", "timestamp": "ts2"}
        ]
        encrypted_messages = [
            {"role": msg["role"], "text": encrypt_message(msg["text"]), "timestamp": msg["timestamp"]}
            for msg in raw_messages
        ]
        db_data = {"session_id": session_id, "messages": encrypted_messages, "metadata": {"key": "value"}}
        
        self.mock_supabase_client.table().select().eq().single().execute.return_value = self._get_mock_response(db_data)
        
        result = self.store.get(session_id)
        
        self.mock_supabase_client.table.assert_called_with("sessions")
        self.mock_supabase_client.table().select.assert_called_with("*")
        self.mock_supabase_client.table().select().eq.assert_called_with("session_id", session_id)
        
        self.assertEqual(result["session_id"], session_id)
        self.assertEqual(len(result["messages"]), 2)
        self.assertEqual(result["messages"][0]["text"], "Hello")
        self.assertEqual(result["messages"][1]["text"], "Hi there")
        self.assertEqual(result["metadata"], {"key": "value"})

    def test_get_session_not_found(self):
        """Test retrieving a non-existent session."""
        session_id = "non-existent-session"
        self.mock_supabase_client.table().select().eq().single().execute.return_value = self._get_mock_response(None)
        
        result = self.store.get(session_id)
        self.assertEqual(result, {})

    def test_get_session_db_error(self):
        """Test handling of a database error during get."""
        session_id = "error-session"
        self.mock_supabase_client.table().select().eq().single().execute.side_effect = Exception("DB Error")
        
        with patch('builtins.print') as mock_print:
            result = self.store.get(session_id)
            self.assertEqual(result, {})
            mock_print.assert_any_call(f"Error getting session {session_id}: DB Error")

    def test_get_session_empty_messages_or_metadata(self):
        """Test get with session having empty or None messages/metadata."""
        session_id = "empty-data-session"
        # Case 1: messages is None
        db_data_none_messages = {"session_id": session_id, "messages": None, "metadata": {"key": "value"}}
        self.mock_supabase_client.table().select().eq().single().execute.return_value = self._get_mock_response(db_data_none_messages)
        result = self.store.get(session_id)
        self.assertEqual(result["messages"], [])
        self.assertEqual(result["metadata"], {"key": "value"})

        # Case 2: metadata is None
        db_data_none_metadata = {"session_id": session_id, "messages": [], "metadata": None}
        self.mock_supabase_client.table().select().eq().single().execute.return_value = self._get_mock_response(db_data_none_metadata)
        result = self.store.get(session_id)
        self.assertEqual(result["messages"], [])
        self.assertEqual(result["metadata"], {})

    def test_append_message_new_session(self):
        """Test appending a message to a new session."""
        session_id = "new-session-append"
        message = {"role": "user", "text": "First message", "timestamp": "ts1"}
        # Mock response for checking if session exists (it doesn't)
        self.mock_supabase_client.table().select().eq().maybe_single().execute.return_value = self._get_mock_response(None)
        # Mock response for upsert
        self.mock_supabase_client.table().upsert().execute.return_value = self._get_mock_response([{"session_id": session_id}])
        self.store.append_message(session_id, message)
        self.mock_supabase_client.table.assert_any_call("sessions")
        self.mock_supabase_client.table().select.assert_called_with("messages, metadata")
        self.mock_supabase_client.table().upsert.assert_any_call({"session_id": session_id, "messages": unittest.mock.ANY, "metadata": {}})
        args, _ = self.mock_supabase_client.table().upsert.call_args
        upsert_data = args[0]
        self.assertEqual(upsert_data["session_id"], session_id)
        self.assertEqual(len(upsert_data["messages"]), 1)
        self.assertEqual(decrypt_message(upsert_data["messages"][0]["text"]), "First message")
        self.assertEqual(upsert_data["messages"][0]["role"], "user")
        self.assertEqual(upsert_data["metadata"], {})

    def test_append_message_existing_session(self):
        """Test appending a message to an existing session."""
        session_id = "existing-session-append"
        initial_raw_message = {"role": "user", "text": "Old message", "timestamp": "ts0"}
        initial_encrypted_message = {
            "role": initial_raw_message["role"],
            "text": encrypt_message(initial_raw_message["text"]),
            "timestamp": initial_raw_message["timestamp"]
        }
        existing_db_data = {
            "messages": [initial_encrypted_message],
            "metadata": {"initial": "data"}
        }
        new_message = {"role": "agent", "text": "New reply", "timestamp": "ts1"}
        # Mock response for checking if session exists (it does)
        self.mock_supabase_client.table().select().eq().maybe_single().execute.return_value = self._get_mock_response(existing_db_data)
        # Mock response for upsert
        self.mock_supabase_client.table().upsert().execute.return_value = self._get_mock_response([{"session_id": session_id}])
        self.store.append_message(session_id, new_message)
        self.mock_supabase_client.table().upsert.assert_any_call({"session_id": session_id, "messages": unittest.mock.ANY, "metadata": {"initial": "data"}})
        args, _ = self.mock_supabase_client.table().upsert.call_args
        upsert_data = args[0]
        self.assertEqual(upsert_data["session_id"], session_id)
        self.assertEqual(len(upsert_data["messages"]), 2)
        self.assertEqual(decrypt_message(upsert_data["messages"][0]["text"]), "Old message")
        self.assertEqual(decrypt_message(upsert_data["messages"][1]["text"]), "New reply")
        self.assertEqual(upsert_data["messages"][1]["role"], "agent")
        self.assertEqual(upsert_data["metadata"], {"initial": "data"})

    def test_append_message_invalid_message_format(self):
        """Test append_message raises ValueError for invalid message format."""
        session_id = "invalid-format-session"
        invalid_message = {"role": "user", "content": "Missing text and timestamp"}
        with self.assertRaisesRegex(ValueError, "Message must contain 'role', 'text', and 'timestamp' keys."):
            self.store.append_message(session_id, invalid_message)

    def test_append_message_db_error(self):
        """Test handling of a database error during append_message."""
        session_id = "append-error-session"
        message = {"role": "user", "text": "Test", "timestamp": "ts1"}
        
        self.mock_supabase_client.table().select().eq().maybe_single().execute.return_value = self._get_mock_response(None)
        self.mock_supabase_client.table().upsert().execute.side_effect = Exception("DB Upsert Error")
        
        with patch('builtins.print') as mock_print:
            with self.assertRaises(Exception) as context:
                self.store.append_message(session_id, message)
            self.assertTrue('DB Upsert Error' in str(context.exception))
            mock_print.assert_any_call(f"Error appending message to session {session_id}: DB Upsert Error")

    def test_clear_session(self):
        """Test clearing an existing session."""
        session_id = "clear-me-session"
        self.mock_supabase_client.table().delete().eq().execute.return_value = self._get_mock_response(None) # Success, no data needed
        self.store.clear(session_id)
        self.mock_supabase_client.table.assert_called_with("sessions")
        self.mock_supabase_client.table().delete.assert_any_call()
        self.mock_supabase_client.table().delete().eq.assert_called_with("session_id", session_id)

    def test_clear_session_db_error(self):
        """Test handling of a database error during clear."""
        session_id = "clear-error-session"
        self.mock_supabase_client.table().delete().eq().execute.side_effect = Exception("DB Delete Error")
        
        with patch('builtins.print') as mock_print:
            with self.assertRaises(Exception) as context:
                self.store.clear(session_id)
            self.assertTrue('DB Delete Error' in str(context.exception))
            mock_print.assert_any_call(f"Error clearing session {session_id}: DB Delete Error")

    def test_delete_session_alias_for_clear(self):
        """Test delete_session is an alias for clear."""
        session_id = "delete-me-alias-session"
        with patch.object(self.store, 'clear') as mock_clear:
            self.store.delete_session(session_id)
            mock_clear.assert_called_once_with(session_id)

    @patch('backend.app.storage.session_store.create_client') # Re-patch create_client for this specific env
    def test_get_session_decryption_error(self, mock_create_client_decrypt_error):
        """Test get session when decryption fails for a message."""
        session_id = "decrypt-error-session"
        encrypted_malicious_text = encrypt_message("this was encrypted with old key")
        db_data = {
            "session_id": session_id,
            "messages": [{"role": "user", "text": encrypted_malicious_text, "timestamp": "ts1"}],
            "metadata": {"foo": "bar"}
        }
        self.mock_supabase_client.table().select().eq().single().execute.return_value = self._get_mock_response(db_data)
        with patch('backend.app.storage.session_store.decrypt_message', side_effect=InvalidToken):
            with patch('builtins.print') as mock_print:
                result = self.store.get(session_id)
                self.assertEqual(result, {})
                mock_print.assert_any_call(f"Error getting session {session_id}: ")


if __name__ == '__main__':
    # This setup is for running tests directly. 
    # Ensure environment variables are set if you run this file directly.
    # For a real project, use a test runner like pytest which handles discovery and environment better.
    if not os.getenv("FERNET_KEY"):
        print("WARNING: FERNET_KEY is not set for direct test run. Defaulting to test key.")
        os.environ["FERNET_KEY"] = TEST_FERNET_KEY
    if not os.getenv("SUPABASE_URL"):
        os.environ["SUPABASE_URL"] = TEST_SUPABASE_URL
    if not os.getenv("SUPABASE_API_KEY"):
        os.environ["SUPABASE_API_KEY"] = TEST_SUPABASE_API_KEY
    
    unittest.main()