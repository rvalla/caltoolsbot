import datetime as dt

class Usage():
	"The class to save usage data..."

	def __init__(self, path):
		self.output_path = path
		self.reset()

	#Resseting data variables...
	def reset(self):
		self.last_save = dt.datetime.now() #the start up time...
		self.start = 0
		self.pcs = [0,0,0] #success, wrong set, wrong input...
		self.language = [0,0] #spanish, english...
		self.help = 0
		self.errors = 0

	#Building usage information message...
	def build_usage_message(self):
		m = "<b>Usage data:</b>" + "\n" + \
			"start: " + str(self.start) + "\n" + \
			"pcs: " + str(self.pcs) + "\n" + \
			"language: " + str(self.language) + "\n" + \
			"help: " + str(self.help) + "\n" + \
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
		line += str(self.language) + ";"
		line += str(self.help) + ";"
		line += str(self.errors) + "\n"
		return line

	#Registering a new start command...
	def add_start(self):
		self.start += 1

	#Registering a new color...
	def add_pcs(self, key):
		self.pcs[key] += 1

	#Registering a new language...
	def add_language(self, l):
		self.language[l] += 1

	#Registering a new help...
	def add_help(self):
		self.help += 1

	#Registering a new error...
	def add_error(self):
		self.errors += 1
