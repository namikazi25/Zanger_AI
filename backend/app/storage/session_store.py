import os
from supabase import create_client, Client
from typing import List, Dict, Any
from backend.app.utils.crypto import encrypt_message, decrypt_message

# SUPABASE_URL and SUPABASE_API_KEY will be fetched in __init__

class SupabaseSessionStore:
    """Manages session state using Supabase PostgreSQL for storage."""

    def __init__(self):
        """Initializes the Supabase client."""
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_api_key = os.getenv("SUPABASE_API_KEY")

        if not supabase_url or not supabase_api_key:
            raise ValueError("SUPABASE_URL and SUPABASE_API_KEY environment variables must be set for SupabaseSessionStore.")
        
        self.client: Client = create_client(supabase_url, supabase_api_key)

    def get(self, session_id: str) -> Dict[str, Any]:
        """Retrieves and decrypts messages and metadata for a given session_id."""
        try:
            response = self.client.table("sessions").select("*").eq("session_id", session_id).single().execute()
            if not response.data:
                return {}

            decrypted_messages = []
            if response.data.get("messages"):
                for msg in response.data["messages"]:
                    decrypted_messages.append({
                        "role": msg["role"],
                        "text": decrypt_message(msg["text"]),
                        "timestamp": msg["timestamp"]
                    })
            
            return {
                "session_id": session_id,
                "messages": decrypted_messages,
                "metadata": response.data.get("metadata") or {}
            }
        except Exception as e:
            # Log error (e.g., using a proper logger)
            print(f"Error getting session {session_id}: {e}")
            return {}

    def append_message(self, session_id: str, message: Dict[str, Any]):
        """Encrypts and appends a message to the session. Creates the session if it doesn't exist."""
        if not all(key in message for key in ["role", "text", "timestamp"]):
            raise ValueError("Message must contain 'role', 'text', and 'timestamp' keys.")

        encrypted_message = {
            "role": message["role"],
            "text": encrypt_message(str(message["text"])), # Ensure text is string
            "timestamp": message["timestamp"]
        }

        try:
            existing_session_data = self.client.table("sessions").select("messages, metadata").eq("session_id", session_id).maybe_single().execute()
            
            current_messages = []
            current_metadata = {}

            if existing_session_data.data:
                current_messages = existing_session_data.data.get("messages", []) or [] # handle None from db
                current_metadata = existing_session_data.data.get("metadata", {}) or {} # handle None from db
            
            updated_messages = current_messages + [encrypted_message]
            
            self.client.table("sessions").upsert({
                "session_id": session_id,
                "messages": updated_messages,
                "metadata": current_metadata # Metadata is not updated here, can be extended if needed
            }).execute()
        except Exception as e:
            # Log error
            print(f"Error appending message to session {session_id}: {e}")
            raise

    def clear(self, session_id: str):
        """Deletes all data for a given session_id."""
        try:
            self.client.table("sessions").delete().eq("session_id", session_id).execute()
        except Exception as e:
            # Log error
            print(f"Error clearing session {session_id}: {e}")
            raise

    def delete_session(self, session_id: str):
        """Alias for clear, for GDPR 'Right to be Forgotten'."""
        self.clear(session_id)

# Example Usage (for testing purposes, typically not here)
if __name__ == '__main__':
    # This requires .env file with SUPABASE_URL, SUPABASE_API_KEY, FERNET_KEY
    # and a 'sessions' table in your Supabase project as per the schema.
    print("Attempting to initialize SupabaseSessionStore...")
    try:
        store = SupabaseSessionStore()
        print("SupabaseSessionStore initialized.")
        
        test_session_id = "test-session-123"
        
        print(f"Clearing session {test_session_id} (if exists)...")
        store.clear(test_session_id)
        print("Session cleared.")

        print(f"Getting session {test_session_id} (should be empty)...")
        session_data = store.get(test_session_id)
        print(f"Initial session data: {session_data}")
        assert session_data == {} or session_data.get("messages") == [], "Session should be empty or have no messages"

        print("Appending first message...")
        store.append_message(test_session_id, {"role": "user", "text": "Hello Supabase!", "timestamp": "2024-07-30T10:00:00Z"})
        print("First message appended.")

        print("Appending second message...")
        store.append_message(test_session_id, {"role": "agent", "text": "Hello User!", "timestamp": "2024-07-30T10:00:05Z"})
        print("Second message appended.")

        print(f"Getting session {test_session_id} again...")
        session_data_updated = store.get(test_session_id)
        print(f"Updated session data: {session_data_updated}")
        assert len(session_data_updated.get("messages", [])) == 2, "Should have two messages"
        assert session_data_updated["messages"][0]["text"] == "Hello Supabase!", "Decryption failed or message mismatch"

        print(f"Clearing session {test_session_id} again...")
        store.clear(test_session_id)
        print("Session cleared.")
        final_check = store.get(test_session_id)
        print(f"Final session data after clear: {final_check}")
        assert final_check == {} or final_check.get("messages") == [], "Session should be empty after final clear"

        print("SupabaseSessionStore tests passed (basic functionality).")

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"An error occurred during SupabaseSessionStore testing: {e}")
        import traceback
        traceback.print_exc()