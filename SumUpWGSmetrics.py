#!/usr/bin/env python2.7
# script summarizing results of multiple picard whole genome summuary Metrics
	# runs into a single table
# WARNING: the script is not MATURE!
# usage:
usage = "./SumUpWGSmetrics.py <WGSmetrics_files> <WGSmetrics_files> ..."

__author__ = "Ludovic Duvaux"
__maintainer__ = "Ludovic Duvaux"
__license__ = "GPL_v3"

import sys, re, os.path

argv = sys.argv
if len(argv) < 2:
	print "Usage: " + usage
	sys.exit()


fils = argv[1:]

res = {}
i = 0
inds = []
scos = []
runs = []
for inp in fils:
	with open(inp) as f:
		# get file flag
		ff = os.path.basename(inp)
		ind = re.split("\.|-", ff)[0]	#individual
		if ind not in inds:
			inds.append(ind)

		sco = re.split("\.|-", ff)[-2]	# score
		if sco not in scos:
			scos.append(sco)

		run = inp.split("/")[-2].split(".")[0]	# run
		if run not in runs:
			runs.append(run)
		
		# process txt
		txt = f.readlines()
		# save header once
		if i == 0:
			header = "INDIVIDUAL\tRUN\tMMQ\t" + txt[6].strip()
			i = 1
		
		# save res
		res[(ind, run, sco)] = txt[7].strip()	# create dict res[ind]

#~print res
#~print inds

# print res
	# print header
print header
	# print res
for i in inds:
	for r in runs:
		for s in scos:
			try:
				l = res[(i, r, s)]
				print i + "\t" + r + "\t" + s + "\t" + l
			except KeyError:
				pass
