from audio.player import StreamPlayer
from sc.connection import Client

class Terminal(object):

	def __init__(self):
		self.client = Client()
		self.splayer = None
		self.commands = {}

	def welcome(self):
		print 'welcome to pysc! soundcloud in your terminal.'
		print 'type \'genres\' to discover, or just \'help\' to see available commands'

	def not_found(self, data):
		print 'sorry, command not found.'

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

			self.commands.get(command, self.not_found)(arguments)

	def load_commands(self):
		self.commands = {
			'genre': self.genre,
			'add': self.add,
			'pause': self.pause,
			'resume': self.resume,
			'next': self.next,
			'prev': self.prev,
		}
