#!/usr/bin/env python3

import glob
import jinja2 as jinja
import sys
import os
import sh
from sh import bower
from sh import cp
from sh import rm


# First update bower
if '--no-bower' not in sys.argv:
	print("Updating bower...")
	bower('install')


print("Building website...")
jinja_env = jinja.Environment(loader=jinja.FileSystemLoader(['.', 'templates']))

DIRECTORIES = ('demos', 'work-in-progress', 'raw', '.')
DESCRIPTIONS = {
		'demos':"""\
Polished pseudo-production demos. While liable to go down at any time (this is
research after all!), these are projects in a more-or-less "working" state.""",
		'work-in-progress':"""\
New projects we're working on building right now. Very hit-or-miss if these will
be working at any given time. Don't rely on these pages if you're showing
something off ;)""",
		'raw':"""\
An "under-the-hood" view into the raw data streams that power our demos. To
build queries yourself, check out the "Streams" demo above!""",
		'.':"Uncategorized legacy pages",
}

for directory in DIRECTORIES:
	rm('-f', sh.glob(directory + '/built/*'))
	for filename in glob.glob(directory + '/*.jinja'):
		basedir, name = os.path.split(filename)
		name = os.path.splitext(name)[0]
		outputname = os.path.join(basedir, 'built', name + '.html')

		output = jinja_env.get_template(filename).render()

		with open(outputname, 'w') as f:
			f.write(output)
	for filename in glob.glob(directory + '/*.html'):
		basedir, name = os.path.split(filename)
		dst = os.path.join(basedir, 'built', name)
		cp(filename, dst)

categories = []
for directory in DIRECTORIES:
	demo_list = ''
	for filename in sorted(glob.glob(directory + '/built/*.html')):
		name = os.path.splitext(os.path.basename(filename))[0].title()
		demo_list += jinja_env.get_template('demo_item.jinja').render(name=name, path=filename)
	category = jinja_env.get_template('demo_category.jinja').render(
			category=directory,
			description=DESCRIPTIONS[directory],
			demos=demo_list,
			)
	categories.append(category)

index = jinja_env.get_template('index.jinja').render(categories=categories)
with open('index.html', 'w') as f:
	f.write(index)
