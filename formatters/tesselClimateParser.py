import parser

class tesselClimateParser (parser.parser):

	# Parameters for this profile
	name = 'Tessel Climate'
	description = 'Temperature and humidity from a Tessel board.'
	no_parse = True

	def __init__ (self):
		pass