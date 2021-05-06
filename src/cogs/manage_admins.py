"""Manage admin list of bot.

This cog handles addition/removal id's of user to/from admin list
"""


import asyncio
import src.lib.database as database
import src.lib.users as users
from discord.ext import commands


class ManageAdmins(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.delete_time = 5

    @commands.command(aliases=['админ'])
    @commands.dm_only()
    async def admin_manager(self, ctx, *args):
        """Check if user is admin and execute required operation.

        This function handles user checking and executing addition/deletion
        of user's ID to/from admin list

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List with selected mode and user's ID
        """
        if len(args) == 2 and users.is_user_admin(ctx.author.id):
            if args[0] == 'добавить':
                await ManageAdmins.add_admin(self, ctx, args[1])
            elif args[0] == 'удалить':
                await ManageAdmins.remove_admin(self, ctx, args[1])

    async def add_admin(self, ctx, user_id):
        """Add user's ID to admin list.

        This function handles addition of user's ID to admin list.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            user_id (str): User's ID to add as an admin
        """
        if users.is_user_admin(user_id):
            await ctx.reply('Данный пользователь уже админ')
        else:
            database.modify_data(
                'mainDB',
                'INSERT INTO admin_list VALUES (?)',
                user_id
            )
            await ctx.reply('Я успешно добавил такого админа')

    async def remove_admin(self, ctx, user_id):
        """Remove user's ID from admin list.

        This function handles removal of user's ID from admin list.

        **Noteworthy:** Since this list is very important for the bot's operation,
        several checks have been added here: if the list consists of one ID,
        it cancels the deletion, if the admin wants to delete himself,
        he is asked to confirm the action

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            user_id (str): User's ID to remove from admins
        """
        if int(user_id) == ctx.author.id and users.is_user_admin(user_id):
            if len(database.get_data(
                'mainDB',
                False,
                'SELECT admins_id FROM admin_list'
            )) == 1:
                await ctx.reply('Вы единственный админ бота. '
                                'Управление ботом будет затруднено, '
                                'если список админов будет пуст, '
                                'поэтому я отменяю удаление')
            else:
                ask_msg = await ctx.reply('Вы уверены что хотите убрать себя?'
                                          ' (Да/Нет)')
                try:
                    wait_msg = await self.client.wait_for('message', timeout=15)
                except asyncio.TimeoutError:
                    await ask_msg.edit(content='Похоже вы не решились с выбором. '
                                               'Я отменил удаление вас из списка')
                else:
                    if wait_msg.content.lower() in ['да', 'ок', 'давай']:
                        database.modify_data(
                            'mainDB',
                            'DELETE FROM admin_list WHERE admins_id = ?',
                            user_id
                        )
                        await ask_msg.edit(content='Я удалил вас из админов :(')
                    elif wait_msg.content.lower() in ['не', 'нет', 'неа']:
                        await ask_msg.edit(content='Удаление было отменено')
                    else:
                        await ask_msg.edit(content='Вы ответили как-то иначе, '
                                                   'удаление было отменено')
        else:
            if not users.is_user_admin(user_id):
                await ctx.reply('Данный пользователь не является админом')
            else:
                database.modify_data(
                    'mainDB',
                    'DELETE FROM admin_list WHERE admins_id = ?',
                    user_id
                )
                await ctx.reply('Я успешно удалил такого админа')


def setup(client):
    client.add_cog(ManageAdmins(client))
