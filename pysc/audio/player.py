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

	def build_pipeline(self):
		if self.pipeline:
			self.pipeline.set_state(gst.STATE_NULL)
			self.pipeline = None

		self.pipeline = gst.Pipeline()
		self.pipeline.add(self.player)

	def connect_signals(self):
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.connect('message', self.manager.message_handler)

	def pause(self):
		self.pipeline.set_state(gst.STATE_PAUSED)

	def play(self):
		self.pipeline.set_state(gst.STATE_PLAYING)

	def change(self, uri):
		self.build_pipeline()
		self.player.set_property('uri', uri)
		self.play()
