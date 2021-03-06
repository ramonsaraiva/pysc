import gobject
gobject.threads_init()

import pygst
pygst.require('0.10')
import gst

from threading import Thread

class StreamPlayer(Thread):
	def __init__(self, manager):
		Thread.__init__(self)

		self.manager = manager

		self.player = gst.element_factory_make('playbin2', 'theplayer')
		self.src = gst.element_factory_make('audiotestsrc', 'src')

		self.pipeline = None
		self.build_pipeline()

		self.audiosink = gst.element_factory_make('autoaudiosink', 'audiosink')
		self.audiosink.set_property('async-handling', True)

		self.control = gst.Controller(self.src, 'volume')
		self.control.set_interpolation_mode('volume', gst.INTERPOLATE_LINEAR)

		self.control.set('volume', 0, 0.0)
		self.control.set('volume', 2 * gst.SECOND, 1.0)
		self.control.set('volume', 4 * gst.SECOND, 0.0)
		self.control.set('volume', 6 * gst.SECOND, 1.0)

		self.connect_signals()
		self.mainloop = gobject.MainLoop()

	def run(self):
		self.mainloop.run()

	def quit_mainloop(self):
		self.mainloop.quit()

	def build_pipeline(self):
		if self.pipeline:
			self.pipeline.set_state(gst.STATE_NULL)
			self.pipeline = None

		self.pipeline = gst.Pipeline()
		self.pipeline.add(self.player)

	def connect_signals(self):
		self.bus = self.pipeline.get_bus()
		self.bus.add_signal_watch()
		self.bus.connect('message::eos', self.manager.gst_message_handler)

	def pause(self):
		self.pipeline.set_state(gst.STATE_PAUSED)

	def play(self):
		self.pipeline.set_state(gst.STATE_PLAYING)

	def change(self, uri):
		self.pipeline.set_state(gst.STATE_NULL)
		self.player.set_property('uri', uri)
		self.play()

	def query_pos(self):
		try:
			pos, format = self.player.query_position(gst.FORMAT_TIME)
		except:
			pos = gst.CLOCK_TIME_NONE

		try:
			dur, format = self.player.query_duration(gst.FORMAT_TIME)
		except:
			dur = gst.CLOCK_TIME_NONE

		return (pos, dur)

	def seek(self, location, bypos):
		location = (location + self.query_pos()[0] if bypos else location)

		try:
			event = gst.event_new_seek(1.0, gst.FORMAT_TIME,
				gst.SEEK_FLAG_FLUSH,
				gst.SEEK_TYPE_SET, location,
				gst.SEEK_TYPE_NONE, 0)
		except:
			return False

		res = self.player.send_event(event)
		if res:
			self.player.set_new_stream_time(0L)
			return True
		return False
