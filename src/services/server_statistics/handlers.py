from aiogram import types

from bot import config
from core import dispatcher
from services.server_statistics.filters import command_stats, command_memgraph
from services.server_statistics.main import memgraph, stats


def reg_server_stats_handlers():
    dispatcher.register_message_handler(server_stats,
                                        commands=[command_stats.commands[0], command_memgraph.commands[0]])


@dispatcher.message_handler(commands=[command_stats.commands[0], command_memgraph.commands[0]])
async def server_stats(message: types.Message):
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        if message.get_command(pure=True) == command_stats.commands[0]:
            await stats(user_id)
        elif message.get_command(pure=True) == command_memgraph.commands[0]:
            await memgraph(user_id)
