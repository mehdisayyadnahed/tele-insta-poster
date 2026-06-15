import os
from telegram import Update
from telegram.ext import ContextTypes
from constants import *
from read_write_file import *
from show_button import *
from telebot import start_menu, main_menu

global trade_cfg_file


# ==============================================================================
# 1. Main Trade Menu Handler (Placeholder Component)
# ==============================================================================

async def trade_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Renders the main Trading submenu.
    Handles navigation to trades stats or trading configurations.
    """
    global back_stpr
    choice = update.message.text

    # Route input choice to the designated subsystem
    if choice == trades_btn:
        return await trades_menu(update, context)

    if choice == config_btn:
        return await config_menu(update, context)

    # Handle step-back navigation to the home starting menu
    if choice == back_btn and back_stpr:
        back_stpr = False
        return await start_menu(update, context)
        
    back_stpr = True
    
    options = [
        [trades_btn, config_btn],
        [back_btn]
    ]
    message = "Choose an option:"
    await show_button(options, message, update)

    return TRADE_MENU


# ==============================================================================
# 2. Trades Submenu Handler (Incomplete Module)
# ==============================================================================

async def trades_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Renders trade dashboard mock statistics (currently a development placeholder).
    """
    global back_stpr
    choice = update.message.text

    # Handle step-back navigation to the trade home menu
    if choice == back_btn and back_stpr:
        back_stpr = False
        return await trade_menu(update, context)
        
    back_stpr = True

    options = [
        [back_btn]
    ]
    message = 'This part is not complete.'
    await show_button(options, message, update)

    return TRADES_MENU


# ==============================================================================
# 3. Config Submenu Handler (Incomplete Module)
# ==============================================================================

async def config_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Renders trading rule configurations (currently a development placeholder).
    """
    global back_stpr
    choice = update.message.text

    # Handle step-back navigation to the trade home menu
    if choice == back_btn and back_stpr:
        back_stpr = False
        return await trade_menu(update, context)
        
    back_stpr = True

    options = [
        [back_btn]
    ]
    message = 'This part is not complete.'
    await show_button(options, message, update)

    return CONFIG_MENU