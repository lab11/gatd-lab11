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
from sh import find
from sh import rm
from sh import mv
from sh import ln
import time
import watchdog.observers
import watchdog.events
import watchdog.utils.unicode_paths

try:
	import titlecase
except ImportError:
	print('Missing titlecase package.')
	print('You need to:')
	print('\tsudo python3-pip install ez_setup')
	print('\tsudo python3-pip install titlecase')
	print("(Package doesn't list dependencies correctly but is hosted on")
	print(" launchpad and I'm not fixing that...")
	raise

parser = argparse.ArgumentParser()
parser.add_argument('--no-bower',
                    action='store_true',
                    help='Do not run bower at the beginning.')
parser.add_argument('--debug',
                    action='store_true',
                    help='Run a local webserver')
parser.add_argument('--monitor',
                    action='store_true',
                    help='Watch for changes')
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
		demo_data = {} # dictionary of filename -> [name, description]

		for directory in DIRECTORIES:
			demos[directory] = []
			demo_data[directory] = {}

			for filename in glob.glob(directory + '/*.jinja'):
				basedir, name = os.path.split(filename)
				name = os.path.splitext(name)[0]
				outputname = os.path.join(WORKING_DIR, name + '.html')

				output = je.get_template(filename).render()

				with open(outputname, 'w') as f:
					f.write(output)

				if name != 'index':
					html_name = name + '.html'
					demos[directory].append(html_name)

					# default name and description
					name = os.path.splitext(html_name)[0].replace('_', ' ')
					name = titlecase.titlecase(name)
					desc = name

					# open file to read from it
					with open(filename, 'r') as f:
						for line in f:
							if line[0:8] == '{#Name: ':
								# '{#Name: <name>#}\n'
								name = line[8:-3]
							if line[0:8] == '{#Desc: ':
								# '{#Desc: <description>#}\n'
								desc = line[8:-3]

					demo_data[directory][html_name] = [name, desc]
				
			for filename in glob.glob(directory + '/*.html'):
				basedir, html_name = os.path.split(filename)
				dst = os.path.join(WORKING_DIR, html_name)
				demos[directory].append(html_name)
				cp(filename, dst)

				# default name and description
				name = os.path.splitext(html_name)[0].replace('_', ' ')
				name = titlecase.titlecase(name)
				desc = name

				# open file to read from it
				with open(filename, 'r') as f:
					for line in f:
						if line[0:8] == '{#Name: ':
							# '{#Name: <name>#}\n'
							name = line[8:-3]
						if line[0:8] == '{#Desc: ':
							# '{#Desc: <description>#}\n'
							desc = line[8:-3]

				demo_data[directory][html_name] = [name, desc]

		categories = []
		for directory in DIRECTORIES:
			demo_list = ''

			# sort demo_data by name
			for filename, [name, desc] in sorted(demo_data[directory].items(), key=lambda e: e[1][0]):
				demo_list += je.get_template('demo_item.jinja').render(
						name=name, desc=desc, path=filename)

			if demo_list == '':
				# No demos in this category, skip it
				continue
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

		find(BUILT_DIR, '-type', 'd', '-exec', 'chmod', '755', '{}', ';')
		find(BUILT_DIR, '-type', 'f', '-exec', 'chmod', '644', '{}', ';')


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
