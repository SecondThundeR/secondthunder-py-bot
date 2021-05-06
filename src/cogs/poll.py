"""Create poll with positive and negative options.

This cog can create simple message with two reactions and when time ends,
it collects reactions and sends overcome of poll
"""


import asyncio
from discord.ext import commands


class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.time = 60
        self.text = None
        self.author = None
        self.p_votes = 0
        self.n_votes = 0

    @commands.command(aliases=['полл'])
    async def create_poll(self, ctx, *args):
        """Create poll and send message with it.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List of arguments to work with
        """
        if not args:
            return
        await ctx.message.delete()
        self.author = ctx.author.mention
        if args[0].isnumeric():
            self.time = int(args[0])
            self.text = " ".join(args[1:])
        else:
            self.time = 60
            self.text = " ".join(args)
        vote_msg = await ctx.send('**Время голосования от '
                                  f'{self.author}**\n'
                                  f'Вопрос: {self.text}\n'
                                  '*Голосование закончится через '
                                  f'{self.time} секунд*')
        await vote_msg.add_reaction(emoji="👍")
        await vote_msg.add_reaction(emoji="👎")
        await asyncio.sleep(self.time)
        vote_msg = await vote_msg.channel.fetch_message(vote_msg.id)
        for reaction in vote_msg.reactions:
            if reaction.emoji == '👍':
                self.p_votes = reaction.count - 1
            if reaction.emoji == '👎':
                self.n_votes = reaction.count - 1
        await vote_msg.delete()
        if self.p_votes > self.n_votes:
            await ctx.send('**Голосование окончено!**\n'
                           f'Вопрос **{self.text}** '
                           f'от {self.author} '
                           'был **принят** среди многих **положительно**!\n'
                           '*Ну разве это не счастье?*')
        elif self.p_votes < self.n_votes:
            await ctx.send('**Голосование окончено!**\n'
                           f'Вопрос **{self.text}** от '
                           f'{self.author} '
                           'был **принят** среди многих **отрицательно**!\n'
                           '*Что ж, неудачам тоже свойственно быть*')
        elif self.p_votes == self.n_votes and self.p_votes and self.n_votes:
            await ctx.send('**Голосование окончено!**\n'
                           f'Вопрос **{self.text}** от '
                           f'{self.author} '
                           'получил **одинаковое** количество голосов\n'
                           'Голосование объявляется **несостоявшимся!**')
        elif not self.p_votes and not self.n_votes:
            await ctx.send('**Голосование окончено!**\n'
                           f'Вопрос **{self.text}** от '
                           f'{self.author} '
                           'не получил **никаких** голосов\n'
                           'Голосование объявляется **несостоявшимся!**')


def setup(client):
    client.add_cog(Poll(client))
