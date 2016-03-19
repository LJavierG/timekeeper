import curses
import curses.wrapper
import time
import os

class Category:
	def __init__(self, name, parent=None, init_time=0):
		self.name = name
		self._time = init_time
		self.subcategories = []
		self.parent = parent
		if self.parent is not None:
			self.level = self.parent.level + 1
			self.parent.stack(self)
		else:
			self.level = 0

	def time(self):
		return self._time + sum([cat.time() for cat in self.subcategories])

	def tick(self,nsec=1):
		self._time += nsec

	def stack(self, newsubcat):
		self.subcategories.append(newsubcat)

	def indent(self):
		myid = self.parent.subcategories.index(self)
		if myid is not 0:
			self.parent.subcategories.remove(self)
			self.parent = self.parent.subcategories[myid-1]
			self.parent.stack(self)
			self.level += 1
			for cat in self.subcategories:
				cat.level += 1

	def unindent(self):
		if self.parent.parent is not None:
			self.parent.subcategories.remove(self)
			self.parent = self.parent.parent
			self.parent.stack(self)
			self.level -= 1
			for cat in self.subcategories:
				cat.level -= 1

	def move_up(self):
		myid = self.parent.subcategories.index(self)
		if myid > 0:
			aux = self.parent.subcategories[myid-1]
			self.parent.subcategories[myid-1] = self.parent.subcategories[myid]
			self.parent.subcategories[myid] = aux

	def move_down(self):
		myid = self.parent.subcategories.indexOf(self)
		if myid < len(self.parent.subcategories) - 1:
			aux = self.parent.subcategories[myid+1]
			self.parent.subcategories[myid+1] = self.parent.subcategories[myid]
			self.parent.subcategories[myid] = aux

	def debug(self):
		print "\t"*self.level + self.name
		for cat in self.subcategories:
			cat.debug()

	def __str__(self):
		return "<"+str(self.level)+"-"+self.name+":"+str(len(self.subcategories))+">"


class TimeSession:
	def __init__(self):
		#categories is a dict indexed by a character and that contains
		#the index of a list of ['str', 'level', 'seconds'] in a list aux_categories
		#each of those elements should be mutable
		self.categories = {}
		self.root_category = Category("root")
		self.tab = "."
		self.path = ".time/"
		self.log_file = "time.log"
		self.config_file = "keeper.rc"

	def new_config_here(self):
		"""
		creates the file hierarchy for the default config file and log folder
		"""
		try:
			if self.path != "":
				os.mkdir(self.path)
		except OSError:
			pass
		with open(self.path + self.config_file,"w") as f:
			pass

	def new_log_here(self):
		"""
		creates the file hierarchy for the default log file and folder
		"""
		try:
			if self.path != "":
				os.mkdir(self.path)
		except OSError:
			pass
		with open(self.path + self.config_file,"w") as f:
			pass

	def parse_filename(self, filename):
		if filename is not None:
			fsplit = filename.split("/")
			base_file = fsplit[-1]
			fsplit.pop()
			if len(fsplit) > 0:
				self.path = "/".join(fsplit)
				if filename[0] == "/":
					self.path = "/" + self.path
			else:
				self.path = ""
		return base_file

	def load_config(self, filename=None):
		"""
		load configuration from a specified file or default if not specified,
		also calls to new_config_here in case of first invocation.
		"""
		cf = self.parse_filename(filename)
		if cf is not None:
			self.config_file = cf
		filename = "/".join([self.path,self.config_file])

		try:
			f = open(filename)
		except:
			self.new_config_here()
			return

		try:
			lines = f.readlines()
			for line in lines:
				if line[0] is "#" or line in ["", "\n"]:
					continue
				dots = 0
				while line[dots] is self.tab:
					dots += 1
				sline = line.split(":")
				newc = Category(sline[1].strip("\n"), self.root_category)
				self.categories[sline[0][dots:]] = newc
				while dots > 0:
					newc.indent()
					dots -= 1
		except:
			print("error while parsing config file")
			raise

	def parse_logs(self, filename=None):
		"""
		parse the log file and load total seconds in categories
		"""
		lf = parse_filename(filename)
		if lf is not None:
			self.log_file = lf
		filename = "/".join([self.path,self.log_file])

		try:
			f = open(filename)
		except:
			self.new_logs_here()
			return

	def write_log_key(self, key):
		pass
		#with open(self.log_file + key, "a") as f:
		#	f.write(

	def on_event(self, e):
		"""
		response to e event
		"""
		pass

	def debug(self):
		"""
		just a simple debugging method
		"""
		print(self.categories)
		self.root_category.debug()


def main(stdscr):
	curses.noecho()
	curses.cbreak()
	stdscr.keypad(1)
	pad = curses.newpad(100, 100)
	#  These loops fill the pad with letters; this is
	# explained in the next section
	for y in range(0, 100):
		for x in range(0, 100):
			try:
				pad.addch(y,x, ord('a') + (x*x+y*y) % 26)
			except curses.error:
				pass
	#  Displays a section of the pad in the middle of the screen
	pad.refresh(0,0, 5,5, 20,75)
	time.sleep(10)

#curses.wrapper(main)

#pruebas:
import sys
ts=TimeSession()
ts.load_config(sys.argv[1])
ts.debug()

