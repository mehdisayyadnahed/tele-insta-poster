import logging
from time import sleep

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ConversationHandler, 
    ContextTypes
)

from show_button import show_button
from constants import *

# Initialize basic logger to monitor the bot's runtime activity
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==============================================================================
# 1. Start Menu Handler (Conversation Entry Point)
# ==============================================================================

async def start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Acts as the main entry point for the Telegram bot.
    Authenticates the user against authorized IDs, routing them to the Instagram menu.
    """
    # Unused local variables kept for structural compatibility
    back_stpr = True
    user_data = {}
    select_username_var = ''

    user_id = update.message.from_user.id

    # Check if the incoming Telegram ID is authorized
    if user_id in my_user_ids:
        from insta_menus import insta_menu
        return await insta_menu(update, context)
    
    # Return unauthorized state fallback (kept identical to original logic)
    return START


# ==============================================================================
# 2. Application Core Launch Loop
# ==============================================================================

def main() -> None:
    """
    Initializes the Telegram application, configures conversation handlers, 
    and starts polling for updates.
    """
    # Dynamic imports from the menus module to ensure smooth transitions
    from insta_menus import (
        insta_menu, report_menu, content_menu, select_user_content, get_content,
        setting_menu, show_user_setting, get_user_counter, get_user_caption,
        account_menu, add_account_menu, do_add_username, do_add_password,
        do_add_secret, del_account_menu, do_del_account
    )

    # Initialize the Application client using the token defined in constants.py
    application = ApplicationBuilder().token(my_token).build()

    # Define structural layout for conversational routing
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_menu)],
        states={
            START_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, start_menu)
            ],
            INSTA_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, insta_menu)
            ],
            REPORT_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, report_menu)
            ],
            CONTENT_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, content_menu)
            ],
            SELECT_USER_CONTENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, select_user_content)
            ],
            GET_CONTENT: [
                MessageHandler(filters.PHOTO | filters.VIDEO | (filters.TEXT & ~filters.COMMAND), get_content)
            ],
            SETTING_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, setting_menu)
            ],
            SHOW_USER_SETTING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, show_user_setting)
            ],
            GET_USER_CAPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_user_caption)
            ],
            GET_USER_COUNTER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_user_counter)
            ],
            ACCOUNT_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, account_menu)
            ],
            ADD_ACCOUNT_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_account_menu)
            ],
            DEL_ACCOUNT_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, del_account_menu)
            ],
            DO_ADD_USERNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, do_add_username)
            ],
            DO_ADD_PASSWORD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, do_add_password)
            ],
            DO_ADD_SECRET: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, do_add_secret)
            ],
            DO_DEL_ACCOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, do_del_account)
            ]
        },
        fallbacks=[],
    )

    # Attach conversation handler to dispatcher
    application.add_handler(conv_handler)
    
    # Start the continuous polling loop
    logger.info("Starting Telegram bot polling...")
    application.run_polling()


if __name__ == '__main__':
    main()