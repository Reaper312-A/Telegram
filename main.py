import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import logging
import database

from config import TOKEN, logger
from handlers import (
    start, broadcast, handle_broadcast,
    button_click, handle_message
)
from telegram.ext import filters

def main():
    database.init_db()
    application = Application.builder().token(TOKEN).build()

    # Добавляем хендлеры в правильном порядке
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(MessageHandler(filters.PHOTO & filters.CAPTION, handle_broadcast))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'===Кнопка==='), handle_broadcast))
    application.add_handler(CallbackQueryHandler(button_click))
    # Этот хендлер должен быть последним, так как он перехватывает все текстовые сообщения
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == '__main__':
    main()