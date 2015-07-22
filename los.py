#!/bin/env python3

import sys,os
import random
import functools


p_sg = ['el', 'la']
p_pl = ['los', 'las']

# func to add prefix
def with_prefix(name):
	if name[-1:] == 's':
		# plural
		return random.choice(p_pl) + ' ' + name
	else:
		return random.choice(p_sg) + ' ' + name

# Find the path
path = '.'
if len(sys.argv) > 1:
	for i, p in enumerate(sys.argv[1:]):
		# ignore ls options
		if p[0] == '-':
			continue

		path = p

# handle nonexistent
if not os.path.exists(path):
	print('No such file or directory.', file=sys.stderr)
	sys.exit(1)

# is not a directory
if not os.path.isdir(path):
	print(with_prefix(os.path.basename(path)))
	sys.exit(1)

# comparator
def compare(x, y):

	dirx = os.path.isdir(os.path.join(path, x))
	diry = os.path.isdir(os.path.join(path, y))

	if dirx and not diry: return -1
	if diry and not dirx: return 1
	if x < y: return -1
	if x > y: return 1
	return 0

# list dir and sort using comparator
files = os.listdir(path)
files.sort(key=functools.cmp_to_key(compare))

# Print
for f in files:
	s = with_prefix(f)
	pa = os.path.join(path, f)

	if os.path.isdir(pa):
		s += '/'

	if os.path.islink(pa):
		s = '\033[1;36m' + s + '\033[0m' # cyan
	elif os.path.isdir(pa): # blue
		s = '\033[1;34m' + s + '\033[0m' # blue
	elif os.access(pa, os.X_OK):
		s = '\033[1;32m' + s + '\033[0m' # green
	else:
		s = s

	print(s)
