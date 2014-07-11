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

		ret['address'] = str(meta['addr'])
		ret['port']    = meta['port']
		ret['time']    = meta['time']

		return ret
