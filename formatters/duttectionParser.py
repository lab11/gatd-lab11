import IPy
import json
import struct
import parser
import binascii
import datetime
import pytz
import time
import sys

class duttectionParser (parser.parser):

	name = 'Hemera Sensor Data'
	description = 'Light, humidity, temperature, & motion.'
	no_parse = False

	def __init__ (self):
		pass

	def parse (self, data, meta, extra, settings):
		ret = {}

		try:
			jsonpkt = json.loads(data[10:])
			ret     = json.loads(jsonpkt['data'])

		except ValueError:
			values = struct.unpack('!10s H H H H B B', data[0:20])

			# ret['profile_id']  = values[0]
			ret['sequence']    = values[1]
			ret['temperature'] = values[2]
			ret['humidity']    = values[3]
			ret['light']       = values[4]
			ret['motion']      = bool(values[5])
			ret['id']          = values[6]
			# ret['battery']     = values[6]

			# Standard GATD Footer
			ret['address'] = str(meta['addr'])
			ret['port']    = meta['port']
			ret['time']    = meta['time']
	
		return ret

