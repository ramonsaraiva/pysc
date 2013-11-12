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
			print 'now playing \'' + self.manager.client.current_track().title + '\''
		else:
			self.change()

		self.manager.splayer.play()

class CommandManager(object):
	def __init__(self, client, splayer):
		self.client = client
		self.splayer = splayer

		self.commands = {
			'exit': ExitCommand(self),
			'play': PlayCommand(self),
		}

class Terminal(object):
	def __init__(self):
		self.cmanager = CommandManager(Client(), None)
		self.router = {
			'exit': self.cmanager.commands['exit'],
			'play': self.cmanager.commands['play']
		}

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
