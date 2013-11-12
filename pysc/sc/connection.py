import soundcloud
import settings

class Client(object):
	def __init__(self):
		self.client = soundcloud.Client(client_id=settings.CLIENT_ID)

	def get_tracks(self, genre=None, limit=10):
		return self.client.get('/tracks', genres=genre, streamable=True, limit=limit)

	def get_stream_url(self, track):
		stream = self.client.get(track.stream_url, allow_redirects=False)
		return stream.location
