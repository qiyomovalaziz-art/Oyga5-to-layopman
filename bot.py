import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name  # ← Foydalanuvchi ismini olish
    await update.message.reply_text(
        f"Assalomu alaykum, {user_name}! 🤖\n"
        "Botga xush kelibsiz!\n\n"
        "Bu bot orqali siz savollaringizga tez va aniq javob olishingiz mumkin. ✍️\n"
        "Marhamat, savolingizni yozing 🙂"
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    user_name = update.effective_user.first_name

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Siz {user_name} ismli foydalanuvchiga muloyim va tushunarli javob beradigan yordamchisiz."},
            {"role": "user", "content": user_msg}
        ]
    )

    answer = response.choices[0].message.content
    await update.message.reply_text(answer)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
