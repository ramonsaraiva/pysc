import soundcloud
import settings

class Client(object):
	def __init__(self):
		self.client = soundcloud.Client(client_id=settings.CLIENT_ID)
		self.genres = [
			'80s', 'abstract', 'acid-jazz', 'acoustic', 'acoustic-rock', 'african', 'alternative',
			'ambient', 'americana', 'arabic', 'avantgarde', 'bachata', 'ballads', 'bhangra', 'blues',
			'blues-rock', 'bossa-nova', 'breakbeats', 'chanson', 'chillout', 'chiptunes', 'choir', 'classic-rock',
		]

		self.tracks = []
		self.it = 0

	def get_tracks(self, genre=None):
		try:
			self.tracks = self.client.get('/tracks', genres=genre, streamable=True, limit=settings.TRACKS_PER_PAG)
			self.it = 0
			return True
		except:
			return False

	def current_track(self):
		if not self.tracks:
			return None
		return self.tracks[self.it % len(self.tracks)]

	def next_track(self):
		self.it += 1

	def prev_track(self):
		self.it += 1

	def current_stream_url(self):
		stream = self.client.get(self.current_track().stream_url, allow_redirects=False)
		return stream.location
