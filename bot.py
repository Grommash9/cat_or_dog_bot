import time

import aiogram
import numpy as np
from aiogram import types
from aiogram.types import ChatType, ParseMode
from aiogram.utils import executor
from keras_preprocessing.image import img_to_array, load_img
from get_results import resize_image, model
import config
from create_bot import dp, bot, scheduler
from PIL import Image
import io

@dp.message_handler(aiogram.filters.ChatTypeFilter(chat_type=ChatType.PRIVATE), commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=config.bot_texts['bot_start_text'],
                           parse_mode=ParseMode.HTML)


@dp.message_handler(aiogram.filters.ChatTypeFilter(chat_type=ChatType.PRIVATE), content_types=aiogram.types.ContentTypes.PHOTO)
async def get_new_photo_proccesing(message: types.Message):
    file_telegram_data = await bot.get_file(file_id=message.photo[-1]['file_id'])
    file = await bot.download_file(file_path=file_telegram_data['file_path'])
    img = Image.open(file)
    img = img.convert('RGB')
    img_array = img_to_array(img)
    img_resized, _ = resize_image(img_array, label=None)
    img_expended = np.expand_dims(img_resized, axis=0)
    prediction = model.predict(img_expended)[0][0]
    pred_label = 'Думаю на картинке кот' if prediction < 0.5 else 'Думаю на картинке собака'

    await bot.send_message(chat_id=message.from_user.id,
                           text=f"{pred_label} уверенность - {round(abs(prediction) * 10, 1)}%")



if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp)