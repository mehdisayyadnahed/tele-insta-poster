# ==============================================================================
# Telegram Bot Configuration and Constants
# ==============================================================================

Telegram Bot Token (Replace with your actual bot token from @BotFather)
my_token = 'YOUR_TELEGRAM_BOT_TOKEN'

List of authorized Telegram User IDs allowed to access and control the bot
my_user_ids = [
    YOUR_TELEGRAM_USER_ID_1,
    YOUR_TELEGRAM_USER_ID_2,
    YOUR_TELEGRAM_USER_ID_3
]

# Conversation state definitions for python-telegram-bot's ConversationHandler
(
    START_MENU,
    MAIN_MENU,
    INSTA_MENU,
    REPORT_MENU,
    CONTENT_MENU,
    SELECT_USER_CONTENT,
    GET_CONTENT,
    SETTING_MENU,
    SHOW_USER_SETTING,
    GET_USER_CAPTION,
    GET_USER_COUNTER,
    ACCOUNT_MENU,
    ADD_ACCOUNT_MENU,
    DEL_ACCOUNT_MENU,
    DO_ADD_USERNAME,
    DO_ADD_PASSWORD,
    DO_ADD_SECRET,
    DO_DEL_ACCOUNT
) = range(18)

# ------------------------------------------------------------------------------
# Instagram Bot Button Labels and Paths
# ------------------------------------------------------------------------------
insta_btn = "Insta"
report_btn = "Report"
content_btn = "Content"
setting_btn = "Setting"
account_btn = "Account"
add_account_btn = "Add Account"
del_account_btn = "Delete Account"

# File system paths to instabot configurations and assets
downloads_folder = "../instabot/downloads"
configs_folder = "../instabot/configs"
sessions_folder = "../instabot/sessions"
insta_cfg_file = "insta_configs.json"
report_posted_file = 'report_posted.json'

# ------------------------------------------------------------------------------
# Instagram Session Runtime Variables
# ------------------------------------------------------------------------------
get_media = False
selected_user = ''
user_data = {}
users_list = []
select_username_var = ''
max_post_in_day = 13

# ------------------------------------------------------------------------------
# General Telegram Bot Settings
# ------------------------------------------------------------------------------
back_btn = "Back"
back_stpr = True  # Controlling flag for navigation step-back functionality
