import logging
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
from src.config import settings

logger = logging.getLogger(__name__)
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

async def send_review_post(chat_id: int, job_id: str, artifacts: list):
    text_lines = [f"Review ready for job: {job_id}"]
    for a in artifacts:
        text_lines.append(f"{a['name']}: {a['url']}")
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Re-run Review", callback_data=f"rerun:{job_id}")]])
    try:
        msg = await bot.send_message(chat_id=chat_id, text='\n'.join(text_lines), reply_markup=keyboard)
        return {"message_id": msg.message_id, "chat_id": msg.chat.id}
    except TelegramError as e:
        logger.exception("Failed to send telegram message: %s", e)
        raise

async def delete_message(chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except TelegramError as e:
        logger.warning("Failed to delete message: %s", e)

async def update_message(chat_id: int, message_id: int, text: str, keyboard=None):
    try:
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=keyboard)
    except TelegramError as e:
        logger.warning("Failed to update message: %s", e)
