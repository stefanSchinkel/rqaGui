""" Progressbar.py

	A simple Tkinter progress bar.
	Creates a toplevel Widget in 
	which a bar shows the progress.

	$Log: Progressbar.py,v $
	Revision 1.1.1.1  2008/08/11 11:44:59  schinkel
	Initial Import





"""

from Tkinter import *	

class Progressbar():
	
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

if __name__ == "__main__":
	"""
	Test Routine 
	"""
	
	from Tkinter import *
	import time
	global app
	def whatever():
		pass
	def run():
		global app

		# initialise
		app = Progressbar()

		counterEnd = 200
		counterStep = 25
		#iterate through data		
		for i in range(1,counterEnd,counterStep):

			app.update(i,counterEnd)

		#update root Tk() otherwise movement stuck in queque
			root.update_idletasks()
			time.sleep(.5)

		app.destroy()		
		return
		
	def kill():
		global app
		app.destroy()
		
	# test the bloody thing	
	root = Tk()
	Button(root,text="Show Waitbar",command=run).pack(side=LEFT)
	Button(root,text="Kill Waitbar",command=kill).pack(side=LEFT)
	Button(root,text="Close Sample App",command=root.destroy).pack(side=LEFT)
	root.mainloop()

