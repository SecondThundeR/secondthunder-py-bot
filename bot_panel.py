"""Ghosty Control Panel (Beta).

This script performs the first initial and further
configuration of the bot through the console.

**Noteworthy:** This script not meant to be imported as a module.
"""


import sys
import time
import src.lib.database as database
import src.utils.panel_scripts as panel_scripts


def bot_menu():
    """Bot setup.

    This function allows user to select 6 functions
    for configuring the bot and the database
    """
    while True:
        print('Main menu:'
          '\n1. Change settings of bot'
          '\n2. Add new bot in database'
          '\n3. Remove bot from database'
          '\n4. Choose default bot on startup'
          '\n5. Edit words database'
          '\n6. Reset bot settings'
          '\n0. Exit\n')
        menu_input = panel_scripts.get_user_input(
            'Enter the number of option:'
        )
        if menu_input.isnumeric():
            menu_input = int(menu_input)
            if menu_input == 1:
                panel_scripts.manage_bot_settings()
            elif menu_input == 2:
                panel_scripts.add_bot_config()
            elif menu_input == 3:
                panel_scripts.remove_bot_config()
            elif menu_input == 4:
                panel_scripts.select_bot_config()
            elif menu_input == 5:
                panel_scripts.manage_words_base()
            elif menu_input == 6:
                panel_scripts.change_setup_status()
            elif menu_input == 0:
                print('Hope you come back soon! See you later')
                sys.exit()
        else:
            print('\nYou have chosen something wrong, please try again')
            time.sleep(0.5)
            panel_scripts.clear_console()


def bot_panel_init():
    """Select function depending on status.

    This function checks the current setting status
    and selects the required function to run.
    If current_status is 0, launches setup of bot,
    otherwise - main menu
    """
    current_status = database.get_data(
        'mainDB',
        True,
        'SELECT is_setup_completed FROM variables'
    )
    if not current_status:
        panel_scripts.bot_setup()
    bot_menu()


bot_panel_init()
