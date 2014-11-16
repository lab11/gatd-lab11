import parser
import json

class bleAddrParser ():

	name = 'BLE Address Parser'
	description = 'Scans of BLE Addresses of all bluetooth low-energy devices in a location.'

        # old information from Terraswarm Demo
        #scanner_mapping = {
        #        #'mac address': 'some location in Berkeley'
        #        '1C:BA:8C:ED:ED:2A': ('104', '0'),
        #        '78:A5:04:CC:26:B0': ('102', '1'),
        #        '78:A5:04:DC:83:7C': ('auditorium', '2'),
        #        '1C:BA:8C:ED:E0:B2': ('204', '3'),
        #        '1C:BA:8C:9B:BC:57': ('203', '4')
        #        }

        scanner_mapping = {
                '00:0C:29:73:8A:3C': ('University of Michigan|BBB|4908', '0')
                }

        superhero_mapping = {
                #'ble address': 'a superhero name'
                'e0:8f:e6:fa:33:dc': ('None', 'Miss Martian'),
                'c5:61:7c:78:9f:43': ('None', 'Impulse'),
                'e0:05:bf:ee:09:b9': ('None', 'Martian Manhunter'),
                'd2:a1:1a:3a:60:d4': ('None', 'Deadpool'),
                'eb:b2:3f:cb:dc:27': ('None', 'Flash'),
                'c6:9b:58:f3:c1:a6': ('None', 'Doctor Strange'),
                'd8:a4:2c:40:17:e4': ('None', 'Rogue'),
                'd8:a6:a0:fd:ca:43': ('None', 'Question'),
                'c8:52:a4:6b:ef:0b': ('None', 'Swamp Thing'),
                'dc:e2:36:b8:db:2d': ('None', 'Cyclops'),
                'd4:1b:1b:ba:0c:ff': ('None', 'Catwoman'),
                'cf:53:9b:2a:84:d2': ('None', 'Doctor Fate'),
                'ca:ba:56:5c:f0:fe': ('None', 'Green Goblin'),
                'c9:0b:5c:b0:d4:54': ('None', 'Robin'),
                'd9:79:95:5d:18:dd': ('None', 'Jean Grey'),
                'c4:16:5d:79:de:3e': ('None', 'Static Shock'),
                'f7:4b:c5:80:56:eb': ('None', 'Magneto'),
                'ec:a8:bb:79:8d:74': ('None', 'Flash Gordon'),
                'fb:49:10:95:b5:71': ('None', 'Garbage Man'),
                'df:d4:1d:e0:ff:a8': ('None', 'Spiderman'),
                'f4:af:36:71:d2:4d': ('None', 'Nick Fury'),
                'c6:2d:d3:02:11:3f': ('None', 'Lex Luthor'),
                'dc:e7:4c:53:25:72': ('None', 'Star-Lord'),
                'f3:52:db:63:ca:6a': ('None', 'Doctor Octopus'),
                'd1:ea:00:82:12:70': ('None', 'Groot'),
                'f4:32:73:2e:65:16': ('None', 'Wolverine'),
                'e5:e0:40:df:65:11': ('None', 'Space Ghost'),
                'c4:ef:7d:19:3f:4b': ('None', 'Black Adam'),
                'ce:ae:40:a1:68:b5': ('None', 'Juggernaut'),
                'fb:0e:ae:b6:c5:15': ('None', 'Captain Planet'),
                'd3:3a:15:17:10:74': ('None', 'Captain America'),
                'd1:07:e5:3f:0c:be': ('None', 'Binary'),
                'e9:f4:ac:28:5c:fe': ('None', 'Sandman'),
                'e2:58:37:c0:50:73': ('None', 'Two-Face'),
                'df:f1:0d:78:93:87': ('None', 'Zatanna'),
                'd8:3e:72:90:bb:a7': ('None', 'Aquaman'),
                'c1:f0:24:60:d0:66': ('None', 'Birdman'),
                'c0:07:a3:69:a9:17': ('None', 'Rocket Raccoon'),
                'e5:8a:37:f7:a2:60': ('None', 'Captain Britain'),
                'fb:5c:80:11:f7:47': ('None', 'Ironman'),
                'd1:26:82:a8:47:46': ('None', 'Raven'),
                'd8:6f:dd:5a:dd:98': ('None', 'Nite Owl'),
                'f9:f5:6b:43:4c:5f': ('None', 'General Zod'),
                'c2:62:4a:d9:f6:1b': ('None', 'Doctor Doom'),
                'de:76:80:67:c3:6a': ('None', 'Riddler'),
                'f2:cc:83:34:11:62': ('None', 'Green Arrow'),
                'd4:34:1b:d1:2a:f6': ('None', 'Brainiac'),
                'e3:d4:75:e7:eb:1c': ('None', 'Blackout'),
                'ca:39:64:b9:9f:f0': ('None', 'The Comedian'),
                'd3:cb:0f:50:ee:32': ('None', 'Mister Freeze'),
                'e2:77:d9:b4:21:8a': ('None', 'Rorschach'),
                'ed:59:3a:a4:57:0a': ('None', 'Ant-Man'),
                'ed:bc:ed:14:6b:bf': ('None', 'Dr. Manhattan'),
                'd5:e0:fa:59:f4:e5': ('None', 'Poison Ivy'),
                'd7:21:33:19:0a:b5': ('None', 'Thor'),
                'ed:0c:a6:37:0a:e8': ('None', 'Solomon Grundy'),
                'fe:9d:c1:f3:1f:8a': ('None', 'Quailman'),
                'd4:be:a0:2d:f0:fb': ('None', 'Joker'),
                'c8:5d:e7:42:97:8f': ('None', 'Hulk'),
                'df:d4:20:25:eb:62': ('None', 'Loki'),
                'fd:51:88:77:3d:b8': ('None', 'Cable'),
                'c5:ef:3d:d9:3f:79': ('None', 'Crimson Dynamo'),
                'ce:bd:be:59:4b:59': ('None', 'Penguin'),
                'e7:38:c1:54:4f:60': ('None', 'Gambit'),
                'fe:54:f3:19:7c:53': ('None', 'Kraven the Hunter'),
                'd7:4a:c4:7d:0d:53': ('None', 'Batman'),
                'cd:4e:73:c5:5e:63': ('None', 'Scarlet Witch'),
                'e9:03:45:6b:7d:fd': ('None', 'Animal Man'),
                'ea:f8:b0:c7:06:41': ('None', 'Harley Quinn'),
                'e2:97:bd:07:e8:e4': ('None', 'Bane'),
                'e1:59:1e:f2:24:aa': ('None', 'Alfred Pennyworth'),
                'df:70:82:56:c1:3e': ('None', 'Superman'),
                'e9:2e:38:a2:4a:28': ('None', 'Captain Canuck'),
                'f8:e7:72:96:6c:cb': ('None', 'Batgirl'),
                'e2:a7:7f:78:34:24': ('None', 'The Halderman')
                }

        normalPeople_mapping = {
                'ec:84:04:f4:4a:07': ('nealjack', 'Neal Jackson'),
                'e2:a7:7f:78:34:24': ('jhalderm', 'Alex Halderman'),
                'f9:97:1e:8b:e7:27': ('brghena', 'Branden Ghena'),
                'ee:b7:8c:0d:8d:4d': ('bradjc', 'Brad Campbell'),
                'e8:74:72:8f:e4:57': ('wwhuang', 'William Huang'),
                'ca:a3:bb:ea:94:5b': ('mclarkk', 'Meghan Clark'),
                'd1:c6:df:67:1c:60': ('rohitram', 'Rohit Ramesh'),
                'f0:76:0f:09:b8:63': ('nklugman', 'Noah Klugman'),
                'ec:6d:04:74:fa:69': ('yhguo', 'Yihua Guo'),
                'f4:bb:3c:af:99:6c': ('bpkempke', 'Ben Kempke'),
                'db:eb:52:c7:90:74': ('sdebruin', 'Sam DeBruin'),
                'f7:fd:9a:80:91:79': ('genevee', 'Genevieve Flaspohler'),
                'cb:14:57:58:b4:89': ('cfwelch', 'Charlie Welch'),
                'de:da:9c:f1:75:94': ('davadria', 'David Adrian'),
                'cd:49:fa:6a:98:b1': ('None', 'Spare Blue Force'),
                'ca:2d:39:50:f0:b1': ('ppannuto', 'Pat Pannuto'),
                'ee:47:fa:fe:ac:c2': ('evrobert', 'Eva Robert'),
                'c4:26:da:a4:72:c3': ('samkuo', 'Ye-Sheng Kuo'),
                'f1:7c:98:6e:b9:d1': ('jdejong', 'Jessica De Jong'),
                'e0:5e:5a:28:85:e3': ('tzachari', 'Thomas Zachariah'),
                'ca:28:2b:08:f3:f7': ('adkinsjd', 'Josh Adkins')
                }

	def __init__ (self):
		pass

        def parse (self, data, meta, extra, settings):
            ret = json.loads(json.loads(data[10:])['data'])

            # do parsing for terraSwarm demo
            #if 'location_str' in ret and ret['location_str'] == 'terraswarm-demo':
            #    # find the location string
            #    if 'bbb_mac_addr' in ret and ret['bbb_mac_addr'] in self.scanner_mapping:
            #        ret['location_str'] = (
            #            'USA|California|Berkeley|UCB|Clark Kerr|Conference Center|' +
            #            self.scanner_mapping[ret['bbb_mac_addr']][0])
            #        ret['location_id'] =  self.scanner_mapping[ret['bbb_mac_addr']][1]
            #    else:
            #        ret['location_str'] = 'unknown'
            #        ret['location_id'] = -1

            #    # add in a superhero identity
            #    if 'ble_addr' in ret and ret['ble_addr'] in self.superhero_mapping:
            #        ret['uniqname'] = self.superhero_mapping[ret['ble_addr']]
            #        ret['full_name'] = self.superhero_mapping[ret['ble_addr']]

            # location parsing
            if 'location_str' in ret and ret['location_str'] == 'demo':
                # find the location string
                if 'scanner_macAddr' in ret and ret['scanner_macAddr'] in self.scanner_mapping:
                    ret['location_str'] = self.scanner_mapping[ret['scanner_macAddr']][0]
                    ret['location_id'] = self.scanner_mapping[ret['scanner_macAddr']][1]
                else:
                    ret['location_str'] = 'unknown'
                    ret['location_id'] = -1

            # add in a superhero identity
            if 'ble_addr' in ret and ret['ble_addr'] in self.superhero_mapping:
                ret['uniqname'] = self.superhero_mapping[ret['ble_addr']][0]
                ret['full_name'] = self.superhero_mapping[ret['ble_addr']][1]

            # add normal people too
            if 'ble_addr' in ret and ret['ble_addr'] in self.normalPeople_mapping:
                ret['uniqname'] = self.normalPeople_mapping[ret['ble_addr']][0]
                ret['full_name'] = self.normalPeople_mapping[ret['ble_addr']][1]


            # add meta data to the dict
            ret['address'] = str(meta['addr'])
            ret['port']    = meta['port']
            ret['time']    = meta['time']

            return ret
            
