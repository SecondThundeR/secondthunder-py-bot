"""Text version of RSP game.

This cog handles game logic of rock scissors paper.
"""


import discord
import random
import asyncio
import src.lib.database as database
from discord.ext import commands


class RSPGame(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.fail_delay = 4
        self.success_delay = 1
        self.win_variants = {
            'камень': 'ножницы',
            'бумага': 'камень',
            'ножницы': 'бумага'
        }

    @commands.command(aliases=['цуефа'])
    async def rsp_mode(self, ctx, *args):
        """Execute correct mode of game depending on arguments.

        If arguments aren't provided, executes multiplayer game.
        Otherwise, executes game with bot

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List of arguments (RSP variants, if playing with bot)
        """
        if not args:
            if database.get_data(
                'mainDB',
                True,
                'SELECT rsp_game_active FROM variables'
            ):
                await ctx.reply('Сессия игры уже запущена, '
                                'чтобы начать новую игру, закончите старую')
            else:
                await RSPGame.rsp_multi_game(self, ctx)
        else:
            await RSPGame.rsp_bot_game(self, ctx, args[0])

    @staticmethod
    def join_check(ctx):
        """Check for correct command to join.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions

        Returns:
            bool: True if all conditions are met, False otherwise
        """
        test_string = ctx.message.content.lower()
        test_channel = isinstance(ctx.message.channel, discord.channel.DMChannel)
        return bool(test_string == 'играть' and not test_channel)

    def choice_check(self, ctx):
        """Check for correct answer from user.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions

        Returns:
            True, if all conditions are met
        """
        test_string = ctx.message.content.lower()
        test_channel = isinstance(ctx.message.channel, discord.channel.DMChannel)
        return bool(test_string in self.win_variants and test_channel)

    async def purge_messages(self, messages):
        """Delete all messages, that can distract users in channel.

        Parameters:
            message (list): List with messages to delete
        """
        for message in messages:
            await message.delete()

    def rsp_game(self, first_var, second_var, first_user_id, second_user_id):
        """Get the outcome of the game and return its result.

        This function handles check for winner of RSP
        If no one wins, throw 'Draw'

        Parameters:
            first_var (str): First player choice
            second_var (str): Second player choice
            first_user_id (int): First player ID to mention
            second_user_id (int): Second player ID to mention

        Returns:
            str: Outcome of the game
        """
        f_user_mention = f'<@{first_user_id}>'
        s_user_mention = f'<@{second_user_id}>'
        end_text = '**Игра между ' \
                   f'{f_user_mention} и {s_user_mention} ' \
                   'окончена!**\n'
        outcome_text = ''
        if first_var == self.win_variants[second_var]:
            outcome_text = f'**Результаты:** {second_var}  🤜  {first_var}\n' \
                        f'{s_user_mention} победил!'
        elif second_var == self.win_variants[first_var]:
            outcome_text = f'**Результаты:** {first_var}  🤜  {second_var}\n' \
                        f'{f_user_mention} победил!'
        else:
            outcome_text = f'**Результаты:** {first_var}  🙏  {second_var}\n' \
                        'И у нас ничья!'
        return end_text + outcome_text

    async def rsp_bot_game(self, ctx, user_choice):
        """Game with bot.

        This function executes random choice of bot and comparing it with
        players choice

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            user_choice (str): Player's move variant
        """
        if user_choice not in self.win_variants:
            await ctx.reply('Похоже вы выбрали что-то не то...')
        else:
            bot_choice = random.choice(list(self.win_variants))
            await ctx.send(RSPGame.rsp_game(
                self, user_choice, bot_choice,
                ctx.author.id, self.client.user.id
            ))

    async def rsp_multi_game(self, ctx):
        """Game with other users of server.

        This function executes game with other users.

        Also, it waits for another user to play,
        and waits for a response from each in turn,
        then displays the outcome of the game

        **Noteworthy:** When game is live, lock other games to be played,
        while current game isn't finished

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
        """
        database.modify_data(
            'mainDB',
            'UPDATE variables SET rsp_game_active = ?',
            1
        )
        current_channel = ctx.message.channel
        first_user = ctx.author
        users_choice = []
        messages_to_purge = []
        await ctx.message.delete()
        init_msg = await ctx.reply('Вы запустили игру! '
                                   'Второй игрок, напишите "Играть"\n'
                                   '*До автоотмены - 1 минута*')
        messages_to_purge.append(init_msg)
        try:
            s_user_wait = await self.client.wait_for(
                'message',
                timeout=60,
                check=RSPGame.join_check
            )
            second_user = s_user_wait.author
        except asyncio.TimeoutError:
            database.modify_data(
                'mainDB',
                'UPDATE variables SET rsp_game_active = ?',
                0
            )
            game_fail = ctx.reply('Похоже никто не решил сыграть с вами. '
                                  'Пока что я отменил данную игру')
            messages_to_purge.append(game_fail)
            await asyncio.sleep(self.fail_delay)
            await RSPGame.purge_messages(self, messages_to_purge)
            return
        else:
            if s_user_wait.author.id == first_user.id:
                database.modify_data(
                    'mainDB',
                    'UPDATE variables SET rsp_game_active = ?',
                    0
                )
                f_user_join = await ctx.reply('Вы решили поиграть сам собой, '
                                              'я отменяю данную игру')
                messages_to_purge.append(s_user_wait)
                messages_to_purge.append(f_user_join)
                await asyncio.sleep(self.fail_delay)
                await RSPGame.purge_messages(self, messages_to_purge)
                return
        await s_user_wait.delete()
        await init_msg.edit(content='Сейчас идёт игра между '
                                    f'{first_user.mention} и {second_user.mention}')
        try:
            await first_user.send('Ваш вариант *(На ответ 1 минута)*:')
            first_response = await self.client.wait_for(
                'message',
                timeout=30,
                check=RSPGame.choice_check
            )
            users_choice.append(first_response.content.lower())
        except asyncio.TimeoutError:
            database.modify_data(
                'mainDB',
                'UPDATE variables SET rsp_game_active = ?',
                0
            )
            f_move_fail = await current_channel.send(f'{first_user.mention} '
                                                     'не успел ответить вовремя. '
                                                     'Игра отменена')
            messages_to_purge.append(f_move_fail)
            await asyncio.sleep(self.fail_delay)
            await RSPGame.purge_messages(self, messages_to_purge)
            return
        try:
            await second_user.send('Ваш вариант *(На ответ 1 минута)*:')
            second_response = await self.client.wait_for(
                'message',
                timeout=30,
                check=RSPGame.choice_check
            )
            users_choice.append(second_response.content.lower())
        except asyncio.TimeoutError:
            database.modify_data(
                'mainDB',
                'UPDATE variables SET rsp_game_active = ?',
                0
            )
            s_move_fail = await current_channel.send(f'{second_user.mention} '
                                                     'не успел ответить вовремя. '
                                                     'Игра отменена')
            messages_to_purge.append(s_move_fail)
            await asyncio.sleep(self.fail_delay)
            await RSPGame.purge_messages(self, messages_to_purge)
            return
        database.modify_data(
            'mainDB',
            'UPDATE variables SET rsp_game_active = ?',
            0
        )
        await current_channel.send(RSPGame.rsp_game(
            self, users_choice[0], users_choice[1],
            first_user.id, second_user.id
        ))
        await RSPGame.purge_messages(self, messages_to_purge)


def setup(client):
    client.add_cog(RSPGame(client))
