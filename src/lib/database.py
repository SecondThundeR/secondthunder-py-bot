"""SQL Database Handler Library (Beta).

This script allows the user to work with a SQL database with basic functions
that only require the necessary data from the user to work with

The module can accept commands as strings and list of data to add

**Noteworthy:** Module returns custom exception on every SQL failure to
prevent the main script from making sudden errors

This file can also be imported as a module and contains the following functions:
    * clear_tables - clears specific tables on load
    * reset_bot_tables - clears specific tables on bot reset
    * get_data - returns list of data from table
    * modify_data - operates with data by executing SQL queries
"""


import sys
import sqlite3


class Database:
    """A class to control database.

    Parameters:
        path (str): Path to database

    Methods:
        connect_db: Makes connection with database
        disconnect_db: Closes connection with database
    """

    def __init__(self, db_name):
        """Initialize all necessary variables for DB.

        This function get path to DB and connect with it

        Parameters:
            db_name (str): Name of selected database
        """
        self.db_path = [
            './src/db/mainDB.db',
            './src/db/confDB.db',
            './src/db/wordsDB.db'
        ]
        self.conn = None
        self.cur = None
        self.connect_db(db_name)

    def connect_db(self, selected_db):
        """Make connection with local database.

        Parameters:
            selected_db (str): Name of DB to connect to
        """
        self.conn = sqlite3.connect(
            f'./src/db/{selected_db}.db',
            check_same_thread=False
        )
        self.cur = self.conn.cursor()

    def disconnect_db(self):
        """Close connection with local database."""
        self.conn.close()


def clear_tables():
    """Clear specific tables on bot load.

    **Noteworthy:** This function is necessary for the internal work of the bot,
    when main script is executed
    """
    modify_data(
        'mainDB',
        'UPDATE variables SET poll_locked = ?, ship_in_active = ?,'
        'rsp_game_active = ?',
        0,
        0,
        0
    )
    modify_data(
        'mainDB',
        'DELETE FROM bots'
    )
    modify_data(
        'mainDB',
        'DELETE FROM users'
    )


def reset_bot_tables():
    """Clear specific tables on bot reset.

    This function handles clearing some tables, when bot is resetted
    in `bot_panel`
    """
    modify_data(
        'mainDB',
        'UPDATE variables SET poll_locked = ?, ship_date = ?,'
        'ship_text_full = ?, ship_text_short = ?, ship_activated = ?,'
        'ship_in_active = ?, is_setup_completed = ?,'
        'current_selected_bot = ?, bot_uptime = ?, avatar_cooldown = ?,'
        'rsp_game_active = ?',
        0, 0, '', '', 0, 0, 0, 0, 0, 0, 0
    )
    modify_data(
        'mainDB',
        'DELETE FROM bots'
    )
    modify_data(
        'mainDB',
        'DELETE FROM users'
    )
    modify_data(
        'mainDB',
        'DELETE FROM admin_list'
    )
    modify_data(
        'mainDB',
        'DELETE FROM block_list'
    )
    modify_data(
        'confDB',
        'DELETE FROM tokens'
    )


def get_data(path_num, is_single, command, *data):
    """Retrieve data from a database and return it as an array.

    Args:
        path_num (int): Number of path in path list
        is_single (bool): Boolean for getting data w/o array
        command (str): Command to execute
        data (tuple): Variable length list of data

    Returns:
        Union[list, str, int, None]: Array with data, single data or None

    Raises:
        Exception: Returns info about error
    """
    try:
        data_arr = []
        database = Database(path_num)
        if not data:
            database.cur.execute(command)
        else:
            database.cur.execute(command, data)
        received_data = database.cur.fetchall()
        database.disconnect_db()
        if is_single:
            if not received_data:
                return None
            return received_data[0]
        for element in received_data:
            if len(element) > 1:
                for item in element:
                    data_arr.append(item)
            else:
                data_arr.append(element[0])
        return data_arr
    except sqlite3.Error as err:
        print('\nThere is an error while working with DB '
              '(Method: get_data).\n'
              f'Here are error details: {err}')
        sys.exit()


def modify_data(path_num, command, *data):
    """Modify data in the DB.

    Parameters:
        path_num (int): Number of path in path list
        command (str): Command to execute
        data (tuple): List of data

    Raises:
        Exception: Returns info about error
    """
    try:
        database = Database(path_num)
        if len(data) > 0:
            database.cur.execute(command, data)
        else:
            database.cur.execute(command)
        database.conn.commit()
        database.disconnect_db()
    except sqlite3.Error as err:
        print('\nThere is an error while working with DB '
              '(Method: modify_data).\n'
              f'Here are error details: {err}')
        sys.exit()
