from commands import CommandManager

class Terminal(object):
	def __init__(self):
		self.cmd_manager = CommandManager()
		self.router = {
			'not_found': self.cmd_manager.commands['not_found'],
			'exit': self.cmd_manager.commands['exit'],
			'play': self.cmd_manager.commands['play'],
		}

	def welcome(self):
		print 'welcome to pysc! soundcloud in your terminal ~ powered by soundcloud'
		print 'type \'genres\' to discover, or just \'help\' to see available commands'

	def loop(self):
		self.welcome()

		while 1:
			in_data = raw_input('-> ')

			params = in_data.split(' ')

			if len(params) > 1:
				command = params[0]
				arguments = params[1:]
			else:
				command = params[0]
				arguments = ''

			self.router.get(command, self.router['not_found']).execute(arguments)
