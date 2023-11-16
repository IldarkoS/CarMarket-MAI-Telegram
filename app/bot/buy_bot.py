import telebot
import pathlib

import app.markups.buy_mk as buy_mk
from config import config
from database import CarDAL, CarMarkDAL, CarModelDAL, CarGearboxDAL, Session
from database.models import CarMark, CarModel, CarGearbox, Car

config = config.load_config()

bot = telebot.TeleBot(token=config.tg_bot.token)

filters: dict[int: dict[str: str]] = {}

@bot.message_handler(commands=['buy'])
def buy_start(message) -> None:
    if filters.get(message.chat.id) is None:
        filters[message.chat.id] = {
            'mark': None,
            'model': None,
            'gearbox': None,
            'min_mile': 0,
            'max_mile': 1000000,
            'min_price': 0,
            'max_price': 10000000
        }
    bot.send_message(
        chat_id=message.chat.id,
        text="Выберите фильтры:",
        reply_markup=buy_mk.BuyMarkups.buy_start_menu(filters[message.chat.id])
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('buy'))
def buy_callbacks(call) -> None:
    print(call.data)
    if call.data == "buy_select_mark":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        with Session.begin() as session:
            marks = CarMarkDAL(session).get_all_marks(CarMark)
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Выберите марку:",
            reply_markup=buy_mk.BuyMarkups.buy_mark_menu(marks)
        )
    if call.data == "buy_select_model":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        with Session.begin() as session:
            selected_mark = CarMarkDAL(session).get_mark_by_name(CarMark, filters[call.message.chat.id]['mark'])
            models = CarModelDAL(session).get_all_models(CarModel, selected_mark.id_mark)
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Выберите марку:",
            reply_markup=buy_mk.BuyMarkups.buy_model_menu(models)
        )
    if call.data == "buy_select_gearbox":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        with Session.begin() as session:
            gearboxes = CarGearboxDAL(session).get_all_gearboxes(CarGearbox)
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Выберите марку:",
            reply_markup=buy_mk.BuyMarkups.buy_gearbox_menu(gearboxes)
        )
    if call.data == "buy_select_min_mileage":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        msg = bot.send_message(
            chat_id=call.message.chat.id,
            text="Введите минимальный пробег:",
            reply_markup=buy_mk.BuyMarkups.buy_back_to_buy_menu()
        )
        bot.register_next_step_handler(msg, step_enter_values, "min", "mile")
    if call.data == "buy_select_max_mileage":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        msg = bot.send_message(
            chat_id=call.message.chat.id,
            text="Введите максимальный пробег:",
            reply_markup=buy_mk.BuyMarkups.buy_back_to_buy_menu()
        )
        bot.register_next_step_handler(msg, step_enter_values, "max", "mile")
    if call.data == "buy_select_min_price":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        msg = bot.send_message(
            chat_id=call.message.chat.id,
            text="Введите минимальную цену:",
            reply_markup=buy_mk.BuyMarkups.buy_back_to_buy_menu()
        )
        bot.register_next_step_handler(msg, step_enter_values, "min", "price")
    if call.data == "buy_select_max_price":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        msg = bot.send_message(
            chat_id=call.message.chat.id,
            text="Введите максимальную цену:",
            reply_markup=buy_mk.BuyMarkups.buy_back_to_buy_menu()
        )
        bot.register_next_step_handler(msg, step_enter_values, "max", "price")
    if call.data == "buy_reset_filter":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        filters[call.message.chat.id] = {
            'mark': None,
            'model': None,
            'gearbox': None,
            'min_mile': 0,
            'max_mile': 1000000,
            'min_price': 0,
            'max_price': 10000000
        }
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Выберите фильтры:",
            reply_markup=buy_mk.BuyMarkups.buy_start_menu(filters[call.message.chat.id])
        )
    if call.data.split('#')[0] == "buy_selected_mark":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        filters[call.message.chat.id]['mark'] = call.data.split('#')[1]
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Выберите фильтры:",
            reply_markup=buy_mk.BuyMarkups.buy_start_menu(filters[call.message.chat.id])
        )
    if call.data.split('#')[0] == "buy_selected_model":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        filters[call.message.chat.id]['model'] = call.data.split('#')[1]
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Выберите фильтры:",
            reply_markup=buy_mk.BuyMarkups.buy_start_menu(filters[call.message.chat.id])
        )
    if call.data.split('#')[0] == "buy_selected_gearbox":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        filters[call.message.chat.id]['gearbox'] = call.data.split('#')[1]
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Выберите фильтры:",
            reply_markup=buy_mk.BuyMarkups.buy_start_menu(filters[call.message.chat.id])
        )
    if call.data == "buy_back_to_buy":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Выберите фильтры:",
            reply_markup=buy_mk.BuyMarkups.buy_start_menu(filters[call.message.chat.id])
        )
    if call.data == "buy_show_cars":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        with Session.begin() as session:
            model = CarModelDAL(session).get_model_by_name(CarModel, filters[call.message.chat.id]['model'])
            gearbox = CarGearboxDAL(session).get_gearbox_by_type(CarGearbox, filters[call.message.chat.id]['gearbox'])
            raw_cars = CarDAL(session).select_cars(
                Car,
                id_model=model.id_model,
                id_gearbox=gearbox.id_gearbox,
                min_mile=filters[call.message.chat.id]['min_mile'],
                max_mile=filters[call.message.chat.id]['max_mile'],
                min_price=filters[call.message.chat.id]['min_price'],
                max_price=filters[call.message.chat.id]['max_price']
            )
            cars = []
            for item in raw_cars:
                mark = CarMarkDAL(session).get_mark_by_id(CarMark, model.id_mark)
                name_model = model.name_model
                price = item.price
                gearbox = gearbox.gear_type
                mileage = item.mileage
                cars.append([mark.name_mark, name_model, price, gearbox, mileage])
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Подходящие варианты:",
            reply_markup=buy_mk.BuyMarkups.buy_cars_menu(cars)
        )
    if call.data.split('#')[0] == "buy_selected_car":
        mark = call.data.split('#')[1]
        model = call.data.split('#')[2]
        price = call.data.split('#')[3]
        mileage = call.data.split('#')[4]
        gearbox = call.data.split('#')[5]
        with Session.begin() as session:
            model = CarModelDAL(session).get_model_by_name(CarModel, model)
            raw_car = CarDAL(session).select_spec_car(Car, model.id_model, price, mileage)
            car = [raw_car, mark, model, gearbox]
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        kor = pathlib.Path(__file__).parent.parent.parent
        bot.send_photo(
            chat_id=call.message.chat.id,
            photo=open(f'{kor}\storage\{car[0].dir_photo}.jpg', 'rb'),
            caption=buy_mk.BuyTexts.buy_spec_car(car),
            reply_markup=buy_mk.BuyMarkups.buy_back_from_car()
        )

def step_enter_values(message, type_, value) -> None:
    bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    filters[message.chat.id][f"{type_}_{value}"] = message.text
    bot.send_message(
        chat_id=message.chat.id,
        text="Выберите фильтры:",
        reply_markup=buy_mk.BuyMarkups.buy_start_menu(filters[message.chat.id])
    )


if __name__ == '__main__':
    bot.polling(none_stop=True)
