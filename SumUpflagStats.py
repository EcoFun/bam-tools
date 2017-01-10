#!/usr/bin/env python2.7
# script summarizing results of multiple samtools flagstats runs into a single table
# WARNING: the script is not MATURE!
# usage:
usage = "./SumUpfastqc_res.py <fastqc_data.txt> <fastqc_data.txt> ..."

__author__ = "Ludovic Duvaux"
__maintainer__ = "Ludovic Duvaux"
__license__ = "GPL_v3"

import sys, re

argv = sys.argv
if len(argv) < 2:
	print "Usage: " + usage
	sys.exit()

#~print argv

fils = argv[1:]

res = {}
flagkey = []
h0 = ["Nreads", "mapped", "Pc_mapped", "PairedInSeq", "PropPaired", "Pc_PropPaired",
		"singletons", "Pc_singletons"]
for inp in fils:
	data = []
	# define keys from file names
	inp=inp.strip()
	ff = inp.split("/")[-1]
	ind=re.split("\.|-", ff)[0]
	#~print ind
	flag=inp.split("/")[-2]
	#~print flag
	if flag not in flagkey:
		flagkey.append(flag)
	with open(inp) as f:
		for l in f:
			l = l.strip()
			# get mapping info
			if "(QC-passed reads" in l:
				m = re.split("\+|\(|\:", l)
				N = m[0].strip().strip("%")
			if "mapped (" in l:
				m = re.split("\+|\(|\:", l)
				p0 = m[0].strip().strip("%")
				pp0 = float(m[2].strip().strip("%"))
			if "paired in sequencing" in l:
				m = re.split("\+|\(|\:", l)
				pis = m[0].strip().strip("%")
			if "properly paired (" in l:
				m = re.split("\+|\(|\:", l)
				p1 = m[0].strip().strip("%")
				pp1 = float(m[2].strip().strip("%"))
			if "singletons" in l:
				m = re.split("\+|\(|\:", l)
				s = m[0].strip().strip("%")
				ps = float(m[2].strip().strip("%"))
			# update data
		ll = [ N, p0, pp0, pis, p1, pp1, s, ps]
		try:
			res[ind][flag] = ll
		except KeyError:
			res[ind]={flag: ll}

#~print res
#~print flagkey

# print res
	# header
h1 = [ "Individual" ] + [ str(h) + "_" + str(f) for h in h0 for f in flagkey ]
##~print h1
print "\t".join(h1)
	# results
for i in res.keys():
	r = [i]
	for j in range(len(h0)):
		for k in flagkey:
			r += [ str(res[i][k][j]) ]
	##~print r
	print "\t".join(r)

