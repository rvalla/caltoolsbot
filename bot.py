from telegram.ext import (
			Application, InlineQueryHandler, CommandHandler,
			CallbackQueryHandler, ContextTypes, ConversationHandler,
			MessageHandler, filters
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
import traceback, logging
from datetime import datetime as dt, timedelta
import json as js
from usage import Usage
from messages import Messages
from pcs import PCS
from chain import Chain
#from music import Music
from users import Users
from util import Util
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

#Filterint warnings about conversation handlers configuration...
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

print("Starting musiCal Bot...", end="\n")
config = js.load(open("config.json")) #The configuration file (token included)
en_users = set() #In this set the bot store ids from users who prefer to speak in English
us = Usage("data/usage.csv", "data/errors.csv") #The class to work with usage data...
msg = Messages() #The class to build content of text messages...
pcs = PCS() #A class to analyze pitch class sets...
users = Users("data/users/") #A class to save user's configuration...
ut = Util() #Some useful functions...
#mus = Music() #A class to create experimental music...
START_AN, START_TS, PCS, ALLSTATES, CHAIN, RANDOM_S, RANDOM_D, RANDOM_B, RANDOM_C, ERROR_1, ERROR_2, ADMIN = range(12) #The general conversation states...
#CP_T, CP_M, CP_D = range(3) #The music conversation states...

#Welcome message for people who start the bot...
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	chat_id = update.effective_chat.id
	logging.info(str(hide_id(chat_id)) + " started the bot...")
	us.add_start()
	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("start_start", get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("start_name", get_language(context)), parse_mode=ParseMode.HTML)
	return START_AN

#Saving the user's artistic name...
async def save_artistic_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	m = update.message.text
	context.chat_data["name"] = m
	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("start_ts", get_language(context)), parse_mode=ParseMode.HTML)
	return START_TS

#Saving the user's prefered time signature...
async def save_prefered_time_signature(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	m = update.message.text
	if msg.is_time_signature(m):
		context.chat_data["t_signature"] = m
		users.save_user_data(chat_id, context.chat_data)
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("start_end", get_language(context)), parse_mode=ParseMode.HTML)
		return ConversationHandler.END
	else:
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("start_error", get_language(context)), parse_mode=ParseMode.HTML)
		return START_TS

#Starting a pitch class set analysis session...
async def trigger_pcs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	logging.info(str(hide_id(chat_id)) + " starts pcs conversation...")
	await context.bot.send_message(chat_id=chat_id, text=msg.get_conversation_start(get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("pcs_start", get_language(context)), parse_mode=ParseMode.HTML)
	return PCS

#Analyzing pitch class sets sent by the user...
async def get_pcs_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	text = update.message.text
	try:
		cardinality, ordinal, interval, is_inverted, z_pair, states, ordered_form, prime_form = pcs.get_set_info(text)
		vector = pcs.interval_vector(ordered_form)
		if not ordinal == None:
			m = msg.build_pcs_message(cardinality, ordinal, interval, is_inverted, z_pair, states, ordered_form, prime_form, vector, get_language(context))
			us.add_pcs(0)
			await context.bot.send_message(chat_id=chat_id, text=m, parse_mode=ParseMode.HTML)
		else:
			us.add_pcs(1)
			await context.bot.send_message(chat_id=chat_id, text=msg.get_message("pcs_pcserror", get_language(context)), parse_mode=ParseMode.HTML)
	except:
		us.add_pcs(2)
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("pcs_nerror", get_language(context)), parse_mode=ParseMode.HTML)
	return PCS

#Starting a pitch class set all states session...
async def trigger_allstates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	logging.info(str(hide_id(chat_id)) + " starts allstates conversation...")
	await context.bot.send_message(chat_id=chat_id, text=msg.get_conversation_start(get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("allstates_start", get_language(context)), parse_mode=ParseMode.HTML)
	return ALLSTATES

#Creating a pcs all states matrix to send...
async def get_all_states(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	text = update.message.text
	try:
		allstates_matrix = pcs.states_to_string(pcs.get_states_matrix(pcs.string_to_notes(text)))
		us.add_allstates(0)
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("allstates_msg", get_language(context)), parse_mode=ParseMode.HTML)
		await context.bot.send_message(chat_id=chat_id, text=allstates_matrix, parse_mode=ParseMode.HTML)
	except:
		us.add_allstates(1)
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("allstates_error", get_language(context)), parse_mode=ParseMode.HTML)
	return ALLSTATES

#Starting a constant pitch class set sequence creation session...
async def trigger_chain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	logging.info(str(hide_id(chat_id)) + " starts chain conversation...")
	await context.bot.send_message(chat_id=chat_id, text=msg.get_conversation_start(get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("chain_start", get_language(context)), parse_mode=ParseMode.HTML)
	return CHAIN

#Creating a new constant pitch class set notes sequence...
async def get_new_chain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	text = update.message.text
	if text.lower() == "h":
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("chain_help", get_language(context)), parse_mode=ParseMode.HTML)
	elif text.startswith("+") and "chain" in context.chat_data:
		t = int(text[1:])
		context.chat_data["chain"].translate(t)
		m, c = msg.build_operation_chain_message(context.chat_data["chain"], get_language(context))
		us.add_chain(1)
		await context.bot.send_message(chat_id=chat_id, text=m, parse_mode=ParseMode.HTML)
		await context.bot.send_message(chat_id=chat_id, text=c, parse_mode=ParseMode.HTML)
	elif text.lower() == "i" and "chain" in context.chat_data:
		context.chat_data["chain"].invert()
		m, c = msg.build_operation_chain_message(context.chat_data["chain"], get_language(context))
		us.add_chain(1)
		await context.bot.send_message(chat_id=chat_id, text=m, parse_mode=ParseMode.HTML)
		await context.bot.send_message(chat_id=chat_id, text=c, parse_mode=ParseMode.HTML)
	elif text.lower() == "n" and "chain" in context.chat_data:
		context.chat_data["chain"].run()
		m, c = msg.build_new_chain_message(context.chat_data["chain"], get_language(context))
		us.add_chain(1)
		await context.bot.send_message(chat_id=chat_id, text=m, parse_mode=ParseMode.HTML)
		await context.bot.send_message(chat_id=chat_id, text=c, parse_mode=ParseMode.HTML)
	else:
		try:
			context.chat_data["chain"] = Chain(pcs, text, 7, 14, 3)
			m, c = msg.build_new_chain_message(context.chat_data["chain"], get_language(context))
			us.add_chain(0)
			await context.bot.send_message(chat_id=chat_id, text=m, parse_mode=ParseMode.HTML)
			await context.bot.send_message(chat_id=chat_id, text=c, parse_mode=ParseMode.HTML)
		except:
			us.add_chain(2)
			await context.bot.send_message(chat_id=chat_id, text=msg.get_message("chain_nerror", get_language(context)), parse_mode=ParseMode.HTML)
	return CHAIN

#Starting a random functions session...
async def trigger_random(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	logging.info(str(hide_id(chat_id)) + " starts random conversation...")
	await context.bot.send_message(chat_id=chat_id, text=msg.get_conversation_start(get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("random_size", get_language(context)), parse_mode=ParseMode.HTML)
	return RANDOM_S

#Saving the sequence size preference...
async def set_random_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	text = update.message.text
	try:
		size = int(text)
		context.chat_data["random_size"] = size
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("random_dice", get_language(context)), parse_mode=ParseMode.HTML)
		return RANDOM_D
	except:
		us.add_random(1)
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("random_error", get_language(context)), parse_mode=ParseMode.HTML)
		return RANDOM_S

#Saving the dice size preference...
async def set_dice_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	text = update.message.text
	try:
		size = int(text)
		context.chat_data["random_dice"] = size
		keyboard = random_keyboard(get_language(context))
		reply = InlineKeyboardMarkup(keyboard)
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("random_distribution", get_language(context)), reply_markup=reply, parse_mode=ParseMode.HTML)
		return RANDOM_B
	except:
		us.add_random(1)
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("random_error", get_language(context)), parse_mode=ParseMode.HTML)
		return RANDOM_D

#Building the random keyboard...
def random_keyboard(language: int):
	tags = msg.get_keyboard_tags("random_keyboard", get_language(context))
	keyboard = [[InlineKeyboardButton(text=tags[0], callback_data="r_0"), InlineKeyboardButton(text=tags[1], callback_data="r_1")],
							[InlineKeyboardButton(text=tags[2], callback_data="r_2"), InlineKeyboardButton(text=tags[3], callback_data="r_3")],
							[InlineKeyboardButton(text=tags[4], callback_data="r_4")]]
	return keyboard

#Shuffling a user's message...
async def shuffle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	text = update.message.text
	m = ut.shuffle_string(text)
	await context.bot.send_message(chat_id=chat_id, text=m, parse_mode=ParseMode.HTML)
	return RANDOM_B

#Random message with user's list...
async def get_controlled_random(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	text = update.message.text
	m = ut.controlled_random(context.chat_data["random_size"], text.split(" "))
	await context.bot.send_message(chat_id=chat_id, text=m, parse_mode=ParseMode.HTML)
	return RANDOM_B

#Handling random conversation clicks...
async def random_conversation_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	query = update.callback_query
	await query.answer()
	us.add_random(0)
	selection = int(query.data.split("_")[1])
	if selection == 0:
		m = msg.sequence_to_string(ut.dice(context.chat_data["random_size"], context.chat_data["random_dice"]))
		await context.bot.send_message(chat_id=chat_id, text=m, parse_mode=ParseMode.HTML)
		return RANDOM_B
	elif selection == 1:
		m = msg.sequence_to_string(ut.minor_of_a_pair(context.chat_data["random_size"], context.chat_data["random_dice"]))
		await context.bot.send_message(chat_id=chat_id, text=m, parse_mode=ParseMode.HTML)
		return RANDOM_B
	elif selection == 2:
		m = msg.sequence_to_string(ut.sum_of_dice(context.chat_data["random_size"], context.chat_data["random_dice"], 2))
		await context.bot.send_message(chat_id=chat_id, text=m, parse_mode=ParseMode.HTML)
		return RANDOM_B
	elif selection == 3:
		m = msg.sequence_to_string(ut.sum_of_dice(context.chat_data["random_size"], context.chat_data["random_dice"], 3))
		await context.bot.send_message(chat_id=chat_id, text=m, parse_mode=ParseMode.HTML)
		return RANDOM_B
	elif selection == 4:
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("random_list", get_language(context)), parse_mode=ParseMode.HTML)
		return RANDOM_C

#Starting a music creation session...
#async def trigger_mus(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#	chat_id = update.effective_chat.id
#	logging.info(str(hide_id(chat_id)) + " starts a music creation session...")
#	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("music_t", get_language(context)), parse_mode=ParseMode.HTML)
#	return CP_T

#Deciding a title for the composition...
#async def get_mus_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#	chat_id = update.effective_chat.id
#	m = update.message.text
#	context.chat_data["music_t"] = m
#	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("music_c_m", get_language(context)), parse_mode=ParseMode.HTML)
#	return CP_M

#Deciding a title for the composition...
#async def get_mus_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#	chat_id = update.effective_chat.id
#	m = update.message.text
#	if m == "1":
#		mode = "random"
#	elif m == "2":
#		mode = "control"
#	elif m == "3":
#		mode = "markov"
#	context.chat_data["music_m"] = mode
#	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("music_c_d", get_language(context)), parse_mode=ParseMode.HTML)
#	return CP_D

#Creating and sending the counterpoint...
#async def build_counterpoint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#	chat_id = update.effective_chat.id
#	data = update.message.text
#	title = context.chat_data["music_t"]
#	mode = context.chat_data["music_m"]
#	if mode == "control":
#		c = mus.control_counterpoint(title, "musiCalBot", data)
#	elif mode = "markov":
#		c = mus.markov_counterpoint(title, "musiCalBot")
#	elif mode = "random":
#		c = mus.random_counterpoint(title, "musiCalBot")
#	filename = "temp/" + title + "_" + composer + ".mid"
#	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("music_c", get_language(context)), parse_mode=ParseMode.HTML)
#	await context.bot.send
#	return ConversationHandler.END

#Starting an error report session...
async def trigger_error_submit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	logging.info(str(hide_id(chat_id)) + " wants to report an error...")
	await context.bot.send_message(chat_id=chat_id, text=msg.get_apology(get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("submit_error_command", get_language(context)), parse_mode=ParseMode.HTML)
	return ERROR_1

#Saving error related command...
async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	m = update.message.text
	context.chat_data["error_command"] = m
	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("submit_error_about", get_language(context)), parse_mode=ParseMode.HTML)
	return ERROR_2

#Saving error description...
async def report_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	m = context.chat_data["error_command"]
	m2 = update.message.text
	context.chat_data["error_description"] = m2
	us.add_error_report()
	us.save_error_report(m, m2, str(hide_id(chat_id)))
	admin_msg = "Error reported:\n-command: " + m + "\n-description: " + m2
	await context.bot.send_message(chat_id=config["admin_id"], text=admin_msg, parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("submit_error_end", get_language(context)), parse_mode=ParseMode.HTML)
	return ConversationHandler.END

#Starting admin session...
async def trigger_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	password = update.message.text.split(" ")
	if len(password) > 1 and password[1] == config["password"]:
		us.add_admin()
		context.chat_data["admin_t"] = dt.now()
		if get_language(context) == 0:
			keyboard = [[InlineKeyboardButton(text="Últimos datos", callback_data="a_0")]]
		else:
			keyboard = [[InlineKeyboardButton(text="Last data", callback_data="a_0")]]
		reply = InlineKeyboardMarkup(keyboard)
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("admin", get_language(context)), reply_markup=reply, parse_mode=ParseMode.HTML)
		return ADMIN
	else:
		logging.info(hide_id(chat_id) + " wanted to start an admin session...")
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("intruder", get_language(context)), parse_mode=ParseMode.HTML)
		return ConversationHandler.END

#Ending any convertation...
async def end_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	logging.info(str(hide_id(chat_id)) + " endss a conversation...")
	await context.bot.send_message(chat_id=chat_id, text=msg.get_conversation_end(get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("end_conversation", get_language(context)), parse_mode=ParseMode.HTML)
	return ConversationHandler.END

#Printing privacy command...
async def print_privacy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	chat_id = update.effective_chat.id
	logging.info(str(hide_id(chat_id)) + " checked privacy policy...")
	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("privacy", get_language(context)), parse_mode=ParseMode.HTML)

#Sending a help message...
async def print_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	chat_id = update.effective_chat.id
	logging.info(str(hide_id(chat_id)) + " asked for help...")
	us.add_help()
	m, m2 = msg.build_help_message(get_language(context))
	await context.bot.send_message(chat_id=chat_id, text=m, parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=chat_id, text=m2, parse_mode=ParseMode.HTML)

#Checking which language to use with the actual user...
def get_language(context: ContextTypes.DEFAULT_TYPE) -> None:
	if "language" in context.chat_data:
		return context.chat_data["language"]
	else:
		return 0

#A command to allow a user decide which language to use...
async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	chat_id = update.effective_chat.id
	logging.info(str(hide_id(chat_id)) + " will set language...")
	keyboard = [[InlineKeyboardButton(text="Español", callback_data="l_0"),
				InlineKeyboardButton(text="English", callback_data="l_1")]]
	reply = InlineKeyboardMarkup(keyboard)
	await context.bot.send_message(chat_id=chat_id, text=msg.get_message("language_start", get_language(context)), reply_markup=reply, parse_mode=ParseMode.HTML)

#Setting language configuration for actual user...
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE, query) -> None:
	chat_id = update.effective_chat.id
	if query == "l_1":
		logging.info("English is the language selected by " + str(hide_id(chat_id)))
		context.chat_data["language"] = 1
		us.add_language(1)
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("language_warning", get_language(context)), parse_mode=ParseMode.HTML)
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("language_end", get_language(context)), parse_mode=ParseMode.HTML)
	else:
		logging.info("Spanish is the language selected by " + str(hide_id(chat_id)))
		context.chat_data["language"] = 0
		us.add_language(0)
		await context.bot.send_message(chat_id=chat_id, text=msg.get_message("language_end", get_language(context)), parse_mode=ParseMode.HTML)

#Handling default clicks on InlineKeyboardButtons...
async def default_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	query = update.callback_query
	await query.answer()
	if query.data.startswith("l"):
		await set_language(update, context, query.data)

#Handling conversation clicks on InlineKeyboardButtons...
async def conversation_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	chat_id = update.effective_chat.id
	query = update.callback_query
	await query.answer()
	if query.data.startswith("a"):
		if dt.now() - context.chat_data["admin_t"] < timedelta(minutes=5):
			selection = int(query.data.split("_")[1])
			if selection == 0:
				await bot_usage(update, context)
			return ConversationHandler.END
		else:
			chat_id = update.effective_chat.id
			await context.bot.send_message(chat_id=chat_id, text=msg.get_message("admin_end", get_language(chat_id)), parse_mode=ParseMode.HTML)
			return ConversationHandler.END
	
#Sending usage data...
async def bot_usage(update, context):
	chat_id = update.effective_chat.id
	m = us.build_usage_message()
	await context.bot.send_message(chat_id=chat_id, text=m, parse_mode=ParseMode.HTML)

#Notifying the user about out of context conversation...
async def out_of_context(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	chat_id = update.effective_chat.id
	us.add_outofcontext()
	logging.info(str(hide_id(chat_id)) + " sent out of context message...")
	await context.bot.send_message(chat_id=chat_id, text=msg.get_outofcontext(get_language(context)), parse_mode=ParseMode.HTML)

#Sending error notification to administrator...
async def error_notification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	chat_id = update.effective_chat.id
	m = "An error ocurred! While comunicating with chat " + str(hide_id(chat_id))
	logging.info(m)
	await context.bot.send_message(chat_id=config["admin_id"], text=m, parse_mode=ParseMode.HTML)

#Hiding the first numbers of a chat id for the log...
def hide_id(chat_id):
	s = str(chat_id)
	return "****" + s[len(s)-4:]

#Building the general conversation handler...
def build_general_conversation_handler():
	print("Building general conversation handler...", end="\n")
	handler = ConversationHandler(
		entry_points=[CommandHandler("start", start), CommandHandler("pcs", trigger_pcs),
					CommandHandler("allstates", trigger_allstates), CommandHandler("chain", trigger_chain),
					CommandHandler("matrix", trigger_matrix), CommandHandler("random", trigger_random),
					CommandHandler("admin", trigger_admin), CommandHandler("error", trigger_error_submit)],
		states={
			START_AN: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_artistic_name)],
			START_TS: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_prefered_time_signature)],
			PCS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_pcs_info)],
			ALLSTATES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_all_states)],
			CHAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_new_chain)],
			RANDOM_S: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_random_size)],
			RANDOM_D: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_dice_size)],
			RANDOM_B: [MessageHandler(filters.TEXT & ~filters.COMMAND, shuffle_message),
								CallbackQueryHandler(random_conversation_button_click)],
			RANDOM_C: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_controlled_random)],
			ADMIN: [CallbackQueryHandler(conversation_button_click)],
			ERROR_1: [MessageHandler(filters.TEXT, report_command)],
			ERROR_2: [MessageHandler(filters.TEXT & ~filters.COMMAND, report_error)],
		},
		fallbacks=[MessageHandler(filters.COMMAND, end_conversation)]
		)
	return handler

#Building the general conversation handler...
#def build_music_conversation_handler():
#	print("Building general conversation handler...", end="\n")
#	handler = ConversationHandler(
#		entry_points=[CommandHandler("mus", trigger_mus)],
#		states={
#			CP_T: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_mus_title)],
#			CP_D: [MessageHandler(filters.TEXT, build_counterpoint)],
#			CP_M: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_mus_mode)],
#		},
#		fallbacks=[MessageHandler(filters.COMMAND, end_conversation)]
#		)
#	return handler

#Here the magic happens...
def main() -> None:
	if config["logging"] == "persistent":
		logging.basicConfig(filename="history.txt", filemode='a',level=logging.INFO,
						format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	elif config["logging"] == "debugging":
		logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	else:
		logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	print("Ready to build the bot...", end="\n")
	app = Application.builder().token(config["token"]).build()
	app.add_error_handler(error_notification)
	app.add_handler(CommandHandler("language", select_language), group=2)
	app.add_handler(CommandHandler("help", print_help), group=2)
	app.add_handler(CommandHandler("privacy", print_privacy), group=2)
	app.add_handler(CallbackQueryHandler(default_button_click), group=2)
	app.add_handler(build_general_conversation_handler(), group=1)
	#app.add_handler(build_music_conversation_handler(), group=1)
	app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, out_of_context), group=1)
	if config["webhook"]:
		print("Ready to set webhook...", end="\n")
		wh_url = "https://" + config["public_ip"] + ":" + str(config["webhook_port"])
		app.run_webhook(listen="0.0.0.0", port=config["webhook_port"], secret_token=config["webhook_path"], key="webhook.key",
							cert="webhook.pem", webhook_url=wh_url, drop_pending_updates=True)
	else:
		print("Ready to start polling...", end="\n")
		app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
	main()
