import os
import base64
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    await update.message.reply_text(
        f"Assalomu alaykum {user_name}! 😊\n"
        "Botga xush kelibsiz!\n"
        "Bu bot orqali savollaringizga javob olishingiz mumkin ✍️🤖"
    )

# Matnli xabarlar uchun ChatGPT
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Sen foydalanuvchiga yordam beradigan aqlli yordamchisan."},
            {"role": "user", "content": user_msg}
        ]
    )

    answer = response.choices[0].message.content
    await update.message.reply_text(answer)

# Rasm yuborilsa – uni tahlil qilish
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    file_path = "/mnt/data/image.jpg"
    await file.download_to_drive(file_path)

    with open(file_path, "rb") as img:
        img_bytes = img.read()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Sen rasmni tahlil qilib tushuntiradigan yordamchisan."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Mana rasm. Uni tushuntirib ber."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                ]
            }
        ]
    )

    answer = response.choices[0].message.content
    await update.message.reply_text(answer)


# Matndan rasm yaratish
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text.replace("/rasm", "").strip()

    if not prompt:
        await update.message.reply_text("Rasm yasash uchun so‘z yozing.\nMasalan: /rasm kosmosda kit uchyapti")
        return

    await update.message.reply_text("⏳ Rasm yaratilmoqda, kuting...")

    img = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_url = img.data[0].url
    await update.message.reply_photo(image_url, caption="✅ Tayyor!")

# Botni ishga tushirish
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rasm", generate_image))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
