import struct

class airflowParser ():

	# Parameters for this profile
	name = 'Airflow'
	description = 'MEMS airflow sensor.'

	def __init__ (self):
		pass

	def parse (self, data, meta, extra, settings):
		ret = {}

		values = struct.unpack("!10BB", data[0:11])
		airflow_type = values[10]
		data = data[11:]

		if airflow_type == 0:
			values = struct.unpack("!BhL", data)
			ret['type'] = 'airflow_test'
			ret['version'] = values[0]
			ret['airflow_reading'] = values[1]
			if ret['airflow_reading'] > 7000:
				ret['airflow_state'] = 'on'
			else:
				ret['airflow_state'] = 'off'
			ret['seq_no'] = values[2]

		elif airflow_type == 1:
			values = struct.unpack("!BLLH5H", data)
			ret['type']    = 'breeze'
			ret['version'] = values[0]
			ret['seq_no']  = values[1]
			ret['total']   = values[2]
			ret['count']   = values[3]
			ret['airflow_reading'] = float(ret['total']/ret['count'])
			# if ret['airflow_reading'] > 7000:
			# 	ret['airflow_state'] = 'on'
			# else:
			# 	ret['airflow_state'] = 'off'

		ret['address'] = str(meta['addr'])
		ret['port']    = meta['port']
		ret['time']    = meta['time']

		return ret
