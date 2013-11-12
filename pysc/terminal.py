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
		print('welcome to pysc! soundcloud in your terminal ~ powered by soundcloud')
		print('type \'genres\' to discover, or just \'help\' to see available commands')

	def loop(self):
		self.welcome()

		while 1:
			data = raw_input('>>> ')

			data = data.split(' ')

			if len(data) > 1:
				cmd = data[0]
				args = data[1:]
			else:
				cmd = data[0]
				args = ''

			self.router.get(cmd, self.router['not_found']).execute(args)
