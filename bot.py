from telegram.ext import (
			Application, InlineQueryHandler, CommandHandler,
			CallbackQueryHandler, ContextTypes, ConversationHandler,
			MessageHandler, filters
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
import traceback, logging
import json as js
from usage import Usage
from messages import Messages
from pcs import PCS

config = js.load(open("config.json")) #The configuration file (token included)
en_users = set() #In this set the bot store ids from users who prefer to speak in English
us = Usage("usage.csv", "errors.csv") #The class to work with usage data...
msg = Messages() #The class to build content of text messages...
pcs = PCS() #A class to analyze pitch class sets...
PCS_SESSION, ERROR1, ERROR2 = range(3) #The conversation states...

#Welcome message for people who start the bot...
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " started the bot...")
	us.add_start()
	await context.bot.send_message(chat_id=id, text=msg.get_message("hello", get_language(id)), parse_mode=ParseMode.HTML)

#Starting a pitch class set analysis session...
async def trigger_pcs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " starts pcs conversation...")
	await context.bot.send_message(chat_id=id, text=msg.get_conversation_start(get_language(id)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_message("pcs_1", get_language(id)), parse_mode=ParseMode.HTML)
	return PCS_SESSION

#Analyzing pitch class sets sent by the user...
async def get_pcs_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	text = update.message.text
	try:
		cardinality, ordinal, interval, is_inverted, z_pair, states, ordered_form, prime_form = pcs.get_set_info(text)
		vector = pcs.interval_vector(ordered_form)
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
	return PCS_SESSION

#Starting an error report session...
async def trigger_error_submit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " wants to report an error...")
	await context.bot.send_message(chat_id=id, text=msg.get_apology(get_language(id)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_message("submit_error_1", get_language(id)), parse_mode=ParseMode.HTML)
	return ERROR1

#Saving error related command...
async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	m = update.message.text
	context.chat_data["error_command"] = m
	await context.bot.send_message(chat_id=id, text=msg.get_message("submit_error_2", get_language(id)), parse_mode=ParseMode.HTML)
	return ERROR2

#Saving error description...
async def report_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	m = context.chat_data["error_command"]
	m2 = update.message.text
	context.chat_data["error_description"] = m2
	us.save_error_report(m, m2, str(hide_id(id)))
	admin_msg = "Error reported:\n-command: " + m + "\n-description: " + m2
	await context.bot.send_message(chat_id=config["admin_id"], text=admin_msg, parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_message("submit_error_3", get_language(id)), parse_mode=ParseMode.HTML)
	return ConversationHandler.END

#Ending any convertation...
async def end_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " endss a conversation...")
	await context.bot.send_message(chat_id=id, text=msg.get_conversation_end(get_language(id)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_message("end_conversation", get_language(id)), parse_mode=ParseMode.HTML)
	return ConversationHandler.END

#Sending a help message...
async def print_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " asked for help...")
	us.add_help()
	m, m2 = msg.build_help_message(get_language(id))
	await context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=m2, parse_mode=ParseMode.HTML)

#Checking which language to use with the actual user...
def get_language(id):
	if id in en_users:
		return 1
	else:
		return 0

#A commando to allow a user decide which language to use...
async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " will set language...")
	keyboard = [[InlineKeyboardButton(text="Español", callback_data="l_0"),
				InlineKeyboardButton(text="English", callback_data="l_1")]]
	reply = InlineKeyboardMarkup(keyboard)
	await context.bot.send_message(chat_id=id, text=msg.get_message("language", get_language(id)), reply_markup=reply, parse_mode=ParseMode.HTML)

#Setting language configuration for actual user...
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

#Handling clicks on InlineKeyboardButtons...
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

#Sending error notification to administrator...
async def error_notification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	m = "An error ocurred! While comunicating with chat " + str(hide_id(id))
	logging.info(m)
	await context.bot.send_message(chat_id=config["admin_id"], text=m, parse_mode=ParseMode.HTML)

#Hiding the first numbers of a chat id for the log...
def hide_id(id):
	s = str(id)
	return "****" + s[len(s)-4:]

#Building the conversation handler...
def build_conversation_handler():
	handler = ConversationHandler(
		entry_points=[CommandHandler("pcs", trigger_pcs),CommandHandler("error", trigger_error_submit)],
		states={
			PCS_SESSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_pcs_info)],
			ERROR1: [MessageHandler(filters.TEXT, report_command)],
			ERROR2: [MessageHandler(filters.TEXT & ~filters.COMMAND, report_error)],
		},
		fallbacks=[MessageHandler(filters.COMMAND, end_conversation)]
		)
	return handler

#Here the magic happens...
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
	app.add_handler(CommandHandler("start", start), group=2)
	app.add_handler(CommandHandler("language", select_language), group=2)
	app.add_handler(CommandHandler("help", print_help), group=2)
	app.add_handler(CommandHandler("botusage", bot_usage), group=2)
	app.add_handler(CommandHandler("saveusage", save_usage), group=2)
	app.add_handler(CallbackQueryHandler(button_click), group=2)
	app.add_handler(build_conversation_handler(), group=1)
	if config["webhook"]:
		wh_url = "https://" + config["public_ip"] + ":" + str(config["webhook_port"]) + "/" + config["webhook_path"]
		updater.start_webhook(listen="0.0.0.0", port=config["webhook_port"], url_path=config["webhook_path"], key="webhook.key",
							cert="webhook.pem", webhook_url=wh_url, drop_pending_updates=True)
	else:
		app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
	main()