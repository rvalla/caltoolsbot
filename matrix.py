import random as rd

class Matrix():
	"A matrix to make music"

	#building an instance of a Matrix...
	def __init__(self, module, string_matrix):
		self.mod = module #defining the cardinality of notes set to work (commonly 12)...
		self.h = None #height of the matrix...
		self.w = None #width of the matrix...
		self.max_in_cell = 0 #the maximum number of elements on any cell...
		self.data = [] #this is the matrix...
		self.r_status = [] #order of rows...
		self.c_status = [] #order of columns...
		self.swap_degraded = True #to check swap_candidates health...
		self.swap_candidates = None #the place to stores swap candidates...
		self.build_cells(string_matrix)
		self.build_status()

	#function to move the matrix in pitch space...
	def translate(self, t):
		self.swap_degraded = True
		for r in range(self.h):
			for c in range(self.w):
				self.data[r][c] = self.translate_notes(self.data[r][c], t)

	#function to move the matrix in pitch space...
	def invert(self):
		self.swap_degraded = True
		for r in range(self.h):
			for c in range(self.w):
				for v in range(len(self.data[r][c])):
					self.data[r][c][v] = -(self.data[r][c][v]) % self.mod

	#function to multiply elements in pitch space...
	def multiply(self, f):
		self.swap_degraded = True
		for r in range(self.h):
			for c in range(self.w):
				for v in range(len(self.data[r][c])):
					self.data[r][c][v] = (self.data[r][c][v] * f) % self.mod

	#function to transpose the matrix (inefficient)...
	def transpose(self):
		self.swap_degraded = True
		past_h = self.h
		past_w = self.w
		self.h = past_w
		self.w = past_h
		new_data = []
		for pr in range(past_w):
			new_row = []
			for pc in range(past_h):
				new_row.append(self.data[pc][pr])
			new_data.append(new_row)
		self.data = new_data
		self.transpose_status()

	#function to rotate the matrix (inefficient)...
	def rotate(self, direction):
		self.transpose()
		if direction > 0:
			self.r_status = self.r_status[::-1]
		else:
			self.c_status = self.c_status[::-1]

	#functions to change matrix status (order of rows and columns)...
	def shuffle_status(self):
		self.shuffle_rows()
		self.shuffle_columns()

	def shuffle_rows(self):
		rd.shuffle(self.r_status)

	def shuffle_columns(self):
		rd.shuffle(self.c_status)

	def set_status(self, new_r_status, new_c_status):
		self.set_r_status(new_r_status)
		self.set_c_status(new_c_status)

	def set_r_status(self, new_r_status):
		for r in range(self.h):
			new_r_status[r] = self.r_status[new_r_status[r]-1]
		self.r_status = new_r_status			

	def set_c_status(self, new_c_status):
		for c in range(self.w):
			new_c_status[c] = self.c_status[new_c_status[c]-1]
		self.c_status = new_c_status	

	def transpose_status(self):
		past_r_status = self.r_status
		self.r_status = self.c_status
		self.c_status = past_r_status

	#functions to make the swap operation...
	def swap_round(self):
		self.check_swap_health()
		swapable_notes = self.get_swapable_notes()
		for n in swapable_notes:
			self.swap_note(n)
				
	#function to swap a note...
	def swap_note(self, note):
		self.check_swap_health()
		targets = rd.sample(self.swap_candidates[note], 2)
		self.data[targets[0][0]][targets[0][1]].remove(note)
		self.data[targets[1][0]][targets[1][1]].remove(note)
		self.data[targets[0][0]][targets[1][1]].append(note)
		self.data[targets[1][0]][targets[0][1]].append(note)
		self.update_swap_candidates(note, targets)
		if len(self.data[targets[0][0]][targets[1][1]]) > self.max_in_cell or \
					len(self.data[targets[1][0]][targets[0][1]]) > self.max_in_cell:
			self.max_in_cell += 1
		else:
			self.update_max_in_cell()

	#function to swap a selected note...
	def swap_note_in_targets(self, note, targets):
		self.check_swap_health()
		self.data[self.r_status[targets[0][0]]][self.c_status[targets[0][1]]].remove(note)
		self.data[self.r_status[targets[1][0]]][self.c_status[targets[1][1]]].remove(note)
		self.data[self.r_status[targets[0][0]]][self.c_status[targets[1][1]]].append(note)
		self.data[self.r_status[targets[1][0]]][self.c_status[targets[0][1]]].append(note)
		self.update_swap_candidates(note, targets)
		if len(self.data[self.r_status[targets[0][0]]][self.c_status[targets[1][1]]]) > self.max_in_cell or \
					len(self.data[self.r_status[targets[1][0]]][self.c_status[targets[0][1]]]) > self.max_in_cell:
			self.max_in_cell += 1
		else:
			self.update_max_in_cell()

	#function to build a list of each ocurrence of each note coordinates...
	def build_swap_candidates(self):
		self.swap_candidates = [[] for n in range(self.mod)]
		for r in range(self.h):
			for c in range(self.w):
				for v in range(len(self.data[r][c])):
					self.swap_candidates[self.data[r][c][v]].append((r,c))

	#function to update swap_candidates after a swap...
	def update_swap_candidates(self, note, targets):
		self.swap_candidates[note].remove(targets[0])
		self.swap_candidates[note].remove(targets[1])
		self.swap_candidates[note].append((targets[0][0], targets[1][1]))
		self.swap_candidates[note].append((targets[1][0], targets[0][1]))

	#function to get a random order of swapable notes...
	def get_swapable_notes(self):
		notes = []
		for n in range(self.mod):
			if len(self.swap_candidates[n]) > 1:
				notes.append(n)
		return rd.sample(notes, len(notes))

	#function to check swap_candidates health...
	def check_swap_health(self):
		if self.swap_degraded:
			self.build_swap_candidates()
			self.swap_degraded = False

	#function to build the status (order of rows and columns)...
	def build_status(self):
		self.r_status = []
		self.c_status = []
		for r in range(self.h):
			self.r_status.append(r)
		for c in range(self.w):
			self.c_status.append(c)

	#function to build the cells of the matrix from a complete string...
	def build_cells(self, string_matrix):
		self.swap_degraded = True
		string_rows = string_matrix.split("/")
		for r in string_rows:
			row = []
			string_cell = r.split("-")
			for c in string_cell:
				notes = self.get_notes(c)
				row.append(notes)
				if self.max_in_cell < len(notes):
					self.max_in_cell = len(notes)
			self.data.append(row)
		self.h = len(self.data)
		self.w = len(self.data[0])
	
	#function to create a cell notes list...
	def get_notes(self, string_notes):
		notes = []
		for n in string_notes.split(" "):
			try:
				notes.append(int(n))
			except:
				pass
		return notes
	
	#getting a trasposition of a cell...
	def translate_notes(self, notes, t):
		new_notes = []
		for n in notes:
			new_notes.append((n+t)%self.mod)
		return new_notes
	
	#setting up matrix size...
	def set_size(self, w, h):
		self.h = h
		self.w = w

	#function to get notes from a cell in random order...
	def get_cell(self, r, c):
		rd.shuffle(self.data[self.r_status[r]][self.c_status[c]])
		return self.data[self.r_status[r]][self.c_status[c]]

	#function to get notes from a cell without shuffling notes...
	def get_static_cell(self, r, c):
		return self.data[self.r_status[r]][self.c_status[c]]

	#function to set a matrix cell...
	def set_cell(self, position, string_notes):
		self.swap_degraded = True
		notes = self.get_notes(string_notes)
		self.data[position[0]][position[1]] = notes
		if self.max_in_cell < len(notes):
			self.max_in_cell = len(notes)

	#function to update max_in_cell...
	def update_max_in_cell(self):
		self.max_in_cell = 0
		for r in range(self.h):
			for c in range(self.w):
				if self.max_in_cell < len(self.data[r][c]):
					self.max_in_cell = len(self.data[r][c])

	#function to create an empty matrix...
	def empty_matrix(self, width, height):
		self.swap_degraded = True
		self.set_size(width, height)
		self.max_in_cell = 0
		self.data = []
		for r in range(self.h):
			row = []
			for c in range(self.w):
				row.append([])
			self.data.append(row)
		self.build_status()
	
	#function to create a random matrix...
	def random_matrix(self, max_cell, width, height):
		self.swap_degraded = True
		self.set_size(width, height)
		self.max_in_cell = 0
		self.data = []
		for r in range(self.h):
			row = []
			for c in range(self.w):
				elements = rd.randint(0,max_cell)
				row.append(self.random_cell(elements))
				if self.max_in_cell < elements:
					self.max_in_cell = elements
			self.data.append(row)
		self.build_status()

	#creating a random cell...
	def random_cell(self, elements):
		notes = []
		for n in range(elements):
			notes.append(rd.randint(0, self.mod - 1))
		return notes

	#function to create a type 1 matrix...
	def build_type_one(self, notes):
		self.build_type_two(notes, notes)

	#function to create a type 2 matrix...
	def build_type_two(self, notes, other_notes):
		self.swap_degraded = True
		self.set_size(len(notes), len(other_notes))
		self.max_in_cell = 1
		self.data = []
		for o in other_notes:
			row = []
			for n in notes:
				row.append([(n+o)%self.mod])
			self.data.append(row)
		self.build_status()
	
	#function to build a matrix by translation...
	def translation_cycle(self, string_row, t):
		self.swap_degraded = True
		size = self.trasposition_cycle_size(t)
		first_row = self.get_first_cycle_row(string_row, size)
		self.set_size(size, size)
		self.max_in_cell = 1
		self.data = [first_row]
		for h in range(1, size):
			row = []
			for c in range(len(self.data[h-1])):
				row.append(self.translate_notes(self.data[h-1][(c-1)%size], t))
				if len(row[c]) > self.max_in_cell:
					self.max_in_cell = len(row[c])
			self.data.append(row)
		self.build_status()

	#function to get the first row of a matrix by trasposition...
	def get_first_cycle_row(self, string_row, size):
		cells = string_row.split("-")
		if not len(cells) == size:
			self.repair_first_cycle_row(cells, size)
		return [self.get_notes(c) for c in cells]
		
	#function to repair a bad first row for a matrix by trasposition...
	def repair_first_cycle_row(self, cells_candidate, size):
		if len(cells_candidate) > size:
			return cells_candidate[0:size]
		else:
			difference = size - len(cells_candidate)
			for i in range(difference):
				cells_candidate.append("")

	#function to know a matrix by trasposition size...
	def trasposition_cycle_size(self, t):
		return int(self.lowest_multiple(self.mod, t)/t)

	#function to know the lowest multiple of two numbers...
	def lowest_multiple(self, a, b):
		n = 1
		for i in range(1, b + 1, 1):
			n = a * i #Checking a multiples...
			if (n%b == 0):
				break #We save the minumun which is b multiple too...
		return n

	#function to build a matrix from a closed chain...
	def from_closed_chain(self, string_chain):
		chain = string_chain.split("-")
		if len(chain)%2 == 1 and len(chain)>4:
			size = self.from_chain_size(len(chain))
			self.empty_matrix(size, size)
			r = 0
			c = 0
			for l in range(1, len(chain)-1):
					self.set_cell((r,c), chain[l])
					if l%2 == 0:
						c += 1
					else:
						r += 1
			self.set_cell((0, self.w - 1), chain[0])		
		else:
			self.w = None
			self.h = None
			self.data = None

	#function to know a matrix from chain size...
	def from_chain_size(self, links_count):
		return (links_count - 1)//2
	
	#function to return the pcs in a row...
	def get_clean_row(self):
		notes = []
		for c in range(self.w):
			for n in self.data[1][c]:
				if not self.is_in(n, notes):
					notes.append(n)
		return notes

	#function to return the pcs in a column...
	def get_clean_column(self):
		notes = []
		for r in range(self.h):
			for n in self.data[r][1]:
				if not self.is_in(n, notes):
					notes.append(n)
		return notes

	#function to check if an element is already in a list...
	def is_in(self, new_note, notes):
		is_in = False
		for n in notes:
			if new_note == n:
				is_in = True
				break
		return is_in

	#printing matrix information...
	def __str__(self):
		return "-- Hi, I am a matrix to make music" + "\n" \
				+ "-- I have " + str(self.w) + " columns and " + str(self.h) + " rows" + "\n" \
				+ "-- I think I could sound perfectly." + "\n" \
				+ "-- My current status is: " + str(self.r_status) + ", " + str(self.c_status)

	#function to print the matrix...
	def print_matrix(self):
		print(self.matrix_to_string())
	
	#formatting the matrix...
	def matrix_to_string(self):
		m = ""
		for r in range(self.h):
			row = "| "
			for c in range(self.w):
				row += self.cell_text(self.data[self.r_status[r]][self.c_status[c]])
				row += " | "
			m += row + "\n"
			if r < self.h - 1:
				m += self.line_string(len(row)-3)
		return m
	
	#drawing a line...
	def line_string(self, row_length):
		m = " "
		for r in range(row_length):
			m += "-"
		return m + "\n"

	#trying to print cells content...
	def cell_text(self, cell):
		c_size = len(cell)
		c_text = ""
		if c_size == 0:
			for l in range(self.max_in_cell * 3):
				c_text += " "
		else:
			for l in range(self.max_in_cell):
				if l < c_size:
					n = cell[l]
					if n < 10:
						c_text += " "
					c_text += str(n)
					c_text += " "
				else:
					c_text += "   "
		return c_text

	#to format de matrix as a html table...
	def matrix_to_html(self):
		m = "<table>\n"
		for r in range(self.h):
			row = "<tr>\n"
			for c in range(self.w):
				row += "<td>"
				for n in self.data[self.r_status[r]][self.c_status[c]]:
					row += str(n) + " "
				row += "</td>\n"
			row += "</tr>\n"
			m += row
		m += "</table>\n"
		return m

	#to format de matrix as a latex tabular...
	def matrix_to_latex(self):
		m = "\\begin{tabular}{"
		for c in range(self.w):
			m += " c "
			if c < (self.w - 2):
				m += "|"
		m += "}\n"
		for r in range(self.h):
			row = ""
			for c in range(self.w):
				for n in self.data[self.r_status[r]][self.c_status[c]]:
					row += str(n) + " "
				if c < (self.w - 2):
					row += "&"
			row += "\\\\ \\hline\n"
			m += row
		m += "\\end{tabular}\n"
		return m
