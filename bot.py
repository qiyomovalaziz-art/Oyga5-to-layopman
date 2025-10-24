import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# .env dagi kalitlarni yuklash
load_dotenv()

TELEGRAM_TOKEN = ("8280569385:AAHORjKjv3IGAT6G_EC7sZKu8UFlzLWP_Hc")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(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)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum 😊\nSavolingizni yozing, men javob beraman!")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sen foydalanuvchiga yordam beruvchi o‘zbekcha AI botsan."},
                {"role": "user", "content": user_msg}
            ]
        )

        answer = response.choices[0].message.content
        await update.message.reply_text(answer)

    except Exception as e:
        print("Xato:", e)
        await update.message.reply_text("⚠️ Xatolik yuz berdi. Keyinroq qayta urinib ko‘ring.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
