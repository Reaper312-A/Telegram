from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler, MessageHandler, filters
from config import ADMIN_ID, logger, CHANNEL_USERNAME
import database
import keyboards

async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME, 
            user_id=user_id
        )
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"Ошибка проверки подписки для {user_id}: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    # Проверяем подписку
    if not await check_subscription(user_id, context):
        await update.message.reply_text(
            "❌ Для использования бота подпишитесь на канал:\n"
            f"👉 {CHANNEL_USERNAME}\n\n"
            "После подписки нажмите /start снова.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Подписаться", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
            ])
        )
        return
    
    database.add_user(user_id)
    await update.message.reply_text(
        "✅ Спасибо за подписку! Выберите действие:",
        reply_markup=keyboards.main_menu_keyboard()
    )
    
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("У вас нет прав для выполнения этой команды.")
        return

    await update.message.reply_text(
        "📤 Отправьте контент для рассылки:\n\n"
        "1. Фото + подпись (формат ниже)\n"
        "2. Или просто текст (аналогичный формат)\n\n"
        "Формат:\n"
        "Многострочное описание (можно с переносами)\n"
        "===Кнопка===\n"
        "Текст кнопки\n"
        "https://example.com\n\n"
        "Пример:\n"
        "Привет! Это тестовая рассылка...\n"
        "===Кнопка===\n"
        "Перейти\n"
        "https://example.com"
    )

async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        return

    success = 0
    failed = []
    users = database.get_all_users()
    total_users = len(users)

    try:
        if update.message.photo:
            photo = update.message.photo[-1].file_id
            caption = update.message.caption

            if not caption or "===Кнопка===" not in caption:
                await update.message.reply_text("❌ Используйте формат с разделителем ===Кнопка===")
                return

            parts = caption.split("===Кнопка===")
            description = parts[0].strip()
            button_part = parts[1].strip().split('\n')

            if len(button_part) < 2:
                await update.message.reply_text("❌ Неверный формат кнопки. Нужно:\nТекст кнопки\nURL")
                return

            button_text = button_part[0].strip()
            button_url = button_part[1].strip()

            if not button_url.startswith(('http://', 'https://')):
                await update.message.reply_text("❌ URL должен начинаться с http:// или https://")
                return

            keyboard = [[InlineKeyboardButton(button_text, url=button_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            for user in users:
                try:
                    await context.bot.send_photo(
                        chat_id=user,
                        photo=photo,
                        caption=description,
                        reply_markup=reply_markup,
                        parse_mode="Markdown"
                    )
                    success += 1
                except Exception as e:
                    failed.append(user)
                    logger.error(f"Ошибка отправки пользователю {user}: {e}")

        else:
            text = update.message.text

            if not text or "===Кнопка===" not in text:
                await update.message.reply_text("❌ Используйте формат с разделителем ===Кнопка===")
                return

            parts = text.split("===Кнопка===")
            description = parts[0].strip()
            button_part = parts[1].strip().split('\n')

            if len(button_part) < 2:
                await update.message.reply_text("❌ Неверный формат кнопки. Нужно:\nТекст кнопки\nURL")
                return

            button_text = button_part[0].strip()
            button_url = button_part[1].strip()

            if not button_url.startswith(('http://', 'https://')):
                await update.message.reply_text("❌ URL должен начинаться с http:// или https://")
                return

            keyboard = [[InlineKeyboardButton(button_text, url=button_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            for user in users:
                try:
                    await context.bot.send_message(
                        chat_id=user,
                        text=description,
                        reply_markup=reply_markup,
                        parse_mode="Markdown"
                    )
                    success += 1
                except Exception as e:
                    failed.append(user)
                    logger.error(f"Ошибка отправки пользователю {user}: {e}")

        stats_message = (
            f"📊 Статистика рассылки:\n\n"
            f"• Всего пользователей: {total_users}\n"
            f"• Успешно отправлено: {success}\n"
            f"• Не удалось отправить: {len(failed)}\n"
            f"• Процент успеха: {round(success/total_users*100 if total_users > 0 else 0, 2)}%"
        )

        if failed:
            stats_message += f"\n\nСписок ID, кому не отправилось:\n{', '.join(map(str, failed[:50]))}"
            if len(failed) > 50:
                stats_message += f"\n...и еще {len(failed)-50} пользователей"

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=stats_message
        )

    except Exception as e:
        logger.error(f"Ошибка в рассылке: {e}")
        await update.message.reply_text(f"❌ Ошибка при рассылке: {str(e)}")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'start_bybit':
        await query.edit_message_text("Выберите одну из кнопок:", reply_markup=keyboards.bybit_menu_keyboard())
    elif query.data == 'bybit_referral':
        await query.edit_message_text("Выберите одну из кнопок:", reply_markup=keyboards.referral_menu_keyboard())
    elif query.data == 'main_learn':
        await query.edit_message_text("Выберите одну из кнопок:", reply_markup=keyboards.learn_menu_keyboard())
    elif query.data == 'learn_basics':
        await query.edit_message_text("Выберите одну из кнопок:", reply_markup=keyboards.basics_menu_keyboard())
    elif query.data == 'learn_spot':
        await query.edit_message_text("Выберите одну из кнопок:", reply_markup=keyboards.spot_menu_keyboard())
    elif query.data == 'learn_derivatives':
        await query.edit_message_text("Выберите одну из кнопок:", reply_markup=keyboards.derivatives_menu_keyboard())
    elif query.data == 'main_about':
        await query.edit_message_text(
            "🤖 **Бесплатный бот для обучения трейдингу на Bybit**\n\n"
            "Привет! Этот бот создан для тех, кто хочет освоить трейдинг на криптовалютах, но не готов переплачивать за курсы или нарваться на 'гуру', которые только обещают золотые горы, а на деле дают воду.\n\n"
            "Я сам когда-то начинал с нуля и знаю, как сложно найти **честную и полезную информацию** бесплатно. Вокруг одни пиздаболы, которые наживаются на новичках. Поэтому я решил сделать этот бот — чтобы ты мог учиться без лишних трат и обмана.\n\n"
            "### Что внутри?\n"
            "✅ **Основы трейдинга**: от создания аккаунта на Bybit до понимания графиков и ордеров.\n"
            "✅ **Практические стратегии**: проверенные подходы для торговли на разных таймфреймах.\n"
            "✅ **Управление рисками**: как не потерять депозит и торговать с умом.\n"
            "✅ **Психология трейдинга**: как не поддаваться эмоциям и не сливать деньги.\n"
            "✅ **Актуальные тренды**: обзоры рынка, новости и полезные инсайты.\n\n"
            "### Почему бесплатно?\n"
            "Потому что я верю, что знания должны быть доступны каждому. Не нужно платить тысячи за базовые курсы, чтобы начать разбираться в трейдинге. Здесь ты получишь всё необходимое, чтобы стартовать и развиваться.\n\n"
            "🚀 **Твой путь к успеху в трейдинге начинается здесь!**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data='main_back')]]),
            parse_mode="Markdown"
        )
    elif query.data == 'main_other':
        await query.edit_message_text("Выберите одну из кнопок:", reply_markup=keyboards.other_menu_keyboard())
    elif query.data == 'other_thanks':
        await query.edit_message_text("Выберите одну из кнопок:", reply_markup=keyboards.thanks_menu_keyboard())
    elif query.data == 'other_author':
        await query.edit_message_text(
            "Автор(менеджер): @The_CardinaI\n\n"
            "Писать по любым вопросам",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data='main_other')]])
        )
    elif query.data == 'other_ad':
        await query.edit_message_text(
            "Выберите рекламную опцию:",
            reply_markup=keyboards.ad_menu_keyboard()
        )
    elif query.data == 'other_materials':
        books_list = """
📚 *Топ-10 книг по трейдингу:*

1. _«Трейдер-инвестор»_ — Александр Элдер  
   Основы психологии и риск-менеджмента.

2. _«Дисциплинированный трейдер»_ — Марк Дуглас  
   Как контролировать эмоции.

3. _«Технический анализ рынков»_ — Джек Швагер  
   Классика для работы с графиками.

4. _«Воспоминания биржевого спекулянта»_ — Эдвин Лефевр  
   Философия трейдинга от легенды.

5. _«Японские свечи»_ — Стив Нисон  
   Полное руководство по свечным паттернам.

6. _«Алгоритмический трейдинг»_ — Эрнест Чан  
   Стратегии для Quant-трейдинга.

7. _«Путь черепах»_ — Куртис Фейс  
   История легендарного эксперимента.

8. _«Справочник по фьючерсам»_ — Джек Швагер  
   Производные инструменты.

9. _«Черный лебедь»_ — Нассим Талеб  
   Как работать с непредсказуемыми событиями.

10. _«Сверхдоходность»_ — Андреас Клёнер  
    Современные рыночные стратегии.
    """
        await query.edit_message_text(
            books_list,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data='main_other')]
            ]),
            parse_mode="Markdown"
        )
    elif query.data == 'rent_bot':
        await query.edit_message_text(
            "🤖 Условия аренды бота:\n\n"
            "1. Бот проверяет подписку на ваш канал\n"
            "2. Полная настройка под ваши требования\n"
            "3. Техническая поддержка 24/7\n"
            "4. Статистика по кликам\n\n"
            "💵 Стоимость: 5000 руб./месяц\n\n"
            "📩 Для заказа: @The_CardinaI",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Назад", callback_data='other_ad')]
            ])
        )
    elif query.data == 'ad_mailing':
        try:
            await query.message.delete()
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=open('example.jpg', 'rb'),
                caption="""🎯 Пример рекламной рассылки

Ваше сообщение увидят все пользователи бота в таком формате:

━━━━━━━━━━━━━━━━
📢 Специальное предложение!
💰 Доходность до 15% в месяц
🛡️ Гарантия безопасности средств
⏳ Предложение ограничено
━━━━━━━━━━━━━━━━

✨ Нажмите кнопку ниже, чтобы получить персональные условия""",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📩 Перейти", url="https://t.me/The_CardinaI")],
                    [InlineKeyboardButton("🔙 Назад", callback_data='back_to_ad_menu')]
                ]),
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке примера рассылки: {e}")
            await query.answer("Произошла ошибка")

    elif query.data == 'back_to_ad_menu':
        try:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="Выберите рекламную опцию:",
                reply_markup=keyboards.ad_menu_keyboard()
            )
            await query.message.delete()
        except Exception as e:
            logger.error(f"Ошибка при возврате в меню: {e}")

    elif query.data == 'main_back':
        await query.edit_message_text("Выберите одну из кнопок:", reply_markup=keyboards.main_menu_keyboard())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    # Проверяем подписку (если нужно)
    if not await check_subscription(user_id, context):
        await update.message.reply_text(
            "❌ Для использования бота подпишитесь на канал:\n"
            f"👉 {CHANNEL_USERNAME}\n\n"
            "После подписки нажмите /start снова.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Подписаться", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
            ])
        )
        return
    
    
    
    # Если подписка есть (или проверка не требуется) — отправляем меню
    await update.message.reply_text(
        "Я вас не понял. Выберите функцию из меню:",
        reply_markup=keyboards.main_menu_keyboard()
    )