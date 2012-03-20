#!/usr/bin/env python

import matplotlib
#use TkAggregatar since Tkinter has to be installed for the GUI to run
matplotlib.use('TkAgg')
import pylab 

a = pylab.load('rp.tif');
## make that to find max of a[(0,:))
lenRP =  int(max(a[:,0]))
# size needs to be a tuple
b = pylab.eye(lenRP)
for i in range(pylab.size(a,0)):
	b[(a[(i,0)]-1,a[(i,1)]-1)] = a[(i,2)];

pylab.pcolor(b)
pylab.axis('tight')
pylab.colorbar()
pylab.cla()
pylab.show()


