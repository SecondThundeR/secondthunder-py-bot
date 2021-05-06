"""Send message on behalf of bot.

This cog allows you to send messages on behalf of the bot.
There are several flags that change the message sending behavior
"""


from discord.ext import commands


class MeMessage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['йа'])
    async def send_me_message(self, ctx, *args):
        """Send a user message on behalf of a bot.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): Arguments to work with (Mode + Message)
        """
        me_data = {
            'message': '',
            'tts': False
        }
        if args:
            await ctx.message.delete()
            if args[0] == 'анон':
                me_data['message'] = " ".join(args[1:])
            elif args[0] == 'анонттс':
                me_data['message'] = " ".join(args[1:])
                me_data['tts'] = True
            elif args[0] == 'ттс':
                me_data['message'] = f'{ctx.author.mention} ' \
                                     f'{" ".join(args[1:])}'
                me_data['tts'] = True
            else:
                me_data['message'] = f'{ctx.author.mention} ' \
                                     f'{" ".join(args)}'
            await ctx.send(me_data['message'], tts=me_data['tts'])


def setup(client):
    client.add_cog(MeMessage(client))
