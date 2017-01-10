#!/usr/bin/env python2
# script calculating the proportion of unmapped bases per read
# usage:
#~usage = "./keepBadReads.py <bamfile> <out>"

__author__ = "Ludovic Duvaux"
__maintainer__ = "Ludovic Duvaux"
__license__ = "GPL_v3"

import argparse, sys
from pysam import Samfile

parser = argparse.ArgumentParser(description='Filter in reads with MAPQ < threshold')
parser.add_argument("-b", "--bad-qual", help="Keep reads with MAPQ below threshold only.",
                    action="store_true")	# here, a default value is superfluous.
parser.add_argument('threshold', type=int, help="MAPQ threshold")
parser.add_argument('input_file', help="input file name")
parser.add_argument('output_file', help="output file name")
args = parser.parse_args()
if(args.threshold == None or args.input_file == None or args.output_file == None) :
    parser.print_help()
    sys.exit()

#~print args

#One could look at the file name too see if we're dealing with a SAM or BAM file, but this is simpler
ifile = Samfile(args.input_file, "rb")	# "B04.pacbio.allib.sorted.bam"
ofile = Samfile(args.output_file, "wb", template=ifile)

if args.bad_qual:
#~# then we keep low MAPQ reads
	while(1) :
		 try :
			  r1 = ifile.next()
		 except :
			  break

		 if r1.mapq < int(args.threshold):
			  ofile.write(r1)
else:
#~# we keep high MAPQ reads instead
	while(1) :
		 try :
			  r1 = ifile.next()
		 except :
			  break

		 if r1.mapq >= int(args.threshold):
			  ofile.write(r1)
ifile.close()
ofile.close()
