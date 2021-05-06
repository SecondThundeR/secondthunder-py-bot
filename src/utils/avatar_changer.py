"""'On-fly' avatar changer.

This script allows to change avatar of bot while it's running.
Script gets randomly choosen avatar data to replace current avatar.

This file can also be imported as a module and contains the following functions:
    * get_avatar_bytes - gets bytes from avatar picture
"""


import random
import time
import pathlib
import src.lib.database as database


CHANGE_COOLDOWN = 900


def get_avatar_bytes():
    """Get bytes from avatar picture.

    This function has built-in check for
    avatar change cooldown

    Returns:
        int: Cooldown time
        bytes: Bytes of PNG
    """
    curr_cooldown = database.get_data(
        'mainDB',
        True,
        'SELECT avatar_cooldown FROM variables',
    ) - int(time.time())
    if curr_cooldown > 0:
        return int(curr_cooldown)
    database.modify_data(
        'mainDB',
        'UPDATE variables SET avatar_cooldown = ?',
        int(time.time()) + CHANGE_COOLDOWN
    )
    avatar_path = f"{pathlib.Path().absolute()}/src/avatars/" \
                  f"Avatar_{random.randint(1, 16)}.png"
    with open(avatar_path, 'rb') as f:
        avatar_bytes = f.read()
    f.close()
    return avatar_bytes
