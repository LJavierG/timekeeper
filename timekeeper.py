import curses
import curses.wrapper
import time
import os

class TimeSession:
	def __init__(self):
		self.categories = {}
		self.path = ".time/"
		self.log_file = "time.log"
		self.config_file = "keeper.rc"

	def new_config_here(self):
		"""
		creates the file hierarchy for the default config file and logs folder
		"""
		try:
			if self.path != "":
				os.mkdir(self.path)
		except OSError:
			pass
		with open(self.path + self.config_file,"w") as f:
			pass

	def load_config(self, filename=None):
		"""
		load configuration from a specified file or default if not specified,
		also calls to new_config_here in case of first invocation.
		"""
		if filename is not None:
			fsplit = filename.split("/")
			self.config_file = fsplit[-1]
			fsplit.pop()
			if len(fsplit) > 0:
				self.path = "/".join(fsplit)
				if filename[0] == "/":
					self.path = "/" + self.path
			else:
				self.path = ""

		filename = self.path + self.config_file

		try:
			f = open(filename)
		except:
			self.new_config_here()
			return

		try:
			lines = f.readlines()
			for line in lines:
				if line.startsWith("#"):
					continue
				self.categories[line.split(":")[0]] = line.split(":")[1].strip("\n")
		except e:
			print("error while parsing config file")
			raise e

	def event(self, e):
		"""
		response to e event
		"""
		pass

	def debug(self):
		print(self.categories)


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
