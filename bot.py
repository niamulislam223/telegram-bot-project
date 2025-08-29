from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, PollHandler
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set in environment variables!")

# Google Sheets Setup (optional)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = os.getenv("GOOGLE_CREDS_JSON")  # store JSON content in environment variable
client = gspread.service_account_from_dict(eval(creds_json))
sheet = client.open("TelegramBotDB").sheet1

# Allowed users for messaging
ALLOWED_USERS = [@niamulislam_007]  # replace with Telegram user IDs

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /help to see commands.")

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "/message <text> - Send message to allowed users\n" \
           "/poll - Start MCQ poll\n" \
           "/stats - Show your stats\n" \
           "/rd - R&D / info commands"
    await update.message.reply_text(text)

# /message command
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Please provide a message!")
        return
    msg = " ".join(context.args)
    for user_id in ALLOWED_USERS:
        await context.bot.send_message(chat_id=user_id, text=f"Message from {update.effective_user.first_name}: {msg}")
    await update.message.reply_text("Message sent!")

# /poll command
async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = "What is 2+2?"
    options = ["2", "3", "4", "5"]
    await context.bot.send_poll(chat_id=update.effective_chat.id,
                                question=question,
                                options=options,
                                is_anonymous=False)

# /stats command
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Feature coming soon! Poll results will be here.")

# /rd command
async def rd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("R&D / extra options placeholder.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("message", message))
    app.add_handler(CommandHandler("poll", poll))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("rd", rd))
    app.run_polling()

if __name__ == "__main__":
    main()
