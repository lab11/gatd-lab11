import IPy
import json
import struct
import parser
import binascii
import datetime
import pytz
import time

class opoParser (parser.parser):

	name = 'Opo'
	description = 'Human inter-contact measurement.'

	def __init__ (self):
		pass

	def parse (self, data, meta, extra, settings):
		def convert_bcd(raw_t):
			h = hex(raw_t)
			t = int(h.split('x')[1])
			return t

		ret = {}
		n = datetime.datetime.now()

		# Opo-Specific
		s = struct.unpack('!10s I I H H 8B H 8B', data)
		gatd_profile_id   = s[0]
		ret['seq'] = s[1]
		ret['reset_counter'] = s[2]
		ret['rx_id'] = s[3]
		ret['tx_id'] = s[4]
		ret['m_full_time'] = list(s[5:13])
		ret['dt_ul_rf'] = s[13]
		ret['last_full_time'] = list(s[14:22])
		ret['range'] = float(ret['dt_ul_rf'])/32000.0 * 340.29 - .12

		for i in range(len(ret['full_time'])):
			"""
			Time Format, from 0-8: second, minute, hour, day (wrong), date, month, year (no century)
			"""
			ret['full_time'][i] = convert_bcd(ret['full_time'][i])
			ret['last_full_time'][i] = convert_bcd(ret['last_full_time'][i])

		ret['full_time'][7] += 2000 # accounting for century bits in month

		true_full_time = [0, n.second, n.minute, n.hour, n.weekday(), n.day, n.month, n.year]
		ret['true_full_time'] = true_full_time

		sec = ret['full_time'][1]
		minute = ret['full_time'][2]
		hr = ret['full_time'][3]
		d = ret['full_time'][5]
		month = ret['full_time'][6]
		year = ret['full_time'][7]

		lsec = ret['last_full_time'][1]
		lminute = ret['last_full_time'][2]
		lhr = ret['last_full_time'][3]
		ld = ret['last_full_time'][5]
		lmonth = ret['last_full_time'][6]
		lyear = ret['last_full_time'][7]

		m_date = datetime.datetime(year, month, d, hr, minute, sec, tzinfo=pytz.timezone('US/Eastern'))
		l_date = datetime.datetime(lyear, lmonth, ld, lhr, lminute, lsec, tzinfo=pytz.timezone('US/Eastern'))

		tdiff = n - m_date

		adjusted_l_date = l_date + tdiff

		ret['adjusted_last_full_timestamp'] = time.mktime(adjusted_l_date.timetuple())

		# Standard GATD Footer
		ret['address'] = str(meta['addr'])
		ret['port']    = meta['port']
		ret['time']    = meta['time']

		return ret
