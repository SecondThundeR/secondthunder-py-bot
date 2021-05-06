"""Text version of roulette game.

This cog handles game logic of russian roulette.
"""


import random
import asyncio
import src.lib.database as database
import src.lib.words_base as words_base
from discord.ext import commands


class RussianRoulette(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.tables_aliases = {
            'вин': 'win',
            'луз': 'lose',
            'ноль': 'zero',
            'минус': 'minus'
        }
        self.delete_time = 5
        self.delay_time = 2
        self.bullet_list = []
        self.bullet_count = 0

    @commands.command(aliases=['рулетка'])
    async def switch_avatar(self, ctx, *args):
        """Handle game logic and start game.

        This function handles all russian roulette logic.
        Also, it has certain checks for any non-standard situation

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List of arguments (Bullet count number)
        """
        if not args:
            self.bullet_count = 1
        else:
            args = list(args)
            if args[0] == 'добавить' and args[1] in self.tables_aliases:
                TABLE_TO_MODIFY = self.tables_aliases[args[1]]
                for i in range(2):
                    args.pop(0)
                WORD_TO_ADD = " ".join(args)
                await ctx.reply(
                    words_base.manage_r_words_tables(
                        WORD_TO_ADD,
                        TABLE_TO_MODIFY,
                        'add'
                    ),
                    delete_after=self.delete_time
                )
                await asyncio.sleep(self.delete_time)
                await ctx.message.delete()
                return
            if args[0] == 'удалить':
                bot_admin = database.get_data(
                    'mainDB',
                    True,
                    'SELECT * FROM admin_list '
                    'WHERE admins_id = ?',
                    ctx.author.id
                )
                if bot_admin and args[1] in self.tables_aliases:
                    TABLE_TO_MODIFY = self.tables_aliases[args[1]]
                    for i in range(2):
                        args.pop(0)
                    WORD_TO_DELETE = " ".join(args)
                    await ctx.reply(
                        words_base.manage_r_words_tables(
                            WORD_TO_DELETE,
                            TABLE_TO_MODIFY,
                            'del'
                        ),
                        delete_after=self.delete_time
                    )
                    await asyncio.sleep(self.delete_time)
                    await ctx.message.delete()
                    return
            try:
                self.bullet_count = int(args[0])
            except ValueError:
                await ctx.reply('Похоже вы передали не число.'
                                '\nПопробуйте ещё раз, '
                                'но уже с правильными данными')
                return
        if self.bullet_count == 0:
            await ctx.reply(RussianRoulette.get_random_word("zero"))
        elif self.bullet_count < 0:
            await ctx.reply(RussianRoulette.get_random_word("minus"))
        elif self.bullet_count == 6:
            await ctx.reply('Поздравляю! Вы гуль!')
        elif self.bullet_count > 6:
            await ctx.reply('Может стоит напомнить, '
                            'что по правилам русской рулетки, '
                            'можно брать только до 6 патронов, не?')
        else:
            self.bullet_list = []
            for i in range(self.bullet_count):
                CHARGED_SECTION = random.randint(1, 6)
                if CHARGED_SECTION in self.bullet_list:
                    i -= 1
                else:
                    self.bullet_list.append(CHARGED_SECTION)
            deadly_bullet = random.randint(1, 6)
            if deadly_bullet in self.bullet_list:
                result_msg = await ctx.reply('**БАХ**')
                await asyncio.sleep(self.delay_time)
                await result_msg.edit(
                    content=RussianRoulette.get_random_word("lose")
                )
            else:
                result_msg = await ctx.reply('*тишина*')
                await asyncio.sleep(self.delay_time)
                await result_msg.edit(
                    content=RussianRoulette.get_random_word("win")
                )

    @staticmethod
    def get_random_word(condition):
        """Get random word from database.

        This function handles getting random word from DB
        depending on condition of game

        Parameters:
            condition (str): Condition of game when executed

        Returns:
            str: Random chosen word depending on condition
        """
        if condition == 'win':
            WIN_WORDS_LIST = database.get_data(
                'wordsDB',
                False,
                'SELECT words FROM roulette_win_words'
            )
            random_word = random.choice(WIN_WORDS_LIST)
        elif condition == 'lose':
            LOSE_WORDS_LIST = database.get_data(
                'wordsDB',
                False,
                'SELECT words FROM roulette_lose_words'
            )
            random_word = random.choice(LOSE_WORDS_LIST)
        elif condition == 'zero':
            ZERO_WORDS_LIST = database.get_data(
                'wordsDB',
                False,
                'SELECT words FROM roulette_zero_words'
            )
            random_word = random.choice(ZERO_WORDS_LIST)
        elif condition == 'minus':
            MINUS_WORDS_LIST = database.get_data(
                'wordsDB',
                False,
                'SELECT words FROM roulette_minus_words'
            )
            random_word = random.choice(MINUS_WORDS_LIST)
        return random_word


def setup(client):
    client.add_cog(RussianRoulette(client))
