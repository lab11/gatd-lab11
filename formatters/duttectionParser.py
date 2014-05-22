import IPy
import json
import struct
import parser
import binascii
import datetime
import pytz
import time

class duttectionParser (parser.parser):

	name = 'Hemera Sensor Data'
	description = 'Light, humidity, temperature, & motion in Prabal\'s office.'

	def __init__ (self):
		pass

	def parse (self, data, meta, extra, settings):
		ret = {}

		values = struct.unpack('!10s H H H H 8B', data)

		gatd_profile_id    = values[0]
		ret['sequence']    = values[1]
		ret['temperature'] = values[2]
		ret['humidity']    = values[3]
		ret['light']       = values[4]
		ret['motion']      = bool(values[5])
		# ret['battery']     = values[6]

		# Standard GATD Footer
		ret['address'] = str(meta['addr'])
		ret['port']    = meta['port']
		ret['time']    = meta['time']
	
		return ret

