import pathlib
from telebot import TeleBot
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove

from config.config import Config, load_config
from app.markups import SellMarkups, SellMenu
from database import Session, CarDAL

config: Config = load_config()

bot = TeleBot(config.tg_bot.token)


@bot.message_handler(commands=['start'])
def process_start_command(message: Message) -> None:
    bot.send_message(chat_id=message.chat.id, text=SellMarkups.commands['/start'])


@bot.message_handler(commands=['sell'])
def process_sell_command(message: Message) -> None:
    bot.send_message(chat_id=message.chat.id, text=SellMarkups.commands['/sell'], reply_markup=SellMenu.sell_car())


@bot.callback_query_handler(func=lambda call: call.data == 'ToSell')
def process_to_sell(call: CallbackQuery) -> None:
    bot.register_next_step_handler(
        message=bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=SellMarkups.static['fill_mark'], reply_markup=SellMenu.reset()),
        callback=step_fill_mark, message_id_to_free_menu=call.message.message_id)


def step_fill_mark(message: Message, message_id_to_free_menu: int) -> None:
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id_to_free_menu, reply_markup=None)
    bot.register_next_step_handler(
        message=(new_message := bot.send_message(
            chat_id=message.chat.id, text=SellMarkups.static['fill_model'], reply_markup=SellMenu.reset())),
        callback=step_fill_model, mark=message.text, message_id_to_free_menu=new_message.message_id)


def step_fill_model(message: Message, mark: str, message_id_to_free_menu: int) -> None:
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id_to_free_menu, reply_markup=None)
    bot.register_next_step_handler(
        message=bot.send_message(
            chat_id=message.chat.id, text=SellMarkups.static['choose_gear_type'],
            reply_markup=SellMenu.choose(['automatic', 'mechanika', 'reset'])),
        callback=step_choose_gear_type, mark=mark, model=message.text)


def step_choose_gear_type(message: Message, mark: str, model: str) -> None:

    if message.text == SellMarkups.static['reset']:
        reset_filling(message=message)
        return

    bot.register_next_step_handler(
        message=bot.send_message(
            chat_id=message.chat.id, text=SellMarkups.static['choose_fuel_type'],
            reply_markup=SellMenu.choose(['petrol', 'solyara', 'reset'])),
        callback=step_choose_fuel_type, mark=mark, model=model, gear_type=message.text)


def step_choose_fuel_type(message: Message, mark: str, model: str, gear_type: str) -> None:

    if message.text == SellMarkups.static['reset']:
        reset_filling(message=message)
        return

    bot.register_next_step_handler(
        message=bot.send_message(
            chat_id=message.chat.id, text=SellMarkups.static['choose_condition'],
            reply_markup=SellMenu.choose(['factory_new', 'ponoshennoe', 'zakalennoe_v_boyah', 'reset'])),
        callback=step_choose_condition, mark=mark, model=model, gear_type=gear_type, fuel_type=message.text)


def step_choose_condition(message: Message, mark: str, model: str, gear_type: str, fuel_type: str) -> None:

    if message.text == SellMarkups.static['reset']:
        reset_filling(message=message)
        return

    bot.register_next_step_handler(
        message=(new_message := bot.send_message(
            chat_id=message.chat.id, text=SellMarkups.static['fill_hoursepower'], reply_markup=SellMenu.reset())),
        callback=step_fill_hoursepower, mark=mark, model=model, gear_type=gear_type, fuel_type=fuel_type,
        condition=message.text, message_id_to_free_menu=new_message.message_id)


def step_fill_hoursepower(message: Message, mark: str, model: str, gear_type: str, fuel_type: str, condition: str,
                          message_id_to_free_menu: int) -> None:
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id_to_free_menu, reply_markup=None)
    bot.register_next_step_handler(
        message=(new_message := bot.send_message(
            chat_id=message.chat.id, text=SellMarkups.static['fill_caparcity'], reply_markup=SellMenu.reset())),
        callback=step_fill_caparcity, mark=mark, model=model, gear_type=gear_type, fuel_type=fuel_type,
        condition=condition, hoursepower=message.text, message_id_to_free_menu=new_message.message_id)


def step_fill_caparcity(message: Message, mark: str, model: str, gear_type: str, fuel_type: str, condition: str,
                        hoursepower: int, message_id_to_free_menu: int) -> None:
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id_to_free_menu, reply_markup=None)
    bot.register_next_step_handler(
        message=(new_message := bot.send_message(
            chat_id=message.chat.id, text=SellMarkups.static['fill_year'], reply_markup=SellMenu.reset())),
        callback=step_fill_year, mark=mark, model=model, gear_type=gear_type, fuel_type=fuel_type, condition=condition,
        hoursepower=hoursepower, caparcity=message.text, message_id_to_free_menu=new_message.message_id)


def step_fill_year(message: Message, mark: str, model: str, gear_type: str, fuel_type: str, condition: str,
                   hoursepower: int, caparcity: str, message_id_to_free_menu: int) -> None:
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id_to_free_menu, reply_markup=None)
    bot.register_next_step_handler(
        message=(new_message := bot.send_message(
            chat_id=message.chat.id, text=SellMarkups.static['fill_mileage'], reply_markup=SellMenu.reset())),
        callback=step_fill_mileage, mark=mark, model=model, gear_type=gear_type, fuel_type=fuel_type,
        condition=condition, hoursepower=hoursepower, caparcity=caparcity, year=message.text,
        message_id_to_free_menu=new_message.message_id)


def step_fill_mileage(message: Message, mark: str, model: str, gear_type: str, fuel_type: str, condition: str,
                      hoursepower: int, caparcity: str, year: int, message_id_to_free_menu: int) -> None:
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id_to_free_menu, reply_markup=None)
    bot.register_next_step_handler(
        message=(new_message := bot.send_message(
            chat_id=message.chat.id, text=SellMarkups.static['fill_colour'], reply_markup=SellMenu.reset())),
        callback=step_fill_colour, mark=mark, model=model, gear_type=gear_type, fuel_type=fuel_type,
        condition=condition, hoursepower=hoursepower, caparcity=caparcity, year=year, mileage=message.text,
        message_id_to_free_menu=new_message.message_id)


def step_fill_colour(message: Message, mark: str, model: str, gear_type: str, fuel_type: str, condition: str,
                     hoursepower: int, caparcity: str, year: int, mileage: int, message_id_to_free_menu: int) -> None:
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id_to_free_menu, reply_markup=None)
    bot.register_next_step_handler(
        message=(new_message := bot.send_message(
            chat_id=message.chat.id, text=SellMarkups.static['fill_price'], reply_markup=SellMenu.reset())),
        callback=step_fill_price, mark=mark, model=model, gear_type=gear_type, fuel_type=fuel_type, condition=condition,
        hoursepower=hoursepower, caparcity=caparcity, year=year, mileage=mileage, colour=message.text,
        message_id_to_free_menu=new_message.message_id)


def step_fill_price(message: Message, mark: str, model: str, gear_type: str, fuel_type: str, condition: str,
                    hoursepower: int, caparcity: str, year: int, mileage: int, colour: str,
                    message_id_to_free_menu: int) -> None:
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id_to_free_menu, reply_markup=None)
    bot.register_next_step_handler(
        message=(new_message := bot.send_message(
            chat_id=message.chat.id, text=SellMarkups.static['fill_owner_mobile'], reply_markup=SellMenu.reset())),
        callback=step_fill_owner_mobile, mark=mark, model=model, gear_type=gear_type, fuel_type=fuel_type,
        condition=condition, hoursepower=hoursepower, caparcity=caparcity, year=year, mileage=mileage, colour=colour,
        price=message.text, message_id_to_free_menu=new_message.message_id)


def step_fill_owner_mobile(message: Message, mark: str, model: str, gear_type: str, fuel_type: str, condition: str,
                           hoursepower: int, caparcity: str, year: int, mileage: int, colour: str, price: int,
                           message_id_to_free_menu: int) -> None:
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id_to_free_menu, reply_markup=None)
    bot.register_next_step_handler(
        message=(new_message := bot.send_message(
            chat_id=message.chat.id, text=SellMarkups.static['load_photo'],  reply_markup=SellMenu.reset())),
        callback=step_load_photo, mark=mark, model=model, gear_type=gear_type, fuel_type=fuel_type, condition=condition,
        hoursepower=hoursepower, caparcity=caparcity, year=year, mileage=mileage, colour=colour, price=price,
        owner_mobile=message.text, message_id_to_free_menu=new_message.message_id)


def step_load_photo(message: Message, mark: str, model: str, gear_type: str, fuel_type: str, condition: str,
                    hoursepower: int, caparcity: str, year: int, mileage: int, colour: str, price: int,
                    owner_mobile: str, message_id_to_free_menu: int) -> None:
    if message.content_type == 'photo':
        downloaded_file = bot.download_file((file_info := bot.get_file(message.photo[-1].file_id)).file_path)
        with open(f'../../storage/{file_info.file_unique_id}.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id_to_free_menu, reply_markup=None)
        bot.send_message(
            chat_id=message.chat.id, text=SellMarkups.static['sell_successful'], reply_markup=ReplyKeyboardRemove())

        with Session.begin() as session:
            CarDAL(session).create_car(
                name_mark=mark, name_model=model, gear_type=gear_type, fuel_type=fuel_type, condition=condition,
                hoursepower=hoursepower, caparcity=caparcity, year=year, mileage=mileage, name_colour=colour,
                price=price, owner_mobile=owner_mobile, dir_photo=file_info.file_unique_id)


def reset_filling(message: Message):
    bot.clear_step_handler(message)
    bot.send_message(chat_id=message.chat.id, text=SellMarkups.static['after_reset'],
                     reply_markup=ReplyKeyboardRemove())


@bot.callback_query_handler(func=lambda call: call.data == 'reset')
def process_to_delete_message(call: CallbackQuery) -> None:
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    reset_filling(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'DeleteMessage')
def process_to_delete_message(call: CallbackQuery) -> None:
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: True)
def process_bin(call: CallbackQuery) -> None:
    bot.answer_callback_query(callback_query_id=call.id)


if __name__ == '__main__':
    bot.polling(none_stop=True)
