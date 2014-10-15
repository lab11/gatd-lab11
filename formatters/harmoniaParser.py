import IPy
import json
import struct
import parser
import binascii
import datetime
import pytz
import time

class harmoniaParser ( ):

	name = 'Harmonia'
	description = 'Harmonic Localization System.'

	def __init__ (self):
		pass

	def parse (self, data, meta, extra, settings):
		def convert_bcd(raw_t):
			h = hex(raw_t)
			t = int(h.split('x')[1])
			return t

		ret = {}
		n = datetime.datetime.fromtimestamp(meta['time']/1000)

		#Harmonia-specific
		s = struct.unpack('!10s I I H H 8B H 8B', data)
		gatd_profile_id   = s[0]
		ret['seq'] = s[1]
		ret['reset_counter'] = s[2]
		ret['id'] = s[3]
		ret['last_heard_id'] = s[4]
		ret['m_full_time'] = list(s[5:13])
		ret['dt_ul_rf'] = s[13]
		ret['last_full_time'] = list(s[14:22])
		ret['range'] = float(ret['dt_ul_rf'])/32000.0 * 340.29 - .12

		return ret
