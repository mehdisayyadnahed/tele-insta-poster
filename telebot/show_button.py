from telegram import Update, ReplyKeyboardMarkup

async def show_button(options, text, update: Update):
    """
    Asynchronously sends a reply text message accompanied by a custom, 
    persistent reply keyboard configuration.

    Args:
        options (list): A multi-dimensional list representing rows and columns of button labels.
        text (str): The body text of the message to send.
        update (Update): The Telegram Update instance handling the request.
    """
    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            options, 
            resize_keyboard=True, 
            one_time_keyboard=False
        )
    )