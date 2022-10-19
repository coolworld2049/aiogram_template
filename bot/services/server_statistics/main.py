import asyncio
import collections
import io
import operator
from datetime import datetime

import matplotlib
import psutil
from aiogram import types
from aiogram.types import InputFile
from loguru import logger
from matplotlib import pyplot as plt

from bot import config
from bot.filters.callback_filters import server_stats_cb
from bot.strings.locale import navigation_BTN_back
from bot.utils.chat_mgmt import save_message, delete_previous_messages
from core import bot
from bot.services.server_statistics.filters import memgraph_cb, stats_cb
from bot.services.server_statistics.strings import server_stats_BTN_reload
from bot.services.server_statistics.utils import async_wrapper

matplotlib.use("Agg")

poll_seconds = 300

memlist = []
graphstart = datetime.now()
axis_X = []
memorythreshold = 85


async def stats(user_id):
    await delete_previous_messages(by_user_id=user_id)
    await bot.send_chat_action(user_id, 'typing')
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boottime = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    timedif = "Online for: %.1f Hours" % (((now - boottime).total_seconds()) / 3600)
    memtotal = "Total memory: %.2f GB " % (memory.total / 1000000000)
    memavail = "Available memory: %.2f GB" % (memory.available / 1000000000)
    memuseperc = "Used memory: " + str(memory.percent) + " %"
    diskused = "Disk used: " + str(disk.percent) + " %"
    pids = psutil.pids()
    pidsreply = ''
    procs = {}
    for pid in pids:
        p = psutil.Process(pid)
        try:
            pmem = p.memory_percent()
            if pmem > 0.5:
                if p.name() in procs:
                    procs[p.name()] += pmem
                else:
                    procs[p.name()] = pmem
        except Exception as e:
            logger.info(f"Exception {e}")
    sortedprocs = sorted(procs.items(), key=operator.itemgetter(1), reverse=True)
    for proc in sortedprocs:
        pidsreply += proc[0] + " " + ("%.2f" % proc[1]) + " %\n"
    reply = timedif + "\n" + memtotal + "\n" + memavail + "\n" + memuseperc + "\n" + diskused + "\n\n" + pidsreply
    IK = types.InlineKeyboardMarkup()
    IK.row(types.InlineKeyboardButton(navigation_BTN_back, callback_data=server_stats_cb.new()))
    IK.insert(types.InlineKeyboardButton(server_stats_BTN_reload, callback_data=stats_cb.new()))
    msg = await bot.send_message(user_id, reply, disable_web_page_preview=True, reply_markup=IK)
    await save_message(user_id, msg.message_id)


async def memgraph(user_id):
    await delete_previous_messages(by_user_id=user_id)
    await bot.send_chat_action(user_id, 'typing')
    tmperiod = "Last %.2f hours" % ((datetime.now() - graphstart).total_seconds() / 3600)
    path = await async_wrapper(plotmemgraph, tmperiod)
    IK = types.InlineKeyboardMarkup()
    IK.row(types.InlineKeyboardButton(navigation_BTN_back, callback_data=server_stats_cb.new()))
    IK.insert(types.InlineKeyboardButton(server_stats_BTN_reload, callback_data=memgraph_cb.new()))
    msg = await bot.send_photo(user_id, InputFile(path), reply_markup=IK)
    await save_message(user_id, msg.message_id)


def plotmemgraph(tmperiod):
    plt.xlabel(tmperiod)
    plt.ylabel('% Used')
    plt.title('Memory Usage Graph')
    plt.text(0.1 * len(axis_X), memorythreshold + 2, 'Threshold: ' + str(memorythreshold) + ' %')
    memthresholdarr = []
    for _ in axis_X:
        memthresholdarr.append(memorythreshold)
    plt.plot(axis_X, memlist, 'b-', axis_X, memthresholdarr, 'r--')
    plt.axis([0, len(axis_X) - 1, 0, 100])
    buffer = io.BytesIO()
    plt.savefig(buffer)
    buffer.seek(0)
    return buffer


async def SERVICE_server_stats():
    global memlist
    tr = 0
    xx = 0
    while True:
        if tr == poll_seconds:
            tr = 0
            memck = psutil.virtual_memory()
            mempercent = memck.percent
            if len(memlist) > 300:
                memq = collections.deque(memlist)
                memq.append(mempercent)
                memq.popleft()
                memlist = memq
                memlist = list(memlist)
            else:
                axis_X.append(xx)
                xx += 1
                memlist.append(mempercent)
            if mempercent > memorythreshold:
                memavail = "Available memory: %.2f GB" % (memck.available / 1000000000)
                graphend = datetime.now()
                tmperiod = "Last %.2f hours" % ((graphend - graphstart).total_seconds() / 3600)
                f_msg = int()
                for i, admin_id in enumerate(config.ADMINS):
                    await delete_previous_messages(by_user_id=admin_id)
                    path = async_wrapper(plotmemgraph(tmperiod))
                    msg = await bot.send_photo(admin_id, path, caption="CRITICAL! LOW MEMORY!\n" + memavail)
                    if i == 0:
                        f_msg = msg.message_id
                    elif i == len(config.ADMINS) - 1:
                        await save_message(admin_id, f"{f_msg}-{msg.message_id}")
        await asyncio.sleep(10)
        tr += 10
