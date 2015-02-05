import parser

class bleServiceParser (parser.parser):

	name = 'BLE Service Parser'
	description = 'Discovers services of BLE devices that have been scanned.'
	no_parse = True

	def __init__ (self):
		pass
