#!/usr/bin/env python3

import glob
import jinja2 as jinja
import sys
import os
from sh import bower



# First update bower
if '--no-bower' not in sys.argv:
	print("Updating bower...")
	bower('install')


print("Building website...")
jinja_env = jinja.Environment(loader=jinja.FileSystemLoader(['.', 'templates']))

DIRECTORIES = ('demos', '.')

for directory in DIRECTORIES:
	for filename in glob.glob(directory + '/*.jinja'):
		basename = os.path.splitext(filename)[0]
		outputname = basename + '.html'

		output = jinja_env.get_template(filename).render()

		with open(outputname, 'w') as f:
			f.write(output)

categories = []
for directory in DIRECTORIES:
	demo_list = ''
	for filename in sorted(glob.glob(directory + '/*.html')):
		name = os.path.splitext(os.path.basename(filename))[0].title()
		demo_list += jinja_env.get_template('demo_item.jinja').render(name=name, path=filename)
	category = jinja_env.get_template('demo_category.jinja').render(category=directory, demos=demo_list)
	categories.append(category)

index = jinja_env.get_template('index.jinja').render(categories=categories)
with open('index.html', 'w') as f:
	f.write(index)
