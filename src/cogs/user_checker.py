"""Get random percent of who the user is.

Also, this cog allows to pass many options to execute
certain test outputs
"""


import discord
import asyncio
import random
import src.lib.users as users
from src.lib.exceptions import UsersNotFound
from discord.ext import commands


class UserChecker(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.delay_time = 5
        self.count = None
        self.text = None
        self.user = None
        self.random_mode = False

    @commands.command(aliases=['тест'])
    async def regular_user_checker(self, ctx, *args):
        if not args:
            await ctx.reply('Вы не передали никаких аргументов',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()
            return
        args = list(args)
        self.user = ctx.author
        self.count = 1
        self.random_mode = False
        if args[0].isnumeric():
            self.count = int(args[0])
            args.pop(0)
        elif args[0] == 'рандом':
            try:
                self.user = await users.get_random_user(ctx.message)
            except UsersNotFound as warning:
                await ctx.reply(f'Произошла ошибка: {warning}!')
                return
            self.random_mode = True
            args.pop(0)
        elif not self.random_mode:
            if args[0].startswith('<@!'):
                self.user = await ctx.guild.fetch_member(args[0][3:len(args[0]) - 1])
                args.pop(0)
            elif args[0].startswith('--'):
                self.user = args[0][2:]
                args.pop(0)
        self.text = ' '.join(args)
        percent_data = UserChecker.get_test_percent(self.count)
        if not self.text:
            await ctx.reply('Вы не передали текст для теста',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()
            return
        final_msg = UserChecker.format_percent_to_message(
            percent_data,
            self.text,
            self.user
        )
        await ctx.send(final_msg)

    @staticmethod
    def get_test_percent(amount):
        if amount == 1:
            return random.randint(0, 100)
        perc_list = []
        avg_percent = 0
        i = 0
        while i < amount:
            perc_list.append(random.randint(0, 100))
            avg_percent += perc_list[i]
            i += 1
        avg_percent /= amount
        return [perc_list, avg_percent]

    @staticmethod
    def format_percent_to_message(percent_data, text, user):
        warn_msg = 'Вы превысили лимит Discord по длине сообщения!'
        user_name = None
        if isinstance(user, str):
            user = f'**{user}**'
            user_name = user
        if isinstance(user, discord.Member):
            user_name = users.get_members_name(user)
            user = user.mention
        if isinstance(percent_data, list):
            percent_list = percent_data[0]
            avg_num = float(percent_data[1], 2)
            msg = f'Журнал тестирования {user}\n\n'
            for i, perc in enumerate(percent_list):
                if len(msg) > 2000:
                    msg = warn_msg
                    break
                if perc == 0:
                    msg += f'*Тест {i + 1}.* **{user_name}** сегодня не {text} :c\n'
                elif perc == 100:
                    msg += f'*Тест {i + 1}.* Кто бы мог подумать то!\n' \
                           f'**{user_name}** {text} на **{perc}%**\n'
                else:
                    msg += f'*Тест {i + 1}.* **{user_name}** {text} на **{perc}%**\n'
            msg += f'\nСреднее значение всех тестов - **{avg_num}%**'
            return msg
        if percent_data == 0:
            return f'{user} сегодня не {text} :c'
        if percent_data == 100:
            return f'Кто бы мог подумать то! {user}' \
                   f'\n{text} на **{percent_data}%**'
        return f'{user} {text} на **{percent_data}%**'


def setup(client):
    client.add_cog(UserChecker(client))
