#!/usr/bin/env python
# coding: utf-8

# In[15]:


#import necessary components# Python program to create 
import pandas as pd 
from datetime import datetime, date
from tkinter import *
import numpy as np
import seaborn as sb; sb.set()
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
from matplotlib import rcParams
from tkinter import filedialog 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.filedialog import asksaveasfilename 

# Function for opening the  
# file explorer window 

    
# Create the root window 
window = Tk()

# Set window title 
window.title('HEATMAPPA') 
   
# Set window size 
window.geometry("525x400") 
   
# Set window background color 
window.config(background = "white") 

#Color map ON or OFF

CmapOn= IntVar()

cc=Checkbutton(window, 
    text="Color map ON(checked)/OFF(unchecked)",font='Times 15',  
    variable=CmapOn,
    onvalue=1, offvalue=0)
cc.grid(row = 4, column = 0, columnspan=2, pady = 3)


# open file
def browseFiles(): 
    #set df as global variable
    global filename
    filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("Text files", 
                                                        "*.txt"), 
                                                       ("all files", 
                                                        "*.*")))
    label_file_explorer.configure(text="FILE PATH: "+filename)  

    
# make graph and save it    
    
class mclass:           
            
        def __init__(self,  window):
            self.window = window
            self.button = Button (window, text="Plot and Save",font='Times 15', command=self.plot)
            self.button.grid(row=19 , column = 0)   

        def plot(self):
            global smplN
            smplN = e2.get()
            global ttle
            ttle=e1.get()
            global canvas
            global fig
            global file
            global sv
            global NCC
            global NC
            global df
            global val1
            
            global sclmax
            global sclmin
            
            global shrink
            
            val1 = CmapOn.get()
            sclmax=int(e3.get())       #maximum scale value collected from window in widget
            sclmin=0-int(sclmax)       #mimimum scale value collected from window in widget deriving from sclmax
            
            files = [('Figure', '*.png')] 
            file = asksaveasfilename(filetypes = files, defaultextension = files) 
            df=pd.read_table(filename)
            NC=len(df)
            shrink=NC
            NS=int(smplN)
            cols=list(df.columns) 
            S1=cols[2:(NS+2)]
            P1=cols[(NS+2):((NS+2)+(NS))]
            rn= df["Gene ID"]+"-" + df["Name"].astype(str)
            df = df.set_index(rn)
            dfS=df[S1]
            dfP=df[P1]
            dfPV = dfP.replace(np.nan, '', regex=True)
            annotations=np.array(dfPV)
            clrmp = LinearSegmentedColormap.from_list('mycmap', ['yellow', 'white', 'darkviolet'])
            
            #for color map shrinking in proportion with the number of rows samples
            shrink=(39*0.3)/NC
                       
            
            #For rigure size depending on row number
            FS=(NC*25)/48    #figure size 
            T=len(ttle)
            TD=(30*18)/T
            
            if FS>20:
                FSa=FS
            else:
                FSa=20             
            
            if TD>30:
                TD=30

            fig = plt.figure(figsize = (FSa,FS))
            sb.set(font_scale=1)
            plt.title(ttle, fontsize = (TD), fontweight="bold")
            rcParams['axes.titlepad'] = 3
            heat_map = sb.heatmap(dfS, 
                              cmap=clrmp, 
                              center=0, 
                              vmin=sclmin, 
                              vmax=sclmax, 
                              square=True, 
                              annot=annotations,
                              annot_kws={"fontsize":15,"fontweight":"bold", "color":"black"}, 
                              fmt="",
                              cbar=val1,
                              cbar_kws = {"shrink": shrink, 'orientation': 'horizontal', 'pad': 0.2},
                              linewidths=0.3,
                              linecolor='grey')
            fig.savefig(file, dpi=200)

            #canvas = FigureCanvasTkAgg(fig, master=self.window)
            #canvas.get_tk_widget().grid(row=8, column=0, columnspan = 2)
            #canvas.draw()

start= mclass (window)


# to show the file opened
label_file_explorer = Label(window,  
                            text = "FILE PATH:", font='Times 10',
                            width = 40, height = 2,  
                            fg = "blue")


# this wil create a label widget
l1 = Label(window, text = "Title:",font='Times 10') 
l2 = Label(window, text = "Number of samples:",font='Times 10') 
l3 = Label(window, text = "Maximum scale value (absolute)", font='Times 10')

# arrange labels
l1.grid(row = 1, column = 0, sticky = E, pady = 3,padx = 50) 
l2.grid(row = 2, column = 0, sticky = E, pady = 3,padx = 3)
l3.grid(row = 3, column = 0 , sticky =E, pady = 3)

# entry widgets, used to take entry from user 
e1 = Entry(window,bd=5, width=20) 
e2 = Entry(window,bd=5, width=20)
e3 = Entry(window,bd=5, width=10)


# this will arrange entry widgets 
e1.grid(row = 1, column = 1, pady = 3, sticky=W) 
e2.grid(row = 2, column = 1, pady = 3, sticky=W) 
e3.grid(row = 3, column = 1 , sticky =W, pady = 3, padx = 30)
    
# checkbutton widget 
c1 = Button(window,  text = "Browse Files",font='Times 15', 
            command = browseFiles) 
c1.grid(row = 15, column = 0, columnspan = 2) 

# setting the infor for table compatibility
Label(window,text= "Your table must contain the following columns:\n Gene ID\tName\t Samples \t Significance (*,**,***) ",
             width =70, height = 4, fg="red").grid(row = 17, column = 0, columnspan = 2, rowspan = 2, padx = 5, pady = 5) 
  
# button exit
be = Button(window, text = "Exit",font='Times 15',command = window.destroy) 

# arranging button exit
be.grid(row = 19, column = 1) 

# arranging file path label
label_file_explorer.grid(row=0,column=0, columnspan=2)

# my signature
sig=Label(window, text = "by Barbe",font='Times 7').grid(row=20, column=1, sticky=E) 

# Close everythinig
window.mainloop()

