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

	def genre(self, data):
		self.client.get_tracks(genre=data[0])
		print len(self.client.tracks)

		current_stream_url = self.client.current_stream_url()

		if not self.splayer:
			self.splayer = StreamPlayer(current_stream_url)
		else:
			self.splayer.change(current_stream_url)

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
		}
