import os

# Base directory where saved Instagram credentials/sessions are stored
session_folder = "../instabot/sessions"

# Target testing username to reset session (Replace with your actual test account)
cfg_data = "YOUR_TEST_ACCOUNT_USERNAME"

# Safely construct the full path to the session file
session_file_path = os.path.join(session_folder, f"{cfg_data}.json")

# Remove the session file if it exists to force a login re-authentication
if os.path.exists(session_file_path):
    os.remove(session_file_path)
    print("done")