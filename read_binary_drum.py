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
p.add_option("-v", action="store_true",        dest="verbose",  help="Verbose")
p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, .vtu output")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 2:
   p.print_help()
   sys.exit(1)
(in_file, out_file) = args


f = open(in_file, 'rb')
fout = open(out_file, 'w')

x = np.fromfile(f, dtype=np.float)  # read the data into numpy

index = 2

if opts.verbose:print "Reading binary ",in_file," and written to ASCII ",out_file

fout.write(str(int(x[0]))+'\n')
for i in range(0,int(x[0])):
  fout.write(str(5*x[index]*1e+3)+'\t'+str(5*x[index+1]*1e+3)+'\t'+str(x[index+2]*1e+3)+'\n')
  index += 9

#index = 0
for i in range(0,int(x[1])):
  fout.write(str(int(x[index]))+'\t'+str(int(x[index+1]))+'\t'+str(int(x[index+2]))+'\n')
  index += 3

print "DONE"

fout.close()
f.close()
