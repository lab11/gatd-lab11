import parser
import json

class bleAddrParser ():

	name = 'BLE Address Parser'
	description = 'Scans of BLE Addresses of all bluetooth low-energy devices in a location.'

        scanner_mapping = {
                #'mac address': 'some location in Berkeley'
                '1C:BA:8C:ED:ED:2A': ('104', '0'),
                '78:A5:04:CC:26:B0': ('102', '1'),
                '78:A5:04:DC:83:7C': ('auditorium', '2'),
                '1C:BA:8C:ED:E0:B2': ('204', '3'),
                '1C:BA:8C:9B:BC:57': ('203', '4')
                }

        superhero_mapping = {
                #'ble address': 'a superhero name'
                'e0:8f:e6:fa:33:dc': 'Miss Martian',
                'c5:61:7c:78:9f:43': 'Impulse',
                'e0:05:bf:ee:09:b9': 'Martian Manhunter',
                'd2:a1:1a:3a:60:d4': 'Deadpool',
                'eb:b2:3f:cb:dc:27': 'Flash',
                'c6:9b:58:f3:c1:a6': 'Doctor Strange',
                'd8:a4:2c:40:17:e4': 'Rogue',
                'd8:a6:a0:fd:ca:43': 'Question',
                'c8:52:a4:6b:ef:0b': 'Swamp Thing',
                'dc:e2:36:b8:db:2d': 'Cyclops',
                'd4:1b:1b:ba:0c:ff': 'Catwoman',
                'cf:53:9b:2a:84:d2': 'Doctor Fate',
                'ca:ba:56:5c:f0:fe': 'Green Goblin',
                'c9:0b:5c:b0:d4:54': 'Robin',
                'd9:79:95:5d:18:dd': 'Jean Grey',
                'c4:16:5d:79:de:3e': 'Static Shock',
                'f7:4b:c5:80:56:eb': 'Magneto',
                'ec:a8:bb:79:8d:74': 'Flash Gordon',
                'fb:49:10:95:b5:71': 'Garbage Man',
                'df:d4:1d:e0:ff:a8': 'Spiderman',
                'f4:af:36:71:d2:4d': 'Nick Fury',
                'c6:2d:d3:02:11:3f': 'Lex Luthor',
                'dc:e7:4c:53:25:72': 'Star-Lord',
                'f3:52:db:63:ca:6a': 'Doctor Octopus',
                'd1:ea:00:82:12:70': 'Groot',
                'f4:32:73:2e:65:16': 'Wolverine',
                'e5:e0:40:df:65:11': 'Space Ghost',
                'c4:ef:7d:19:3f:4b': 'Black Adam',
                'ce:ae:40:a1:68:b5': 'Juggernaut',
                'fb:0e:ae:b6:c5:15': 'Captain Planet',
                'd3:3a:15:17:10:74': 'Captain America',
                'd1:07:e5:3f:0c:be': 'Binary',
                'e9:f4:ac:28:5c:fe': 'Sandman',
                'e2:58:37:c0:50:73': 'Two-Face',
                'df:f1:0d:78:93:87': 'Zatanna',
                'd8:3e:72:90:bb:a7': 'Aquaman',
                'c1:f0:24:60:d0:66': 'Birdman',
                'c0:07:a3:69:a9:17': 'Rocket Raccoon',
                'e5:8a:37:f7:a2:60': 'Captain Britain',
                'fb:5c:80:11:f7:47': 'Ironman',
                'd1:26:82:a8:47:46': 'Raven',
                'd8:6f:dd:5a:dd:98': 'Nite Owl',
                'f9:f5:6b:43:4c:5f': 'General Zod',
                'c2:62:4a:d9:f6:1b': 'Doctor Doom',
                'de:76:80:67:c3:6a': 'Riddler',
                'f2:cc:83:34:11:62': 'Green Arrow',
                'd4:34:1b:d1:2a:f6': 'Brainiac',
                'e3:d4:75:e7:eb:1c': 'Blackout',
                'ca:39:64:b9:9f:f0': 'The Comedian',
                'd3:cb:0f:50:ee:32': 'Mister Freeze',
                'e2:77:d9:b4:21:8a': 'Rorschach',
                'ed:59:3a:a4:57:0a': 'Ant-Man',
                'ed:bc:ed:14:6b:bf': 'Dr. Manhattan',
                'd5:e0:fa:59:f4:e5': 'Poison Ivy',
                'd7:21:33:19:0a:b5': 'Thor',
                'ed:0c:a6:37:0a:e8': 'Solomon Grundy',
                'fe:9d:c1:f3:1f:8a': 'Quailman',
                'd4:be:a0:2d:f0:fb': 'Joker',
                'c8:5d:e7:42:97:8f': 'Hulk',
                'df:d4:20:25:eb:62': 'Loki',
                'fd:51:88:77:3d:b8': 'Cable',
                'c5:ef:3d:d9:3f:79': 'Crimson Dynamo',
                'ce:bd:be:59:4b:59': 'Penguin',
                'e7:38:c1:54:4f:60': 'Gambit',
                'fe:54:f3:19:7c:53': 'Kraven the Hunter',
                'd7:4a:c4:7d:0d:53': 'Batman',
                'cd:4e:73:c5:5e:63': 'Scarlet Witch',
                'e9:03:45:6b:7d:fd': 'Animal Man',
                'ea:f8:b0:c7:06:41': 'Harley Quinn',
                'e2:97:bd:07:e8:e4': 'Bane',
                'e1:59:1e:f2:24:aa': 'Alfred Pennyworth',
                'df:70:82:56:c1:3e': 'Superman',
                'e9:2e:38:a2:4a:28': 'Captain Canuck',
                'f8:e7:72:96:6c:cb': 'Batgirl'
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
                        self.scanner_mapping[ret['bbb_mac_addr']][0])
                    ret['location_id'] =  self.scanner_mapping[ret['bbb_mac_addr']][1]
                else:
                    ret['location_str'] = 'unknown'
                    ret['location_id'] = -1

                # add in a superhero identity
                if 'ble_addr' in ret and ret['ble_addr'] in self.superhero_mapping:
                    ret['uniqname'] = self.superhero_mapping[ret['ble_addr']]
                    ret['full_name'] = self.superhero_mapping[ret['ble_addr']]

            # add meta data to the dict
            ret['address'] = str(meta['addr'])
            ret['port']    = meta['port']
            ret['time']    = meta['time']

            return ret
            
