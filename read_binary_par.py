#!/tools/python/2.6-x86_64/bin/python

import numpy as np
import os
import sys
from optparse import OptionParser, OptionValueError

# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')



# parse command line
p = OptionParser(usage="""usage: %prog [options] <inputfile> <outputfile>
Reads binary file and written to ascii format


""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, .vtu output")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 2:
   p.print_help()
   sys.exit(1)
(in_file, out_file) = args


f = open(in_file, 'rb')
fout = open(out_file, 'w')
x = np.fromfile(f, dtype=np.float)  # read the data into numpy array


if opts.verbose:print "Reading binary ",in_file," and written to ASCII ",out_file
index = 1

size = len(x)/8

for i in range(0,size):
  fout.write(str(x[index]*1e+3)+'\t'+str(x[index+1]*1e+3)+'\t'+str(x[index+2]*1e+3)
	+'\t'+str(x[index+3])+'\t'+str(x[index+4])+'\t'+str(x[index+5])+'\t'+str(x[index+6])+'\n')
  index += 8

#for i in range(0,int(x[0])):
#  fout.write(str(x[index]*1e+3)+'\t'+str(x[index+1]*1e+3)+'\t'+str(x[index+2]*1e+3)+'\n')
#  index += 8


f.close()
fout.close()

print "DONE"

