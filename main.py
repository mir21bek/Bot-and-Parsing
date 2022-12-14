from aiogram import Bot, executor, types, Dispatcher
import requests
from bs4 import BeautifulSoup
import logging
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '5960515236:AAFjwZtNAvCPA7ayod_ApWXKm14hUnX33Vo'


logging.basicConfig(level=logging.INFO)
#initialiing bot and dispatcher
bot = Bot(token=API_TOKEN)
#изменения бота
dp = Dispatcher(bot)

button_detail = InlineKeyboardButton('Подробнее', callback_data='detail')
button_detail1 = InlineKeyboardButton('Подробнее', callback_data='detail1')
button_detail2 = InlineKeyboardButton('Подробнее', callback_data='detail2')

geek_go = InlineKeyboardMarkup().add(button_detail)
geek_go1 = InlineKeyboardMarkup().add(button_detail1)
geek_go2 = InlineKeyboardMarkup().add(button_detail2)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    req = requests.get("https://kloop.kg/").content
    soup = BeautifulSoup(req, 'html.parser')
    div = soup.find_all('div', class_='elementor-post__text')
    image1 = div[5].find_previous('a', class_="elementor-post__thumbnail__link").find('img', class_="attachment-full")['src']
    image2 = div[6].find_previous('a', class_="elementor-post__thumbnail__link").find('img', class_="attachment-full")['src']
    image3 = div[7].find_previous('a', class_="elementor-post__thumbnail__link").find('img', class_="attachment-full")['src']
    await message.answer_photo(photo=image1, caption=f"{div[5].find_next('h3').find('a').text}", reply_markup = geek_go)
    await message.answer_photo(photo=image2, caption=f"{div[6].find_next('h3').find('a').text}", reply_markup = geek_go)
    await message.answer_photo(photo=image3, caption=f"{div[7].find_next('h3').find('a').text}", reply_markup = geek_go)


greet_kb = InlineKeyboardMarkup()


#отработка кнопок из callback_data
@dp.callback_query_handler()
async def process_callback(call: types.CallbackQuery):
    req = requests.get('https://kloop.kg/').content
    soup = BeautifulSoup(req, 'html.parser')
    news_str = ''
    news_href = soup.find_all('a', class_='elementor-post__thumbnail__link', href=True)

    if call.data == 'detail':

        news_req = requests.get(news_href[4]["href"]).content
        soup_news = BeautifulSoup(news_req, 'html.parser')
        news = soup_news.find_all('p', class_='stk-reset wp-exclude-emoji')
        header = soup_news.find('h1', class_='entry-title').text
        news_str += header+'\n'
        for i in news[1:6]:
            news_str += i.text+'\n'
        await bot.send_message(chat_id=call.from_user.id, text=f'{news_str}')

    elif call.data == 'detail1':

        news_req = requests.get(news_href[5]["href"]).content
        soup_news = BeautifulSoup(news_req, 'html.parser')
        news = soup_news.find_all('p', class_='stk-reset wp-exclude-emoji')
        header = soup_news.find('h1', class_='entry-title').text
        news_str += header + '\n'
        for i in news[1:6]:
            news_str += i.text+'\n'
        await bot.send_message(chat_id=call.from_user.id, text=f'{news_str}')

    elif call.data == 'detail2':

        news_req = requests.get(news_href[6]["href"]).content
        soup_news = BeautifulSoup(news_req, 'html.parser')
        news = soup_news.find_all('p', class_='stk-reset wp-exclude-emoji')
        header = soup_news.find('h1', class_='entry-title').text
        news_str += header + '\n'
        for i in news[1:6]:
            news_str += i.text+'\n'
        await bot.send_message(chat_id=call.from_user.id, text=f'{news_str}')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)