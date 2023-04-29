import argparse
import io
import os
import logging
import sys
import tempfile
import aiohttp
from pathlib import Path
from datetime import datetime as dt
import time

from pyrogram.client import Client
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from aiogram.types import ContentType, Message, File
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config.botSettings as config

from services.filesUtils import convert_to_wav, delete_file, unique_filename
from services.vosk import load_vosk_model, transcribe_vosk
from services.whisper import load_whisper_model, transcribe_whisper 

from states import VoiceRecognitionStates

parser = argparse.ArgumentParser(description="Python telegram bot")
parser.add_argument("-d", "--dev", help="Debug", action="store_true")
args = parser.parse_args(sys.argv[1:])

if args.dev:
    from config.dev.botToken import API_TOKEN, API_HASH, API_ID    

    logging.basicConfig(level=logging.DEBUG)
else:
    from config.prod.botToken import API_TOKEN, API_HASH, API_ID    

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.ERROR, filename = 'bot.log', encoding = 'UTF-8', datefmt = '%Y-%m-%d %H:%M:%S')


app = Client("speech_recognition_bot", api_id=API_ID, api_hash=API_HASH, bot_token=API_TOKEN)
bot = Bot(token = API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
temp_path = tempfile.gettempdir()
whisper_model = None
vosk_model = None

# Handlers
@dp.message_handler(CommandStart())
async def send_welcome(message: types.Message):
    logging.info(f'Starting chat with the user @{message.from_user.username} ({message.from_user.first_name} {message.from_user.last_name}, user_id = {message.from_id}), chat_id = {message.chat.id} ({message.chat.title})')
    reply_text = f'Hello {message.from_user.full_name}!\n\nYour Id: {message.from_id}\nThis chat Id: {message.chat.id}\n'
    await message.reply(reply_text)


@dp.message_handler(CommandHelp())
async def help(message: types.Message):
    reply_text = '''/start - start Bot
    /help - show this help    
    '''
    await message.reply(reply_text)


# Добавьте обработчик для выбора языка
@dp.message_handler(lambda message: message.text in ['English', 'Русский', 'Українська', 'Português'], state=VoiceRecognitionStates.language)
async def process_language_choice(message: types.Message, state: FSMContext):
    language = message.text
    lang_code = ''

    if language == 'English':
        lang_code = 'en'
    elif language == 'Русский':
        lang_code = 'ru'
    elif language == 'Українська':
        lang_code = 'uk'
    elif language == 'Português':
        lang_code = 'pt'

    async with state.proxy() as data:   
        global vosk_model
        global whisper_model
        try:
            _lang_code = data['language']
        except:
            _lang_code = None
        if _lang_code is None or not (_lang_code == lang_code):
            data['language'] = lang_code            
            if config.speech_recognition_lib == 'whisper':                                
                whisper_model = load_whisper_model(lang_code)        
            else:                
                vosk_model = load_vosk_model(lang_code)

        voice_data = data['voice_data']        
        file_audio_path = voice_data['file_audio_path']

        if config.speech_recognition_lib == 'whisper':
            text = transcribe_whisper(whisper_model, file_audio_path, language=lang_code)
        else:                        
            # Конвертирование файла в WAV 16000 Гц и одноканальный формат
            converted_file_path = convert_to_wav(file_audio_path)
            text = transcribe_vosk(converted_file_path, vosk_model)

        with io.BytesIO(text.encode()) as file:
            file.name = voice_data['file_name']
            await message.reply_document(file, caption=text[0:1023])

        await delete_file(file_audio_path)

    await state.finish()


@dp.message_handler(content_types=[ContentType.VOICE, ContentType.AUDIO])
async def handle_voice_message(message: Message, state: FSMContext):
    logging.info
    logging.info(f'Received voice message from @{message.from_user.username}')          
    
    if (message.content_type == ContentType.VOICE):
        file_id = message.voice.file_id
        file_type = ".ogg"        
    else:
        file_id = message.audio.file_id
        file_type = message.audio.file_name                              
        
    curr_date = dt.now().strftime('%Y%m%d%H%M%S') + str(message.message_id)
    file_name = unique_filename(curr_date, temp_path)
    file_note_name = file_name  + file_type + '.md'
    file_audio_name = file_name + file_type
    
    if (config.download_big_files == True):
        await handle_big_file(file_id=file_id, file_name=file_audio_name, path=temp_path)        
    else:
        file = await bot.get_file(file_id)
        await handle_file(file=file, file_name=file_audio_name, path=temp_path)        
    file_audio_path = os.path.join(temp_path, file_audio_name)

    # save file path in state FSM
    async with state.proxy() as data:
        data['voice_data'] = {            
            'file_name': file_note_name,
            'file_audio_path': file_audio_path
        }

    # Entering voice language
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['English', 'Русский', 'Українська', 'Português']
    keyboard.add(*buttons)
    await message.reply("Choose the language of the voice message:", reply_markup=keyboard)
    await VoiceRecognitionStates.language.set()
     


@dp.message_handler()
async def process_message(message: types.Message):
#    if message.chat.id != config.my_chat_id: return
    logging.info(f'Received text message from @{message.from_user.username}')   
    

# Functions
async def handle_file(file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)
    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")

async def handle_big_file(file_id, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)    
    async with app:            
        await app.download_media(file_id, file_name=f"{path}/{file_name}")            

async def download(url, session: aiohttp.ClientSession) -> str:
    async with session.get(url) as response:
        return await response.text()


if __name__ == '__main__':    
    while True:
        try:
            executor.start_polling(dp)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            time.sleep(5)
