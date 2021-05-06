"""Get random word from list.

This cog sends randomly chosen word from list
"""


import random
import asyncio
import src.lib.database as database
import src.lib.users as users
import src.lib.words_base as words_base
from src.lib.exceptions import UsersNotFound
from discord.ext import commands


class RandomWord(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.delay_time = 5
        self.curr_user = None

    @commands.command(aliases=['ху', 'who'])
    async def get_random_word(self, ctx, *args):
        """Get random word from list and send it.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List of arguments (Custom name or mode of function)
        """
        if not args:
            self.curr_user = ctx.author.mention
        else:
            args = list(args)
            if args[0] == 'добавить':
                args.pop(0)
                word_to_add = " ".join(args)
                await ctx.reply(
                    words_base.manage_words_table(word_to_add, 'add'),
                    delete_after=self.delay_time
                )
                await asyncio.sleep(self.delay_time)
                await ctx.message.delete()
                return
            if args[0] == 'удалить':
                if database.get_data(
                    'mainDB',
                    True,
                    'SELECT * FROM admin_list WHERE admins_id = ?',
                    ctx.author.id
                ):
                    args.pop(0)
                    word_to_delete = " ".join(args)
                    await ctx.reply(
                        words_base.manage_words_table(word_to_delete, 'del'),
                        delete_after=self.delay_time
                    )
                    await asyncio.sleep(self.delay_time)
                    await ctx.message.delete()
                return
            if args[0] == 'рандом':
                try:
                    r_user = await users.get_random_user(ctx.message)
                except UsersNotFound as warning:
                    await ctx.reply(f'Произошла ошибка: {warning}!')
                    return
                self.curr_user = r_user.mention
            else:
                self.curr_user = args[0]
        WORDS_ARRAY = database.get_data(
            'wordsDB',
            False,
            'SELECT words FROM main_words_base'
        )
        if not WORDS_ARRAY:
            await ctx.reply('Я пока не знаю никаких слов, '
                            'однако вы можете добавить новые слова в мой словарь',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()
        else:
            await ctx.send(f'{self.curr_user} {random.choice(WORDS_ARRAY)}')


def setup(client):
    client.add_cog(RandomWord(client))
