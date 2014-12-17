#!/usr/bin/env python

import IPy
import json
import sys

try:
	import socketIO_client as sioc
except ImportError:
	print('Could not import the socket.io client library.')
	print('sudo pip install socketIO-client')
	sys.exit(1)

import logging
logging.basicConfig()

SOCKETIO_HOST      = 'gatd.eecs.umich.edu'
SOCKETIO_PORT      = 8082
SOCKETIO_NAMESPACE = 'stream'

query = {'profile_id': '7aiOPJapXF',
         'ccid_mac': {'$in': ['c0:98:e5:49:4d:df:c2:df',
                              'c0:98:e5:49:4d:df:b6:c5',
                              'c0:98:e5:49:4d:df:dc:75',
                              'c0:98:e5:49:4d:df:b8:ad',
                              'c0:98:e5:49:4d:df:cc:91',
                              'c0:98:e5:49:4d:df:e8:26',
                              'c0:98:e5:49:4d:df:b7:16',
                              '00:12:6d:43:4f:e2:7c:aa']},
         'type': 'coilcube_freq',
         'time': 120000}

pkts = {}


class stream_receiver (sioc.BaseNamespace):
	def on_reconnect (self):
		if 'time' in query:
			del query['time']
		stream_namespace.emit('query', query)

	def on_connect (self):
		stream_namespace.emit('query', query)

	def on_data (self, *args):
		pkt = args[0]
		#print(pkt)

		if 'freq' not in pkt:
			return

		if pkt['ccid'] not in pkts:
			pkts[pkt['ccid']] = []

		pkts[pkt['ccid']].append(pkt['freq'])

		avg = sum(pkts[pkt['ccid']])/float(len(pkts[pkt['ccid']]))

		print('{} {} {:f} {:f}'.format(pkt['time'], pkt['ccid_mac'], pkt['freq'], avg))

socketIO = sioc.SocketIO(SOCKETIO_HOST, SOCKETIO_PORT)
stream_namespace = socketIO.define(stream_receiver,
	'/{}'.format(SOCKETIO_NAMESPACE))

socketIO.wait()
