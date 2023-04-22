from telegram.ext import Application, InlineQueryHandler, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
import traceback, logging
import json as js
from usage import Usage
from messages import Messages
from pcs import PCS

config = js.load(open("config.json"))
en_users = set()
us = Usage("usage.csv")
msg = Messages()
pcs = PCS()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " started the bot...")
	us.add_start()
	await context.bot.send_message(chat_id=id, text=msg.get_message("hello", get_language(id)), parse_mode=ParseMode.HTML)

async def get_pcs_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " ask for a pcs...")
	text = update.message.text
	try:
		cardinality, ordinal, interval, is_inverted, z_pair, states, ordered_form, prime_form = pcs.get_set_info(text[5:])
		vector = pcs.interval_vector(ordered_form)
		await context.bot.send_message(chat_id=id, text=msg.get_message("pcs_1", get_language(id)), parse_mode=ParseMode.HTML)	
		if not ordinal == None:
			m = msg.build_pcs_message(cardinality, ordinal, interval, is_inverted, z_pair, states, ordered_form, prime_form, vector, get_language(id))
			us.add_pcs(0)
			await context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)
		else:
			us.add_pcs(1)
			await context.bot.send_message(chat_id=id, text=msg.get_message("pcs_2", get_language(id)), parse_mode=ParseMode.HTML)
	except:
		us.add_pcs(2)
		await context.bot.send_message(chat_id=id, text=msg.get_message("pcs_3", get_language(id)), parse_mode=ParseMode.HTML)	

async def print_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " asked for help...")
	us.add_help()
	await context.bot.send_message(chat_id=id, text=msg.build_help_message(get_language(id)), parse_mode=ParseMode.HTML)

def get_language(id):
	if id in en_users:
		return 1
	else:
		return 0

async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " will set language...")
	keyboard = [[InlineKeyboardButton(text="Español", callback_data="l_0"),
				InlineKeyboardButton(text="English", callback_data="l_1")]]
	reply = InlineKeyboardMarkup(keyboard)
	await context.bot.send_message(chat_id=id, text=msg.get_message("language", get_language(id)), reply_markup=reply, parse_mode=ParseMode.HTML)

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE, query) -> None:
	id = update.effective_chat.id
	if query == "l_1":
		logging.info("English is the language selected by " + str(hide_id(id)))
		en_users.add(id)
		us.add_language(1)
		await context.bot.send_message(chat_id=id, text=msg.get_message("language2", get_language(id)), parse_mode=ParseMode.HTML)
	else:
		logging.info("Spanish is the language selected by " + str(hide_id(id)))
		en_users.discard(id)
		us.add_language(0)
		await context.bot.send_message(chat_id=id, text=msg.get_message("language3", get_language(id)), parse_mode=ParseMode.HTML)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	query = update.callback_query
	query.answer()
	if query.data.startswith("l"):
		await set_language(update, context, query.data)

#Sending usage data...
async def bot_usage(update, context):
	id = update.effective_chat.id
	m = update.message.text.split(" ")
	if len(m) > 1 and m[1] == config["password"]:
		m = us.build_usage_message()
		await context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)
	else:
		logging.info(hide_id(id) + " wanted to check bot usage data...")
		await context.bot.send_message(chat_id=id, text=msg.get_message("intruder", get_language(id)), parse_mode=ParseMode.HTML)

#Saving usage data...
async def save_usage(update, context):
	id = update.effective_chat.id
	m = update.message.text.split(" ")
	if len(m) > 1 and m[1] == config["password"]:
		us.save_usage()
		await context.bot.send_message(chat_id=id, text="Datos guardados...", parse_mode=ParseMode.HTML)
	else:
		logging.info(hide_id(id) + " wanted to save bot usage data...")
		await context.bot.send_message(chat_id=id, text=msg.get_message("intruder", get_language(id)), parse_mode=ParseMode.HTML)

async def error_notification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	m = "An error ocurred! While comunicating with chat " + str(hide_id(id))
	logging.info(m)
	await context.bot.send_message(chat_id=config["admin_id"], text=m, parse_mode=ParseMode.HTML)

#Hiding the first numbers of a chat id for the log...
def hide_id(id):
	s = str(id)
	return "****" + s[len(s)-4:]

def main() -> None:
	if config["logging"] == "persistent":
		logging.basicConfig(filename="history.txt", filemode='a',level=logging.INFO,
						format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	elif config["logging"] == "debugging":
		logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	else:
		logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	app = Application.builder().token(config["token"]).build()
	#app.add_error_handler(error_notification)
	app.add_handler(CommandHandler("start", start))
	app.add_handler(CommandHandler("language", select_language))
	app.add_handler(CommandHandler("pcs", get_pcs_info))
	app.add_handler(CommandHandler("help", print_help))
	app.add_handler(CommandHandler("botusage", bot_usage))
	app.add_handler(CommandHandler("saveusage", save_usage))
	app.add_handler(CallbackQueryHandler(button_click))
	if config["webhook"]:
		wh_url = "https://" + config["public_ip"] + ":" + str(config["webhook_port"]) + "/" + config["webhook_path"]
		updater.start_webhook(listen="0.0.0.0", port=config["webhook_port"], url_path=config["webhook_path"], key="webhook.key",
							cert="webhook.pem", webhook_url=wh_url, drop_pending_updates=True)
	else:
		app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
	main()