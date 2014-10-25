import parser
import json

class bleAddrParser ():

	name = 'BLE Address Parser'
	description = 'Scans of BLE Addresses of all bluetooth low-energy devices in a location.'

        scanner_mapping = {
                #'mac address': 'some location in Berkeley'
                '1C:BA:8C:ED:ED:2A': 'test',
                '00:0C:29:73:8A:3C': 'tucker'
                }

        superhero_mapping = {
                #'ble address': 'a superhero name'
                'c8:5d:e7:42:97:8f': 'TestNode1',
                'c4:16:5d:79:de:3e': 'TestNode2',
                'ed:59:3a:a4:57:0a': 'TestNode3'
                }

	def __init__ (self):
		pass

        def parse (self, data, meta, extra, settings):
            ret = json.loads(json.loads(data[10:])['data'])

            # do parsing for terraSwarm demo
            if 'location_str' in ret and ret['location_str'] == 'terraswarm-demo':
                # find the location string
                if 'bbb_mac_addr' in ret and ret['bbb_mac_addr'] in self.scanner_mapping:
                    ret['location_str'] = (
                        'USA|California|Berkeley|UCB|Clark Kerr|Conference Center|' +
                        self.scanner_mapping[ret['bbb_mac_addr']])
                else:
                    ret['location_str'] = 'unknown'

                # add in a superhero identity
                if 'ble_addr' in ret and ret['ble_addr'] in self.superhero_mapping:
                    ret['uniqname'] = self.superhero_mapping[ret['ble_addr']]
                    ret['full_name'] = self.superhero_mapping[ret['ble_addr']]

            # add meta data to the dict
            ret['address'] = str(meta['addr'])
            ret['port']    = meta['port']
            ret['time']    = meta['time']

            return ret
            
