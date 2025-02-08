from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import json
import os
import asyncio

# Load or initialize subscriber list
SUBSCRIBERS_FILE = "subscribers.json"
try:
    with open(SUBSCRIBERS_FILE, "r") as file:
        subscribers = json.load(file)
except FileNotFoundError:
    subscribers = []

# Bot Token from Environment Variable
BOT_TOKEN = "8191521148:AAFwcbfFgGVTgZX6_HUa5ylkyD4ikWuDd64"

# Promo Message
PROMO_MESSAGE = "\U0001F525 BIG NEWS FOR STUDENTS! \U0001F525\n\n\U0001F680 Get an **EXCLUSIVE STUDENT DISCOUNT** on **ALL ONLINE PW COURSES!** \U0001F4DA✨\n\n\U0001F4A1 IIT-JEE | NEET | UPSC | GATE | DEFENCE | MBA | CA | SSC & More!\n\n\U0001F3AF **Use Coupon Code: ABHSIN0003**\n\U0001F4B0 **Save BIG on your learning journey!**\n\n\U0001F4E2 Don't miss out—grab this offer NOW! \U0001F3C6\n\U0001F4A8 **Limited time only! Share with friends!**\n\n\U0001F517 Enroll today & ace your exams! \U0001F680\U0001F525\n\n#PW #StudentDiscount #ExamPrep #BigSavings"

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if user_id not in subscribers:
        subscribers.append(user_id)
        with open(SUBSCRIBERS_FILE, "w") as file:
            json.dump(subscribers, file)
        await update.message.reply_text("✅ You have subscribed for updates!")
    else:
        await update.message.reply_text("You're already subscribed! ✅")
    
    await update.message.reply_text(PROMO_MESSAGE, parse_mode="Markdown")

async def broadcast(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id in subscribers:
        for user_id in subscribers:
            try:
                await context.bot.send_message(chat_id=user_id, text=PROMO_MESSAGE, parse_mode="Markdown")
            except Exception as e:
                print(f"Error sending message to {user_id}: {e}")
        await update.message.reply_text("✅ Broadcast sent to all subscribers!")
    else:
        await update.message.reply_text("❌ You're not authorized to use this command.")

async def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN is not set.")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))

    await app.run_polling()

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
