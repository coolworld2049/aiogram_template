import asyncio
import collections
import operator
from datetime import datetime

import matplotlib
import psutil
from aiogram import types
from aiogram.types import InputMedia, InputMediaPhoto, InputFile
from matplotlib import pyplot as plt

from bot import config
from core import bot
from services.journal.logger import logger
from services.server_statistics.config import server_stats_commands
from services.server_statistics.utils import async_wrapper

matplotlib.use("Agg")

poll_seconds = 300

memlist = []
graphstart = datetime.now()
axis_X = []
memorythreshold = 85


async def stats(user_id):
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
    await bot.send_message(user_id, reply, disable_web_page_preview=True)


async def memgraph(user_id):
    await bot.send_chat_action(user_id, 'typing')
    tmperiod = "Last %.2f hours" % ((datetime.now() - graphstart).total_seconds() / 3600)
    path = await async_wrapper(plotmemgraph, tmperiod)
    await bot.send_photo(user_id, InputFile(path))


def plotmemgraph(tmperiod):
    save_path = '/tmp/graph.png'
    plt.xlabel(tmperiod)
    plt.ylabel('% Used')
    plt.title('Memory Usage Graph')
    plt.text(0.1 * len(axis_X), memorythreshold + 2, 'Threshold: ' + str(memorythreshold) + ' %')
    memthresholdarr = []
    for _ in axis_X:
        memthresholdarr.append(memorythreshold)
    plt.plot(axis_X, memlist, 'b-', axis_X, memthresholdarr, 'r--')
    plt.axis([0, len(axis_X) - 1, 0, 100])
    plt.savefig(save_path)
    plt.close()
    return save_path


async def server_stats_run():
    global memlist
    tr = 0
    xx = 0
    for admin_id in config.ADMINS:
        await bot.send_message(admin_id, server_stats_commands)
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
                for admin_id in config.ADMINS:
                    await bot.send_message(admin_id, "CRITICAL! LOW MEMORY!\n" + memavail)
                    path = async_wrapper(plotmemgraph(tmperiod))
                    await bot.send_photo(admin_id, path)
        await asyncio.sleep(10)
        tr += 10
