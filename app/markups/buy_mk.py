from telebot import types


class BuyMarkups:
    @staticmethod
    def buy_start_menu(filters):
        menu = types.InlineKeyboardMarkup(row_width=1)
        not_selected = 'Не выбрано'
        # filters:
        # Марка:
        if filters.get('mark') is None:
            menu.add(types.InlineKeyboardButton(
                text=f"Марка: {not_selected}",
                callback_data="buy_select_mark")
            )
        else:
            menu.add(types.InlineKeyboardButton(
                text=f"Марка: {filters['mark']}",
                callback_data="buy_select_mark")
            )
            # Модель:
            menu.add(types.InlineKeyboardButton(
                text=f"Модель: {not_selected if filters.get('model') is None else filters['model']}",
                callback_data="buy_select_model")
            )
        # Тип коробки:
        menu.add(types.InlineKeyboardButton(
            text=f"Тип коробки: {not_selected if filters.get('gearbox') is None else filters['gearbox']}",
            callback_data="buy_select_gearbox")
        )
        # Минимальный пробег:
        menu.add(types.InlineKeyboardButton(
            text=f"Минимальный пробег: {not_selected if filters.get('min_mile') is None else filters['min_mile']}",
            callback_data="buy_select_min_mileage")
        )
        # Максимальный пробег:
        menu.add(types.InlineKeyboardButton(
            text=f"Максимальный пробег: {not_selected if filters.get('max_mile') is None else filters['max_mile']}",
            callback_data="buy_select_max_mileage")
        )
        # Минимальная цена:
        menu.add(types.InlineKeyboardButton(
            text=f"Минимальная цена: {not_selected if filters.get('min_price') is None else filters['min_price']}",
            callback_data="buy_select_min_price")
        )
        # Максимальная цена:
        menu.add(types.InlineKeyboardButton(
            text=f"Максимальная цена: {not_selected if filters.get('max_price') is None else filters['max_price']}",
            callback_data="buy_select_max_price")
        )
        if filters.get('mark') is not None:
            menu.add(types.InlineKeyboardButton(text="Показать варианты", callback_data="buy_show_cars"))
        menu.add(types.InlineKeyboardButton(text="Очистить фильтры", callback_data="buy_reset_filter"))
        menu.add(types.InlineKeyboardButton(text="Назад", callback_data="buy_back_to_start"))
        return menu

    @staticmethod
    def buy_mark_menu(marks: list):
        menu = types.InlineKeyboardMarkup(row_width=1)
        for item in marks:
            menu.add(types.InlineKeyboardButton(text=f"{item.name_mark}", callback_data=f"buy_selected_mark#{item.name_mark}"))
        menu.add(types.InlineKeyboardButton(text="Назад", callback_data="buy_back_to_buy"))
        return menu

    @staticmethod
    def buy_model_menu(models: list):
        menu = types.InlineKeyboardMarkup(row_width=1)
        for item in models:
            menu.add(types.InlineKeyboardButton(text=f"{item.name_model}",
                                                callback_data=f"buy_selected_model#{item.name_model}"))
        menu.add(types.InlineKeyboardButton(text="Назад", callback_data="buy_back_to_buy"))
        return menu

    @staticmethod
    def buy_gearbox_menu(tipes: list):
        menu = types.InlineKeyboardMarkup(row_width=1)
        for item in tipes:
            menu.add(types.InlineKeyboardButton(text=f"{item.gear_type}",
                                                callback_data=f"buy_selected_gearbox#{item.gear_type}"))
        menu.add(types.InlineKeyboardButton(text="Назад", callback_data="buy_back_to_buy"))
        return menu

    @staticmethod
    def buy_back_to_buy_menu():
        menu = types.InlineKeyboardMarkup(row_width=1)
        menu.add(types.InlineKeyboardButton(text="Назад", callback_data="buy_back_to_buy"))
        return menu

    @staticmethod
    def buy_cars_menu(cars: list):
        menu = types.InlineKeyboardMarkup(row_width=1)
        # mark.name_mark, name_model, price, gearbox, mileage
        for item in cars:
            menu.add(types.InlineKeyboardButton(text=f"{item[0]} {item[1]} | {item[4]} км | {item[2]}₽",
                                                callback_data=f"buy_selected_car#{item[0]}#{item[1]}#{item[2]}#{item[4]}#{item[3]}"))
        menu.add(types.InlineKeyboardButton(text="Назад", callback_data="buy_back_to_buy"))
        return menu

    @staticmethod
    def buy_back_from_car():
        menu = types.InlineKeyboardMarkup(row_width=1)
        menu.add(types.InlineKeyboardButton(text="Назад", callback_data="buy_back_to_buy"))
        return menu

class BuyTexts:
    @staticmethod
    def buy_spec_car(car):
        res = f'Марка: {car[1]}\n'
        res += f'Модель: {car[2].name_model}\n'
        res += f'Коробка: {car[3]}\n'
        res += f'Пробег: {car[0].mileage}\n'
        res += f'Цена: {car[0].price}₽\n'
        res += f'Номер владельца: {car[0].owner_mobile}'
        return res