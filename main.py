"""Entry point of Ghosty bot.

This is a bot script that runs on the Discord.py library and
allows you to execute functions using specific text commands

There is the starting point of the bot control, from where it begin its
work. Here you can change the entire logic of the bot and adjust it to
fit your needs
"""


import time
import aiocron
import asyncio
import discord
import src.lib.database as database
import src.lib.users as users
import src.utils.avatar_changer as avatar_changer
import src.utils.general_scripts as general_scripts
from discord.ext import commands


TOKENS = database.get_data(
    'confDB',
    False,
    'SELECT bot_token FROM tokens'
)
SELECTED_BOT = database.get_data(
    'mainDB',
    True,
    'SELECT current_selected_bot FROM variables'
)
DELAY_TIME = 5
client = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@aiocron.crontab('0 */3 * * *')
async def update_avatar():
    """Update avatar picture periodically.

    This function changes the bot avatar every 3 hours using a cron job.
    It also checks and updates the `avatar_cooldown` value
    to lock manual avatar changing during/after updating by cron job,
    which helps prevent getting a cooldown from the Discord API.
    """
    avatar_data = avatar_changer.get_avatar_bytes()
    if isinstance(avatar_data, int):
        pass
    else:
        await client.user.edit(avatar=avatar_data)


@client.event
async def on_ready():
    """Execute necessary functions.

    This function executes certain actions on bot's load, such as:
    Resetting DB table, loading commands, updating table with users,
    changing bot's status, changing bot's avatar, setting up new bot's uptime
    """
    database.clear_tables()
    await general_scripts.load_commands(client)
    await general_scripts.update_member_list(client)
    await client.change_presence(status=discord.Status.dnd)
    avatar_data = avatar_changer.get_avatar_bytes()
    if isinstance(avatar_data, int):
        pass
    else:
        await client.user.edit(avatar=avatar_data)
    database.modify_data(
        'mainDB',
        'UPDATE variables SET bot_uptime = ?',
        int(time.time())
    )
    print(f'Successfully logged in as {client.user}!')


@client.event
async def on_command_error(ctx, error):
    """Handle commands exceptions.

    This function catches certain exception and sends info message to the user
    Currently, this commands handles `CommandNotFound` and `PrivateMessageOnly`

    Args:
        ctx (discord.ext.commands.Context): The invocation context
        error (discord.ext.commands.CommandError): The error that was raised

    Raises:
        discord.ext.commands.CommandError: It there is an error 
            that isn't included in the handling
    """
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply('Данной команды не существует. '
                        'Попробуйте ввести что-то другое!',
                        delete_after=DELAY_TIME)
        await asyncio.sleep(DELAY_TIME)
        await ctx.message.delete()
    elif isinstance(error, commands.PrivateMessageOnly):
        await ctx.reply('Данной команда доступна только в личных сообщениях.',
                        delete_after=DELAY_TIME)
        await asyncio.sleep(DELAY_TIME)
        await ctx.message.delete()
    else:
        raise error


@client.event
async def on_member_join(member):
    """Add new server users to database.

    This function adds every new user to database, while bot is running.
    This helps prevent new users from being ignored in commands
    that use use a table of users.

    Args:
        member (discord.member.Member): Data about joined user
    """
    users.add_member_to_db(member)


@client.event
async def on_member_leave(member):
    """Remove left server users from database.

    This function removes every left user from database, while bot is running.
    This helps to prevent any problems with commands that use a table of users.

    Args:
        member (discord.member.Member): Data about left user
    """
    users.rem_member_from_db(member)


client.run(TOKENS[int(SELECTED_BOT)])
