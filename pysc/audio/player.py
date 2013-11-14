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
