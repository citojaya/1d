#!/tools/python/2.6-x86_64/bin/python
import numpy as np
import os
import random
import math
import sys
import library.vtk_tools as vtk_t
import glob

from optparse import OptionParser, OptionValueError



# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line:
p = OptionParser(usage="""Program <start> <end>

<start> - starting file
<end> - finishing file

Call following scirpts
./read_binary_drum.py - Read "out_0disk*" binary file and writtne to ASCII format
./vtk_from_triangle.py - Read triangulate mesh file which contains information of the drum and convert to vtu format



""")
p.add_option("-v", action="store_true",        dest="verbose",  help="Verbose")
p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, .vtu output")
p.add_option("-s", action="store", dest="input_dump", type="str", help="read sample dump file")

(opts, args) = p.parse_args()
# get the com filename
if len(args) != 2:
   p.print_help()
   sys.exit(1)
(start, end) = args

fileNames = []

#tools = vtk_t.VTK_XML_Serial_Unstructured()

for no_of_files in range(int(start),int(end)):
  file_name = "out_0disk"+str(no_of_files)+".dat"
  os.system("read_binary_drum.py "+file_name+" "+"ascii_"+file_name)
  
  f_name = file_name[0:len(file_name)-4]
  os.system("vtk_from_triangle.py "+"ascii_"+file_name+" "+f_name+".vtu")
  
  fileNames.append(f_name+".vtu")

#fileNames = glob.glob("out_0disk*.vtu")

#outFile = open("drum.pvd", 'w')

import xml.dom.minidom

pvd = xml.dom.minidom.Document()
pvd_root = pvd.createElementNS("VTK", "VTKFile")
pvd_root.setAttribute("type", "Collection")
pvd_root.setAttribute("version", "0.1")
pvd_root.setAttribute("byte_order", "LittleEndian")
pvd.appendChild(pvd_root)

collection = pvd.createElementNS("VTK", "Collection")
pvd_root.appendChild(collection)

for i in range(len(fileNames)):
  dataSet = pvd.createElementNS("VTK", "DataSet")
  dataSet.setAttribute("timestep", str(i))
  dataSet.setAttribute("group", "")
  dataSet.setAttribute("part", "0")
  dataSet.setAttribute("file", str(fileNames[i]))
  collection.appendChild(dataSet)

outFile = open("drum.pvd", 'w')
pvd.writexml(outFile, newl='\n')
outFile.close()



print "DONE" 

