from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler
from telegram.ext import Updater, CommandHandler, CallbackContext, filters

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Message
import asyncio
import time
import json
from basichandlers import answer_request, default_handler
import create_route
import namemanager


async def start(update: Update, context: CallbackContext):
    routes = []
    subscriptions = []
    context.chat_data["routes"] = json.dumps(routes)
    context.chat_data["subscriptions"] = json.dumps(subscriptions)
    context.chat_data["status"] = "default"
    await default_handler(update, context)

locmsg: Message = None


def getloc():
    if (locmsg is not None):
        print(f"{locmsg.location.latitude} and {locmsg.location.longitude}")
    time.sleep(3)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global locmsg

    if (update.message is not None and update.message.location is not None):
        await update.message.reply_text("Roger that")
        locmsg = update.message
    elif update.message is not None and "inquiry" in update.message.text:
        # loc = context.user_data.
        global loc
        print(context.user_data)
        await update.message.reply_text(f"{loc.latitude} and {loc.longitude}")


async def updloc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global loc
    print("updloc")
    if update.message is None:
        loc = update.edited_message.location
    else:
        loc = update.message.location
    print(f"{loc.latitude} and {loc.longitude}")


async def dispatcher(update: Update, context: CallbackContext) -> None:
    if (update.callback_query):
        await update.callback_query.answer(None)

        upd: dict = json.loads(update.callback_query.data)
        if ("change_status" in upd):
            context.chat_data["status"] = upd["change_status"]
    status = context.chat_data["status"]

    if (status == 'start_route_creation'):
        await create_route.start_route_creation(update, context)
    elif status == 'confirm_start_point_name':
        await create_route.confirm_start_point_name(update, context)
    elif status == 'confirm_end_point_name':
        await create_route.confirm_end_point_name(update, context)
    elif status == 'request_end_point_name':
        await create_route.request_end_point_name(update, context)
    elif status == 'finalize_route_creation':
        await create_route.finalize_route_creation(update, context)
    elif status == 'answer_request':
        await answer_request(update, context)
    else:
        context.chat_data["status"] = "default"
        await default_handler(update, context)


namemanager.init()
app = ApplicationBuilder().token(
    "7056812856:AAHhDqLXV1KX1fuTpWDYAjUacLd1nPfEfpE").arbitrary_callback_data(True).build()

app.add_handler(CommandHandler("start", start))
# app.add_handler(MessageHandler(filters=filters.LOCATION, callback=updloc))
app.add_handler(CallbackQueryHandler(dispatcher))
app.add_handler(MessageHandler(filters=None, callback=dispatcher))

# app.add_handler(MessageHandler(filters=None, callback=default_handler))


app.run_polling(allowed_updates=Update.ALL_TYPES)
