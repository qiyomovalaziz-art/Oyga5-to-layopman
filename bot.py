import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# ==== BU YERGA TOKENLARNI KIRITING ====
TELEGRAM_TOKEN = "8245974811:AAEkryr5_vYZ4m_1M8D56tIrViMe3Iwhmpc"
OPENAI_API_KEY = "BU_YERGA_OPENAI_API_KEYNI_YOZING"
# ======================================

openai.api_key = OPENAI_API_KEY


def start(update, context):
    update.message.reply_text("Assalomu alaykum! Savolingizni yozing, men javob beraman 🤖")


def ask_ai(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",   # AI modeli
            messages=[
                {"role": "system", "content": "Siz foydalanuvchining savollariga o'zbek tilida javob beradigan yordamchisiz."},
                {"role": "user", "content": question}
            ],
            max_tokens=300,
            temperature=0.8
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except:
        return "⚠️ Xatolik yuz berdi. Keyinroq urinib ko‘ring."


def message_handler(update, context):
    user_text = update.message.text
    update.message.reply_text("⏳ Javob tayyorlanyapti...")
    answer = ask_ai(user_text)
    update.message.reply_text(answer)


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, message_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
