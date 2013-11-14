from audio.player import StreamPlayer
from sc.connection import Client
import sys
import gst
import os
from threading import Thread

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
	def execute(self, args):
		self.manager.splayer.quit_mainloop()
		self.manager.splayer.join()
		sys.exit()

class ClearCommand(Command):
	def execute(self, args):
		os.system('cls' if os.name=='nt' else 'clear')

class GenresCommand(Command):
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

		print('getting tracks..')

		if not self.manager.client.get_tracks(genre=genre):
			print("sorry, we couldn't get any track.. maybe no internet connection?")
			return

		self.manager.client.clean_parameters()
		self.manager.update_player()

class PauseCommand(Command):
	def execute(self, args):
		self.manager.splayer.pause()
		print('player paused')

class ResumeCommand(Command):
	def execute(self, args):
		self.manager.splayer.play()
		print('player resumed')

class NextCommand(Command):
	def execute(self, args):
		self.manager.client.next_track()
		self.manager.update_player()

class PrevCommand(Command):
	def execute(self, args):
		self.manager.client.prev_track()
		self.manager.update_player()

class LoopCommand(Command):
	def execute(self, args):
		print('looping track!')
		self.manager.client.looping = True

class UnloopCommand(Command):
	def execute(self, args):
		print('no more loop!')
		self.manager.client.looping = False

class CommandManager(object):
	def __init__(self):
		self.client = Client()
		self.splayer = StreamPlayer(self)
		self.splayer.start()

		self.commands = {
			'not_found': NotFoundCommand(None),
			'exit': ExitCommand(self),
			'clear': ClearCommand(None),
			'genres': GenresCommand(self),
			'play': PlayCommand(self),
			'pause': PauseCommand(self),
			'resume': ResumeCommand(self),
			'next': NextCommand(self),
			'prev': PrevCommand(self),
			'loop': LoopCommand(self),
			'unloop': UnloopCommand(self),
			#'forwards': ForwardsCommand(self),
			#'backwards': BackwardsCommand(self),
		}

	def update_player(self):
		self.splayer.change(self.client.current_stream_url())
		print('now playing \'' + self.client.current_track().title + '\'')

		if self.client.looping:
			print("looping track, use 'unloop' to disable looping")

	def gst_message_handler(self, bus, message):
		if message.type == gst.MESSAGE_EOS:
			if not self.client.looping:
				self.client.next_track()
			self.update_player()
