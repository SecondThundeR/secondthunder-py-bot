"""Script for getting random answer from list.

This cog gets question from user and randomly selects
answer from list with answers
"""


import random
import asyncio
from discord.ext import commands


class MagicBall(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.magic_ball_answers = [
            'Бесспорно', 'Предрешено', 'Никаких сомнений',
            'Определённо да', 'Можешь быть уверен в этом', 'Мне кажется — «да»',
            'Вероятнее всего', 'Хорошие перспективы', 'Знаки говорят — «да»', 'Да',
            'Пока не ясно, попробуй снова', 'Спроси позже', 'Лучше не рассказывать',
            'Сейчас нельзя предсказать', 'Сконцентрируйся и спроси опять',
            'Даже не думай', 'Мой ответ — «нет»', 'По моим данным — «нет»',
            'Перспективы не очень хорошие', 'Весьма сомнительно'
        ]
        self.delay_time = 3

    @commands.command(aliases=['шар'])
    async def ask_magic_ball(self, ctx, text=None):
        """Get random answer from list and send it.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            text (str | None): Question from user to answer
            (Used only to check for existence)
        """
        if not text:
            await ctx.reply('Вы не дали мне вопроса, '
                            'чтобы я на него ответил',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()
        else:
            await ctx.reply(random.choice(self.magic_ball_answers))


def setup(client):
    client.add_cog(MagicBall(client))
