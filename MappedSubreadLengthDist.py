#!/usr/bin/env python2
# script calculating the proportion of unmapped bases per read
# usage:
usage = "./MappedSubreadLengthDist.py <samfile>"

__author__ = "Ludovic Duvaux"
__maintainer__ = "Ludovic Duvaux"
__license__ = "GPL_v3"

import sys, numpy as np, re
from pysam import AlignmentFile

argv = sys.argv
if len(argv) != 2:
    print "Usage: " + usage
    sys.exit()
finp = argv[1]


# script
# 1) calculating the proportion of unmapped bases per read
#~finp="B04.pacbio.allib.sorted.ds.bam"
f = AlignmentFile(finp, "rb")


M = 0
L = 0
for i in f.head(10000):
    S=i.get_cigar_stats()
    #~for j in range(0, len(S[0])):
        #~stats[j] += S[0][j]
    M += float(S[0][0])
    L += i.infer_query_length()

r=round(M/L, 2)
l=[str(x) for x in [L, M, r]]
print "ReadLength\tMappedBases\tratio"
print "\t".join(l)


f.close()
