"""Bot's uptime handler.

This cog handles calculating and sending current bot's uptime
"""


import time
import asyncio
import datetime
import src.lib.database as database
import src.utils.timedelta_formatter as td_format
from discord.ext import commands


class Uptime(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.delay_time = 5

    @commands.command(aliases=['uptime'])
    async def send_uptime(self, ctx):
        """Calculate and send current uptime of bot.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
        """
        curr_uptime = int(time.time()) - database.get_data(
            'mainDB',
            True,
            'SELECT bot_uptime FROM variables',
        )
        time_string = td_format.format_timedelta(
            datetime.timedelta(seconds=curr_uptime)
        )
        if curr_uptime < 36000:
            await ctx.reply(f'Я не сплю уже на протяжении **0{time_string}**',
                            delete_after=self.delay_time)
        else:
            await ctx.reply(f'Я не сплю уже на протяжении **{time_string}**',
                            delete_after=self.delay_time)
        await asyncio.sleep(self.delay_time)
        await ctx.message.delete()


def setup(client):
    client.add_cog(Uptime(client))
