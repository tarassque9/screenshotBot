from aiogram import Bot, Dispatcher, executor, types
import json
from screenshot import take_screenshot
import time
import re


with open('config.json') as secrets_file:
    secrets = json.load(secrets_file)


def get_secret(setting, secrets=secrets):
    return secrets[setting]


API_TOKEN = get_secret('token')

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
pattern = '((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)'


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Hi!\n"
        "I'm UrlScreenshotBot!\n"
        "Type site address and I'll give you a screenshot of the site."
        )


@dp.message_handler(regexp='.*?')
async def echo(message: types.Message):
    try:
        url = re.match(pattern, message.text).group(0)
    except Exception:
        await message.answer('Your URL adress not correct, please try again')
    else:
        filename = time.time()
        if not take_screenshot(url, filename):
            await message.answer('Somethink wrong with screenshot')
        with open(f'screenshots/{filename}.jpg', 'rb') as photo:
            await message.reply_photo(photo, caption='Your screeshot')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)