# Конфигурационные параметры бота
TOKEN = '8014498725:AAFcloekJ_XFM0Jte0CQaJFY-l5CETb8Slc'
ADMIN_ID = 1635179080
CHANNEL_USERNAME = "@Sygnalyy"

# Настройка логирования
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)
logger = logging.getLogger(__name__)