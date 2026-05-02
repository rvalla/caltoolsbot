import re
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

	def get_keyboard_tags(self, key, l):
		return self.get_message(key, l).split(",")
	
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
		z_string = " "
		targets = ["SET", "Z_PAIR", "STATES", "ORDERED_FORM", "PRIME_FORM", "INTERVAL_VECTOR"]
		if l == 0:
			m = self.msg_es["pcs_info"]
			if not z_pair == -1:
				z_string = self.msg_es["pcs_zpair"]
		else:
			m = self.msg_en["pcs_info"]
			if not z_pair == -1:
				z_string = self.msg_en["pcs_zpair"]
		if len(z_string) > 1:
			z_string = re.sub("SET", self.get_set_class(c, z_pair, z_pair), z_string)
		data = [self.get_complete_set_class(c, o, i, inverted, z_pair)]
		data.append(z_string)
		data.append(str(states))
		data.append(self.notes_to_string(ordered))
		data.append(self.notes_to_string(prime))
		data.append(self.vector_to_string(vector))
		for k, v in zip(targets, data):
			m = re.sub(k, v, m)
		return m
	
	def build_new_chain_message(self, chain, l):
		m = ""
		targets = ["SET_DATA", "STATE"]
		states = []
		if l == 0:
			m = self.msg_es["chain_new"]
			states = self.msg_es["chain_states"].split(",")
		else:
			m = self.msg_en["chain_new"]
			states = self.msg_en["chain_states"].split(",")
		data = [self.get_set_class(chain.base_data["cardinality"], chain.base_data["ordinal"], chain.base_data["z_pair"])]
		if chain.is_closed:
			data.append(states[0])
		elif chain.is_closable:
			data.append(states[1])
		else:
			data.append(states[2])
		for k, v in zip(targets, data):
			m = re.sub(k, v, m)
		return m, chain.sequence_to_string(chain.sequence)

	def build_operation_chain_message(self, chain, l):
		m = ""
		states = []
		if l == 0:
			m = self.msg_es["chain_op"]
		else:
			m = self.msg_en["chain_op"]
		return m, chain.sequence_to_string(chain.sequence)

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

	def sequence_to_string(self, notes):
		m = ""
		for n in notes:
			m += str(n)
			m += " "
		return m[:len(m)-1]
	
	def vector_to_string(self, vector):
		m = "["
		for v in vector:
			m += str(v)
		return m +"]"
	
	def is_time_signature(self, string):
		success = False
		values = string.split("/")
		if len(values) == 2:
			try:
				x = int(values[0])
				y = int(values[1])
				success = True
			except:
				pass
		return success

	def build_help_message(self, l):
		m = ""
		if l == 0:
			m += "Podés pedirme distintas cosas. Acá te dejo los comandos disponibles:\n\n"
			m += "> Mandame /pcs para analizar conmigo conjuntos de grados cromáticos (ojo que entiendo números (0-11)).\n"
			m += "> Mandame /chain para crear secuencias de notas con un conjunto de grados cromáticos constante.\n"
			m += "> Mandame /error para reportar cualquier error que me encuentres."
		else:
			m += "You can ask me for different things. Here is a list with the available commands:\n\n"
			m += "> Send me /pcs to start a pitch class set analysis sesion (note that I understand numbers (0-11)).\n" 
			m += "> Send me /chain to start a constant pitch class set sequence creation session.\n"
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
