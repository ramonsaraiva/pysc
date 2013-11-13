import soundcloud
import settings

class Client(object):
	def __init__(self):
		self.client = soundcloud.Client(client_id=settings.CLIENT_ID)
		self.genres = [
			'80s', 'Abstract', 'Acid Jazz', 'Acoustic', 'Acoustic Rock',
			'African', 'Alternative', 'Ambient', 'Americana', 'Arabic',
			'Avantgarde', 'Bachata', 'Ballads', 'Bhangra', 'Blues',
			'Blues Rock', 'Bossa Nova', 'Breakbeats', 'Chanson',
			'Chillout', 'Chiptunes', 'Choir', 'Classic Rock', 'Classical',
			'Classical Guitar', 'Contemporary', 'Country', 'Cumbia',
			'Dance', 'Dancehall', 'Death Metal', 'Dirty South', 'Disco',
			'Dream Pop', 'Drum & Bass', 'Dub', 'Dubstep', 'Easy Listening',
			'Electro House', 'Electronic', 'Electronic Pop', 'Electronic Rock',
			'Folk', 'Folk Rock', 'Funk', 'Glitch', 'Gospel', 'Grime', 'Grindcore',
			'Grunge', 'Hard Rock', 'Hardcore', 'Heavy Metal', 'Hip-Hop', 'House',
			'Indie', 'Indie Pop', 'Industrial Metal', 'Instrumental',
			'Instrumental Rock', 'J-Pop', 'Jazz', 'Jazz Funk', 'Jazz Fusion',
			'K-Pop', 'Latin', 'Latin Jazz', 'Mambo', 'Metalcore', 'Middle Eastern',
			'Minimal', 'Modern Jazz', 'Moombahton', 'New Wave', 'Nu Jazz',
			'Opera', 'Orchestral', 'Piano', 'Pop', 'Post Hardcore', 'Post Rock',
			'Progressive House', 'Progressive Metal', 'Progressive Rock', 'Punk',
			'R&B', 'Rap', 'Reggae', 'Reggaeton', 'Riddim', 'Rock', 'Rocn \'n\' Roll',
			'Salsa', 'Samba', 'Shoegaze', 'Singer / Songwriter', 'Smooth Jazz', 'Soul',
			'Synth Pop', 'Tech House', 'Techno', 'Trash Metal', 'Trance', 'Trap',
			'Trip-hop', 'Turntablism', 'Underground',
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
		try:
			stream = self.client.get(self.current_track().stream_url, allow_redirects=False)
			location = stream.location
		except:
			self.next_track()
			location = self.current_stream_url()
		return location
