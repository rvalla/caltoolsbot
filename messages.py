import json as js

class Messages():
	"The class the bot use to know what to say..."

	def __init__(self):
		self.msg_es = js.load(open("messages_es.json"))
		self.msg_en = js.load(open("messages_en.json"))

	def get_message(self, key, l):
		if l == 1:
			return self.msg_en[key]
		else:
			return self.msg_es[key]
	
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
			m += "> Mandame /pcs seguido de una lista de notas separadas con espacios (ojo que entiendo números 0-11).\n" 
		else:
			m += "You can ask me for different things. Here is a list with the available commands:\n\n"
			m += "> Send me /pcs followed by a list of notes separated with spaces (note that I understand numbers 0-11).\n" 
		return m