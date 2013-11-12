import pygst
pygst.require('0.10')
import gst

import time

class StreamPlayer(object):
	def __init__(self, channel):
		self.pipeline = gst.Pipeline("pipe")

		self.player = gst.element_factory_make("playbin2", "theplayer")
		self.pipeline.add(self.player)

		self.audiosink = gst.element_factory_make("autoaudiosink", 'audiosink')
		self.audiosink.set_property('async-handling', True)

		self.player.set_property('uri', channel)

	def new_pipeline(self):
		self.pipeline.set_state(gst.STATE_NULL)
		self.pipeline = None

		self.pipeline = gst.Pipeline()
		self.pipeline.add(self.player)

	def pause(self):
		self.pipeline.set_state(gst.STATE_PAUSED)

	def play(self):
		self.pipeline.set_state(gst.STATE_PLAYING)

	def change(self, uri):
		self.new_pipeline()

		self.player.set_property('uri', uri)
		self.pipeline.set_state(gst.STATE_PLAYING)
