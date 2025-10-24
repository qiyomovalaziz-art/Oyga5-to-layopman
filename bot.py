import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Tokenlar / API kalitlar
TELEGRAM_TOKEN = os.getenv("8280569385:AAHrAXpAae0uUyg_cSa08RUPRtsFjqK1_64")
OPENAI_API_KEY = os.getenv("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")

openai.api_key = OPENAI_API_KEY

def start(update, context):
    update.message.reply_text("Assalomu alaykum! Savolingizni yozing, men javob beraman 🤖")

def ask_ai(question: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Siz foydalanuvchining savollariga o‘zbek tilida javob beradigan yordamchisiz."},
                {"role": "user", "content": question}
            ],
            max_tokens=300,
            temperature=0.7
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        logger.error(f"OpenAI bilan muammo: {e}")
        return "⚠️ Xatolik yuz berdi. Keyinroq urinib ko‘ring."

def message_handler(update, context):
    user_text = update.message.text
    update.message.reply_text("⏳ Javob tayyorlanmoqda…")
    answer = ask_ai(user_text)
    update.message.reply_text(answer)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
