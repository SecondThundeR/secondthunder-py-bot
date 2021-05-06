"""Send help message for using the bot.

This cog provides a message with all available commands for bot
"""


import discord
import asyncio
from discord.ext import commands


HELP_MESSAGE = 'Доступные команды бота: ' \
               '\n\n**полл (время и текст | текст)** - запускает простое голосование' \
               '\n**шар (текст)** - симулятор шара с ответами' \
               '\n**макар** - возвращает предложение "Улыбок тебе ' \
               'дед [перевёрнутая строка]"' \
               '\n**хелп** - выводит информацию с командами' \
               '\n**uptime** - выводит время работы бота' \
               '\n**йа (ттс | анон | анонттс)** - аналог команды `/me`' \
               '\n**рандом (число | два числа)** - получение рандомного числа' \
               '\n**шип (два имени)** - шипперит двух рандомных пользователей' \
               '\n**цуефа** - игра в "Камень Ножницы Бумага"' \
               '\n**рулетка** - запускает игру в русскую рулетку' \
               '\n**аватарка** - запускает смену текущей аватарки' \
               '\n**система (фулл)** - показывает данные о системе' \
               '\n**ху | who** - рандомный пользователь + рандомное предложение' \
               '\n**поиск (пидорасов)** -  *поиск пидорасов активирован...*'


class HelpMessage(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.delay_time = 5

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.remove_command('help')

    @commands.command(aliases=['хелп'])
    async def send_help_message(self, ctx):
        """Send message with all available commands of bot.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
        """
        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(HELP_MESSAGE)
        else:
            await ctx.author.send(HELP_MESSAGE)
            await ctx.reply('Хей, проверь личку! '
                            'Я отправил тебе помощь по командам',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()


def setup(client):
    client.add_cog(HelpMessage(client))
