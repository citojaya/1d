#!/tools/python/2.6-x86_64/bin/python
import numpy as np
import os
import random
import math
import sys
import vtk
#import library.vtk_tools as vtk_t

from optparse import OptionParser, OptionValueError



# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line
p = OptionParser(usage="""usage: %prog [options] <start> <end>

Reads "out_0par*.dat" files and constructs "particle.pvd" which contains particle information 
for PARAVIEW visualization 


""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 2:
   p.print_help()
   sys.exit(1)
(start, end) = args

tools = vtk.vtk_t.VTK_XML_Serial_Unstructured()

for no_of_files in range(int(start),int(end)):
  file_name = "_out_0par"+str(no_of_files)+".dat"
  f = open(file_name, 'r')
  data = f.readlines()
  f.close()

  x = []
  y = []
  z = []

  x_jump = []
  y_jump = []
  z_jump = []

  x_force = []
  y_force = []
  z_force = []

  radii = []
  color = []

  for i in range(data.__len__()-1):
    line = data[i].strip()
    tuple = line.split()
  
    x.append(float(tuple[0]))
    y.append(float(tuple[1]))
    z.append(float(tuple[2]))
    radii.append(0.5*(float(tuple[3])))
    color.append(float(tuple[6]))

  vtu_file = "par"+str(no_of_files)+".vtu"
  if opts.verbose:print "Writing ",vtu_file
  tools.snapshot(vtu_file, x, y, z, x_jump, y_jump, z_jump, x_force, y_force, z_force, radii, color)
#val.snapshot("filename.vtu", x, y, z)
  tools.writePVD("particle.pvd")

