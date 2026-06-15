import os
import pyotp
from instagrapi import Client
from constants import *

def insta_login_checker(username, password, two_factor_secret):
    """
    Validates Instagram credentials and the 2FA secret configuration.
    Upon a successful login, it saves the session file and returns True.

    Args:
        username (str): Instagram account username.
        password (str): Instagram account password.
        two_factor_secret (str): TOTP 2FA secret key.

    Returns:
        bool: True if login is successful and session is dumped, False otherwise.
    """
    global sessions_folder

    client = Client()

    try:
        # Generate the current 2FA verification code using TOTP
        totp = pyotp.TOTP(two_factor_secret)
        verification_code = totp.now()

        # Attempt to authenticate with Instagram
        client.login(username, password, verification_code=verification_code)

        # Create the sessions directory if it does not exist
        if not os.path.isdir(sessions_folder):
            os.makedirs(sessions_folder)
        
        # Dump the authenticated session to skip login challenges in future attempts
        session_file_path = os.path.join(sessions_folder, f"{username}.json")
        client.dump_settings(session_file_path)
        return True

    except Exception as e:
        # Gracefully handle login exceptions and return False
        return False

# Example testing snippet (Replace placeholders with your test credentials)
# print(str(insta_login_checker(
#     "YOUR_INSTAGRAM_USERNAME", 
#     "YOUR_INSTAGRAM_PASSWORD", 
#     "YOUR_INSTAGRAM_2FA_SECRET"
# )))