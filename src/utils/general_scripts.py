"""General utils.

This script contains functions used in bot's main script

This file can also be imported as a module and contains the following functions:
    * update_member_list - updates users database on load
    * load_commands - prepares extensions on load
"""


import os
import src.lib.users as users


async def update_member_list(client):
    """Update users database on load.

    Parameters:
        client (discord.Client): Used to fetch members of server
    """
    for guild in client.guilds:
        async for member in guild.fetch_members(limit=None):
            users.add_member_to_db(member)


async def load_commands(client):
    """Prepare extensions on load.

    Parameters:
        client (discord.Client): Client object to load extension
    """
    for filename in os.listdir('./src/cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'src.cogs.{filename[:-3]}')
