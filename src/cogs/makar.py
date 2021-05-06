"""Send meme sentence with reversed username.

This cog sends sentence 'Улыбок тебе дед ...' where at the end
reverse username goes
"""

import emoji
import asyncio
import src.lib.users as users
from discord.ext import commands
from src.lib.exceptions import UsersNotFound


class DedMakar(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.delay_time = 5

    @commands.command(aliases=['макар'])
    async def send_makar_message(self, ctx, *, arg=None):
        """Send famous (maybe) sentence.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            arg (str | None): String with custom name or user mention
        """
        if not arg:
            try:
                r_user = await users.get_random_user(ctx.message)
            except UsersNotFound as warning:
                await ctx.reply(f'Произошла ошибка: {warning}!')
                return
            user = users.get_members_name(r_user)
            await ctx.reply(f'Улыбок тебе дед {user[::-1]}')
        else:
            if emoji.emoji_count(ctx.message.content) > 0:
                await ctx.reply('К сожалению, отзеркаливание смайлов не имеет смысла',
                                delete_after=self.delay_time)
                await asyncio.sleep(self.delay_time)
                await ctx.message.delete()
            elif arg.startswith('<@&'):
                await ctx.reply('К сожалению, я не могу обработать это',
                                delete_after=self.delay_time)
                await asyncio.sleep(self.delay_time)
                await ctx.message.delete()
            elif arg.startswith('<:'):
                await ctx.reply('К сожалению, отзеркаливание эмодзи не имеет смысла...',
                                delete_after=self.delay_time)
                await asyncio.sleep(self.delay_time)
                await ctx.message.delete()
            elif '@everyone' in arg or '@here' in arg:
                await ctx.reply('Похоже вы пытаетесь передать '
                                '`@here` или `@everyone`, что может вызвать ошибку',
                                delete_after=self.delay_time)
                await asyncio.sleep(self.delay_time)
                await ctx.message.delete()
            else:
                if arg.startswith('<@!'):
                    custom_member = await ctx.guild.fetch_member(arg[3:len(arg) - 1])
                    user = users.get_members_name(custom_member)
                else:
                    user = arg
                await ctx.reply(f'Улыбок тебе дед {user[::-1]}')


def setup(client):
    client.add_cog(DedMakar(client))
