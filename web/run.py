#!/usr/bin/env python3

import re
import glob
import jinja2 as jinja
import sys
import os
import tempfile
from sh import bower
from sh import cp
from sh import rm
from sh import mv
from sh import ln

try:
	import pyinotify
except ImportError:
	print('Missing pyinotify')
	print('\tsudo pip-python3 install pyinotify')
	print('')
	raise

import subprocess
import shlex
import threading

def usage():
	print("{0} -- Autobuild demo website".format(sys.argv[0]))
	print('')
	print('  --no-bower  By default, bower is run when this script starts')
	print('  --once      By default, the script monitors this directory and rebuilds'
	      '              whenever a website source file changes.')
	print('  --no-server By default, the script will start a webserver on port 8000'
	      '              when the site is built. This is very useful because the actual'
	      '              directory is replaced every time.'
	      '              (implied by --once)')
	print('')
	sys.exit()

if ('-h' in sys.argv) or ('--help' in sys.argv) or ('-?' in sys.argv):
	usage()

# First update bower
if '--no-bower' not in sys.argv:
	print("Updating bower...")
	bower('install')


def build_site():
	print("Building website...")
	jinja_env = jinja.Environment(loader=jinja.FileSystemLoader(['.', 'templates']))

	BUILT_DIR = 'built'
	DIRECTORIES = ('demos', 'work-in-progress', 'raw', '.')
	DESCRIPTIONS = {
			'demos':"""\
	Polished pseudo-production demos. While liable to go down at any time (this is
	research after all!), these are projects in a more-or-less "working" state.""",
			'work-in-progress':"""\
	New projects we're working on building right now. Can be hit-or-miss if these will
	be working at any given time. Don't rely on these pages if you're showing
	something off ;)""",
			'raw':"""\
	An "under-the-hood" view into the raw data streams that power our demos. To
	build queries yourself, check out the "Streams" demo above!""",
			'.':"Uncategorized legacy pages",
	}

	try:
		WORKING_DIR = tempfile.mkdtemp()

		demos = {}
		for directory in DIRECTORIES:
			demos[directory] = []

			for filename in glob.glob(directory + '/*.jinja'):
				basedir, name = os.path.split(filename)
				name = os.path.splitext(name)[0]
				outputname = os.path.join(WORKING_DIR, name + '.html')

				demos[directory].append(name + '.html')

				output = jinja_env.get_template(filename).render()

				with open(outputname, 'w') as f:
					f.write(output)
			for filename in glob.glob(directory + '/*.html'):
				basedir, name = os.path.split(filename)
				dst = os.path.join(WORKING_DIR, name)
				demos[directory].append(name)
				cp(filename, dst)

		categories = []
		for directory in DIRECTORIES:
			demo_list = ''
			for filename in sorted(demos[directory]):
				name = os.path.splitext(filename)[0].title()
				demo_list += jinja_env.get_template('demo_item.jinja').render(name=name, path=filename)
			category = jinja_env.get_template('demo_category.jinja').render(
					category=directory,
					description=DESCRIPTIONS[directory],
					demos=demo_list,
					)
			categories.append(category)

		index = jinja_env.get_template('index.jinja').render(categories=categories)
		with open(os.path.join(WORKING_DIR, 'index.html'), 'w') as f:
			f.write(index)

		rm('-rf', BUILT_DIR)
		mv(WORKING_DIR, BUILT_DIR)
		for d in ('bower_components', 'css', 'images', 'js'):
			ln('-s', '../'+d, BUILT_DIR)
	except:
		print("Unexpected error building site. Working build directory at:")
		print("\t{0}".format(WORKING_DIR))
		print("")
		raise

build_site()
if '--once' in sys.argv:
	sys.exit()

class AsyncCommand():
	def __init__(self, cmd):
		self.cmd = cmd
		self.proc = None

	def run(self):
		def target():
			print("Serving website")
			#args = shlex.split(self.cmd)
			args = self.cmd
			self.proc = subprocess.Popen(
					args,
					shell=True,
					cwd='built/',
					)

			print('[web] ### Worker process terminated')

		thread = threading.Thread(target=target)
		thread.deamon=True
		thread.start()

	def kill(self):
		self.proc.kill()
		self.proc.wait(timeout=1)

# Based off of when-changed utility from
# http://github.com/joh/when-changed
class WhenChanged(pyinotify.ProcessEvent):
	exclude = re.compile(r'^\..*\.sw[px]*$|^4913$|.~$')

	def kill_server(self):
		try:
			self.ac.kill()
		except AttributeError:
			pass

	def serve(self):
		try:
			self.ac.kill()
		except AttributeError:
			self.ac = AsyncCommand('python3 -m http.server 8000')

		self.ac.run()

	def is_interested(self, path):
		basename = os.path.basename(path)

		if self.exclude.match(basename):
			return False
		if 'built' in path:
			return False
		if '.git/' in path:
			return False

		if basename == 'run.py':
			print("#"*80)
			print("About to exec a new instance of self since run.py was edited")
			print("  Killing child web server first")
			self.kill_server()
			os.execl('./run.py', 'run.py', '--no-bower')

		print('Rebuilding because {0} changed'.format(path))
		return True

	def process(self, event):
		path = event.pathname
		if self.is_interested(path):
			build_site()
			self.serve()

	def process_IN_CREATE(self, event):
		return self.process(event)

	def process_IN_CLOSE_WRITE(self, event):
		return self.process(event)

	def run(self):
		wm = pyinotify.WatchManager()
		notifier = pyinotify.Notifier(wm, self)

		mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CREATE
		#watched = set()
		wm.add_watch('.', mask, rec=True, auto_add=True)

		self.serve()
		print('Monitoring for changes')
		notifier.loop()

wc = WhenChanged()
try:
	wc.run()
except KeyboardInterrupt:
	print('')
	print('Keyboard Interrupt. Quitting.')
	wc.kill_server()
	print('')
	sys.exit()
