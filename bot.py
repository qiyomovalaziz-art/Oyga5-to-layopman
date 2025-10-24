from openai import OpenAI
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Tokens
TELEGRAM_TOKEN = "8280569385:AAFF5QyxoXtMw-Q0MlB4Y4ns5cbOynee3ww"
OPENAI_API_KEY = "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"

client = OpenAI(api_key=OPENAI_API_KEY)


def start(update, context):
    update.message.reply_text("Assalomu alaykum! Savolingizni yozing, men javob beraman 🤖")


def ask_ai(question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Siz foydalanuvchining savollariga o'zbek tilida javob beradigan yordamchisiz."},
                {"role": "user", "content": question}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Xatolik:", e)
        return "⚠️ Xatolik yuz berdi. Keyinroq urinib ko‘ring."


def message_handler(update, context):
    user_text = update.message.text
    update.message.reply_text("⏳ Javob tayyorlanmoqda...")
    answer = ask_ai(user_text)
    update.message.reply_text(answer)


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
