import datetime as dt

class Usage():
	"The class to save usage data..."

	def __init__(self, usage_path, errors_path):
		self.output_path = usage_path
		self.errors_path = errors_path
		self.reset()

	#Resseting data variables...
	def reset(self):
		self.last_save = dt.datetime.now() #the start up time...
		self.start = 0
		self.pcs = [0,0,0] #success, wrong set, wrong input...
		self.chain = [0,0] #success, error...
		self.error_reports = 0
		self.language = [0,0] #spanish, english...
		self.help = 0
		self.outofcontext = 0
		self.errors = 0

	#Building usage information message...
	def build_usage_message(self):
		m = "<b>Usage data:</b>" + "\n" + \
			"start: " + str(self.start) + "\n" + \
			"pcs: " + str(self.pcs) + "\n" + \
			"chain: " + str(self.chain) + "\n" + \
			"error reports: " + str(self.error_reports) + "\n" + \
			"language: " + str(self.language) + "\n" + \
			"help: " + str(self.help) + "\n" + \
			"out of context: " + str(self.outofcontext) + "\n" + \
			"errors: " + str(self.errors) + "\n"
		return m

	#Saving usage to file...
	def save_usage(self):
		file = open(self.output_path, "a")
		t = dt.datetime.now()
		i = t - self.last_save
		date = str(t.year) + "-" + str(t.month) + "-" + str(t.day)
		interval = str(i).split(".")[0]
		line = self.build_usage_line(date, interval)
		file.write(line)
		file.close()
		self.reset()

	#Building a data line to save...
	def build_usage_line(self, date, interval):
		line = date + ";"
		line += interval + ";"
		line += str(self.start) + ";"
		line += str(self.pcs) + ";"
		line += str(self.chain) + ";"
		line += str(self.error_reports) + ";"
		line += str(self.language) + ";"
		line += str(self.help) + ";"
		line += str(self.outofcontext) + ";"
		line += str(self.errors) + "\n"
		return line

	#Registering a new start command...
	def add_start(self):
		self.start += 1

	#Registering a new pcs...
	def add_pcs(self, key):
		self.pcs[key] += 1
	
	#Registering a new chain...
	def add_chain(self, key):
		self.chain[key] += 1
	
	#Registering a new error report...
	def add_error_report(self):
		self.error_reports += 1

	#Registering a new language...
	def add_language(self, l):
		self.language[l] += 1

	#Registering a new help...
	def add_help(self):
		self.help += 1
	
	#Registering an out of context message...
	def add_outofcontext(self):
		self.outofcontext += 1

	#Registering a new error...
	def add_error(self):
		self.errors += 1
	
	#Saving en error report...
	def save_error_report(self, command, description, user):
		file = open(self.errors_path, "a")
		t = dt.datetime.now()
		date = str(t.year) + "-" + str(t.month) + "-" + str(t.day)
		file.write(date)
		file.write(command)
		file.write(description)
		file.write(user + "\n")
		file.close()
