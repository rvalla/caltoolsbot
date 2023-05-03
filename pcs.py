class PCS():
	"A tool to recognize pitch class sets"

	def __init__(self):
		#We load prime forms and data related to Z pairs and invariance...
		self.prime_forms, self.set_data = self.load_prime_forms()
	
	#we ask for all pitch class set relevant information...
	def get_set_info(self, string_notes):
		notes = self.string_to_notes(string_notes) #converting a string into an integer list...
		cardinality = len(notes)
		ordered_form = self.ordered_form(notes)
		interval = ordered_form[0]
		prime_form = self.move_set(ordered_form, -ordered_form[0])
		is_inverted, ordinal = self.search_set(cardinality, False, prime_form)
		if is_inverted:
			prime_form = self.prime_form(self.invert_set(cardinality, ordered_form))
		z_pair = None
		states = None
		if not ordinal == None:
			z_pair = self.set_data[cardinality-1][ordinal-1][0]
			states = self.set_data[cardinality-1][ordinal-1][1]
		return cardinality, ordinal, interval, is_inverted, z_pair, states, ordered_form, prime_form
	
	#we ask for a pcs ordinal...
	def get_set_ordinal(self, notes):
		cardinality = len(notes)
		prime_form = self.prime_form(notes)
		is_inverted, ordinal = self.search_set(cardinality, False, prime_form)
		return ordinal
	
	#searching our prime form in the database...
	def search_set(self, cardinality, is_inverted, prime_form):
		found = False
		ordinal = None #if the set is not in the database we will return None
		for s in range(len(self.prime_forms[cardinality-1])):
			#searching for the set in the database...
			found = self.compare_set(prime_form, self.prime_forms[cardinality-1][s])
			if found:
				ordinal = s + 1
				break
		if found:
			return is_inverted, ordinal
		elif not is_inverted:
			#trying again, maybe the set is inverted...
			return self.search_set(cardinality, True, self.prime_form(self.invert_set(cardinality, prime_form)))
		else:
			return is_inverted, ordinal

	#comparing prime forms...
	def compare_set(self, in_set, list_set):
		#comparing sets element by element backwards (they used to be different at the end)...
		is_equal = True
		for s in range(len(in_set)-1,0,-1):
			if in_set[s] != list_set[s]:
				is_equal = False
				break
		return is_equal

	#getting the prime form of a notes set...	
	def prime_form(self, notes):
		#a prime form is simply an ordered form from 0...
		ordered_form = self.ordered_form(notes)
		return self.move_set(ordered_form, -ordered_form[0])

	#getting the order form of a notes set...
	def ordered_form(self, notes):
		notes.sort() #we order the notes...
		cardinality = len(notes)
		candidates = self.get_ordered_candidates(cardinality, notes)
		ordered_form = []
		if len(candidates) == 1:
			#if we received only one candidate we found the ordered form...
			ordered_form = candidates[0]
		else:
			#if there are two or more candidates we need extra work...
			ordered_form = self.debug_candidates(cardinality, candidates)
		return ordered_form
	
	#getting the set of circular permutations that fullfill requirement 1...
	def get_ordered_candidates(self, cardinality, notes):
		candidates = []
		interval = 11 #there isn't any interval bigger than 11...
		for i in range(cardinality):
			d = (notes[(i-1)%cardinality]-notes[i])%12 #checking distance for circular permutations...
			if d < interval:
				interval = d
				candidates = [self.reorder_set(cardinality, notes, i)] #we found a candidate...
			elif d == interval:
				candidates.append(self.reorder_set(cardinality, notes, i)) #our candidate is not alone...
		return candidates

	#getting the correct ordered form in the set of candidates (requirement 2)...
	def debug_candidates(self, cardinality, candidates):
		ordered_form = candidates[0] #if requirement 2 is not decisive any candidate is valid...
		actual_candidates = [i for i in range(len(candidates))] #the candidates for each step...
		interval = 11 #there isn't any interval bigger than 11...
		for i in range(1,cardinality-1):
			new_candidates = [] #we want to discard candidates...
			for c in actual_candidates:
				#checking requirement 2...
				d = (candidates[c][i]-candidates[c][0])%12
				if d < interval:
					interval = d
					new_candidates = [c] #we found a new candidate...
				elif d == interval: 
					new_candidates.append(c) #our candidate if not alone...
			if len(new_candidates) == 1:
				#if we received only one new_candidate we found the ordered form...
				ordered_form = candidates[new_candidates[0]]
				break
			else:
				#if there are two or more new_candidates we need extra work...
				actual_candidates = new_candidates #we will check only these candidates...
				interval = 11 #the interval needs to be reset...
		return ordered_form

	#getting a circular permutation of a set...
	def reorder_set(self, cardinality, notes, start):
		new_notes = []
		for i in range(cardinality):
			new_notes.append(notes[(i+start)%cardinality])
		return new_notes
	
	#inverting a set...
	def invert_set(self, cardinality, notes):
		new_notes = []
		for i in range(cardinality):
			new_notes.append(12-notes[i]%12)
		return new_notes

	#getting the interval vector...
	def interval_vector(self, notes):
		vector = [0,0,0,0,0,0]
		step = 0
		for i in range(len(notes)-1):
			for n in range(step + 1, len(notes)):
				a = notes[n]%12
				b = notes[step]%12
				if a != b:
					interval = abs(a-b)
					if interval > 6:
						interval = 12 - interval
					vector[interval%6-1] += 1
			step += 1
		return vector
	
	#getting interval vector in module 12...
	def big_interval_vector(self, notes):
		vector = [0,0,0,0,0,0,0,0,0,0,0] #ready to build a big interval vector (11 interval classes)...
		step = 0
		for i in range(len(notes)-1):
			for n in range(step + 1, len(notes)):
				a = notes[n]%12
				b = notes[step]%12
				if a != b:
					vector[(abs(a-b))%12-1] += 1
			step += 1
		return vector
	
	#getting the trasposition of a set...
	def move_set(self, notes, interval):
		new_notes = []
		for n in notes:
			new_notes.append((n+interval)%12)
		return new_notes

	#getting notes' list from a string...
	def string_to_notes(self, string_notes):
		notes = []
		for n in string_notes.split(" "):
			notes.append(int(n))
		return notes
	
	#formating ordered and prime forms...
	def notes_to_string(self, notes):
		m = "("
		for n in notes:
			m += str(n)
			m += " "
		return m[0:len(m)-1] + ")"
	
	#formating the interval vector...
	def vector_to_string(self, vector):
		m = "["
		for v in vector:
			m += str(v)
		return m +"]"

	#loading the prime forms database...
	def load_prime_forms(self):
		prime_forms = [[] for i in range(12)]
		set_data = [[] for i in range(12)]
		data = open("data/forte_prime_forms.csv").readlines()[1:] #openning our database file...
		for l in data:
			file_line = l.split(";")
			prime_forms[int(file_line[0])-1].append(self.string_to_notes(file_line[2]))
			set_data[int(file_line[0])-1].append([int(file_line[4]), int(file_line[5])])
		return prime_forms, set_data
	
	#formating set info message...
	def build_set_info_msg(self, cardinality, ordinal, interval, is_inverted, z_pair, states, ordered_form, prime_form):
		#formating set info to print in console...
		m = str(cardinality) + "."
		if z_pair != -1:
			m += "Z"
		m += str(ordinal) + " " + "t" + str(interval)
		if is_inverted:
			m += "i"
		m += "\n"
		m += self.notes_to_string(ordered_form) + " " + self.notes_to_string(prime_form) + "\n"
		m += self.vector_to_string(self.interval_vector(ordered_form)) + " |" + str(states) + "|\n"
		return m
	
	#the class prints itself...
	def __str__(self):
		return "-- Hi, I am a Pitch Class Sets analysis tool." + "\n"