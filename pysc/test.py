from sc.connection import Client
from audio.player import StreamPlayer

if __name__ == '__main__':
	client = Client()
	tracks = client.get_tracks(genre='electronic')
	it = 0

	print "it -> " + str(it)
	print "now playing -> " + tracks[it].title

	player = StreamPlayer(client.get_stream_url(tracks[it]))
	player.play()

	while 1:
		cmd = raw_input('cmd?')

		if cmd == 'q':
			break;
		elif cmd == 'n':
			it += 1
			track = tracks[(it) % len(tracks)]
			print "it -> " + str(it)
			print "now playing -> " + track.title
			new = client.get_stream_url(track)
			print new
			player.stop()
			player.change(new)
			player.play()
