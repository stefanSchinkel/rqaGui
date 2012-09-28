#!/usr/bin/env python

"""
	Purpose:
	
	This script is meant to provide a simple, yet convenient GUI for
	interacting with the crp commandline programme. Essentially it just
	pipes the given parameters to the programme and stores/displays
	the output.
	
	The minium requirements for this GUI is the Tkinter package which should be
	included in your Python distribution. Otherwise you can download it at:
	http://wiki.python.org/moin/TkInter.
	
	For showing the RPs pylab/matplotlib is required. If you do
	not have it installed please visit:
	http://matplotlib.sourceforge.net

	Missing Features: 

	-e > 0			create distance plot
	-p <string>   	filename histogramme diagonal line lengths (output)
	-q <string>   	filename histogramme vertical line lengths (output)
	-c            	cummulative histogramme
	-D <string>   	delimiter in data file, default=TAB
	-d <string>   	delimiter for RQA file, default=TAB
	
	
	Copyright (C) 2009-2012 Stefan Schinkel, HU Berlin
	http://www.people.physik.hu-berlin.de/~schinkel  

	This program is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.





"""

class Progressbar:
	
	def update(self,cnt,cntEnd):
		
		#percentage elapsed
		x =  float(cnt)/cntEnd 

		# enlarge the rectangle
		self.canvas.coords(self.bar,0,0,x* 200,20)

		# print progress in %
		self.canvas.itemconfig(self.progress, text="%2.f%%" % (x*100))
		return

	def destroy(self):
		self.app.destroy()

	def __init__(self):
		
		#class vars
		self.title = "Running RQA"
		self.label = "Computation in Progress"
		
		# create Toplevel to work on		
		self.app = Toplevel()
		
		#title and label
		self.app.title(self.title)
		Label(self.app,text=self.label).pack(fill=X)
		
		#canvas to hold progressbar
		self.canvas = Canvas(self.app,width=200,height=20, bd=2,relief="sunken")
		self.canvas.pack(pady=4,padx=5)
		
		# the actual progressbar in PURPLE - YES!
		self.bar = self.canvas.create_rectangle(0,0,100,20,fill="#75507B")
		self.progress = self.canvas.create_text(100,10, text ="",fill="black")
		
		# center waitbar on screen
		# IMPROVE ME -- PLEASE !!!!!!!!!!! !!!!!!!!!!! 
		# get screen width and height
		ws = self.app.winfo_screenwidth()
		hs = self.app.winfo_screenheight()

		#approx. widget width
		w=200;h=50
		# calculate position x, y
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)
		self.app.geometry('%dx%d+%d+%d' % (w, h, x, y))
		# end centering app 

		return

##################################
##  DEFINE CALLBACKS OF THE GUI	##
##################################

def showRP():
	global flagDistancePlot
	
	
	#RP/CRP/JRP
	rpType = valVariant.get()
	
	#check if we have enough files
	if not checkFiles():
		return
	
	# xFile
	xFile = valData1Text.get()
		
	# second data file for CRP/JRP needed
	if rpType != "RP":
		yFile = valData2Text.get()
	else:
		yFile = xFile	

	
	#default command call binary in silent mode
	cmd = "%s -s " % rpBin;
	# add nurmerical values
	cmd = addNumValues(cmd);
	# add norm & type
	cmd = addNorm(cmd);

	#add data files and run
	cmd = cmd + " -i %s -j %s " % (xFile,yFile);		

	# store RP as ASCII in temp file
	outFile = "%s/rp.tif" % os.getcwd()
	cmd = cmd + " -r %s " % outFile;

	#make sure we don't use anything old
	if os.path.isfile(outFile):
		os.remove(outFile)
		return
	 
	# call binary
	os.system(cmd);

	# the rp binary does not give proper
	# exit codes, hence we check manually
	
	if not os.path.isfile(outFile):
		showerror("Computation Error","Error computing the RP.")
		return

	#load to array and delete tmpFile
	#RPdata = pylab.load(outFile) 
	RPdata =  pylab.np.loadtxt(outFile)
	os.remove(outFile)

	#length of axis
	lenRP =  int(max(RPdata[:,0]))

	#alloc memory
	b = pylab.eye(lenRP)
		
	#reshape data
	for i in range(pylab.size(RPdata,0)):
		b[(RPdata[(i,0)]-1,RPdata[(i,1)]-1)] = RPdata[(i,2)]
	
	#plot
	try: 	
		#clear plot if exist
		plotTitle = "%s %s\n Parameters: d=%s t=%s e=%s " % \
			(valMethod.get(),valVariant.get(),valDim.get(),valTau.get(),valEpsilon.get())

		pylab.clf()
		pylab.imshow(-b,origin='lower')
		pylab.title(plotTitle)
		pylab.axis('tight')
	
		# only distance plots need colour/colourbar

		if float(valEpsilon.get()) < 0 and valMethod.get() != "Order Patterns":
			pylab.colorbar()
			pylab.jet()
		else:
			print "Using gray"
			pylab.gray()
	
		pylab.show()
	
	except: 
		showerror("pylab Error","Error plotting the RP.")
	

def runRQA():

	#RP/CRP or JRP
	rpType = valVariant.get()
	
	#check if we have enough files
	if not checkFiles("RQA"):
		return


	# get hold of data files
	xFile = valData1Text.get()

	# second data file for CRP/JRP needed
	if rpType != "RP":
		yFile = valData2Text.get()
	else:
		yFile = xFile	
	
	# file for data output
	outFile = valResultText.get()
	if os.path.isfile(outFile):
		os.remove(outFile)
		print "Removing old output file"
	

	# For RQA on single files, we 
	# just feed those, without reading 'em first
	
	if not valWs.get():
	
		#assemble command
		cmd = "%s -s " % rpBin;
		# add nurmerical values
		cmd = addNumValues(cmd);
		# add norm
		cmd = addNorm(cmd);

		#add data files and run
		cmd = cmd + " -i %s -j %s -o %s" % (xFile,yFile,outFile);		

			
		# call binary 	
		os.system(cmd);
	
		# the rp binary does not give proper
		# exit codes, hence we check manually

		if not os.path.isfile(outFile):
			showerror("Computation Error","Error computing the RP.")
			return

		# if here, all is probably well
		msg =  "RQA measures computed and stored in %s" % outFile		
		showinfo("Computation Finished",msg)
		return


	##################
	#windowed RQA
	##################	

	else:

		# get params
		ws = int(valWs.get());	
		
		if valSs.get():
			ss = int(valSs.get());
		else:
			ss = int(1);		
			print "No step size provided. Defaulting to 1";
		
		# goody, lets load the data
		xData = open(xFile).readlines()
		yData = open(yFile).readlines()		
		
		lengthX = len(xData)
		lengthY = len(yData)
		
		#check matching length
		if lengthX != lengthY:
			showerror("Data Error","Data Files must be of the same length.")
			return
		
		if lengthX == 1 or lengthY == 1:
			showerror("Data Error","Please provide data as columns.")
			return
		
		if ws > lengthX:
			showerror("Data Error",\
			"The window is larger than the data. That won't work.")
			return
		
		
		# file to hold sliced data
		tempFileX = xFile + ".tmpX";	
		tempFileY = yFile + ".tmpY";			

		#assemble command
		cmd = "%s -s " % rpBin;
		cmd = addNumValues(cmd);
		cmd = addNorm(cmd);
		
		# since we operate on tmpFiles, we can add it here already
		cmd = cmd + " -i %s -j %s -o %s" % (tempFileX,tempFileY,outFile);		
		
		# instatiate progressbar
		waitbar = Progressbar()
		
		# all checks passed, let's loop then
		for i in range(0,lengthX-ws,ss):

			waitbar.update(i,lengthX-ws)
			app.update_idletasks()		

			fpTempFileX	= open(tempFileX,'w')
			fpTempFileY	= open(tempFileY,'w')

			
			for j in range(i,i+ws+1):
				fpTempFileX.write(xData[j])
				fpTempFileY.write(yData[j])
			
			
			fpTempFileX.close()
			fpTempFileY.close()		

			#done chunking, call binary 	
			# the try/catch doesn't make too much sense
			# since rp lacks proper exit codes, but still ...
			try:
				os.system(cmd);
			except: 
				showerror("Computation Error","Error while computing RQA measures.")
				return

		# clean-up
		os.remove(tempFileX);
		os.remove(tempFileY);								

		# close waitbar
		waitbar.destroy()			

		# if we reach here, all is probably well ...
		msg =  "RQA measures computed and stored in %s" % outFile		
		showinfo("Computation Finished",msg)
		return

############################################
## generic dialogs and helper functions	##
############################################

#dialog for data files
def getFile(name,text):

	pathToFile = askopenfilename()

	if pathToFile:
		#stupid but setvar() won't work
		cmd = 'app.%s.set(pathToFile)' % name
		eval(cmd)
		cmd = '%s.set(pathToFile)' % text
		eval(cmd)


#dialog for output files
def getSaveFile(name,text):

	pathToFile = asksaveasfilename()

	if pathToFile:
		cmd = 'app.%s.set(pathToFile)' % name
		eval(cmd)
		cmd = '%s.set(pathToFile)' % text
		eval(cmd)
		overrideAsk = 1

#check consistency of data files
def checkFiles(mode="RP"):
	
	rpType = valVariant.get()
	
	if not valData1Text.get():
		showerror("Input Error","Please provide data file(s).")
		return False
		
	if rpType != "RP":
		if	not valData2Text.get():
			showerror("Input Error","For CRP/JRP 2 data files are required.")
			return False
			
	if mode != "RP":
		if not valResultText.get():
			showerror("Output Error","Please provide a file to store the results in.")
			return False

	return True

def addNumValues(cmd):

	# defaults
	d = 1; t = 1; e = 1; tw = 1; vmin = 2; lmin = 2;
	
	# change default if applicable	
	if valDim.get(): d = valDim.get()	
	if valTau.get(): t = valTau.get()
	if valEpsilon.get(): e = valEpsilon.get()
	if valTheiler.get(): tw = valTheiler.get()
	if valLmin.get(): lmin = valLmin.get()	
	if valVmin.get(): vmin = valVmin.get()
	
	cmd = cmd + "-m %s -t %s -e %s -w %s -l %s -v %s" % (d,t,e,tw,lmin,vmin)

	return cmd

def addNorm(cmd):

	if	valMethod.get(): 

		if valMethod.get() == "Maximum Norm": 
			norm = "max";
		elif valMethod.get() == "Minium Norm":	
			norm = "min";
		elif valMethod.get() == "Order Patterns":	
			norm = "op";
		else:
			 norm = "eucl";
	
	cmd = cmd + " -n %s" % norm;	
	
	if valVariant.get()	== "JRP":
		cmd += " -J "

	return cmd;

def readData(dataFile,colNumber,delimiter='\t'):

	fpDataFile = open(dataFile)
	
	## skip first line (contains header) 
	fpDataFile.readline()
	
	data = []
	for line in fpDataFile.readlines(): 
		line = line[:-1]
		sl = line.split(delimiter)
		data.append(float(sl[colNumber]))
	fpDataFile.close()

	return data

def plotData():

	if not valResultText.get():
		showerror("Data Error","No result file given. Need one though.")
		return
	else:

		plotData = readData(valResultText.get(),plotOpts.index(plotMeasure.get()))
		
		plotTitle = "Recurrence Quantification Analysis for "
		plotTitle += "%s %s\n Parameter: d=%s t=%s e=%s " % \
			(valMethod.get(),valVariant.get(),valDim.get(),valTau.get(),valEpsilon.get())
		plotTitle += "WS: %s SS:%s" %(valWs.get(),valSs.get())
		
		pylab.hold(False)
		pylab.plot(plotData, linewidth=1.0)
		pylab.xlabel('time (discreet)')
		pylab.ylabel(plotMeasure.get())
		pylab.title(plotTitle)
		pylab.show()
		
		
		return


def showHelp():

	helpText = """
The GUI is meant to ease the interaction with the CRP 
commandline programme distributed by the Nonlinear
Dynamics Group within the TOCSY project. It allows 
for interactive data/output selection, parameter 
adjustment and visual inspection of the underlying 
(Cross/Joint) Recurrence Plot. Further you can plot
the RQA measures of a windowed analysis and store
these plots in a file.
"""
	helpWin = Tk()
	helpWin.title("RQA GUI HELP")
	Label(helpWin, justify=CENTER,padx=2,pady=2,text = helpText).pack()
	helpWin.mainloop()
	return



# actually, it shouldn't be imported, but still
if __name__ == '__main__':

	## common vars
	global debug, overrideAsk, waitbar
	flagDistancePlot = False
	disableShowButton = 0
	overrideAsk = 0;

	# modules to call binary and handle files
	import os,sys,stat,os.path


	# the tk stuff
	try:
		from Tkinter import *
		from tkFileDialog import * # file dialogs
		from tkMessageBox import * # message boxes
	except ImportError:
		print "--- Critical Error : Cannot import Tkinter module ---"
		print "Please install the Tkinter module. Otherwise the programme cannot run."
		print "For downloading and further information see: http://wiki.python.org/moin/TkInter"
		sys.exit(-1);

	try:
		import matplotlib
		#use TkAggregatar since Tkinter has to be installed for the GUI to run
		#matplotlib.use('TkAgg')
		import pylab 
	except ImportError:
		print "--- Warning :  Pylab Import Error ---"
		print "Could not the pylab/matplotlib module"
		print "Please visit http://matplotlib.sourceforge.net/  and install the module."
		print "Without this module plotting of RPs/RQA  will not be possible."
		disableShowButton = 1;
	

	# check $PATH for binary, exception needed in 
	# case $PATH contains nonexistent directories	
	rpBin = "";

    	if os.name  == 'nt':
	 	# print "working on windows"
		binaryName = 'rp.exe'
    	else:
		binaryName = 'rp'
	try:
		for d in os.environ['PATH'].split(':'):
			if binaryName in os.listdir(d):
				rpBin = "%s/%s" % (d,binaryName)
				break 
	except:
		pass
	
	# check PWD for binary				
	if len(rpBin) == 0:
		if binaryName in os.listdir(os.getcwd()):
			rpBin = "%s/%s" % (os.getcwd(),binaryName)			

	print "Info: Will use the binary file:  " + rpBin
	# if binary found, check if exectuable
	if len(rpBin) != 0:
		st = os.stat(rpBin)
		mode = st[stat.ST_MODE]
	
		if not mode & stat.S_IEXEC:
			msg = "Change file permissions of binary (%s) to executable and run the GUI again " % rpBin
			showerror(title='Binary is not executable', message=msg)
			sys.exit(-1)
		else:
			pass
	
	# no binary found - error message and exit
	if len(rpBin) == 0:
		print "------- Error: Binary not found --------"
		print "Could not find the binary in your $PATH or the current directory"
		print "Make sure to have downloaded the binary for your plattform from:"
		print "http://tocsy.pik-potsdam.de/crp.php"
		print "Store the file in an accessible place your $PATH or the directory this"
		print "programme is in and make sure to have it renamed 'rp' ('rp.exe' on Windows)"
		print "The GUI only searches your $PATH or the folder this programme is in."
		sys.exit(-1)				

	
	#################
	## GUI Layout	##
	#################

	# mainGUI
	app = Tk()
	app.geometry("420x450+50+50");
	app.title("Graphical RQA interface");

	# declare vars

	# variables for files
	app.data1 = StringVar();valData1Text = StringVar();
	app.data2 = StringVar();valData2Text = StringVar();
	app.out = StringVar();valResultText = StringVar();
	# vars for RP/RQA params
	valMethod = StringVar();
	valVariant = StringVar();
	c1=StringVar();c1.set(1); 	#dim
	c2=StringVar();c2.set(1);	#tau
	c3=StringVar();c3.set(1);	#epsilon
	c4=StringVar();c4.set(1);	#theiler
	c5=StringVar();c5.set(2);	#lmin
	c6=StringVar();c6.set(2);	#vmin
	distPlot=IntVar();			# make distance plot ? 
	ws = StringVar();			# windowsize
	ss = StringVar();			# stepsize
	plotMeasure = StringVar()	# measure for plot

	# title and seperator
	Label(app, text='Commandline Recurrence Plots - Graphical User Interface').pack(fill=X,pady=2)

	# split GUI in 3 parts
	topFrame = Frame(app, borderwidth=2, relief=GROOVE);topFrame.pack(padx=2,pady=2,fill=X);
	midFrame = Frame(app,borderwidth=2,relief=GROOVE);midFrame.pack(padx=2,pady=2, fill=X);
	botFrame = Frame(app, borderwidth=2,relief=GROOVE);botFrame.pack(padx=2,pady=2,fill=X);

	## topframe

	Label(topFrame,anchor=W, font=("Helvetica", 12, "italic"), text='Input:').pack(fill=X)

	rowData1 = Frame(topFrame,border=1, pady=1)
	Label(rowData1,text='Data file 1:').pack(side=LEFT)
	Entry(rowData1,width=35, textvariable=valData1Text).pack(side=LEFT,fill=X)
	Button(rowData1, text='Browse', command=(lambda x='data1', y='valData1Text': getFile(x,y))).pack(side=RIGHT)
	rowData1.pack(side=TOP,fill=X, expand=YES)

	# dataFile 2
	rowData2 = Frame(topFrame,border=1, pady=1)

	Label(rowData2, text='Data file 2:').pack(side=LEFT)
	Entry(rowData2, width=35, textvariable=valData2Text).pack(side=LEFT,fill=X)
	Button(rowData2, text='Browse', command=(lambda x='data2', y='valData2Text' : getFile(x,y))).pack(side=RIGHT)
	rowData2.pack(side=TOP,fill=X, expand=YES)


	# result file
	Label(topFrame,anchor=W, font=("Helvetica", 12, "italic"), text='RQA output:').pack(fill=X)

	rowResult = Frame(topFrame, border=1, pady=1)
	Label(rowResult, text='Result file:').pack(side=LEFT)
	Entry(rowResult,width=35, textvariable=valResultText).pack(side=LEFT,fill=X)
	Button(rowResult, text='Browse', command=(lambda x='out', y='valResultText' : getSaveFile(x,y))).pack(side=RIGHT)
	rowResult.pack(side=TOP,fill=X, expand=YES)

	## midframe
	# numeric params
	Label(midFrame, anchor=W, font=("Helvetica", 12, "italic"), text='RP Parameters:').pack(fill=X)
	row1 = Frame(midFrame, border=1, pady=2)
	Label(row1, width=10, text='Dimension :').pack(side=LEFT)
	valDim = Entry(row1, width=2, textvariable=c1);valDim.pack(side=LEFT)
	Label(row1, width=10, text='Delay :').pack(side=LEFT)
	valTau = Entry(row1, width=2, textvariable=c2);valTau.pack(side=LEFT)
	Label(row1,width=10, text='Threshold:').pack(side=LEFT)
	valEpsilon = Entry(row1, width=4, textvariable=c3);valEpsilon.pack(side=LEFT)
	row1.pack(side=TOP,fill=X, expand=YES)

	# methods
	row2 = Frame(midFrame, border=1,pady=2)
	Label(row2, text='Method: ').pack(side=LEFT)
	OptionMenu(row2, valMethod, 'Euclidian Norm','Maximum Norm','Minium Norm','Order Patterns').pack(side=LEFT)
	valMethod.set('Euclidean Norm')
	row2.pack(side=TOP,fill=X, expand=YES)

	# RP/CRP/JRP
	row3 = Frame(midFrame, border=1,pady=2)
	Label(row3, text='RP type: ').pack(side=LEFT)
	OptionMenu(row3, valVariant, 'RP','CRP','JRP').pack(side=LEFT)
	valVariant.set('RP')
	row3.pack(side=TOP,fill=X, expand=YES)



	## bottomframe

	# Theiler etc.
	Label(botFrame, anchor=W, font=("Helvetica", 12, "italic"), text='RQA Parameters:').pack(fill=X)

	row4 = Frame(botFrame, border=1, pady=2)
	Label(row4, width=10, text='Theiler :', anchor=W).pack(side=LEFT)
	valTheiler = Entry(row4, width=2, textvariable=c4);valTheiler.pack(side=LEFT)
	Label(row4, width=10, text='min. Diag :').pack(side=LEFT)
	valLmin = Entry(row4, width=2, textvariable=c5);valLmin.pack(side=LEFT)
	Label(row4, width=10, text='min. Vert :').pack(side=LEFT)
	valVmin = Entry(row4, width=2, textvariable=c6);valVmin.pack(side=LEFT)
	row4.pack(side=TOP,fill=X, expand=YES)

	# windowed RQA

	Label(botFrame, anchor=W, font=("Helvetica", 12, "italic"), text='Windowed Analysis:').pack(fill=X)
	row5 = Frame(botFrame, border=1, pady=2)
	Label(row5, width=12, text='Window Size :', anchor=W).pack(side=LEFT)
	valWs = Entry(row5, width=6, textvariable=ws)
	valWs.pack(side=LEFT)
	Label(row5, width=10, text='Step Size :', anchor=W).pack(side=LEFT)
	valSs = Entry(row5, width=6)
	valSs.pack(side=LEFT)
	row5.pack(side=TOP,fill=X, expand=YES)

	### add buttons
	if not disableShowButton:
		# show RP only if PIL available
		showRPbutton = Button(app, text='Show RP', command=showRP).pack(side=LEFT)

		# Run Rqa can 
		Button(app, text='Run RQA', command = runRQA).pack(side=LEFT)

		# Plot button
		plotRQAbutton = Button(app, text='Plot:', command = plotData).pack(side=LEFT)
		plotOpts = ["RR","DET","DET/RR","LAM","LAM/DET","L_max","L","L_entr","DIV","V_max",
					"TT","V_entr","T1","T2","W_max","W_mean","W_entr","W_prob","F_min"]
		plotMeasure.set(plotOpts[0]) # default to RR			
		OptionMenu(app,plotMeasure,*plotOpts).pack(side=LEFT)

	## close and help button
	Button(app, text='Quit', command = app.destroy).pack(side=RIGHT)
	Button(app, text='Help', command = showHelp).pack(side=RIGHT)

	# if disableShowButton:
	# 	showRPbutton.itemconfig(state=DISABLED)
	# 	plotRQAbutton.itemconfig(state=DISABLED)		

	#run GUI
	app.mainloop()


