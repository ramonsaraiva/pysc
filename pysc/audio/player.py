import gobject
gobject.threads_init()

import pygst
pygst.require('0.10')
import gst

import time

class StreamPlayer(object):
	def __init__(self, manager, channel):
		self.manager = manager

		self.player = gst.element_factory_make('playbin2', 'theplayer')
		self.player.set_property('uri', channel)

		self.pipeline = None
		self.build_pipeline()

		self.audiosink = gst.element_factory_make('autoaudiosink', 'audiosink')
		self.audiosink.set_property('async-handling', True)

		self.connect_signals()

		self.mainloop = gobject.MainLoop()
		self.mainloop.run()

	def build_pipeline(self):
		if self.pipeline:
			self.pipeline.set_state(gst.STATE_NULL)
			self.pipeline = None

		self.pipeline = gst.Pipeline()
		self.pipeline.add(self.player)

	def connect_signals(self):
		self.bus = self.pipeline.get_bus()
		self.bus.add_signal_watch()

		self.bus.connect('message::eos', self.manager.eos_handler)

	def pause(self):
		self.pipeline.set_state(gst.STATE_PAUSED)

	def play(self):
		self.pipeline.set_state(gst.STATE_PLAYING)

	def change(self, uri):
		self.build_pipeline()
		self.player.set_property('uri', uri)
		self.play()
