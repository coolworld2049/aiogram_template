import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import ITEMS_PER_PAGE, MESSAGE_DELAY
from core import dispatcher, bot
from bot.filters.callback_filters import pagination_cb, back_cb
from bot.keyboards.user.common.common_inline_kb import main_menu_message_IK
from bot.states.PagionationStates import PaginationStates
from bot.utils.chat_mgmt import _delete_message, save_message, get_last_message


def reg_pagination_handlers():
    dispatcher.register_message_handler(step_state_message_controller, state=PaginationStates.STEP)
    dispatcher.register_callback_query_handler(next_step, pagination_cb.filter(way='next'),
                                               state=PaginationStates.STEP)
    dispatcher.register_callback_query_handler(back_step, pagination_cb.filter(way='back'),
                                               state=PaginationStates.STEP)
    dispatcher.register_callback_query_handler(stop_step, pagination_cb.filter(way='stop'),
                                               state=PaginationStates.STEP)


async def answer_with_pagination(user_id: int, menu_page_shift: int, state: FSMContext = None):
    """
    :param user_id:
    :param menu_page_shift: int
    :param state: FSMContext
    :return:
    """
    if state:
        state_data = await state.get_data()
    else:
        state_data = await dispatcher.current_state(chat=user_id, user=user_id).get_data()
    res: list[dict] = state_data['prepared_messages']
    current_page_index = state_data['page_index']
    real_user_id = state_data['user_id']
    back_callback = state_data['back_callback']
    contact_text = state_data['contact_text']

    new_page_index = current_page_index + menu_page_shift
    if new_page_index < 0 or new_page_index > len(res) / ITEMS_PER_PAGE:
        new_page_index = current_page_index
    if state:
        async with state.proxy() as data:
            data['page_index'] = new_page_index
    else:
        async with dispatcher.current_state(chat=real_user_id, user=real_user_id).proxy() as data:
            data['page_index'] = new_page_index
    msgs_list = []
    index = new_page_index * ITEMS_PER_PAGE
    iterable = res[index:index + ITEMS_PER_PAGE]
    first_msg_id = int(await get_last_message(user_id)) + 1
    reply_markup = None
    for i, item in enumerate(iterable):
        await asyncio.sleep(MESSAGE_DELAY)
        if item['reply_markup']:
            ik: list[dict] | None = item['reply_markup']['inline_keyboard'] if len(
                item['reply_markup']['inline_keyboard']) > 0 else None
            if ik:
                for k in ik:
                    k[0]['callback_data'] += f"_{first_msg_id}-{first_msg_id + len(iterable)}"
                reply_markup = InlineKeyboardMarkup(inline_keyboard=ik)
            _msg = await bot.send_message(real_user_id, item['text'], parse_mode=item['parse_mode'],
                                          reply_markup=reply_markup)
        else:
            _msg = await bot.send_message(real_user_id, item['text'], parse_mode=item['parse_mode'])
        if i == 0:
            msgs_list.append(_msg.message_id)
        if i == len(iterable) - 1:
            msgs_list.append(_msg.message_id)
    msg_ids = "-".join(map(str, msgs_list))
    await dispatcher.current_state(chat=real_user_id, user=real_user_id).update_data({'msgs_ids': msg_ids})

    IK_nav = InlineKeyboardMarkup(row_width=2)
    next_ = InlineKeyboardButton(text=">>", callback_data=pagination_cb.new(way='next'))
    curr = InlineKeyboardButton(text=f'страница {new_page_index + 1}/{len(res) // ITEMS_PER_PAGE + 1}',
                                callback_data="...")
    _back = InlineKeyboardButton(text="<<", callback_data=f'_back-step_{msg_ids}')
    IK_nav.row(_back, curr, next_)
    if back_callback:
        stop = InlineKeyboardButton(text='👈 Назад', callback_data=pagination_cb.new(way='stop'))
        menu = InlineKeyboardButton(text='👈️ В меню', callback_data=back_cb.new(to='menu', msg_ids='None'))
        IK_nav.row(stop, menu)
    text = f"*Объявлений*: {len(res)}. *Страниц*: {len(res) // ITEMS_PER_PAGE + 1}"
    text += contact_text if contact_text else ''
    message = await bot.send_message(real_user_id, text, parse_mode=types.ParseMode.MARKDOWN, reply_markup=IK_nav)
    await save_message(user_id, message.message_id)


@dispatcher.message_handler(state=PaginationStates.STEP)
async def step_state_message_controller(message: types.Message, state: FSMContext):
    async with state.proxy():
        if message.text != '/start' or message.text.startswith('/'):
            try:
                data = await state.get_data()
                if data['msgs_ids']:
                    await _delete_message(message.from_user.id, data['msgs_ids'])
            except KeyError:
                pass
            await state.finish()
            await main_menu_message_IK(message.from_user.id)


async def step_state_callback_controller(callback_query: types.CallbackQuery, state: FSMContext):
    cb = str(callback_query.data).split('_')[1]
    if cb not in ['next-step', 'back-step', 'stop-step']:
        msg_ids = callback_query.data.split('_')[-1]
        if msg_ids:
            await callback_query.message.delete()
            await _delete_message(callback_query.from_user.id, msg_ids, MESSAGE_DELAY)
        else:
            await callback_query.message.delete()
        await state.finish()
        await main_menu_message_IK(callback_query.from_user.id)


@dispatcher.callback_query_handler(pagination_cb.filter(way='next'), state=PaginationStates.STEP)
async def next_step(callback_query: types.CallbackQuery, state: FSMContext):
    await asyncio.sleep(0.3)
    state_data = await state.get_data()
    res: list[dict] = state_data['prepared_messages']
    if len(res) > ITEMS_PER_PAGE:
        await step_state_callback_controller(callback_query, state)
        msg_ids = callback_query.data.split('_')[-1]
        if msg_ids:
            await callback_query.message.delete()
            await _delete_message(callback_query.from_user.id, msg_ids, MESSAGE_DELAY)
        else:
            await callback_query.message.delete()

        await answer_with_pagination(callback_query.from_user.id, +1, state)


@dispatcher.callback_query_handler(pagination_cb.filter(way='back'), state=PaginationStates.STEP)
async def back_step(callback_query: types.CallbackQuery, state: FSMContext):
    await asyncio.sleep(0.3)
    state_data = await state.get_data()
    res: list[dict] = state_data['prepared_messages']
    if len(res) > ITEMS_PER_PAGE:
        await step_state_callback_controller(callback_query, state)
        msg_ids = callback_query.data.split('_')[-1]
        if msg_ids:
            await callback_query.message.delete()
            await _delete_message(callback_query.from_user.id, msg_ids, MESSAGE_DELAY)
        else:
            await callback_query.message.delete()
        await answer_with_pagination(callback_query.from_user.id, -1, state)


@dispatcher.callback_query_handler(pagination_cb.filter(way='stop'), state=PaginationStates.STEP)
async def stop_step(callback_query: types.CallbackQuery, state: FSMContext):
    await asyncio.sleep(0.3)
    await step_state_callback_controller(callback_query, state)
    msg_ids = callback_query.data.split('_')[-1]
    if msg_ids:
        await callback_query.message.delete()
        await _delete_message(callback_query.from_user.id, msg_ids, MESSAGE_DELAY)
    else:
        await callback_query.message.delete()
    await state.finish()
    spl = callback_query.data.split('_')[0]
    if spl is ...:
        pass
    elif spl == 'back-to-menu':
        await main_menu_message_IK(callback_query.from_user.id)
    elif spl is ...:
        pass
    elif spl is ...:
        pass
