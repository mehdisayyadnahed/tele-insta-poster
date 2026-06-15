import re
import os
import pyotp
import random
import json
import time
from instagrapi import Client
from read_write_file import save_config
from moviepy.editor import VideoFileClip
from PIL import Image
import pytz
from datetime import datetime
from text_on_video import text_on_video
from text_on_cover import text_on_cover

def post_uploader(username, additional_text):
    """
    Manages pending upload queues for a specific Instagram profile.
    Performs format checks, validates aspect ratios, generates dynamic covers/text overlays,
    re-authenticates active login sessions with pyotp 2FA, uploads the post, and registers reports.

    Args:
        username (str): Target Instagram account username.
        additional_text (str): Pre-configured signature suffix/hashtags to append to the caption.

    Returns:
        bool: True if the file upload completes successfully, False otherwise.
    """
    # Locally load constants to isolate operational variables and maintain scope stability
    from constants import (
        downloads_folder, 
        configs_folder, 
        sessions_folder, 
        insta_cfg_file, 
        report_posted_file, 
        refresh_time, 
        login_check_count, 
        loop_interrupt, 
        covergraphi_usernames, 
        textgraphi_usernames, 
        min_aspect_ratio, 
        max_aspect_ratio
    )

    try:
        login_status = True
        posting_status = True
        file_status = True
        media_file = None
        caption_status = True
        media_path = None
        file_found = False
        custom_cover_image = False
        caption = ''
        aspect_ratio = 0
        
        user_folder = os.path.join(downloads_folder, username)

        # Gather target photo/video assets from the user download folder
        media_files = [file for file in os.listdir(user_folder) if file.endswith('.mp4') or file.endswith('.jpg')]
        # Filter out generated thumbnails and currently processing active clips
        media_files = [file for file in media_files if not (file.endswith('.mp4.jpg') or file.endswith('-tmp.mp4'))]

        if media_files:
            # Scan files sequentially to find the first valid media to process
            for media_file in media_files:
                caption_file = os.path.splitext(media_file)[0] + '.txt'
                caption_path = os.path.join(user_folder, caption_file)
                
                if not os.path.exists(caption_path):
                    caption_status = False

                media_path = os.path.join(user_folder, media_file)

                # Fetch and validate Video dimension aspect ratio
                if media_path.endswith('.mp4'):
                    try:
                        with VideoFileClip(media_path) as clip:
                            aspect_ratio = clip.size[0] / clip.size[1]
                    except Exception:
                        if os.path.exists(media_path):
                            os.remove(media_path)
                        if caption_status and os.path.exists(caption_path):
                            os.remove(caption_path)
                        file_status = False
                # Fetch and validate Image dimension aspect ratio
                else:
                    try:
                        with Image.open(media_path) as img:
                            aspect_ratio = img.width / img.height
                    except Exception:
                        if os.path.exists(media_path):
                            os.remove(media_path)
                        if caption_status and os.path.exists(caption_path):
                            os.remove(caption_path)
                        file_status = False

                # Handle files based on verification checks
                if file_status:
                    if not (min_aspect_ratio < aspect_ratio < max_aspect_ratio):
                        if os.path.exists(media_path):
                            os.remove(media_path)
                        if caption_status and os.path.exists(caption_path):
                            os.remove(caption_path)
                    else:
                        # Fetch original caption details and stitch the configuration signatures
                        if caption_status:
                            try:
                                with open(caption_path, 'r', encoding='utf-8') as file:
                                    caption = file.read().strip()
                            except Exception:
                                pass

                        caption = f"{caption}\n{additional_text}"
                        file_found = True
                        break

            # Proceed only if a fully compatible file exists
            if file_found:
                client = Client()
                session_file = os.path.join(sessions_folder, f"{username}.json")

                # Restore previous active session to prevent repetitive login challenges
                if os.path.exists(session_file):
                    print(f"Loading cached session: {datetime.now(pytz.timezone('Asia/Tehran'))}")
                    client.load_settings(session_file)

                    for loop_counter in range(login_check_count):
                        try:
                            client.account_info().dict()
                            login_status = True
                            break
                        except Exception:
                            login_status = False
                        time.sleep(random.randint(loop_interrupt, loop_interrupt * loop_interrupt))

                # Re-login automatically if session file is missing or validation failed
                if not os.path.exists(session_file) or not login_status:
                    user_config = save_config(insta_cfg_file, '', 'r')
                    password = user_config[username]["password"]
                    two_factor_secret = user_config[username]["secret"]

                    for loop_counter in range(login_check_count):
                        print(f"Login re-authentication try {loop_counter} for {username}")
                        try:
                            totp = pyotp.TOTP(two_factor_secret)
                            verification_code = totp.now()
                            client = Client()
                            print(f"Login initialized: {datetime.now(pytz.timezone('Asia/Tehran'))}")
                            
                            client.login(username, password, verification_code=verification_code)
                            
                            print(f"Dumping session state: {datetime.now(pytz.timezone('Asia/Tehran'))}")
                            client.dump_settings(session_file)
                            login_status = True
                            break
                        except Exception:
                            login_status = False
                            time.sleep(random.randint(loop_interrupt, loop_interrupt * loop_interrupt))

                # Process the upload task if validated and authorized
                if login_status:
                    try:
                        print(f"Uploader thread started: {datetime.now(pytz.timezone('Asia/Tehran'))}")

                        # Trigger Image Post Upload
                        if media_file.endswith('.jpg'):
                            try:
                                print(f"Uploading photo post: {datetime.now(pytz.timezone('Asia/Tehran'))}")
                                client.photo_upload(media_path, caption=caption)
                            except Exception:
                                return False
                        
                        # Trigger Video Clip Post Upload
                        elif media_file.endswith('.mp4'):
                            try:
                                print(f"Uploading video clip: {datetime.now(pytz.timezone('Asia/Tehran'))}")
                                clear_caption = caption.splitlines()[0] if caption.strip() else ""

                                # Check and perform custom cover thumbnail text overlaying
                                if username in covergraphi_usernames:
                                    custom_cover_image = True
                                    cover_file = f"{media_path}.jpg"
                                    if not os.path.exists(cover_file):
                                        print(f"Generating cover thumbnail overlay: {datetime.now(pytz.timezone('Asia/Tehran'))}")
                                        posting_status = text_on_cover(media_path, clear_caption)

                                # Check and perform custom video watermark text overlaying
                                if username in textgraphi_usernames:
                                    tmp_media_path = media_path.replace('.mp4', '-tmp.mp4')
                                    if not os.path.exists(tmp_media_path):
                                        print(f"Generating video watermark overlay: {datetime.now(pytz.timezone('Asia/Tehran'))}")
                                        posting_status = text_on_video(media_path, clear_caption, username)

                                    if posting_status:
                                        # Upload modified video with the generated custom cover
                                        if custom_cover_image:
                                            client.clip_upload(
                                                path=tmp_media_path, 
                                                caption=caption, 
                                                thumbnail=f"{media_path}.jpg"
                                            )
                                            if os.path.exists(f"{media_path}.jpg"):
                                                os.remove(f"{media_path}.jpg")
                                            if os.path.exists(tmp_media_path):
                                                os.remove(tmp_media_path)
                                            if os.path.exists(media_path):
                                                os.remove(media_path)
                                        # Upload modified video with default cover
                                        else:
                                            client.clip_upload(path=tmp_media_path, caption=caption)
                                            if os.path.exists(tmp_media_path):
                                                os.remove(tmp_media_path)
                                            if os.path.exists(media_path):
                                                os.remove(media_path)
                                    else:
                                        return False

                                elif posting_status:
                                    # Upload raw video with the generated custom cover
                                    if custom_cover_image:
                                        client.clip_upload(
                                            path=media_path, 
                                            caption=caption, 
                                            thumbnail=f"{media_path}.jpg"
                                        )
                                        if os.path.exists(f"{media_path}.jpg"):
                                            os.remove(f"{media_path}.jpg")
                                        if os.path.exists(media_path):
                                            os.remove(media_path)
                                    # Upload raw video with default cover
                                    else:
                                        client.clip_upload(path=media_path, caption=caption)
                                        if os.path.exists(f"{media_path}.jpg"):
                                            os.remove(f"{media_path}.jpg")
                                        if os.path.exists(media_path):
                                            os.remove(media_path)
                                else:
                                    return False

                            except Exception:
                                return False

                        # Purge physical text files and register metrics on standard logs
                        if posting_status:
                            if caption_status and os.path.exists(caption_path):
                                os.remove(caption_path)

                            report_file_path = os.path.join(configs_folder, report_posted_file)

                            # Record successes in daily metrics JSON report
                            if os.path.exists(report_file_path):
                                with open(report_file_path, 'r', encoding='utf-8') as file:
                                    data = json.load(file)
                                
                                if username not in data:
                                    data[username] = 1
                                else:
                                    data[username] += 1
                                
                                with open(report_file_path, 'w', encoding='utf-8') as file:
                                    json.dump(data, file, ensure_ascii=False, indent=4)
                            else:
                                data = {username: 1}
                                with open(report_file_path, 'w', encoding='utf-8') as file:
                                    json.dump(data, file, ensure_ascii=False, indent=4)

                            print(f"Posting sequence successful: {datetime.now(pytz.timezone('Asia/Tehran'))}")
                            return True
                        else:
                            return False

                    except Exception:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    except Exception:
        return False

# Master testing command execution placeholder
# post_uploader("YOUR_TEST_INSTAGRAM_ACCOUNT", "YOUR_TEST_SIGNATURE_AND_HASHTAGS")