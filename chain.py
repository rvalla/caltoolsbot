import random as rd

class Chain():
	"A tool to create a constant pitch class set note sequence"

	def __init__(self, pcs, string_notes, link_min, link_max, max_degrading):
		self.pcs = pcs #sometimes we need to analyze pitch class sets...
		self.degrading = 0 #to know how many times we add links trivially...
		self.max_degrading = max_degrading - 1 #to stop after a number of fallbacks...
		self.base_data = self.get_base_data(string_notes)
		self.base = self.base_data["ordered"]
		self.candidates, self.iter_path, self.candidates_size = self.build_candidates_matrix(self.base)
		self.last_start = None
		self.link_sizes = self.get_link_sizes(len(self.base))
		self.link_min = link_min
		self.link_max = link_max
		self.sequence = None #here will be the notes sequence...
		self.building = None #we start this with reset()...
		self.is_closed = None
		self.is_closable = None
		self.sequence_size = None
		self.run()
	
	#we need to create the notes sequence...
	def run(self):
		self.last_start = rd.randint(0,self.candidates_size-1) #we pick a random starting point...
		rd.shuffle(self.link_sizes) #we pick random link size to start...
		self.reset()
		self.sequence = self.start_new_sequence() #we load the first two links...
		while self.building:
			rd.shuffle(self.iter_path) #each time we randomize order in which we read the candidates matrix...
			new_link = self.look_for_link(self.sequence[len(self.sequence)-2], self.sequence[len(self.sequence)-1])
			self.sequence.append(new_link) #appending the new link...
			self.sequence_size += 1 #the sequence is growing...
			if self.check_if_closed() and self.sequence_size >= self.link_min:
				self.building = False #we stop if the sequence is closed and fullfills the minumum links number...
			elif self.degrading > self.max_degrading or self.sequence_size >= self.link_max:
				self.building = False #we stop if the sequence exceeds maximum links number or is degraded...
		self.check_sequence_status() #we check if this sequence is closable...
	
	#starting a new sequence...
	def start_new_sequence(self):
		notes = self.candidates[self.last_start]
		return [notes[0:self.link_sizes[0]], notes[self.link_sizes[0]:len(self.base)]]

	#looking for a new link...
	def look_for_link(self, link_a, link_b):
		link = self.new_link(link_a, link_b)
		if link == None:
			self.degrading += 1
			return link_a #we fallback if we didn't find any new link...
		else:
			return link
	
	#getting a new link for the sequence...
	def new_link(self, link_a, link_b):
		link = None #we return None if we don't find a new link...
		for p in self.iter_path:
			#we are ready to read each row of candidates matrix following iter_path order...
			row_p = (self.last_start+p)%self.candidates_size
			if self.is_link_in(link_b, self.candidates[row_p]): #checking if link_b is in row_p...
				link = self.substract_link(link_b, self.candidates[row_p]) #if so, we get its complement...
				self.last_start = row_p #we save the position in candidates matrix...
				break
		return link

	#we check if the sequence is closed or closable...
	def check_sequence_status(self):
		if self.are_equal(self.sequence[0], self.sequence[self.sequence_size-1]):
			self.is_closed = True
			self.is_closable = True
		else:
			#we check links' pitch class set classification to decide if the sequence is closable...
			ordered_a = self.pcs.ordered_form(self.sequence[0])
			ordered_b = self.pcs.ordered_form(self.sequence[self.sequence_size-1])
			if self.are_the_same_set(ordered_a, ordered_b):
				self.is_closable = True
	
	#we need a function to check if the sequence is closed to stop building the sequence...
	def check_if_closed(self):
		return self.are_equal(self.sequence[0], self.sequence[self.sequence_size-1])

	#comparing two links...
	def are_equal(self, a, b):
		are_equal = True
		if len(a) == len(b):
			for n in a:
				if not self.is_note_in(n, b):
					are_equal = False
					break
		else:
			are_equal = False
		return are_equal 

	#deciding if two links correspond to the same pitch class set...
	def are_the_same_set(self, a, b):
		are_the_same = False
		if len(a) == len(b):
			ordinal_a = self.pcs.get_set_ordinal(a)
			ordinal_b = self.pcs.get_set_ordinal(b)
			if ordinal_a == ordinal_b:
				are_the_same = True
		return are_the_same
	
	#checking if a note is in a link...
	def is_note_in(self, note, notes):
		is_in = False
		for n in notes:
			if note == n:
				is_in = True
				break
		return is_in

	#checking if a link is in a row of the candidates matrix...
	def is_link_in(self, link, notes):
		is_in = True
		for n in link:
			if not self.is_note_in(n, notes):
				is_in = False
				break
		return is_in
	
	#substracting a link from a row of the candidates matrix...
	def substract_link(self, link, notes):
		complement = []
		for n in notes:
			if not self.is_note_in(n, link):
				complement.append(n)
		return complement

	#loading links sizes from base cardinality...
	def get_link_sizes(self, base_cardinality):
		link_sizes = [] #ready to return each link size...
		link_sizes.append(base_cardinality//2)
		link_sizes.append(base_cardinality-link_sizes[0])
		return link_sizes

	#checking if the sequence fullfills constant pitch class set requirement...	
	def check_sequence(self, base, sequence):
		good_sequence = True
		cardinality = len(base)
		ordinal = self.pcs.get_set_ordinal(base) 
		for i in range(len(sequence) - 1): #we check pitch class set's ordinal for each successive pair of links...
			the_set = sequence[i] + sequence[i+1]
			c = len(the_set)
			o = self.pcs.get_set_ordinal(the_set)
			if not (c == cardinality and o == ordinal):
				good_sequence = False
				break
		return good_sequence
	
	#resetting Chain() for a new run...
	def reset(self):
		self.sequence_size = 2 #asuming at least the two links from de base pitch set...
		self.building = True #otherwise we won't create anything...
		self.is_closed = False #we know a sequence of two links is not closed...
		self.is_closable = None #the same here...
	
	#building the candidates matrix...
	def build_candidates_matrix(self, base):
		candidates = []
		for r in range(self.base_data["candidates_size"]):
			row = []
			for n in base:
				row.append((n+r)%12) #we save each different state for base pcs...
			candidates.append(row)
		if self.base_data["invert_candidates"]: #we extend candidates matrix with inversions when possible...
			i_base = self.pcs.invert_set(len(base), base)
			for r in range(self.base_data["candidates_size"]):
				row = []
				for n in i_base:
					row.append((n+r)%12)
				candidates.append(row)
		iter_path = [i for i in range(1,len(candidates))] #the random order to read the matrix...
		return candidates, iter_path, len(candidates)

	#loading base pitch class set data...
	def get_base_data(self, string_notes):
		cardinality, ordinal, interval, is_inverted, z_pair, states, ordered_form, prime_form = self.pcs.get_set_info(string_notes)
		data = {}
		data["cardinality"] = cardinality
		data["ordinal"] = ordinal
		data["z_pair"] = z_pair
		data["is_inverted"] = is_inverted
		data["states"] = states
		data["ordered"] = ordered_form
		data["prime"] = prime_form
		data["candidates_size"], data["invert_candidates"] = self.get_candidates_matrix_size(states)
		return data

	#deciding the candidates matrix size...
	def get_candidates_matrix_size(self, states):
		invert_candidates = True
		size = 12
		if states == 12:
			invert_candidates = False
		elif states == 6:
			invert_candidates = False
			size = 6
		elif states == 4:
			invert_candidates = False
			size = 4
		elif states == 3:
			invert_candidates = False
			size = 3
		elif states == 2:
			invert_candidates = False
			size = 2
		return size, invert_candidates
	
	#formating the sequence...
	def sequence_to_string(self, sequence):
		m = ""
		for link in sequence:
			m += self.notes_to_string(link)
			m += "-"
		return m[:len(m)-1]

	#formating each link...
	def notes_to_string(self, notes):
		m = ""
		for n in notes:
			m += str(n)
			m += " "
		return m[:len(m)-1]

	#formating candidates matrix...
	def candidates_to_string(self):
		m = ""
		for r in range(len(self.candidates)):
			m += self.notes_to_string(self.candidates[r])
			if self.last_start == r:
				m += " <--"
			m += "\n"
		return m

	#setting up a certain Chain() from a string...
	def set_chain(self, string_notes):
		string_links = string_notes.split("-")
		self.base_data = self.get_base_data(string_links[0] + string_links[1])
		self.base = self.base_data["ordered"]
		self.candidates, self.iter_path, self.candidates_size = self.build_candidates_matrix(self.base)
		self.link_sizes = self.get_link_sizes(len(self.base))
		self.load_sequence(string_links)
		self.sequence_size = len(self.sequence)
		self.check_sequence_status()
	
	#loading sequence from a string...
	def load_sequence(self, string_links):
		self.sequence = []
		for l in string_links:
			self.sequence.append(self.pcs.string_to_notes(l))

	#the class prints itself...
	def __str__(self):
		return "-- Hi, I am a notes chain with constant pitch class set." + "\n" + \
				"-- My notes are: " + self.sequence_to_string(self.sequence) + "\n"