from audio.player import StreamPlayer
from sc.connection import Client
import sys

class Command(object):
	def __init__(self, manager):
		self.manager = manager
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

class NotFoundCommand(Command):
	def execute(self, args):
		print 'command not found, try \'help\' to see available commands'

class ExitCommand(Command):
	def __init__(self, manager):
		super(ExitCommand, self).__init__(manager)
		self.name = 'exit'

	def execute(self, args):
		super(ExitCommand, self).execute(args)
		sys.exit()

class PlayCommand(Command):
	def __init__(self, manager):
		super(PlayCommand, self).__init__(manager)
		self.name = 'play'
		self.args = 1
		self.usage = 'play <genre>'

	def execute(self, args):
		super(PlayCommand, self).execute(args)

		self.manager.client.get_tracks(genre=args[0])

		if not self.manager.splayer:
			self.manager.splayer = StreamPlayer(self.manager.client.current_stream_url())
		else:
			self.manager.splayer.change(self.manager.client.current_stream_url())

		self.manager.splayer.play()
		print 'now playing \'' + self.manager.client.current_track().title + '\''

class CommandManager(object):
	def __init__(self):
		self.client = Client()
		self.splayer = None

		self.commands = {
			'not_found': NotFoundCommand(None),
			'exit': ExitCommand(self),
			'play': PlayCommand(self),
		}
