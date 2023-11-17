import pathlib
from telebot import TeleBot
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove

from app.markups import buy_mk
from config.config import Config, load_config
from app.markups import SellMarkups, SellMenu
from database import Session, CarDAL, CarMarkDAL, CarModelDAL, CarGearboxDAL, CarMark, CarModel, CarGearbox, Car

config: Config = load_config()

bot = TeleBot(config.tg_bot.token)

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
        bot.clear_step_handler(call.message)
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
