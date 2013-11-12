from audio.player import StreamPlayer
from sc.connection import Client
import sys

class Command(object):
	def __init__(self):
		self.name = ''
		self.args = 0
		self.usage = ''

	def check_args(self, argc):
		if self.args < argc:
			return False
		return True

	def execute(self, args):
		if not self.check_args(len(args)):
			print self.name + ': wrong parameters. Usage: ' + self.usage
			return

class ExitCommand(Command):
	def __init__(self):
		super(ExitCommand, self).__init__()
		self.name = 'exit'

	def execute(self, args):
		super(ExitCommand, self).execute(args)
		sys.exit()

class Terminal(object):

	def __init__(self):
		self.client = Client()
		self.splayer = None
		self.commands = {'exit': ExitCommand()}
		self.router = {'exit': self.commands['exit']}

	def welcome(self):
		print 'welcome to pysc! soundcloud in your terminal.'
		print 'type \'genres\' to discover, or just \'help\' to see available commands'

	def not_found(self, data):
		print 'sorry, command not found.'

	def exit(self, data):
		sys.exit()

	def pause(self, data):
		self.splayer.stop()
		print 'player paused'

	def resume(self, data):
		self.splayer.play()
		print 'player resumed'

	def change(self):
		self.splayer.change(self.client.current_stream_url())
		print 'now playing \'' + self.client.current_track().title + '\''

	def next(self, data):
		self.client.next_track()
		self.change()

	def prev(self, data):
		self.client.prev_track()
		self.change()

	def genre(self, data):
		self.client.get_tracks(genre=data[0])

		if not self.splayer:
			self.splayer = StreamPlayer(self.client.current_stream_url())
			print 'now playing \'' + self.client.current_track().title + '\''
		else:
			self.change()

		self.splayer.play()

	def add(self, data):
		#not implemented
		current_track = self.client.current_track()

	def loop(self):
		self.welcome()

		while 1:
			in_data = raw_input('-> ')

			params = in_data.split(' ')

			if len(params) > 1:
				command = params[0]
				arguments = params[1:]
			else:
				command = params[0]
				arguments = ''

			self.router.get(command, self.not_found).execute(arguments)
