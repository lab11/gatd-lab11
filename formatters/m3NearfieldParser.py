import parser

class m3NearfieldParser (parser.parser):

	name = 'm3 Nearfield Radio'
	description = 'Michigan Micro Mote bridge parser.'
	#no_parse = True

	def __init__ (self):
		pass

	def parse (self, data, meta, extra, settings):
		ret = {}

		# Opo-Specific
		s = struct.unpack('!10s 28B', data)
		gatd_profile_id   = s[0]
		ret['bytes'] = s[1:29]

		return ret
