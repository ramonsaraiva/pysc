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
		if argc >= self.args:
			return True
		print(self.name + ': wrong parameters. Usage: ' + self.usage)
		return False

class NotFoundCommand(Command):
	def execute(self, args):
		print("command not found, try 'help' to see available commands")

class ExitCommand(Command):
	def __init__(self, manager):
		super(ExitCommand, self).__init__(manager)

	def execute(self, args):
		sys.exit()

class GenresCommand(Command):
	def __init__(self, manager):
		super(GenresCommand, self).__init__(manager)

	def execute(self, args):
		print('\n' + ' ~ '.join( self.manager.client.genres))
		print('\n* use \'play\' command to listen, example: \'play chillout\'')

class PlayCommand(Command):
	def __init__(self, manager):
		super(PlayCommand, self).__init__(manager)
		self.name = 'play'
		self.args = 1
		self.usage = 'play <genre>'

	def execute(self, args):
		if not self.check_args(len(args)):
			return

		genre = ' '.join(args).lower()

		if not genre in map(str.lower, self.manager.client.genres):
			print ('unknown genre, maybe mispelled?')
			return

		if not self.manager.client.get_tracks(genre=genre):
			print("sorry, we couldn't get any track.. maybe no internet connection?")
			return

		self.manager.client.clean_parameters()

		if not self.manager.splayer:
			self.manager.splayer = StreamPlayer(self.manager, self.manager.client.current_stream_url())
		else:
			self.manager.splayer.change(self.manager.client.current_stream_url())

		self.manager.splayer.play()
		print("now playing '" + self.manager.client.current_track().title + "'")

class PauseCommand(Command):
	def __init__(self, manager):
		super(PauseCommand, self).__init__(manager)
		self.args = 0

	def execute(self, args):
		self.manager.splayer.pause()
		print('player paused')

class ResumeCommand(Command):
	def __init__(self, manager):
		super(ResumeCommand, self).__init__(manager)
		self.args = 0

	def execute(self, args):
		self.manager.splayer.play()
		print('player resumed')

class NextCommand(Command):
	def __init__(self, manager):
		super(NextCommand, self).__init__(manager)
		self.args = 0

	def execute(self, args):
		self.manager.client.next_track()
		self.manager.splayer.change(self.manager.client.current_stream_url())
		print("now playing '" + self.manager.client.current_track().title + "'")

class PrevCommand(Command):
	def __init__(self, manager):
		super(PrevCommand, self).__init__(manager)
		self.args = 0

	def execute(self, args):
		self.manager.client.prev_track()
		self.manager.splayer.change(self.manager.client.current_stream_url())
		print('now playing \'' + self.manager.client.current_track().title + '\'')

class CommandManager(object):
	def __init__(self):
		self.client = Client()
		self.splayer = None

		self.commands = {
			'not_found': NotFoundCommand(None),
			'exit': ExitCommand(self),
			'genres': GenresCommand(self),
			'play': PlayCommand(self),
			'pause': PauseCommand(self),
			'resume': ResumeCommand(self),
			'next': NextCommand(self),
			'prev': PrevCommand(self),
		}

	def message_handler(self, bus, message):
		print 'message received!!!!'
		if message.type == gst.MESSAGE_EOS:
			print 'it is a END OF STREAM!!!!!!'
			commands['next'].execute('')
