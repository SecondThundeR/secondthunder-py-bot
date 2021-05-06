"""Get random number.

This cog handles getting random number in different ranges
(From 1 to {some number} or From {some number} to {some number})
"""


import random
import asyncio
from discord.ext import commands


class RandomNumbers(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.delay_time = 5
        self.range_number = None
        self.random_number = None
        self.first_number = None
        self.second_number = None

    @commands.command(aliases=['рандом'])
    async def get_random_number(self, ctx, *args):
        """Get random number and send it.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List of arguments (Range numbers)
        """
        if not args:
            await ctx.reply('К сожалению, я не получил аргументов для вывода рандома',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()
        elif args:
            if len(args) == 1:
                try:
                    self.range_number = int(args[0])
                    if self.range_number <= 1:
                        await ctx.reply('Я не могу выдать рандомное число '
                                        f'от 1 до {self.range_number}',
                                        delete_after=self.delay_time)
                        await asyncio.sleep(self.delay_time)
                        await ctx.message.delete()
                    else:
                        self.random_number = random.randint(1, self.range_number)
                        await ctx.reply('Ваше рандомное число '
                                        f'от 1 до {self.range_number}: '
                                        f'**{self.random_number}**')
                except ValueError:
                    await ctx.reply('Ваш аргумент был введён неправильно',
                                    delete_after=self.delay_time)
                    await asyncio.sleep(self.delay_time)
                    await ctx.message.delete()
            elif len(args) == 2:
                try:
                    self.first_number = int(args[0])
                    self.second_number = int(args[1])
                    if self.first_number >= self.second_number:
                        await ctx.reply('Я не могу выдать рандомное число '
                                        f'в диапазоне от {self.first_number} до '
                                        f'{self.second_number}',
                                        delete_after=self.delay_time)
                        await asyncio.sleep(self.delay_time)
                        await ctx.message.delete()
                    else:
                        self.random_number = random.randint(
                            self.first_number,
                            self.second_number
                        )
                        await ctx.reply('Ваше рандомное число '
                                        f'от {self.first_number} '
                                        f'до {self.second_number}: '
                                        f'**{self.random_number}**')
                except ValueError:
                    await ctx.reply('Ваш аргумент или аргументы '
                                    'были введены неправильно',
                                    delete_after=self.delay_time)
                    await asyncio.sleep(self.delay_time)
                    await ctx.message.delete()
            else:
                await ctx.reply(f'К сожалению, я получил аргументов больше, '
                                f'чем нужно, а именно `{len(args) - 2}`',
                                delete_after=self.delay_time)
                await asyncio.sleep(self.delay_time)
                await ctx.message.delete()


def setup(client):
    client.add_cog(RandomNumbers(client))
