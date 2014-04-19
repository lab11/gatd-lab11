#!/usr/bin/env python3


#import mako.template
#import mako.lookup
#template_lookup = mako.lookup.TemplateLookup(directories=['templates'])
#t = mako.template.Template(filename='opo_simple.mako', lookup=template_lookup)
#print(t.render())




import glob
import jinja2 as jinja
import os


jinja_env = jinja.Environment(loader=jinja.FileSystemLoader(['.', 'templates']))

for filename in glob.glob('./*.jinja'):
	basename = os.path.splitext(filename)[0]
	outputname = basename + '.html'

	output = jinja_env.get_template(filename).render()

	with open(outputname, 'w') as f:
		f.write(output)
