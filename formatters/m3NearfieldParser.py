import parser
import struct

class m3NearfieldParser (parser.parser):

	name = 'm3 Nearfield Radio'
	description = 'Michigan Micro Mote bridge parser.'

	def __init__ (self):
		pass

	def parse (self, data, meta, extra, settings):
		ret = {}

		# Opo-Specific
		s = struct.unpack('!10s 28B', data)
		gatd_profile_id   = s[0]

		temp = 0
		for b in s[1:]:
			temp <<= 1
			temp |= b

		ret['sample'] = temp
		ret['time']   = meta['time']

		return ret
