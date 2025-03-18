import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()

Bot_token = os.getenv('')
bot = Bot(token=Bot_token)