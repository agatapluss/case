
import telebot
import config_
import math
import datetime

bot = telebot.TeleBot(config_.bot_token)

def get_date_now():
    now = datetime.datetime.now()
    date_now =  datetime.datetime.strftime(now, "%d-%m-%Y")
    return date_now


def get_last_date():
    month_now = datetime.datetime.now().month
    any_day = datetime.date(2022, month_now, 1)
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    last_day_of_month = next_month - datetime.timedelta(days=next_month.day)
    return last_day_of_month.strftime("%d-%m-%Y")


def get_count_days():
    days_ = datetime.datetime.strptime(get_last_date(), "%d-%m-%Y")-datetime.datetime.strptime(get_date_now(), "%d-%m-%Y")
    return days_.days




@bot.message_handler(regexp='Я в консоли')
def print_me(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')
    markup.add(btn1)
    print(message.from_user.to_dict())
    text = f'Ты: {message.from_user.to_dict()}'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=['start'])
def admin_panel(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    text = f"""Добрый день, {message.from_user.full_name}! 
Сегодня {get_date_now()}
До конца отчётного периода осталовь {get_count_days()} дней.
Чтобы узнать подробную информацию по отдельному магазину,
нажмите на кнопку "Все магазины"
и выбирете интерисующий"""
    btn2 = telebot.types.KeyboardButton('Все магазины')
    markup.add(btn2)
    bot.send_message(message.chat.id, text, reply_markup=markup)


shops = config_.fake_databasee['shops']
count_in = 5
count_shops = len(shops)
all_lists  = math.ceil(count_shops/count_in)


@bot.message_handler(func=lambda call: True) 
def all_shops(call):
    text = f'Всего магазинов участвующих в акции: {count_shops}'
    if call.text == "Все магазины":
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for shop in shops[:count_in]:
            inline_markup.add(telebot.types.InlineKeyboardButton(text=f'Магазин: {shop["address"]}',
                                                                callback_data=f"shop_{shop['id']}"))
        inline_markup.add(
            telebot.types.InlineKeyboardButton(text="Вперёд",  callback_data="next"), 
            telebot.types.InlineKeyboardButton(text = f'{1}\{all_lists}',  callback_data='lists'))

        bot.send_message(call.chat.id, text, reply_markup=inline_markup)

@bot.callback_query_handler(func=lambda call: True)
def get_other_list(call):
    query_type = call.data.split('_')[0]  # получаем тип запроса
    if query_type == 'shop':
        user_id = call.data.split('_')[1]  # получаем айди магазина из нашей строки
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for shop in shops:
            if str(shop['id']) == user_id:
                inline_markup.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data='back'))
                bot.edit_message_text(text=f'Данные по магазину:\n'
                                           f'ID: {shop["id"]}\n'
                                           f'Адрес магазина: {shop["address"]}\n'
                                           f'Остаток подарков в магазине (без НЗ): {shop["balance"]}\n'
                                           f'Остаток НЗ : {shop["nz_balance"]}\n'
                                           f'ОБЩИЙ ОСТАТОК : {shop["balance"]+shop["nz_balance"]}\n'
                                           f'\n'
                                           f'Среднее кол-во подаренных подарков за месяц: {shop["avg"]}\n'
                                           f'Дней до конца месяца: {get_count_days()}'

                                                                                      ,
                                      chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=inline_markup)
                break
    
    elif query_type == "next":
        text = f'Всего магазинов участвующих в акции: {count_shops}'
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for shop in shops[count_in:2*count_in]: 
            inline_markup.add(
                telebot.types.InlineKeyboardButton(text=f'Магазин: {shop["address"]}',
                                                                callback_data=f"shop_{shop['id']}"))
        inline_markup.add(
            telebot.types.InlineKeyboardButton(text="Назад",  callback_data="back"),           
            telebot.types.InlineKeyboardButton(text = f'{all_lists}\{all_lists}',  callback_data='lists')
                        )
        bot.send_message(call.message.chat.id, text, reply_markup=inline_markup)

    elif query_type== "back":
        text = f'Всего магазинов участвующих в акции: {count_shops}'
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for shop in shops[:count_in]:  
            inline_markup.add(telebot.types.InlineKeyboardButton(text=f"Магазин: {shop['address']}",
                                                                callback_data=f"shop_{shop['id']}"))
        inline_markup.add(
            telebot.types.InlineKeyboardButton(text="Вперёд",  callback_data='next'),           
            telebot.types.InlineKeyboardButton(text = f'{1}\{all_lists}',  callback_data='lists'))
        bot.send_message(call.message.chat.id, text, reply_markup=inline_markup)

    elif query_type == "lists":
        text = 'Все листы:'
        inline_markup = telebot.types.InlineKeyboardMarkup()
        inline_markup.add(
            telebot.types.InlineKeyboardButton(text= '1 лист',  callback_data='back'),           
            telebot.types.InlineKeyboardButton(text ='2 лист',  callback_data='next'))
        bot.send_message(call.message.chat.id, text, reply_markup=inline_markup)

    
bot.infinity_polling()