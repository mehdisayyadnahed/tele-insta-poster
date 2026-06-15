import os
import json
from telegram import Update
from telegram.ext import ContextTypes
from constants import *
from read_write_file import *
from show_button import *
from telebot import start_menu
from insta_login_checker import *

global insta_cfg_file

# ==============================================================================
# 1. Instagram Main Menu Handler
# ==============================================================================

async def insta_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Displays the core Instagram control menu to the user.
    Allows routing to stats reports, content upload queues, settings, and profile registries.
    """
    global back_stpr
    choice = update.message.text

    # Route based on the chosen menu button
    if choice == report_btn:
        return await report_menu(update, context)

    if choice == content_btn:
        return await content_menu(update, context)

    if choice == setting_btn:
        return await setting_menu(update, context)

    if choice == account_btn:
        return await account_menu(update, context)

    # Route navigation back to the starting setup menu
    if choice == back_btn and back_stpr:
        back_stpr = False
        return await start_menu(update, context)
    
    back_stpr = True
    
    options = [
        [report_btn, content_btn],
        [setting_btn, account_btn]
    ]
    message = "Choose an option:"
    await show_button(options, message, update)

    return INSTA_MENU


# ==============================================================================
# 2. Daily Posting Statistics & Local File Reports
# ==============================================================================

async def report_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Scans local upload queue directories and fetches transaction counters
    to print a summary report of successfully published and pending posts.
    """
    global back_stpr
    global downloads_folder
    choice = update.message.text
    users_list = []
    report_text = ""

    # Handle step-back navigation flow
    if choice == back_btn and back_stpr:
        back_stpr = False
        return await insta_menu(update, context)
    
    back_stpr = True

    # Load configured users list
    all_users_data = await save_config(insta_cfg_file, "", "r")
    if all_users_data:
        users_list = list(all_users_data.keys())

    # Count actual files sitting in download queue directories
    for username in users_list:
        user_dir = os.path.join(downloads_folder, username)
        if os.path.isdir(user_dir):
            files_in_folder = os.listdir(user_dir)
            if len(files_in_folder) == 0:
                report_text += f"{username}: 0\n"
            else:
                file_counter = 0
                for file in files_in_folder:
                    if file.endswith('.jpg') or file.endswith('.mp4'):
                        file_counter += 1
                report_text += f"{username}: {file_counter}\n"

    # Fetch recorded upload metrics from JSON storage file
    report_file_path = os.path.join(configs_folder, report_posted_file)
    posted_file_stats = ""

    if os.path.exists(report_file_path):
        with open(report_file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if content:
                data = json.loads(content)
                for username, count in data.items():
                    posted_file_stats += f"{username}: {count}\n"

    # Compose final statistical summary text
    report_text = f"{report_text}==========\n{posted_file_stats}"
    await update.message.reply_text(report_text)

    return INSTA_MENU


# ==============================================================================
# 3. Content File Delivery Menu and Queue Registry
# ==============================================================================

async def content_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Lists existing accounts to allow the user to select which account
    the subsequent media file upload queue belongs to.
    """
    global back_stpr
    choice = update.message.text

    # Handle step-back navigation flow
    if choice == back_btn and back_stpr:
        back_stpr = False
        return await insta_menu(update, context)
    
    back_stpr = True

    all_users_data = await save_config(insta_cfg_file, "", "r")

    if not all_users_data:
        options = [[back_btn]]
        message = "No User To Select."
        await show_button(options, message, update)
        return INSTA_MENU

    # Display configured users as separate keyboard button rows
    users_list = [[username] for username in all_users_data.keys()]
    options = users_list.copy()
    options.append([back_btn])
    
    message = "Choose an Account:"
    await show_button(options, message, update)
    context.user_data['users_list'] = users_list
    
    return SELECT_USER_CONTENT


async def select_user_content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Verifies the profile selection and flags the thread to receive photo/video uploads.
    """
    global back_stpr
    global get_media
    global selected_user
    users_list = context.user_data.get('users_list')
    choice = update.message.text

    # Handle step-back navigation flow
    if choice == back_btn and back_stpr:
        back_stpr = False
        get_media = False
        context.user_data['users_list'] = []
        selected_user = ''
        return await insta_menu(update, context)
    
    back_stpr = True

    if choice is not None:
        if any(choice in item for item in users_list):
            get_media = True
            selected_user = choice
            options = [[back_btn]]
            message = "Send Media To Save:"
            await show_button(options, message, update)
            return GET_CONTENT
        else:
            options = [[back_btn]]
            message = "Can't Find This User."
            await show_button(options, message, update)


async def get_content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Listens for media documents (images or video files) and saves them to local storage folders.
    """
    global downloads_folder
    global back_stpr
    global get_media
    global selected_user
    choice = update.message.text

    # Handle step-back navigation flow
    if choice == back_btn and back_stpr:
        back_stpr = False
        get_media = False
        context.user_data['users_list'] = []
        selected_user = ''
        return await content_menu(update, context)
    
    back_stpr = True

    if get_media:
        folder_path = os.path.join(downloads_folder, selected_user)
        caption_text = update.message.caption if update.message.caption else ""

        # Process photo uploads
        if update.message.photo:
            file = await update.message.photo[-1].get_file()
            file_name = os.path.join(folder_path, f"{update.message.photo[-1].file_id}.jpg")
            await file.download_to_drive(file_name)

            caption_file = os.path.join(folder_path, f"{update.message.photo[-1].file_id}.txt")
            with open(caption_file, 'w', encoding='utf-8') as f:
                f.write(caption_text)

            await update.message.reply_text('File Saved.')
        
        # Process video uploads
        if update.message.video:
            file = await update.message.video.get_file()
            file_name = os.path.join(folder_path, f"{update.message.video.file_id}.mp4")
            await file.download_to_drive(file_name)

            caption_file = os.path.join(folder_path, f"{update.message.video.file_id}.txt")
            with open(caption_file, 'w', encoding='utf-8') as f:
                f.write(caption_text)

            await update.message.reply_text('File Saved.')


# ==============================================================================
# 4. Global Settings Menu (Upload Limits & Default Suffix Signatures)
# ==============================================================================

async def setting_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Lists users as menu options allowing settings updates.
    """
    global back_stpr
    choice = update.message.text

    # Handle step-back navigation flow
    if choice == back_btn and back_stpr:
        back_stpr = False
        context.user_data['users_list'] = []
        return await insta_menu(update, context)
    
    back_stpr = True

    all_users_data = await save_config(insta_cfg_file, "", "r")

    if not all_users_data:
        options = [[back_btn]]
        message = "No User To Select."
        await show_button(options, message, update)
        return INSTA_MENU
    else:
        users_list = [[username] for username in all_users_data.keys()]
        options = users_list.copy()
        options.append([back_btn])
        
        message = "Choose an Account:"
        await show_button(options, message, update)
        
        context.user_data['options'] = options
        context.user_data['users_list'] = users_list
        context.user_data['all_users_data'] = all_users_data
        return SHOW_USER_SETTING


async def show_user_setting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Presents the currently assigned values for daily frequency limits
    and signature caption suffix strings.
    """
    global back_stpr
    options = context.user_data.get('options')
    users_list = context.user_data.get('users_list')
    all_users_data = context.user_data.get('all_users_data')
    choice = update.message.text

    # Handle step-back navigation flow
    if choice == back_btn and back_stpr:
        back_stpr = False
        return await insta_menu(update, context)
    
    back_stpr = True

    if any(choice in item for item in users_list):
        post_in_day = all_users_data[choice].get("post_in_day", "Not Set")
        add_to_caption = all_users_data[choice].get("add_to_caption", "Not Set")

        await update.message.reply_text(f'"{choice}" Post In Day:\n')
        await update.message.reply_text(post_in_day)
        await update.message.reply_text(f'"{choice}" Add To Caption:\n')
        
        back_options = [[back_btn]]
        await show_button(back_options, add_to_caption, update)
    else:
        message = "Can't Find This User."
        await show_button(options, message, update)

    await update.message.reply_text("Enter Account Post Counter (0-13):")
    context.user_data['selected_user'] = choice

    return GET_USER_COUNTER


async def get_user_counter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Saves and validates the adjusted posting daily limit boundaries.
    """
    global back_stpr
    choice = update.message.text

    # Handle step-back navigation flow
    if choice == back_btn and back_stpr:
        back_stpr = False
        return await setting_menu(update, context)
    
    back_stpr = True

    if choice != back_btn:
        try:
            numeric_choice = int(choice)
            if 0 <= numeric_choice <= max_post_in_day:
                await update.message.reply_text("Enter Account Add To Caption Text:")
                context.user_data['user_counter'] = str(numeric_choice)
                return GET_USER_CAPTION
            else:
                await update.message.reply_text("Enter Account Post Counter (0-13):")
                return GET_USER_COUNTER
        except ValueError:
            pass

    return GET_USER_COUNTER


async def get_user_caption(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Writes and saves adjusted caption configurations permanently.
    """
    global back_stpr
    user_counter = context.user_data.get('user_counter')
    selected_user = context.user_data.get('selected_user')
    choice = update.message.text

    # Handle step-back navigation flow
    if choice == back_btn and back_stpr:
        back_stpr = False
        return await setting_menu(update, context)
    
    back_stpr = True

    if choice != back_btn:
        caption = choice
        result = await save_config(insta_cfg_file, [selected_user, user_counter, caption], "m")
        if result:
            await update.message.reply_text("Setting Changed.")
            return await setting_menu(update, context)
    
    return GET_USER_CAPTION


# ==============================================================================
# 5. Instagram Accounts Credentials & Profile Registration Submenu
# ==============================================================================

async def account_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Presents account credentials configurations.
    """
    global back_stpr
    choice = update.message.text

    if choice == add_account_btn:
        return await add_account_menu(update, context)

    if choice == del_account_btn:
        return await del_account_menu(update, context)

    # Handle step-back navigation flow
    if choice == back_btn and back_stpr:
        back_stpr = False
        return await insta_menu(update, context)
    
    back_stpr = True

    options = [
        [add_account_btn],
        [del_account_btn],
        [back_btn]
    ]
    message = "Choose an option:"
    await show_button(options, message, update)

    return ACCOUNT_MENU


async def add_account_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Asks the administrator for the target account username.
    """
    global back_stpr
    choice = update.message.text

    # Handle step-back navigation flow
    if choice == back_btn and back_stpr:
        back_stpr = False
        return await account_menu(update, context)
    
    back_stpr = True

    options = [[back_btn]]
    message = 'Enter Your Username:'
    await show_button(options, message, update)
    return DO_ADD_USERNAME


async def do_add_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Registers the username value and verifies no profile duplication occurs.
    """
    global back_stpr
    global select_username_var
    choice = update.message.text

    # Handle step-back navigation flow
    if choice == back_btn and back_stpr:
        back_stpr = False
        select_username_var = ''
        return await account_menu(update, context)
    
    back_stpr = True

    all_users_data = await save_config(insta_cfg_file, "", "r")

    if all_users_data:
        users_list = list(all_users_data.keys())
        if choice in users_list:
            options = [[back_btn]]
            message = 'Username Exist. Try Another One.'
            await show_button(options, message, update)
            return DO_ADD_USERNAME
            
    select_username_var = choice
    user_data[select_username_var] = {}
    await update.message.reply_text('Enter Your Password:')
    return DO_ADD_PASSWORD


async def do_add_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Holds the password and prompts for the 2FA dynamic authorization key.
    """
    global back_stpr
    global user_data
    global select_username_var
    choice = update.message.text

    # Handle step-back navigation flow
    if choice == back_btn and back_stpr:
        back_stpr = False
        user_data = {}
        select_username_var = ''
        return await account_menu(update, context)
    
    back_stpr = True

    user_data[select_username_var]["password"] = choice
    await update.message.reply_text('Enter Your SECRET:')
    return DO_ADD_SECRET


async def do_add_secret(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Performs live authentication using OTP tokens generated on demand.
    Registers and saves credentials safely upon positive login callback.
    """
    global back_stpr
    global user_data
    global select_username_var
    choice = update.message.text

    # Handle step-back navigation flow
    if choice == back_btn and back_stpr:
        back_stpr = False
        user_data = {}
        select_username_var = ''
        return await account_menu(update, context)
    
    back_stpr = True

    user_data[select_username_var]["secret"] = choice

    # Validate configuration dynamically
    if insta_login_checker(select_username_var, user_data[select_username_var]["password"], user_data[select_username_var]["secret"]):
        await save_config(insta_cfg_file, user_data, "a")
        user_data = {}
        await update.message.reply_text('User Added.')
        return await account_menu(update, context)
    else:
        user_data = {}
        await update.message.reply_text('Wrong User Data.')
        return await account_menu(update, context)


async def del_account_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Renders account deletions keyboard lists.
    """
    global back_stpr
    choice = update.message.text

    # Handle step-back navigation flow
    if choice == back_btn and back_stpr:
        back_stpr = False
        return await account_menu(update, context)
    
    back_stpr = True

    all_users_data = await save_config(insta_cfg_file, "", "r")

    if not all_users_data:
        options = [[back_btn]]
        message = "No User To Select."
        await show_button(options, message, update)
        return DEL_ACCOUNT_MENU
    else:
        users_list = [[username] for username in all_users_data.keys()]
        options = users_list.copy()
        options.append([back_btn])
        
        message = "Choose an Account:"
        await show_button(options, message, update)
        
        context.user_data['options'] = options
        context.user_data['users_list'] = users_list
        return DO_DEL_ACCOUNT


async def do_del_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Removes selected user credentials, file databases, sessions, and downloads queues.
    """
    global back_stpr
    options = context.user_data.get('options')
    users_list = context.user_data.get('users_list')
    choice = update.message.text

    # Handle step-back navigation flow
    if choice == back_btn and back_stpr:
        back_stpr = False
        return await account_menu(update, context)
    
    back_stpr = True

    if any(choice in item for item in users_list):
        result = await save_config(insta_cfg_file, choice, 'd')
        if result:
            message = "User Deleted."
            options.remove([choice])
            await show_button(options, message, update)
        else:
            message = "Problem On Deleting This User."
            await show_button(options, message, update)
    else:
        message = "Can't Find This User."
        await show_button(options, message, update)

    return DO_DEL_ACCOUNT
