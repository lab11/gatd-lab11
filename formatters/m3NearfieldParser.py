import parser
import struct

class m3NearfieldParser (parser.parser):

	name = 'm3 Nearfield Radio'
	description = 'Michigan Micro Mote bridge parser.'

	def __init__ (self):
		pass

	def ecc(self, data_in):
		P5 = \
				((data_in>>19)&0x1) ^\
				((data_in>>18)&0x1) ^\
				((data_in>>17)&0x1) ^\
				((data_in>>16)&0x1) ^\
				((data_in>>15)&0x1) ^\
				((data_in>>14)&0x1) ^\
				((data_in>>13)&0x1) ^\
				((data_in>>12)&0x1) ^\
				((data_in>>11)&0x1)
		P4 = \
				((data_in>>19)&0x1) ^\
				((data_in>>18)&0x1) ^\
				((data_in>>10)&0x1) ^\
				((data_in>>9 )&0x1) ^\
				((data_in>>8 )&0x1) ^\
				((data_in>>7 )&0x1) ^\
				((data_in>>6 )&0x1) ^\
				((data_in>>5 )&0x1) ^\
				((data_in>>4 )&0x1);
		P3 = \
				((data_in>>17)&0x1) ^\
				((data_in>>16)&0x1) ^\
				((data_in>>15)&0x1) ^\
				((data_in>>14)&0x1) ^\
				((data_in>>10)&0x1) ^\
				((data_in>>9 )&0x1) ^\
				((data_in>>8 )&0x1) ^\
				((data_in>>7 )&0x1) ^\
				((data_in>>3 )&0x1) ^\
				((data_in>>2 )&0x1) ^\
				((data_in>>1 )&0x1);
		P2 = \
				((data_in>>17)&0x1) ^\
				((data_in>>16)&0x1) ^\
				((data_in>>13)&0x1) ^\
				((data_in>>12)&0x1) ^\
				((data_in>>10)&0x1) ^\
				((data_in>>9 )&0x1) ^\
				((data_in>>6 )&0x1) ^\
				((data_in>>5 )&0x1) ^\
				((data_in>>3 )&0x1) ^\
				((data_in>>2 )&0x1) ^\
				((data_in>>0 )&0x1);
		P1 = \
				((data_in>>19)&0x1) ^\
				((data_in>>17)&0x1) ^\
				((data_in>>15)&0x1) ^\
				((data_in>>13)&0x1) ^\
				((data_in>>11)&0x1) ^\
				((data_in>>10)&0x1) ^\
				((data_in>>8 )&0x1) ^\
				((data_in>>6 )&0x1) ^\
				((data_in>>4 )&0x1) ^\
				((data_in>>3 )&0x1) ^\
				((data_in>>1 )&0x1) ^\
				((data_in>>0 )&0x1);
		P0 = \
				((data_in>>19)&0x1) ^\
				((data_in>>18)&0x1) ^\
				((data_in>>17)&0x1) ^\
				((data_in>>16)&0x1) ^\
				((data_in>>15)&0x1) ^\
				((data_in>>14)&0x1) ^\
				((data_in>>13)&0x1) ^\
				((data_in>>12)&0x1) ^\
				((data_in>>11)&0x1) ^\
				((data_in>>10)&0x1) ^\
				((data_in>>9)&0x1) ^\
				((data_in>>8)&0x1) ^\
				((data_in>>7)&0x1) ^\
				((data_in>>6)&0x1) ^\
				((data_in>>5)&0x1) ^\
				((data_in>>4)&0x1) ^\
				((data_in>>3)&0x1) ^\
				((data_in>>2)&0x1) ^\
				((data_in>>1)&0x1) ^\
				((data_in>>0)&0x1) ^\
				P5 ^ P4 ^ P3 ^ P2 ^ P1 ;
		data_out = (P5<<5)|(P4<<4)|(P3<<3)|(P2<<2)|(P1<<1)|(P0<<0);
		return data_out;

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

		# data[29:26] = header = 0xF
		# data[25:22] = 4bit counter
		# data[21:20] = 2bit stack id
		# data[19:6] = 14bit temperature code
		# data[5:0] = 6bit ECC for counter+temperature part

		ret['ecc'] = temp & 0x3f
		ret['temp_code'] = (temp >> 6) & 0x3fff
		ret['stack_id'] = (temp >> 20) & 0x3
		ret['counter'] = (temp >> 22) & 0xf
		ret['header'] = (temp >> 26) & 0xf


		ret['computed_ecc'] = self.ecc(ret['counter'] << 16 | ret['stack_id'] << 14 | ret['temp_code'])
		ret['ecc_match'] = ret['computed_ecc'] == ret['ecc']

		if ret['stack_id'] == 1:
			ret['temperature'] = (ret['temp_code'] - 538.54)/2.6667
		elif ret['stack_id'] == 2:
			ret['temperature'] = (ret['temp_code'] - 501.46)/2.9381

		ret['sample'] = temp
		ret['time']   = meta['time']

		return ret
