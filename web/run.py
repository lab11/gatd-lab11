#!/usr/bin/env python3

import argparse
import glob
import http.server
import jinja2 as jinja
import sys
import os
import tempfile
from sh import bower
from sh import cp
from sh import rm
from sh import mv
from sh import ln
import time
import watchdog.observers
import watchdog.events
import watchdog.utils.unicode_paths

parser = argparse.ArgumentParser()
parser.add_argument('--no-bower',
                    action='store_true',
                    help='Do not run bower at the beginning.')
parser.add_argument('--debug',
                    action='store_true',
                    help='Run a local webserver')
parser.add_argument('--monitor',
                    action='store_true',
                    help='Do not watch for changes')
args = parser.parse_args()

def build_site():
	print("Building website...")
	je = jinja.Environment(
		loader=jinja.FileSystemLoader(['.', 'templates']))

	BUILT_DIR = 'built'
	DIRECTORIES = ('demos', 'work-in-progress', 'raw', '.')

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

				output = je.get_template(filename).render()

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
				demo_list += je.get_template('demo_item.jinja').render(
					name=name,
					path=filename
					)
			category = je.get_template('demo_category_{}.jinja'
						.format(directory)).render(
							demos=demo_list,
							)
			categories.append(category)

		index = je.get_template('index.jinja').render(
			categories=categories
			)
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

class FileWatcher (watchdog.events.PatternMatchingEventHandler):
	def on_any_event (self, event):
		src_path = watchdog.utils.unicode_paths.decode(event.src_path)
	#	if not event.is_directory and \
	#	   '/built' not in src_path and \
	#	   '/bower_components' not in src_path:
		if src_path[-6:] == 'run.py':
			print("#"*80)
			print("About to exec a new instance since run.py was edited")
			try:
				httpd.shutdown()
			except NameError:
				print("exec'ing via filewatcher path")
				os.execl(sys.argv[0], *sys.argv)
		else:
			build_site();


# First update bower
if not args.no_bower:
	print("Updating bower...")
	bower('install')

# Rebuild the website HTML
build_site()

# Optionally run a file monitor to re-run build_site()
if args.monitor:
	print('Watching for file changes...')
	observer = watchdog.observers.Observer()
	observer.schedule(FileWatcher(patterns=['*.html', '*.jinja', '*.py'],
	                              ignore_patterns=['*/built/*',
	                                               '*/bower_components/*']),
	                  '.',
	                  recursive=True)
	observer.start()

# Optionally run a local web server
if args.debug:
	print('Running a local webserver...')
	httpd = http.server.HTTPServer(('0.0.0.0', 8000),
	                               http.server.SimpleHTTPRequestHandler)

	try:
		httpd.serve_forever()
		print("Destorying httpd server")
		# I don't know why linux needs this sleep, but it does, so don't delete it
		del httpd
		time.sleep(1)
		print("exec'ing via httpd path")
		os.execl(sys.argv[0], *sys.argv)
	except KeyboardInterrupt:
		print('')
		print('Keyboard Interrupt. Quitting.')
		print('')
		sys.exit(0)

else:
	# If not running a webserver but yes to file watching we need to not
	# exit
	if args.monitor:
		try:
			time.sleep(9999999)
		except KeyboardInterrupt:
			print('')
			print('Keyboard Interrupt. Quitting.')
			print('')
			sys.exit(0)
