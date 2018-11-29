#!/tools/python/2.6-x86_64/bin/python

import os
import sys
#import subprocess
import re
from optparse import OptionParser, OptionValueError

import numpy as np
#import scipy.linalg
import glob
import vtk
from vtk.util import numpy_support

# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')

# parse command line
# parse command line
p = OptionParser(usage="""usage: %prog [options] <input.dat>  <out_vtu> 

Generates 3D mesh based on triangular mesh data
<input.dat> - triangulate mesh data in the following format

no_of_data_points
x1 y1 z1
x2 y2 z2
.......
.......
p1 p2 p3
.......

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, .vtu output")
(opts, args) = p.parse_args()


# Get the arguments

if len(args) == 2:
  (in_file, out_file) = args

else:
   p.print_help()
   sys.exit(1)

nodes = []
nodes_array = vtk.vtkIntArray()
nodes_array.SetName("nodes")
node_x = []
node_y = []
node_z = []

connect_1 = []
connect_2 = []
connect_3 = []

point = vtk.vtkPoints()

counter = 1

output = vtk.vtkUnstructuredGrid()

# Read nod files
if opts.verbose: print "Reading "+in_file+"data file"
infile = open(in_file, 'r')

no_of_points = int(infile.readline())

for i in range(no_of_points):
  line  = infile.readline()
  tuple = line.split()

  nodes_array.InsertNextValue(counter)
  nodes.append(counter)
  node_x.append(tuple[0])
  node_y.append(tuple[1])
  node_z.append(tuple[2])
  counter += 1

counter = 0

for line in infile:
  if not line.split():
    continue
  tuple = line.split()
  connect_1.append(int(tuple[0])+1)
  connect_2.append(int(tuple[1])+1)
  connect_3.append(int(tuple[2])+1)
  counter += 1

infile.close()

#print node_x[0]
#print connect_1[0]
#print connect_1[4]

#exit(0)

for i in range(0,no_of_points):
  point.InsertNextPoint(float(node_x[i]),float(node_y[i]),float(node_z[i]))

 
output.SetPoints(point)
output.GetPointData().AddArray(nodes_array)
#layer = []
#cell = []
 
layer_array = vtk.vtkStringArray()
cell_array = vtk.vtkIntArray()
cell_array.SetName("cell")


# List of .ele files


for i in range(counter):

  #layer.append(tuple[0])
  #cell.append(tuple[1])

  #layer_array.InsertNextValue((tuple[0]))
  cell_array.InsertNextValue(i+1)
  triangle = vtk.vtkTriangle().GetPointIds()
  triangle.SetId(0, int(connect_1[i])-1)
  triangle.SetId(1, int(connect_2[i])-1)
  triangle.SetId(2, int(connect_3[i])-1)
# Enter 5 for triangle
  output.InsertNextCell(5, triangle)



output.GetCellData().AddArray(cell_array)


command_used = vtk.vtkStringArray()
command_used.SetName("provenance")
command_used.InsertNextValue(" ".join(sys.argv))
output.GetFieldData().AddArray(command_used)


# Write output file
if opts.verbose: print "Writing", out_file
writer = vtk.vtkXMLUnstructuredGridWriter()
writer.SetFileName(out_file)


if opts.ascii:
   writer.SetDataModeToAscii()
else:
   writer.SetDataModeToBinary()

writer.SetInputConnection(output.GetProducerPort())
writer.Write()
