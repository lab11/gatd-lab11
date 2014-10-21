import parser
import struct

class m3NearfieldParser (parser.parser):

	name = 'm3 Nearfield Radio'
	description = 'Michigan Micro Mote bridge parser.'

	def __init__ (self):
		pass

	def parse (self, data, meta, extra, settings):
		ret = {}

		l = len(data) - 10

		# Opo-Specific
		s = struct.unpack('!10s {}B'.format(l), data)
		gatd_profile_id   = s[0]

		temp = 0
		for b in s[1:]:
			temp <<= 1
			temp |= b

		ret['ecc'] = temp & 0x3f
		ret['temp_code'] = (temp >> 6) & 0xffff
		ret['counter'] = (temp >> 22) & 0xf
		ret['header'] = (temp >> 26) & 0xf

		ret['sample'] = temp
		ret['time']   = meta['time']

		return ret
