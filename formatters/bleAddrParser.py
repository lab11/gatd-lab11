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
                'df:f1:0d:78:93:87': 'Captain Britain',
                'd1:ea:00:82:12:70': 'Genesis',
                'dc:e2:36:b8:db:2d': 'Ironman',
                'e2:77:d9:b4:21:8a': 'Offspring',
                'fd:51:88:77:3d:b8': 'Birdman',
                'f8:e7:72:96:6c:cb': 'Giganta',
                'c1:f0:24:60:d0:66': 'Hit-Girl',
                'c8:5d:e7:42:97:8f': 'Bumblebee',
                'e9:2e:38:a2:4a:28': 'Abomination',
                'e0:05:bf:ee:09:b9': 'Blink',
                'e0:8f:e6:fa:33:dc': 'Aqualad',
                'd5:e0:fa:59:f4:e5': 'Captain Atom',
                'fb:5c:80:11:f7:47': 'Ant-Man',
                'e3:d4:75:e7:eb:1c': 'Iron Fist',
                'e9:f4:ac:28:5c:fe': 'Beetle',
                'ed:59:3a:a4:57:0a': 'Beast',
                'c4:16:5d:79:de:3e': 'Captain Planet',
                'df:d4:20:25:eb:62': 'Sunspot',
                'c0:07:a3:69:a9:17': 'Cyclops',
                'c2:62:4a:d9:f6:1b': 'Nightcrawler',
                'c5:61:7c:78:9f:43': 'Silverclaw',
                'e5:e0:40:df:65:11': 'Supergirl',
                'd3:cb:0f:50:ee:32': 'Chuck Norris',
                'eb:b2:3f:cb:dc:27': 'Black Cat'
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
            
