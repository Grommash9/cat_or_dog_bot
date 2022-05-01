import asyncio
import logging
import config
from aiogram import Bot
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from apscheduler.schedulers.asyncio import AsyncIOScheduler


bot = Bot(token=config.bot_token)
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, storage=storage, loop=loop)
scheduler = AsyncIOScheduler()