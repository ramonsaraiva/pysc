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

	def error(self, msg):
		print (self.name + ': ' + msg + ' Usage: ' + self.name + ' ' + self.usage)

	def check_args(self, argc):
		if argc >= self.args:
			return True
		self.error('wrong parameters.')
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
		self.usage = '<genre>'

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

class SeekCommand(Command):
	def __init__(self, manager):
		super(SeekCommand, self).__init__(manager)
		self.args = 1
		self.usage = '<seconds>'

	def check_args(self, argc, args):
		if not super(SeekCommand, self).check_args(argc):
			return False

		try:
			secs = int(args[0])
		except:
			self.error('seconds must be an integer')
			return False

		if secs <= 0:
			self.error('seconds must be bigger than 0.')
			return False

		return True

class SimpleSeekCommand(SeekCommand):
	def __init__(self, manager):
		super(SimpleSeekCommand, self).__init__(manager)
		self.name = 'seek'

	def execute(self, args):
		if not self.check_args(len(args), args):
			return

		secs = int(args[0]) * 1000000000

		if not self.manager.splayer.seek(secs, False):
			self.error('unable to seek, number too big.')
			return
		print('seeked to ' + args[0] + ' seconds')


class ForwardsCommand(SeekCommand):
	def __init__(self, manager):
		super(ForwardsCommand, self).__init__(manager)
		self.name = 'forwards'

	def execute(self, args):
		if not self.check_args(len(args), args):
			return

		secs = int(args[0]) * 1000000000

		if not self.manager.splayer.seek(secs, True):
			self.error('unable to go forwards, number too big.')
			return
		print('forwarded ' + args[0] + ' seconds')

class BackwardsCommand(SeekCommand):
	def __init__(self, manager):
		super(BackwardsCommand, self).__init__(manager)
		self.name = 'backwards'

	def execute(self, args):
		if not self.check_args(len(args), args):
			return

		secs = int(args[0]) * 1000000000

		if not self.manager.splayer.seek(-secs, True):
			self.error('unable to go backwards, number too big.')
			return
		print('backwarded ' + args[0] + ' seconds')

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
			'seek': SimpleSeekCommand(self),
			'forwards': ForwardsCommand(self),
			'backwards': BackwardsCommand(self),
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
