#!/tools/python/2.6-x86_64/bin/python
import numpy as np
import os
import random
import math
import sys

from optparse import OptionParser, OptionValueError



# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line
p = OptionParser(usage="""usage: %prog [options] <particle_no><start> <end>

Converts bindary files to ASCII format

<particle_no> particle to be considered
<start>  starting file
<end>    finishing file

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 3:
   p.print_help()
   sys.exit(1)
(par_no,start, end) = args

fout = open("particle_"+par_no+"_trajectory.dat", "w")

for no_of_files in range(int(start),int(end)):
  if opts.verbose:print ("step "+str(no_of_files))
  file_name = "out_0par"+str(no_of_files)+".dat"
  f = open(file_name, 'rb')
  x = np.fromfile(f, dtype=np.float)  # read the data into numpy array
  f.close()

  size = len(x)/8

  index = 0
  
  for i in range(0,size):
#    f.write(str(x[index]*1e+3)+'\t'+str(x[index+1]*1e+3)+'\t'+str(x[index+2]*1e+3)
#      +'\t'+str(x[index+3])+'\t'+str(x[index+4])+'\t'+str(x[index+5])+'\t'+str(x[index+6])+'\n')

    if(int(par_no) == x[index]):
      fout.write(str(x[index])+'\t'+str(x[index+1]*1e+3)+'\t'+str(x[index+2]*1e+3)+'\t'+str(x[index+3]*1e+3)+'\n')

    index += 8
fout.close()

print ("DONE")
