"""Ship randomly selected users.

This cog allows user to ship two random people or two chosen by user.
Cog returns halves of each name and adds a heart.
"""


import emoji
import asyncio
import datetime as dt
import src.lib.database as database
import src.lib.users as users
from src.lib.exceptions import UsersNotFound
from discord.ext import commands


class RandomShip(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.delay_time = 2
        self.delete_time = 5
        self.strings_to_send = [
            '*чтож...*', '**МОРЕ ВОЛНУЕТСЯ РАЗ**',
            '**МОРЕ ВОЛНУЕТСЯ ДВА**', '**МОРЕ ВОЛНУЕТСЯ ТРИ**'
        ]
        self.weekday_dict = {
            0: 'в Понедельник',
            1: 'во Вторник',
            2: 'в Среду',
            3: 'в Четверг',
            4: 'в Пятницу',
            5: 'в Субботу',
            6: 'в Воскресенье',
        }

    @commands.command(aliases=['шип'])
    async def ship_func_chooser(self, ctx, *args):
        """Select correct function depending of statement.

        This function chooses another function to run, when
        certain statement is true

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List of arguments
        """
        if database.get_data(
            'mainDB',
            True,
            'SELECT ship_in_active FROM variables'
        ):
            return
        if len(args) == 1:
            if 'скип' in args:
                await RandomShip.reset_ship(self, ctx)
            elif 'фаст' in args:
                await RandomShip.random_ship(self, ctx, True)
            else:
                await ctx.reply('Я не могу шипперить одного человека. '
                                'Добавьте ещё кого-то, чтобы я смог '
                                'сделать "магию"')
        elif len(args) == 2:
            await RandomShip.custom_ship(self, ctx, list(args))
        else:
            await RandomShip.random_ship(self, ctx)

    async def get_user_info(self, ctx, user):
        """Get names of users from arguments.

        This function gets username if user provided mention of someone,
        otherwise return argument without changes

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            user (str): Custom names for shipping

        Returns:
            list: List with username and it's length divided by two
        """
        if user.startswith('<@!'):
            user_id = user[3:len(user) - 1]
            custom_member = await ctx.guild.fetch_member(user_id)
            user_name = users.get_members_name(custom_member)
            user_length = int(len(user_name) / 2)
        else:
            user_name = user
            user_length = int(len(user_name) / 2)
        return [user_name, user_length]

    async def reset_ship(self, ctx):
        """Reset latest ship results to start over.

        This function resets results of shipping to allow user execute
        new ship function

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
        """
        database.modify_data(
            'mainDB',
            'UPDATE variables SET ship_date = ?, ship_text_short = ?, '
            'ship_text_full = ?, ship_activated = ?',
            '',
            '',
            '',
            0
        )
        await ctx.reply('Результаты шиппинга сброшены! '
                        '*(Вы разлучили, возможно, великолепную парочку!)*',
                        delete_after=self.delete_time)
        await asyncio.sleep(self.delete_time)
        await ctx.message.delete()

    async def custom_ship(self, ctx, args):
        """Ship with two custom names from user.

        This function runs ship with two custom names from arguments,
        rather ship with random users

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            args (list): List of arguments (Custom names for ship)
        """
        if emoji.emoji_count(ctx.message.content):
            await ctx.reply('К сожалению, шип смайлов не имеет смысла',
                            delete_after=self.delete_time)
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
        elif '<@&' in args:
            await ctx.reply('К сожалению, я не могу обработать это',
                            delete_after=self.delete_time)
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
        elif '<:' in args:
            await ctx.reply('К сожалению, шип эмодзи не имеет смысла',
                            delete_after=self.delete_time)
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
        elif '@everyone' in args or '@here' in args:
            await ctx.reply('Похоже вы пытаетесь передать `@here` или `@everyone`, '
                            'что может вызвать ошибку',
                            delete_after=self.delete_time)
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
        else:
            first_user_info = await RandomShip.get_user_info(self, ctx, args[0])
            second_user_info = await RandomShip.get_user_info(self, ctx, args[1])
            first_username_part = first_user_info[0][:first_user_info[1]]
            second_username_part = second_user_info[0][second_user_info[1]:]
            final_name = first_username_part + second_username_part
            await ctx.reply(f'Данная парочка смело бы называлась - **{final_name}**')

    async def random_ship(self, ctx, fast_mode=False):
        """Ship with two randomly chosen names.

        This function runs ship with random users,
        rather shipping two custom names from arguments

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
        """
        current_date = dt.datetime.now().date()
        next_date = (dt.datetime.now() + dt.timedelta(days=1)).date()
        ship_date = database.get_data(
            'mainDB',
            True,
            'SELECT ship_date FROM variables'
        )
        ship_activated = database.get_data(
            'mainDB',
            True,
            'SELECT ship_activated FROM variables'
        )
        ship_in_active = database.get_data(
            'mainDB',
            True,
            'SELECT ship_in_active FROM variables'
        )
        if not ship_activated and not ship_in_active:
            database.modify_data(
                'mainDB',
                'UPDATE variables SET ship_in_active = ?, ship_activated = ?',
                1,
                1
            )
            try:
                users_info = await users.get_shipping_users(ctx.message)
            except UsersNotFound as warning:
                database.modify_data(
                    'mainDB',
                    'UPDATE variables SET ship_in_active = ?, ship_activated = ?',
                    0,
                    0
                )
                await ctx.reply(f'Произошла ошибка: {warning}!',
                                delete_after=self.delete_time)
                await asyncio.sleep(self.delete_time)
                await ctx.message.delete()
                return
            first_username = users.get_members_name(users_info[0])
            first_user_length = int(len(first_username) / 2)
            second_username = users.get_members_name(users_info[1])
            second_user_length = int(len(second_username) / 2)
            first_sliced_username = first_username[:first_user_length]
            second_sliced_username = second_username[second_user_length:]
            final_username = first_sliced_username + second_sliced_username
            ship_text_short = f'{users_info[0].mention} + {users_info[1].mention}'
            ship_text_full = f'{first_username} + {second_username}, #' + final_username
            if fast_mode:
                await ctx.reply(f'**Парочка дня на сегодня:** {ship_text_short} '
                                ':two_hearts:')
            else:
                await RandomShip.random_ship_messages(self, ctx, ship_text_short)
            database.modify_data(
                'mainDB',
                'UPDATE variables SET ship_date = ?, ship_text_full = ?, '
                'ship_text_short = ?, ship_in_active = ?',
                next_date,
                ship_text_full,
                ship_text_short,
                0
            )
        elif database.get_data(
            'mainDB',
            True,
            'SELECT ship_in_active FROM variables'
        ):
            pass
        elif (database.get_data(
            'mainDB',
            True,
            'SELECT ship_activated FROM variables'
            ) and current_date < dt.datetime.strptime(
                ship_date,
                '%Y-%m-%d'
            ).date()
        ):
            ship_text_full = database.get_data(
                'mainDB',
                True,
                'SELECT ship_text_full FROM variables'
            )
            next_date = database.get_data(
                'mainDB',
                True,
                'SELECT ship_date FROM variables'
            )
            next_date_string = self.weekday_dict[
                dt.datetime.strptime(next_date, '%Y-%m-%d').weekday()
            ]
            await ctx.reply(f'**Парочка дня на сегодня:** {ship_text_full} '
                            ':two_hearts: \n\n*Следующий шиппинг будет доступен '
                            f'{next_date_string}*')
        elif (database.get_data(
            'mainDB',
            True,
            'SELECT ship_activated FROM variables'
            ) and current_date >= dt.datetime.strptime(
                ship_date,
                '%Y-%m-%d'
            ).date()
        ):
            database.modify_data(
                'mainDB',
                'UPDATE variables SET ship_activated = ?',
                0
            )
            await RandomShip.random_ship(self, ctx)
        else:
            pass

    async def random_ship_messages(self, ctx, short_text):
        """Send pre-messages and result of shipping.

        This function ships three pre-messages and final message with
        result of shipping

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            short_text (str): Ship's short text
        """
        for strings in self.strings_to_send:
            await ctx.channel.send(strings)
            await asyncio.sleep(self.delay_time)
        await ctx.reply(f'**В ЛЮБОВНОЙ ПОЗЕ ЗАСТРЯЛИ** {short_text} :two_hearts:')


def setup(client):
    client.add_cog(RandomShip(client))
