import os
from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ⚠️ ከታች ባለው ክፍት ቦታ ላይ የቦት Tokenዎን ያስገቡ
TOKEN = "8832259515:AAFvis_WHSXz9tEISCnJ3zALY6YRJt220gY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም! እባክዎን ፕሮፋይል የሚሆን ፎቶ ይላኩልኝ።")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ምስልዎ በመዘጋጀት ላይ ነው...")
    
    # 1. ተጠቃሚው የላከውን ፎቶ ማውረድ
    photo_file = await update.message.photo[-1].get_file()
    user_photo_path = "user_photo.jpg"
    await photo_file.download_to_drive(user_photo_path)

    # 2. ምስሎችን መክፈት
    user_img = Image.open(user_photo_path).convert("RGBA")
    frame_img = Image.open("frame.png").convert("RGBA")

    # 3. የፎቶውን መጠን ከፍሬሙ ጋር ማስተካከል
    user_img = user_img.resize(frame_img.size)

    # 4. ምስሎቹን ማዋሃድ (Overlay)
    final_img = Image.alpha_composite(user_img, frame_img)

    # 5. የተቀናበረውን ምስል ማስቀመጥ
    output_path = "result.png"
    final_img.convert("RGB").save(output_path)

    # 6. መልሶ ለተጠቃሚው መላክ
    await update.message.reply_photo(photo=open(output_path, 'rb'), caption="ምስልዎ ተዘጋጅቷል!")

    # 7. ጊዜያዊ ፋይሎችን ማጽዳት
    if os.path.exists(user_photo_path):
        os.remove(user_photo_path)
    if os.path.exists(output_path):
        os.remove(output_path)

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("ቦቱ ሥራ ጀምሯል...")
    app.run_polling()

if __name__== "__main__":
    main()