from datetime import datetime as dt, timedelta

class Usage():
	"The class to save usage data..."

	def __init__(self, usage_path, errors_path):
		self.date = dt.today()
		self.output_path = usage_path
		self.errors_path = errors_path
		self.reset()

	#Resseting data variables...
	def reset(self):
		self.last_save = dt.now().replace(hour=0, minute=0, second=0, microsecond=0)
		self.start = 0
		self.pcs = [0,0,0] #success, wrong set, wrong input...
		self.allstates = [0,0] #success, error...
		self.chain = [0,0,0] #success, operations, errors...
		self.matrix = [0,0,0] #new matrices, operations, errors...
		self.random = [0,0] #success, errors...
		self.error_reports = 0
		self.language = [0,0,0] #spanish, english, chinese...
		self.privacy = 0
		self.help = 0
		self.outofcontext = 0
		self.errors = 0
		self.admin = 0

	#Building usage information message...
	def build_usage_message(self):
		m = "<b>Usage data:</b>" + "\n" + \
			"start: " + str(self.start) + "\n" + \
			"pcs: " + str(self.pcs) + "\n" + \
			"allstates: " + str(self.allstates) + "\n" + \
			"chain: " + str(self.chain) + "\n" + \
			"matrix: " + str(self.matrix) + "\n" + \
			"random: " + str(self.random) + "\n" + \
			"error reports: " + str(self.error_reports) + "\n" + \
			"language: " + str(self.language) + "\n" + \
			"privacy: " + str(self.privacy) + "\n" + \
			"help: " + str(self.help) + "\n" + \
			"out of context: " + str(self.outofcontext) + "\n" + \
			"errors: " + str(self.errors) + "\n" + \
			"admin: " + str(self.admin) + "\n"
		return m

	#Saving usage to file...
	def save_usage(self):
		file = open(self.output_path, "a")
		t = dt.now()
		date = str(t.year) + "-" + str(t.month) + "-" + str(t.day)
		line = self.build_usage_line(date)
		file.write(line)
		file.close()
		self.reset()

	#Building a data line to save...
	def build_usage_line(self, date):
		line = date + ";"
		line += str(self.start) + ";"
		line += self.list_to_csv_format(self.pcs)
		line += self.list_to_csv_format(self.allstates)
		line += self.list_to_csv_format(self.chain)
		line += self.list_to_csv_format(self.matrix)
		line += self.list_to_csv_format(self.random)
		line += str(self.error_reports) + ";"
		line += self.list_to_csv_format(self.language)
		line += str(self.privacy) + ";"
		line += str(self.help) + ";"
		line += str(self.outofcontext) + ";"
		line += str(self.errors) + ";"
		line += str(self.admin) + "\n"
		return line

	def list_to_csv_format(self, data):
		m = ""
		for d in data:
			m += str(d) + ";"
		return m

	#Checking last new data date...
	def check_data_interval(self):
		if dt.today() - self.last_save > timedelta(hours=24, minutes=0):
			self.save_usage()
			self.reset()

	#Registering a new start command...
	def add_start(self):
		self.check_data_interval()
		self.start += 1

	#Registering a new pcs...
	def add_pcs(self, key):
		self.check_data_interval()
		self.pcs[key] += 1

	#Registering a new pcs...
	def add_allstates(self, key):
		self.check_data_interval()
		self.allstates[key] += 1
	
	#Registering a new chain...
	def add_chain(self, key):
		self.check_data_interval()
		self.chain[key] += 1

	#Registering a new matrix...
	def add_matrix(self, key):
		self.check_data_interval()
		self.matrix[key] += 1

	#Registering a new random...
	def add_random(self, key):
		self.check_data_interval()
		self.random[key] += 1
	
	#Registering a new error report...
	def add_error_report(self):
		self.check_data_interval()
		self.error_reports += 1

	#Registering a new language...
	def add_language(self, l):
		self.check_data_interval()
		self.language[l] += 1

#Registering a new privacy...
	def add_privacy(self):
		self.check_data_interval()
		self.privacy += 1
	
	#Registering a new help...
	def add_help(self):
		self.check_data_interval()
		self.help += 1

	#Registering a new admin...
	def add_admin(self):
		self.check_data_interval()
		self.admin += 1
	
	#Registering an out of context message...
	def add_outofcontext(self):
		self.check_data_interval()
		self.outofcontext += 1

	#Registering a new error...
	def add_error(self):
		self.check_data_interval()
		self.errors += 1
	
	#Saving en error report...
	def save_error_report(self, command, description, user):
		file = open(self.errors_path, "a")
		t = dt.now()
		date = str(t.year) + "-" + str(t.month) + "-" + str(t.day)
		file.write(date + ";")
		file.write(command + ";")
		file.write(description + ";")
		file.write(user + "\n")
		file.close()
