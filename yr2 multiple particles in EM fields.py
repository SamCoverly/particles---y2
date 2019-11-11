import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.mlab as mlab
from Tkinter import *
import os
from tkMessageBox import *
from mpl_toolkits.mplot3d import Axes3D

def button(frame,text,command,size,row,column,padx,pady,helptext): #A function that creates buttons using passed variables, reducing the need for lengthy code
    b=Button(frame,text=text, command=command,width=size)
    b.grid(row=row,column=column,padx=padx,pady=pady)
    b.bind("<Button-3>",lambda x=helptext: showinfo(message=helptext)) #Binds the right mouse click event to a help message explaining button functionality
    return b  
def label(frame,text,size,row,column,padx,pady,helptext): #A function that creates labels using passed variables
    L=Label(frame,text=text,font=("Ariel",size),bg='LightBlue1')
    L.grid(row=row,column=column,padx=padx,pady=pady,sticky='NEWS')
    L.bind("<Button-3>",lambda x=helptext: showinfo(message=helptext)) #Binds the right mouse click event to a help message
    return L
def simopen(): #Runs the simulator as a seperate Tk instance, allowing the menu to be closed
    sim=Tk()
    GUI=Simulator(sim)
    sim.mainloop()
        
        
class Menu:
    def __init__(self,master):
        self.master=master
        master.title("Main Menu")
        frame=Frame(master,bg='LightBlue1')
        frame.pack()
        Title=label(frame,'Simulator: multi-particle system within electromagnetic field',20,0,0,10,10,'A simulator that emulates the motion of 3 seperate particles moving within an electromagnetic field and interacting with each other')
        Title.grid(columnspan=4,sticky='NEWS')
        Sim=button(frame,'Run Simulation',lambda: simopen(),20,1,0,10,10,'Open the simulation') #Button that opens the simulation window
        Report=button(frame,'Open LaTeX report',lambda: os.startfile("ElectricalResonance.pdf"),20,2,0,10,10,'Open the pdf report/manual') #Opens pdf report
        Close=button(frame,'Close Program',lambda: root.destroy(),20,3,0,10,10,'Close the program') #Close the Tk instance
        #photo=PhotoImage(file="Welcomeimg.gif") #Displays and alligns a welcome image
        #logo=Label(frame,image=photo)
        #logo.image = photo
        #logo.grid(row=1,column=1,rowspan=3,columnspan=5)
    
    
class Simulator:
    def __init__(self,master):
        master.state('zoomed') #Forces the window into fullscreen mode
        frame=Frame(master,bg='LightBlue1')
        frame.pack()
        self.master=master
        root.destroy() #Closes main menu
        master.title("Simulation")    
        self.canvas(frame) #Creates the canvas that houses the simulation plot
        self.inputs(frame) #Creates the data entry inputs
        showinfo(message='Welcome to the simulation. This program allows you to model the motion of up to three charged particles moving within an electric and a magnetic field. The top slider can be used to change the duration of the simulation while the second slider changes the timestep, allowing for different degrees of precision. To enter field components as well as particle charge/mass/position/velocity, simply enter the values into the associated boxes, or select from a choice of commonly used particles. For more help, right click on a button or label for a description of its purpose.')
    
    def inputs(self,frame): #Creates the data entry inputs
        frame = Frame(frame,bg='LightBlue1')
        self.master=frame
        frame.grid(column = 0, row = 0) #places this frame at co-ord (0,0) of the master frame
        T=label(frame,'Stop time',8,0,0,3,3,'The time at which the simulation should stop running. Change this value to change the duration of the experiment')
        self.T=Scale(frame, from_=0.001,to_=1,resolution=0.001,orient=HORIZONTAL,bg='LightBlue1') #Slider for entry of stop time
        self.T.grid(row=0,column=1,columnspan=3,sticky='NEWS')
        DT=label(frame,'Time step',8,1,0,3,3,'The timestep between successive calculations. Smaller values allow for greater precision while larger values will be less resource intensive')
        self.DT=Scale(frame,from_=0.00001,to_=0.001,resolution=0.00001,orient=HORIZONTAL,bg='LightBlue1') #Slider for entry of timestep
        self.DT.grid(row=1,column=1,columnspan=3,sticky='NEWS')
        X=label(frame,'X',8,2,1,3,3,"The component of the overall field acting in the X direction")
        Y=label(frame,'Y',8,2,2,3,3,'The component of the overall field acting in the Y direction')
        Z=label(frame,'Z',8,2,3,3,3,'The component of the overall field acting in the Z direction')
        Blab=label(frame,'Components of B field',8,3,0,3,3,'The magnetic field acting on the particles')
        self.Bx=Entry(frame)        #Add entryboxes for the magnetic field
        self.Bx.grid(row=3,column=1)
        self.By=Entry(frame)
        self.By.grid(row=3,column=2)
        self.Bz=Entry(frame)
        self.Bz.grid(row=3,column=3)
        Elab=label(frame,'Components of E field',8,4,0,3,3,'The electric field acting on the particles')
        self.Ex=Entry(frame)        #Add entryboxes for the electric field
        self.Ex.grid(row=4,column=1)
        self.Ey=Entry(frame)
        self.Ey.grid(row=4,column=2)
        self.Ez=Entry(frame)
        self.Ez.grid(row=4,column=3)
        Par1=label(frame,'Particle 1',10,5,0,6,6,'The properties for the first particle to be plotted') #Label to indicate the domain of particle 1
        Par1.grid(columnspan=4,sticky='NEWS')
        Charge1=label(frame,'Charge',8,6,0,3,3,'The charge of particle 1. Can be either positive or negative')
        self.Q1=Entry(frame) #Entrybox for particle 1 charge
        self.Q1.grid(row=6,column=1)
        Electron=button(frame,'Electron',lambda: self.chargemass(1,-1.6e-19,9.1e-31),20,6,2,3,3,'Set the charge/mass of particle 1 to those of an electron') #Change charge/mass values to those of an electron
        Positron=button(frame,'Positron',lambda: self.chargemass(1,1.6e-19,9.1e-31),20,6,3,3,3,'Set the charge/mass of particle 1 to those of a positron')  #Change charge/mass values to those of a positron
        Mass1=label(frame,'Mass',8,7,0,3,3,'The mass of particle 1')
        self.M1=Entry(frame) #Entrybox for particle 1 mass
        self.M1.grid(row=7,column=1)
        Proton=button(frame,'Proton',lambda: self.chargemass(1,1.6e-19,1.7e-27),20,7,2,3,3,'Set the charge/mass of particle 1 to those of a proton')  #Change charge/mass values to those of a proton
        Neutron=button(frame,'Neutron',lambda: self.chargemass(1,0,1.7e-27),20,7,3,3,3,'Set the charge/mass of particle 1 to those of a neutron')  #Change charge/mass values to those of a neutron
        X=label(frame,'X',8,8,1,3,3,"The component of the overall position/velocity of particle 1 acting in the X direction")
        Y=label(frame,'Y',8,8,2,3,3,'The component of the overall position/velocity of particle 1 acting in the Y direction')
        Z=label(frame,'Z',8,8,3,3,3,'The component of the overall position/velocity of particle 1 acting in the Z direction')
        Pos1=label(frame,'Components of position',8,9,0,3,3,'The components of the overall position of particle 1')
        self.Px1=Entry(frame)        #Entryboxes for paricle 1 position
        self.Px1.grid(row=9,column=1)
        self.Py1=Entry(frame)
        self.Py1.grid(row=9,column=2)
        self.Pz1=Entry(frame)
        self.Pz1.grid(row=9,column=3)
        Vel1=label(frame,'Components of velocity',8,10,0,3,3,'The components of the overall velocity of particle 1')
        self.Vx1=Entry(frame)         #Entryboxes for particle 1 velocity
        self.Vx1.grid(row=10,column=1)
        self.Vy1=Entry(frame)
        self.Vy1.grid(row=10,column=2)
        self.Vz1=Entry(frame)
        self.Vz1.grid(row=10,column=3)
        Par2=label(frame,'Particle 2',10,11,0,6,6,'The properties for the second particle to be plotted') #Label to indicate the domain of particle 2
        Par2.grid(columnspan=4,sticky='NEWS')
        Charge2=label(frame,'Charge',8,12,0,3,3,'The charge of particle 2. Can be either positive or negative')
        self.Q2=Entry(frame) #Entrybox for particle 2 charge
        self.Q2.grid(row=12,column=1)
        Electron=button(frame,'Electron',lambda: self.chargemass(2,-1.6e-19,9.1e-31),20,12,2,3,3,'Set the charge/mass of particle 2 to those of an electron')  #Change charge/mass values to those of an electron
        Positron=button(frame,'Positron',lambda: self.chargemass(2,1.6e-19,9.1e-31),20,12,3,3,3,'Set the charge/mass of particle 2 to those of a positron') #Change charge/mass values to those of a positron
        Mass2=label(frame,'Mass',8,13,0,3,3,'The mass of particle 2')
        self.M2=Entry(frame) #Entrybox for particle 2 mass
        self.M2.grid(row=13,column=1)
        Proton=button(frame,'Proton',lambda: self.chargemass(2,1.6e-19,1.7e-27),20,13,2,3,3,'Set the charge/mass of particle 2 to those of a proton') #Change charge/mass values to those of a proton
        Neutron=button(frame,'Neutron',lambda: self.chargemass(2,0,1.7e-27),20,13,3,3,3,'Set the charge/mass of particle 2 to those of a neutron') #Change charge/mass values to those of a neutron
        X=label(frame,'X',8,14,1,3,3,"The component of the overall position/velocity of particle 2 acting in the X direction")
        Y=label(frame,'Y',8,14,2,3,3,'The component of the overall position/velocity of particle 2 acting in the Y direction')
        Z=label(frame,'Z',8,14,3,3,3,'The component of the overall position/velocity of particle 2 acting in the Z direction')
        Pos2=label(frame,'Components of position',8,15,0,3,3,'The components of the overall position of particle 2')
        self.Px2=Entry(frame)          #Entryboxes for particle 2 position
        self.Px2.grid(row=15,column=1)
        self.Py2=Entry(frame)
        self.Py2.grid(row=15,column=2)
        self.Pz2=Entry(frame)
        self.Pz2.grid(row=15,column=3)
        Vel2=label(frame,'Components of velocity',8,16,0,3,3,'The components of the overall velocity of particle 2')
        self.Vx2=Entry(frame)          #Entryboxes for particle 2 velocity
        self.Vx2.grid(row=16,column=1)
        self.Vy2=Entry(frame)
        self.Vy2.grid(row=16,column=2)
        self.Vz2=Entry(frame)
        self.Vz2.grid(row=16,column=3)
        Par3=label(frame,'Particle 3',10,17,0,6,6,'The properties for the third particle to be plotted') #Label to indicate the domain of particle 3
        Par3.grid(columnspan=4,sticky='NEWS')
        Charge3=label(frame,'Charge',8,18,0,3,3,'The charge of particle 3. Can be either positive or negative')
        self.Q3=Entry(frame)          #Entrybox for particle 3 charge
        self.Q3.grid(row=18,column=1)
        Electron=button(frame,'Electron',lambda: self.chargemass(3,-1.6e-19,9.1e-31),20,18,2,3,3,'Set the charge/mass of particle 3 to those of an electron') #Change charge/mass values to those of an electron
        Positron=button(frame,'Positron',lambda: self.chargemass(3,1.6e-19,9.1e-31),20,18,3,3,3,'Set the charge/mass of particle 3 to those of a positron') #Change charge/mass values to those of a positron
        Mass3=label(frame,'Mass',8,19,0,3,3,'The mass of particle 3')
        self.M3=Entry(frame)          #Entrybox for particle 3 mass
        self.M3.grid(row=19,column=1)
        Proton=button(frame,'Proton',lambda: self.chargemass(3,1.6e-19,1.7e-27),20,19,2,3,3,'Set the charge/mass of particle 3 to those of a proton') #Change charge/mass values to those of a proton
        Neutron=button(frame,'Neutron',lambda: self.chargemass(3,0,1.7e-27),20,19,3,3,3,'Set the charge/mass of particle 3 to those of a neutron') #Change charge/mass values to those of a neutron
        X=label(frame,'X',8,20,1,3,3,"The component of the overall position/velocity of particle 3 acting in the X direction")
        Y=label(frame,'Y',8,20,2,3,3,'The component of the overall position/velocity of particle 3 acting in the Y direction')
        Z=label(frame,'Z',8,20,3,3,3,'The component of the overall position/velocity of particle 3 acting in the Z direction')
        Pos3=label(frame,'Components of position',8,21,0,3,3,'The components of the overall position of particle 3')
        self.Px3=Entry(frame)          #Entryboxes for particle 3 position
        self.Px3.grid(row=21,column=1)
        self.Py3=Entry(frame)
        self.Py3.grid(row=21,column=2)
        self.Pz3=Entry(frame)
        self.Pz3.grid(row=21,column=3)
        Vel3=label(frame,'Components of velocity',8,22,0,3,3,'The components of the overall velocity of particle 3')
        self.Vx3=Entry(frame)          #Entryboxes for particle 3 velocity
        self.Vx3.grid(row=22,column=1)
        self.Vy3=Entry(frame)
        self.Vy3.grid(row=22,column=2)
        self.Vz3=Entry(frame)
        self.Vz3.grid(row=22,column=3)
        
        Runsim=button(frame,'Run',lambda: self.runsim(),20,23,0,3,3,'Runs the simulation') #Runs the simulation, collecting values from the entryboxes and plotting the Euler-Cromer method
        Help=label(frame,'Right-click on an object for help',12,23,1,3,3,'Right-click on an object for help')
        Help.grid(columnspan=3,sticky='NEWS')
        
    def runsim(self): #Collects values from entryboxes and plots results using Euler-Cromer method
        try: #runs data entry code while exception has not been raised
            #data entry from entryboxes.
            E=np.array([self.getval('Ex'),self.getval('Ey'),self.getval('Ez')]) #electric field components
            B=np.array([self.getval('Bx'),self.getval('By'),self.getval('Bz')]) #magnetic field components
            p1=[self.getval('Px1'),self.getval('Py1'),self.getval('Pz1')] #initial position of particle 1
            v1=[self.getval('Vx1'),self.getval('Vy1'),self.getval('Vz1')] #initial velocity of particle 1
            q1=self.getval('Q1') #Charge of particle 1
            m1=self.getval('M1') #Mass of particle 1
            p2=[self.getval('Px2'),self.getval('Py2'),self.getval('Pz2')] #initial position of particle 2
            v2=[self.getval('Vx2'),self.getval('Vy2'),self.getval('Vz2')] #initial velocity of particle 2
            q2=self.getval('Q2') #Charge of particle 2
            m2=self.getval('M2') #Mass of particle 2
            p3=[self.getval('Px3'),self.getval('Py3'),self.getval('Pz3')] #initial position of particle 3
            v3=[self.getval('Vx3'),self.getval('Vy3'),self.getval('Vz3')] #initial velocity of particle 3
            q3=self.getval('Q3') #Charge of particle 3
            m3=self.getval('M3') #Mass of particle 3
            x1=[] #Lists to store values of position components
            y1=[]
            z1=[]
            x2=[]
            y2=[]
            z2=[]
            x3=[]
            y3=[]
            z3=[]
            t=0.
            dt=self.getval('DT') #Timestep
            stoptime=self.getval('T') #Time at which to end simulation
            k=9e9 # Coulombs constant
            
            while t<stoptime: #while end time has not been reached
                for n in ('1','2','3'): #iterates through Euler-Cromer method of position computation for each particle (1, 2 and 3)
                    Fxtot=0.
                    Fytot=0.
                    Fztot=0.
                    for m in ('1','2','3'): #iterates through each particle again, only running the intermolecular force calculation when particle n =/= particle m
                        if n != m: #Prevents particle n from imparting a force on itself
                            #Calculates the force on particle 'n' from particle 'm'
                            exec('d=np.sqrt(((p'+n+'[0]-p'+m+'[0])**2)+((p'+n+'[1]-p'+m+'[1])**2)+((p'+n+'[2]-p'+m+'[2])**2))') #calculates the total distance between particles based on x,y and z positions
                            
                            exec('Fxtot=Fxtot+(k*q'+n+'*q'+m+'*(p'+n+'[0]-p'+m+'[0])/(d**2))') #Adds the x component of force on particle 'n' from particle 'm'
                            exec('Fytot=Fytot+(k*q'+n+'*q'+m+'*(p'+n+'[1]-p'+m+'[1])/(d**2))') #Adds the y component of force on particle 'n' from particle 'm'
                            exec('Fztot=Fztot+(k*q'+n+'*q'+m+'*(p'+n+'[2]-p'+m+'[2])/(d**2))') #Adds the z component of force on particle 'n' from particle 'm'
                    
                    exec('Fxtot=Fxtot+(k*q'+n+'*(E[0]+(v'+n+'[1]*B[2])-(v'+n+'[2]*B[1])))') #Evaluates the 'x' component of the force at 't' using Lorentz definition
                    exec('Fytot=Fytot+(k*q'+n+'*(E[1]-(v'+n+'[0]*B[2])+(v'+n+'[2]*B[0])))') #Evaluates the 'y' component of the force at 't'
                    exec('Fztot=Fztot+(k*q'+n+'*(E[2]+(v'+n+'[0]*B[1])-(v'+n+'[1]*B[0])))') #Evaluates the 'z' component of the force at 't'
                    
                    exec('v'+n+'[0] = v'+n+'[0]+( Fxtot/m'+n+' * dt)') #  Calculates v(t+dt) using v(t) and a(t), Acceleration = F/m; dv = a.dt
                    exec('v'+n+'[1] = v'+n+'[1]+( Fytot/m'+n+' * dt)')
                    exec('v'+n+'[2] = v'+n+'[2]+( Fztot/m'+n+' * dt)')
                    
                    exec('p'+n+'[0] = p'+n+'[0]+(v'+n+'[0] * dt)') # updates 'x' at (t+dt)
                    exec('p'+n+'[1] = p'+n+'[1]+(v'+n+'[1] * dt)') # updates 'y' at (t+dt)
                    exec('p'+n+'[2] = p'+n+'[2]+(v'+n+'[2] * dt)') # updates 'z' at (t+dt                
                    
                    exec('x'+n+'.append(p'+n+'[0])') #appends x value of position for particle n to list
                    exec('y'+n+'.append(p'+n+'[1])') #appends y value of position for particle n to list
                    exec('z'+n+'.append(p'+n+'[2])') #appends z value of position for particle n to list
                t+=dt #increment time
            ax=Axes3D(self.fig) #Plot axes on canvas
            ax.set_title("Path of charged particles under influence of electric and magnetic fields")
            ax.set_xlabel('X') #Set axes labels
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.plot3D(x1,y1,z1, color='red', label='particle 1') #Plots the motion of particle 1
            ax.plot3D(x2,y2,z2, color='blue', label='particle 2') #Plots the motion of particle 2
            ax.plot3D(x3,y3,z3, color='green', label='particle 3') #Plots the motion of particle 3
            ax.legend(loc='lower left') #Displays the legend
            self.canvas.show()
            
            
            
        except Exception, e: #runs if exception is raised during data entry
            self.help('Please ensure that only numerical values are entered') #prints error message
        
    def getval(self,entrybox): #passes entrybox name as variable, then retrieves value from entrybox
        s=eval('float(self.%s.get())'%(entrybox)) #retrieves float value of the entrybox passed by reference.Type check: Raises exception if the data is not float format
        if s=='': #Presence check: raises exception if entrybox is blank
            raise Exception
        else:
            return s #returns entrybox value
        
    def chargemass(self,particle,charge,mass): #Clears charge and mass values for particle n, replacing them with passed variables
        eval('self.Q%g.delete(0,END)' %(particle)) #Delete charge value
        eval('self.Q%g.insert(0,charge)' %(particle)) #Enter new charge value
        eval('self.M%g.delete(0,END)' %(particle)) #Delete charge value
        eval('self.M%g.insert(0,mass)' %(particle)) #Enter new charge value
          
    def help(self,helptext): #displays pop-up message, where the message is passed in as a string
        showinfo(message=helptext)
       
    def canvas(self, frame): #Creates a canvas widget to store the final plot
        self.fig = plt.Figure(figsize=(9,9), dpi=100) #creates figure with fixed grid size        
        self.canvas = FigureCanvasTkAgg(self.fig,frame) #Assigns created figure to canvas
        self.canvas.show() 
        self.canvas.get_tk_widget().grid(row = 0, column = 4,rowspan=9,padx=50) #Places canvas at certain grid position
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, frame) #Adds toolbar below canvas
        self.toolbar.update()
        self.toolbar.grid(row = 22, column = 4) #Places toolbar in grid position
        
root = Tk() #Runs main menu as Tk instance when code is run
GUI = Menu(root)
root.mainloop() 
