from aiogram import types
from aiogram.dispatcher.filters import Command

from bot import config
from bot.models.role.role import UserRole
from bot.strings.locale import navigation_BTN_back
from bot.filters.callbacks import server_stats_cb, back_cb
from bot.utils.chat_mgmt import delete_previous_messages, save_message
from core import dispatcher, bot
from bot.services.server_statistics.strings import server_stats_commands_TEXT, server_stats_server_resources, \
    server_stats_memory_usage
from bot.services.server_statistics.filters import stats_cb, memgraph_cb
from bot.services.server_statistics.main import memgraph, stats

server_stats_command = Command('server')


def reg_server_statistics_handlers():
    dispatcher.register_callback_query_handler(stats_hd, stats_cb.filter())
    dispatcher.register_callback_query_handler(memgraph_hd, memgraph_cb.filter())
    dispatcher.register_callback_query_handler(server_stats_cb_hd, server_stats_cb.filter())
    dispatcher.register_message_handler(server_stats_msg_hd, server_stats_command)


@dispatcher.callback_query_handler(stats_cb.filter())
async def stats_hd(message: types.Message):
    await delete_previous_messages(tgtype=message)
    await stats(message.from_user.id)


@dispatcher.callback_query_handler(memgraph_cb.filter())
async def memgraph_hd(message: types.Message):
    await delete_previous_messages(tgtype=message)
    await memgraph(message.from_user.id)


async def _server_stats(tgtype: types.CallbackQuery | types.Message):
    if tgtype.from_user.id in config.ADMINS:
        await delete_previous_messages(tgtype=tgtype)
        btn_stats_hd = types.InlineKeyboardButton(server_stats_server_resources, callback_data=stats_cb.new())
        btn_memgraph_hd = types.InlineKeyboardButton(server_stats_memory_usage, callback_data=memgraph_cb.new())
        btn_back = types.InlineKeyboardButton(navigation_BTN_back,
                                              callback_data=back_cb.new(to=UserRole.ADMIN, msg_ids='None'))
        IK = types.InlineKeyboardMarkup()
        IK.add(btn_stats_hd, btn_memgraph_hd)
        IK.row(btn_back)
        msg = await bot.send_message(tgtype.from_user.id, server_stats_commands_TEXT, reply_markup=IK)
        await save_message(tgtype.from_user.id, msg.message_id)


@dispatcher.callback_query_handler(server_stats_cb.filter())
async def server_stats_cb_hd(callback_query: types.CallbackQuery):
    await _server_stats(callback_query)


@dispatcher.message_handler(server_stats_command)
async def server_stats_msg_hd(message: types.Message):
    await _server_stats(message)
