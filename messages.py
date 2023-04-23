import json as js
import random as rd

class Messages():
	"The class the bot use to know what to say..."

	def __init__(self):
		self.msg_es = js.load(open("assets/text/es/messages.json"))
		self.msg_en = js.load(open("assets/text/en/messages.json"))
		self.r_conversation_start_es = open("assets/text/es/random_conversation_start.txt").readlines()
		self.r_conversation_start_en = open("assets/text/en/random_conversation_start.txt").readlines()
		self.r_conversation_end_es = open("assets/text/es/random_conversation_end.txt").readlines()
		self.r_conversation_end_en = open("assets/text/en/random_conversation_end.txt").readlines()
		self.r_error_message_es = open("assets/text/es/random_apologies.txt").readlines()
		self.r_error_message_en = open("assets/text/en/random_apologies.txt").readlines()
		self.r_outofcontext_es = open("assets/text/es/random_outofcontext.txt").readlines()
		self.r_outofcontext_en = open("assets/text/en/random_outofcontext.txt").readlines()

	def get_message(self, key, l):
		if l == 1:
			return self.msg_en[key]
		else:
			return self.msg_es[key]
	
	def get_conversation_start(self, l):
		if l == 0:
			return rd.choice(self.r_conversation_start_es)
		else:
			return rd.choice(self.r_conversation_start_en)
	
	def get_conversation_end(self, l):
		if l == 0:
			return rd.choice(self.r_conversation_end_es)
		else:
			return rd.choice(self.r_conversation_end_en)
	
	def get_apology(self, l):
		if l == 0:
			return rd.choice(self.r_error_message_es)
		else:
			return rd.choice(self.r_error_message_en)
	
	def get_outofcontext(self, l):
		if l == 0:
			return rd.choice(self.r_outofcontext_es)
		else:
			return rd.choice(self.r_outofcontext_en)
	
	def build_pcs_message(self, c, o, i, inverted, z_pair, states, ordered, prime, vector, l):
		m = ""
		if l == 0:
			m = "El conjunto de alturas que enviaste corresponde al conjunto "
			m += "<b>" + self.get_complete_set_class(c, o, i, inverted, z_pair) + "</b>. "
			if not z_pair == -1:
				m += "Su par Z es el <b>" + self.get_set_class(c,z_pair,z_pair) + "</b>. "
			m += "Existen " + str(states) + " estados diferentes para este conjunto.\n\n"
			m += "- Forma ordenada: <b>" + self.notes_to_string(ordered) + "</b>\n"
			m += "- Forma prima: <b>" + self.notes_to_string(prime) + "</b>\n"
			m += "- Vector interválico: <b>" + self.vector_to_string(vector) + "</b>"
		else:
			m = "The notes you have sent correspond to the following pitch class set: "
			m += "<b>" + self.get_complete_set_class(c, o, i, inverted, z_pair) + "</b>. "
			if not z_pair == -1:
				m += "Its Z related set is the <b>" + self.get_set_class(c,z_pair,z_pair) + "</b>. "
			m += "There are " + str(states) + " different states for this set.\n\n"
			m += "- Ordered form: <b>" + self.notes_to_string(ordered) + "</b>\n"
			m += "- Prime form: <b>" + self.notes_to_string(prime) + "</b>\n"
			m += "- Interval vector: <b>" + self.vector_to_string(vector) + "</b>"
		return m

	def get_complete_set_class(self, cardinal, ordinal, interval, inverted, z_pair):
		m = str(cardinal) + "."
		if not z_pair == -1:
			m += "Z"
		m += str(ordinal) + " t" + str(interval)
		if inverted:
			m += "i"
		return m
	
	def get_set_class(self, cardinal, ordinal, z_pair):
		m = str(cardinal) + "."
		if not z_pair == -1:
			m += "Z"
		m += str(ordinal)
		return m
	
	def notes_to_string(self, notes):
		m = "("
		for n in notes:
			m += str(n)
			m += " "
		return m[0:len(m)-1] + ")"
	
	def vector_to_string(self, vector):
		m = "["
		for v in vector:
			m += str(v)
		return m +"]"

	def build_help_message(self, l):
		m = ""
		if l == 0:
			m += "Podés pedirme distintas cosas. Acá te dejo los comandos disponibles:\n\n"
			m += "> Mandame /pcs para analizar conmigo conjuntos de grados cromáticos (ojo que entiendo números (0-11)).\n"
			m += "> Mandame /error para reportar cualquier error que me encuentres."
		else:
			m += "You can ask me for different things. Here is a list with the available commands:\n\n"
			m += "> Send me /pcs to start a pitch class set analysis sesion (note that I understand numbers (0-11)).\n" 
			m += "> Send me /error to report any error you find on me."
		m2 = ""
		if l == 0:
			m2 += "Podés suscribirte al canal @caltools para enterarte de cómo evoluciono. "
			m2 += "Si tenés dudas, quejas o preguntas podés escribirle a @rvalla (es el culpable de todo). "
			m2 += "También podés visitar la página del proyecto <a href='https://musicaltools.gitlab.io'>musiCal</a>."
		else:
			m2 += "Suscribe to @caltools channel to find out how I evolve (in spanish). "
			m2 += "If you have any doubts, complaints or questions you can write to @rvalla (he's the one to blame for everything). "
			m2 += "You can also visit the <a href='https://musicaltools.gitlab.io/index_en.html'>musiCal</a> project website."
		return m, m2