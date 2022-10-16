from aiogram import types

from bot import config
from bot.answer_blanks.lang import navigation_BTN_back
from bot.filters.callback_filters import server_stats_cb, back_cb
from bot.utils.chat_mgmt import delete_previous_messages, save_message
from core import dispatcher, bot
from services.server_statistics.config import server_stats_commands_TEXT, server_stats_memory_usage, \
    server_stats_server_resources
from services.server_statistics.filters import stats_cb, memgraph_cb
from services.server_statistics.main import memgraph, stats


def reg_server_stats_handlers():
    dispatcher.register_callback_query_handler(stats_hd, stats_cb.filter())
    dispatcher.register_callback_query_handler(memgraph_hd, memgraph_cb.filter())
    dispatcher.register_callback_query_handler(server_stats, server_stats_cb.filter())


@dispatcher.callback_query_handler(stats_cb.filter())
async def stats_hd(message: types.Message):
    await delete_previous_messages(tgtype=message)
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        await stats(user_id)


@dispatcher.callback_query_handler(memgraph_cb.filter())
async def memgraph_hd(message: types.Message):
    await delete_previous_messages(tgtype=message)
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        await memgraph(user_id)


@dispatcher.callback_query_handler(server_stats_cb.filter())
async def server_stats(callback_query: types.CallbackQuery):
    await delete_previous_messages(tgtype=callback_query)
    btn_stats_hd = types.InlineKeyboardButton(server_stats_server_resources, callback_data=stats_cb.new())
    btn_memgraph_hd = types.InlineKeyboardButton(server_stats_memory_usage, callback_data=memgraph_cb.new())
    btn_back = types.InlineKeyboardButton(navigation_BTN_back, callback_data=back_cb.new(to='admin', msg_ids='None'))
    IK = types.InlineKeyboardMarkup()
    IK.add(btn_stats_hd, btn_memgraph_hd)
    IK.row(btn_back)
    msg = await bot.send_message(callback_query.from_user.id, server_stats_commands_TEXT, reply_markup=IK)
    await save_message(callback_query.from_user.id, msg.message_id)
