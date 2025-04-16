from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Старт с Bybit", callback_data='start_bybit')],
        [InlineKeyboardButton("Обучение", callback_data='main_learn')],
        [InlineKeyboardButton("О боте", callback_data='main_about')],
        [InlineKeyboardButton("Прочее", callback_data='main_other')]
    ]
    return InlineKeyboardMarkup(keyboard)

def bybit_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("О Bybit", url='https://telegra.ph/O-Bybit-04-07')],
        [InlineKeyboardButton("Рефералка", callback_data='bybit_referral')],
        [InlineKeyboardButton("Условия программ", url='https://www.bybit.com/ru-RU/help-center/article/Bybit-Platform-Terms-and-Conditions')],
        [InlineKeyboardButton("Назад", callback_data='main_back')]
    ]
    return InlineKeyboardMarkup(keyboard)

def referral_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Реферальный код", url='https://www.bybit.com/invite?ref=PENZ3MW')],
        [InlineKeyboardButton("Как поменять реферала", url='https://telegra.ph/Smena-referala-04-07')],
        [InlineKeyboardButton("Назад", callback_data='start_bybit')]
    ]
    return InlineKeyboardMarkup(keyboard)

def learn_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Основы", callback_data='learn_basics')],
        [InlineKeyboardButton("Спот", callback_data='learn_spot')],
        [InlineKeyboardButton("Деривативы", callback_data='learn_derivatives')],
        [InlineKeyboardButton("Назад", callback_data='main_back')]
    ]
    return InlineKeyboardMarkup(keyboard)

def basics_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Термины и аббревиатуры", url='https://telegra.ph/Terminy-i-abbriviatury-04-07')],
        [InlineKeyboardButton("Торговые инструменты", url='https://telegra.ph/Rukovodstvo-po-torgovym-instrumentam-dlya-kriptotrejdinga-04-07')],
        [InlineKeyboardButton("Анализ рынка", url='https://telegra.ph/Analiz-rynka-04-07-2')],
        [InlineKeyboardButton("Торговые стратегии", url='https://telegra.ph/Torgovye-strategii-04-07')],
        [InlineKeyboardButton("Графики", url='https://telegra.ph/Grafiki-04-07')],
        [InlineKeyboardButton("Назад", callback_data='main_learn')]
    ]
    return InlineKeyboardMarkup(keyboard)

def spot_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Подробнее о спотах", url='https://telegra.ph/Spot-04-07-16')],
        [InlineKeyboardButton("Назад", callback_data='main_learn')]
    ]
    return InlineKeyboardMarkup(keyboard)

def derivatives_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Подробнее о деривативах", url='https://telegra.ph/Derivativy-04-07')],
        [InlineKeyboardButton("Назад", callback_data='main_learn')]
    ]
    return InlineKeyboardMarkup(keyboard)

def other_menu_keyboard():
    keyboard = [
        [  # Первый ряд: 2 кнопки
            InlineKeyboardButton("Отблагодарить", callback_data='other_thanks'),
            InlineKeyboardButton("Материалы", callback_data='other_materials')
        ],
        [  # Второй ряд: 2 кнопки
            InlineKeyboardButton("Автор(менеджер)", callback_data='other_author'),
            InlineKeyboardButton("Реклама", callback_data='other_ad')
        ],
        [  # Третий ряд: кнопка назад
            InlineKeyboardButton("Назад", callback_data='main_back')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def thanks_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("СПБ", url='https://bybit.com/spb')],
        [InlineKeyboardButton("Крипта", url='https://bybit.com/crypto')],
        [InlineKeyboardButton("Назад", callback_data='main_other')]
    ]
    return InlineKeyboardMarkup(keyboard)

def ad_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Аренда бота", callback_data='rent_bot')],
        [InlineKeyboardButton("Рекламная рассылка", callback_data='ad_mailing')],
        [InlineKeyboardButton("Назад", callback_data='main_other')]
    ]
    return InlineKeyboardMarkup(keyboard)