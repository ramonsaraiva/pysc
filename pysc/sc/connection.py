import soundcloud
import settings

class Client(object):
	def __init__(self):
		self.client = soundcloud.Client(client_id=settings.CLIENT_ID)
		self.tracks = []
		self.it = 0

	def get_tracks(self, genre=None, limit=10):
		self.tracks = self.client.get('/tracks', genres=genre, streamable=True, limit=limit)
		self.it = 0

	def get_stream_url(self):
		stream = self.client.get(self.tracks[self.it].stream_url, allow_redirects=False)
		return stream.location
