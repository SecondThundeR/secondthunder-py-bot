"""Avatar switcher (Beta).

This cog allows users to change avatar of bot while it's running
with certain command.
"""


import asyncio
import datetime
import src.utils.timedelta_formatter as td_format
import src.utils.avatar_changer as avatar_changer
from discord.ext import commands


class AvatarSwitcher(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.delay_time = 5

    @commands.command(aliases=['аватарка'])
    async def avatar_switch(self, ctx):
        """Change avatar of bot via command.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
        """
        avatar_data = avatar_changer.get_avatar_bytes()
        if isinstance(avatar_data, int):
            time_string = td_format.format_timedelta(
                datetime.timedelta(seconds=avatar_data)
            )
            await ctx.reply('Пока что нельзя сменить аватарку. '
                            f'Попробуйте через **{time_string}**',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()
        else:
            await self.client.user.edit(avatar=avatar_data)
            await ctx.reply('Аватарка успешно изменена!',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()


def setup(client):
    client.add_cog(AvatarSwitcher(client))
