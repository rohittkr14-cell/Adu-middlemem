from telegram import Update, ChatPermissions
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)

TOKEN = "8570445991:AAHvyZ-EmPztUP0zOYhLPvzbe54IYgVOI0o"
OWNER_ID = 6587658540

TERMS_MESSAGE = """Hey, Please state the terms of the deal.

• What is the deal?
• Who is the buyer/seller?
• What is the agreed price?
• Any conditions like when to release or when to refund?"""

COMPLETE_MESSAGE = """Thank you for using my Middleman service 🤝🏻

Please leave me a vouch here
@middIemem in the comment section."""

RECEIVED_MESSAGE = """I have successfully received the amount and the MM fee. It is safe to deal forward. 

I will process the payment after the deal concludes. Thank you for your cooperation and for your trust!"""

def owner_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != OWNER_ID:
            return
        return await func(update, context)
    return wrapper

@owner_only
async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await chat.set_title("Adu MM | @middlemem")
    msg = await update.message.reply_text(TERMS_MESSAGE)
    await msg.pin()

@owner_only
async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await chat.set_title("Adu MM | Completed 🔵")
    await chat.set_permissions(ChatPermissions(can_send_messages=False))

@owner_only
async def unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await chat.set_permissions(ChatPermissions(can_send_messages=True))

@owner_only
async def complete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(COMPLETE_MESSAGE)

@owner_only
async def received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(RECEIVED_MESSAGE)

app = ApplicationBuilder().token(TOKEN).build()

# DOT COMMAND HANDLERS
app.add_handler(MessageHandler(filters.Regex(r"^\.setup$"), setup))
app.add_handler(MessageHandler(filters.Regex(r"^\.lock$"), lock))
app.add_handler(MessageHandler(filters.Regex(r"^\.unlock$"), unlock))
app.add_handler(MessageHandler(filters.Regex(r"^\.complete$"), complete))
app.add_handler(MessageHandler(filters.Regex(r"^\.rvc$"), received))

app.run_polling()