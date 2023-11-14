from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


class SellMarkups:
    commands = {
        '/start': 'Привет\n\nПродай машину /sell\nКупи машину /buy',
        '/sell': 'Ты можешь выставить здесь свою машину на продажу\n'
                 'Для этого нужно заполнить информацию\nи оставить контакт для покупателя'
    }
    static = {
        'del': '❌',
        'reset': 'Сбросить',
        'after_reset': 'Заполнение сброшено, возвращайтесь',
        'fill_mark': 'Введите марку автомобиля',
        'fill_model': 'Введите модель автомобиля',
        'choose_gear_type': 'Выберите тип коробки передач',
            'automatic': 'Автомат',
            'mechanika': 'Механика',
        'choose_fuel_type': 'Выберите тип топлива автомобиля',
            'petrol': 'Бензин',
            'solyara': 'Дизельное',
        'choose_condition': 'Выберите состояние авто',
            'factory_new': 'Новое',
            'ponoshennoe': 'Б/у',
            'zakalennoe_v_boyah': 'На запчасти',
        'fill_hoursepower': 'Введите мощность, л.с.',
        'fill_caparcity': 'Введите объём двигателя, л',
        'fill_year': 'Введите год вашего авто',
        'fill_mileage': 'Введите пробег авто, км',
        'fill_colour': 'Введите цвет авто',
        'fill_price': 'Введите цену продажи, руб',
        'fill_owner_mobile': 'Введите телефон для связи покупателя с вами\n\nНапример: 89018025060',
        'load_photo': 'Загрузите фото авто',
        'sell_successful': 'Ваш авто выставлен на продажу'
    }


class SellMenu:
    @staticmethod
    def sell_car():
        return InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text='К заполнению', callback_data='ToSell'),
            InlineKeyboardButton(text=SellMarkups.static['del'], callback_data='DeleteMessage')
        )

    @staticmethod
    def reset():
        return InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text=SellMarkups.static['reset'], callback_data='reset')
        )

    @staticmethod
    def choose(args):
        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
            *[KeyboardButton(text=SellMarkups.static[arg]) for arg in args]
        )
