#-----------------------------------------------------------------------------
# Author: Stephanie Ciccone
# BDNE-Visualization_Version2.py
# Consult README.txt for instruction on how to ensure this software properly runs on your machine.
#-----------------------------------------------------------------------------

# imports all necessary libraries and functions
import gc
import os
import csv
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.rcsetup as rcsetup
#print(rcsetup.all_backends)
import matplotlib as mpl
import sys
import Tkinter

# Plot Labels & Titles------------------------------------------------
xlabel = "N"
xlabel1 = """N
Program Written By: Ciccone, Stephanie   |   TRIUMF/McMaster University
Masses: AME 2012 (Wang et al.)   |   Theory:  MOELLER(2003)"""
xlabel1= "N"
xlabel2 = """N
Program Written By: Ciccone, Stephanie   |   TRIUMF/McMaster University
Masses: AME 2012 (Wang et al.)   |   Exp.:  ENSDF, Hosmer (2010), Padgett(2010), Miernik (2013), Birch et al.(2015)"""
xlabel2 = "N"
ylabel = "Z"
                        
CreditTextTHEO_1 = "Program Written By: Ciccone, Stephanie"
CreditTextTHEO_2 = "               TRIUMF/McMaster University"
CreditTextTHEO_3 = "Masses: AME 2012 (Wang et al.)"
CreditTextTHEO_4 = "Theory:        MOELLER(2003)"
CreditTextTHEO_ColorBar_1 = "Program Written By: Ciccone, Stephanie   |   Masses: AME 2012 (Wang et al.)"
CreditTextTHEO_ColorBar_2 = "               TRIUMF/McMaster University   |   Theory:  MOELLER(2003)"

CreditTextEXP_1 = "Program Written By: Ciccone, Stephanie"
CreditTextEXP_2 = "    TRIUMF/McMaster University"
CreditTextEXP_3 = "Masses: AME 2012 (Wang et al.)"
CreditTextEXP_4 = "Exp.: ENSDF, Miernik(2013), Birch(2015)"
CreditTextEXP_5 = "        Hosmer(2010), Padgett(2010)"
CreditTextEXP_6 = "Theory: Moeller(2003)"

Title_Ratio = "Ratio between Theoretical & Experimental Data"
Title_EXP = "Experimentally Known Beta-Delayed Neutron Emitters"
Title_EXP = ""

Title_THEO = "Theoretically Known Beta-Delayed Neutron Emitters"
THEO_ColorTitle_1 = "Theoretically Known Beta-Delayed Neutron Emitters: P(1n) Color Bar"
THEO_ColorTitle_2 = "Theoretically Known Beta-Delayed Neutron Emitters: P(2n) Color Bar"
THEO_ColorTitle_3 = "Theoretically Known Beta-Delayed Neutron Emitters: P(3n) Color Bar"
ColorBarLabel = "Beta-Delayed Neutron Emission Probability"

leg_THEO_1 = "Identified Nuclei"
leg_THEO_2 = "Stable"
leg_THEO_3 = "P(1n) dominates"
leg_THEO_4 = "P(2n) dominates"
leg_THEO_5 = "P(3n) dominates"

leg_EXP_1 = "Stable" #black
leg_EXP_2 = "Delayed Neutron Emission Not Possible" #yellow
leg_EXP_3 = "Potential Precursor" #orange

greek_code_beta = 0x3b2
greek_char_beta = unichr(greek_code_beta).encode('utf-8')

leg_EXP_6 = "Neutron Unbound" #(Sn < 0) #green
leg_EXP_7 = "Not Observed" #white

leg_ValueLabels1_THEO = "  Isotope [%] "
leg_ValueLabels2_THEO = "  P(1n)"
leg_ValueLabels3_THEO = "  P(2n)"
leg_ValueLabels4_THEO = "  P(3n)"
leg_ValueLabels5_THEO = "  P(4n)"

leg_ValueLabels1_EXP = "      Isotope"
leg_ValueLabels2_EXP = "(P1n Exp./P1n Theory)"
leg_ValueLabels3_EXP = "(P2n Exp./P2n Theory)"
leg_ValueLabels4_EXP = "(P3n Exp./P3n Theory)"
leg_ValueLabels5_EXP = "(P4n Exp./P4n Theory)"

leg_ValueLabels1_iso = "     Isotope [%] "
leg_ValueLabels2_iso = "  P(1n)-gs | P(1n)-iso1"
leg_ValueLabels3_iso = "  P(2n)-gs | P(2n)-iso1"
leg_ValueLabels4_iso = "  P(3n)-gs | P(1n)-iso2"
leg_ValueLabels5_iso = "  P(4n)-gs | P(2n)-iso2"
#-----------------------------------------------------------------

class BDNE_GUI(Tkinter.Tk):
    def __init__(self,parent):
        # GUI a hierarchy of objects so each GUI element has a parent or a container
        # ex. button contained in a window
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent #references the parent
        self.initialize() #creates GUI element

    def initialize(self): #can create all GUI elements
        
        self.grid() #how to place widgets in the window (put button at column 2, row 1)

        def OnButtonProgramINFO():
            # text found in Program Information Button
            ABOUT_TEXT = """Beta-Delayed Neutron Chart Program
Author: Stephanie Ciccone, TRIUMF/McMaster University
-------------------------------------------------------------
This program takes data about Beta-Delayed Neutron Emission and uses it to visualize the information in a useful and insightful manner.
It was created at TRIUMF by Stephanie Ciccone, a Co-op student from McMaster University with the guidence of Dr. Iris Dillmann.
It was written using the programming lanquage, Python.

Users first choose which database they wish to work with.
    1. Evaluated Database: Contains P(xn) values taken from ENSDF and
                            Q(bxn) values taken from AME 2012.

    2. Theoretical Database: Contains P(xn) values taken from the MOELLER
                             2003 paper.

If you want to include additional data, you can upload your own data file. All data files must be placed in the Data_Files folder!
Available file formats can be found by clicking the 'User File Formats' button.

Users then choose what range of N and Z values they wish to visualize.

The Chart will zoom in and allow for displaying P(xn) or Ratio values only if the user inputs: 
    1. An N range with a difference equal to 0 and a Z range with a difference equal to 0.
    2. An N range with a difference equal to 4 and a Z range with a difference equal to 4.
    3. An N range with a difference equal to 7 and a Z range with a difference equal to 7.
    4. An N range with a difference equal to 10 and a Z range with a difference equal to 10.

There are 4 checkboxes that quickly set the N(max) and Z(max) to one of the 4 zoom-in ranges.
    
The Chart will output normally if EITHER ranges are different to these limits.
Click the 'NEXT' button after entering your chosen N and Z values to see which display options are available.

Certain ranges may cause aspects of the visualization to be placed in an incorrect position.
Settings have been optimized for the best possible output in as many possible scenarios.

Once the display options are highlighted, choose ONE and click the 'PLOT' button. You will be able to save the visualization if desired.
----------------------------------------------------------------
Data References
Masses: Atomic Mass Evaluation 2012 (Wang et al.)
Experimental Data: Evaluated Nuclear Structure Data File 
Experimental Data from Papers: Miernik(2013), Hosmer(2010), Padgett(2010)
Experimental Data: Z<28 values based on Birch et al. evaluation (NDS 2015)
Theoretical Model: MOELLER (2003)

Software URL: https://github.com/ciccons/TRIUMF-BDNE-Chart
Contact Email: ciccons1928@gmail.com
----------------------------------------------------------------
Acknowledgements: I would like to thank Dr. Iris Dillmann, William Mills, and TRIUMF for contributing to this software project."""
            
            toplevel1 = Tkinter.Toplevel()
            lines = Tkinter.Label(toplevel1,text=ABOUT_TEXT,justify='left') # initializes window containing program info
            lines.grid(column=0,row=0)
            toplevel1.resizable(0,0)

        def OnButtonUFF():
            ABOUT_TEXT = """Data files must be in the format shown. If a P(xn) or Q(bxn) value is unknown in your data, set it to 0.
All data files must be placed in the Data_Files folder!

Formats available for User Files in the Evaluated Database.
Only the FIRST format is available when uploading either experimental or theoretical P(xn) values for the Ratio display option.

HEADER COLUMN TITLES (Each column TAB separated, TAB marked by a -)
N - Z - P(1n) - P(2n) - P(3n) - P(4n) - Nuclei Name  [*Format to upload P(xn) values for the Ratio Display]
    ------------ OR ------------
N - Z - P(1n) - P(2n) - P(3n) - P(4n) - Q(b1n) - Q(b2n) - Q(b3n) - Q(b4n) - Nuclei Name
    ------------ OR ------------
N - Z - P(1n) - P(2n) - P(3n) - P(4n) - Q(b1n) - Q(b2n) - Q(b3n) - Q(b4n) - P(1n)_iso1 - P(2n)_iso1 - P(1n)_iso2 - P(2n)_iso2 - Nuclei Name

Formats available for User Files in the Theoretical Database.
                            
HEADER COLUMN TITLES (Each column TAB separated, TAB marked by a -)
N - Z - P1n - P2n - P3n - Nuclei Name"""
            
            toplevel2 = Tkinter.Toplevel()
            line1 = Tkinter.Label(toplevel2,text=ABOUT_TEXT,justify='left') # initializes window containing program info
            line1.grid(column=0,row=0)
            toplevel2.resizable(0,0)

        buttonINFO = Tkinter.Button(self,text=u"Program Information",command=OnButtonProgramINFO) #add button widget
        buttonINFO.grid(column=1,row=0) #place button in grid

        buttonINFO2 = Tkinter.Button(self,text=u"User File Formats",command=OnButtonUFF)
        buttonINFO2.grid(column=2,row=0)

        labelCRED1 = Tkinter.Label(self,text=u"""    Author: Stephanie Ciccone  [2014]
    Email: ciccons1928@gmail.com""",anchor='w') # add author credit
        labelCRED1.grid(column=3,row=0)

        label1 = Tkinter.Label(self,text=u"Select Database:",anchor='w')
        label1.grid(column=0,row=2,columnspan=5,sticky='EW') #label widget

        def OncheckButtonCHOICE_EXP(): #event for when Experimental Database clicked
            choice_user_EXP = checkButtonCHOICE_EXP.get()

            if choice_user_EXP == 1:
                cUFEXP.configure(state='normal')
                TextEntryEXP.configure(state='normal')
                cCTHEO.configure(state='disabled')
                
            if choice_user_EXP == 0:
                cUFEXP.configure(state='disabled');checkButtonUSER_EXP.set(0)
                TextEntryEXP.configure(state='disabled');userFileEXP.set('')
                cCTHEO.configure(state='normal')

        def OncheckButtonCHOICE_THEO(): #event for when Theoretical Database clicked
            choice_user_THEO = checkButtonCHOICE_THEO.get()

            if choice_user_THEO == 1:
                cUFTHEO.configure(state='normal')
                TextEntryTHEO.configure(state='normal')
                cCEXP.configure(state='disabled')
                
            if choice_user_THEO == 0:
                cUFTHEO.configure(state='disabled');checkButtonUSER_THEO.set(0)
                TextEntryTHEO.configure(state='disabled');userFileTHEO.set('')
                cCEXP.configure(state='normal')

        # buttons to choose database and to choose to upload own data
        checkButtonCHOICE_EXP = Tkinter.IntVar()
        cCEXP = Tkinter.Checkbutton(self,text="Evaluated (ENSDF)",variable=checkButtonCHOICE_EXP,
                                command = OncheckButtonCHOICE_EXP)
        cCEXP.grid(column=1,row=3,sticky='EW')

        checkButtonUSER_EXP = Tkinter.IntVar()
        cUFEXP = Tkinter.Checkbutton(self,text="Upload experiment data:",variable=checkButtonUSER_EXP,state='disabled')
        cUFEXP.grid(column=1,row=4,sticky='EW')

        userFileEXP = Tkinter.StringVar() 
        TextEntryEXP = Tkinter.Entry(self,textvariable=userFileEXP,state='disabled') 
        TextEntryEXP.grid(column=2,row=4,sticky='EW') #add to grid layout

        checkButtonCHOICE_THEO = Tkinter.IntVar()
        cCTHEO = Tkinter.Checkbutton(self,text="Theoretical (MOELLER 2003)",variable=checkButtonCHOICE_THEO,
                                command = OncheckButtonCHOICE_THEO)
        cCTHEO.grid(column=1,row=5,sticky='EW')

        checkButtonUSER_THEO = Tkinter.IntVar()
        cUFTHEO = Tkinter.Checkbutton(self,text="Upload theoretical data:",variable=checkButtonUSER_THEO,
                                      state='disabled')
        cUFTHEO.grid(column=1,row=6,sticky='EW')

        userFileTHEO = Tkinter.StringVar() 
        TextEntryTHEO = Tkinter.Entry(self,textvariable=userFileTHEO,state='disabled') 
        TextEntryTHEO.grid(column=2,row=6,sticky='EW') #add to grid layout

        # labels for plot range information
        label2 = Tkinter.Label(self,anchor='w')
        label2.grid(column=0,row=7,columnspan=5,sticky='EW')
        
        label3 = Tkinter.Label(self,anchor='w',text=u"Plot Range Options: (Click NEXT to proceed when done)")
        label3.grid(column=0,row=8,columnspan=5,sticky='EW') #label widget

        Delta = u"\N{GREEK CAPITAL LETTER DELTA}"

        def OncheckButton0():
            if checkButton0.get() == 1:
                c4.configure(state='disabled');c4.deselect()
                c7.configure(state='disabled');c7.deselect()
                c10.configure(state='disabled');c10.deselect()

                TextEntry3.delete(0,8)
                TextEntry3.insert(0,entryVariable1.get())
                TextEntry4.delete(0,8)
                TextEntry4.insert(0,entryVariable2.get())
                
            if checkButton0.get() == 0:
                c4.configure(state='normal');c4.deselect()
                c7.configure(state='normal');c7.deselect()
                c10.configure(state='normal');c10.deselect()
                TextEntry3.delete(0,8);TextEntry4.delete(0,8)

        def OncheckButton4():
            if checkButton4.get() == 1:
                c0.configure(state='disabled');c0.deselect()
                c7.configure(state='disabled');c7.deselect()
                c10.configure(state='disabled');c10.deselect()

                TextEntry3.delete(0,8)
                TextEntry3.insert(0,entryVariable1.get()+4)
                TextEntry4.delete(0,8)
                TextEntry4.insert(0,entryVariable2.get()+4)
                
            if checkButton4.get() == 0:
                c0.configure(state='normal');c0.deselect()
                c7.configure(state='normal');c7.deselect()
                c10.configure(state='normal');c10.deselect()
                TextEntry3.delete(0,8);TextEntry4.delete(0,8)

        def OncheckButton7():
            if checkButton7.get() == 1:
                c4.configure(state='disabled');c4.deselect()
                c0.configure(state='disabled');c0.deselect()
                c10.configure(state='disabled');c10.deselect()

                TextEntry3.delete(0,8)
                TextEntry3.insert(0,entryVariable1.get()+7)
                TextEntry4.delete(0,8)
                TextEntry4.insert(0,entryVariable2.get()+7)
                
            if checkButton7.get() == 0:
                c4.configure(state='normal');c4.deselect()
                c0.configure(state='normal');c0.deselect()
                c10.configure(state='normal');c10.deselect()
                TextEntry3.delete(0,8);TextEntry4.delete(0,8)

        def OncheckButton10():
            if checkButton10.get() == 1:
                c4.configure(state='disabled');c4.deselect()
                c7.configure(state='disabled');c7.deselect()
                c0.configure(state='disabled');c0.deselect()

                TextEntry3.delete(0,8)
                TextEntry3.insert(0,entryVariable1.get()+10)
                TextEntry4.delete(0,8)
                TextEntry4.insert(0,entryVariable2.get()+10)
                
            if checkButton10.get() == 0:
                c4.configure(state='normal');c4.deselect()
                c7.configure(state='normal');c7.deselect()
                c0.configure(state='normal');c0.deselect()
                TextEntry3.delete(0,8);TextEntry4.delete(0,8)

        checkButton0 = Tkinter.IntVar()
        c0 = Tkinter.Checkbutton(self,text=Delta + "N = 0, " + Delta + "Z = 0 [1x1 Isotopes]",variable=checkButton0,command=OncheckButton0)
        c0.grid(column=1,row=9,sticky='EW')

        checkButton4 = Tkinter.IntVar()
        c4 = Tkinter.Checkbutton(self,text=Delta + "N = 4, " + Delta + "Z = 4 [5x5 Isotopes]",variable=checkButton4,command=OncheckButton4)
        c4.grid(column=1,row=10,sticky='EW')

        checkButton7 = Tkinter.IntVar()
        c7 = Tkinter.Checkbutton(self,text=Delta + "N = 7, " + Delta + "Z = 7 [8x8 Isotopes]*",variable=checkButton7,command=OncheckButton7)
        c7.grid(column=2,row=9,sticky='EW')

        checkButton10 = Tkinter.IntVar()
        c10 = Tkinter.Checkbutton(self,text=Delta + "N = 10, " + Delta + "Z = 10 [11x11 Isotopes]*",variable=checkButton10,command=OncheckButton10)
        c10.grid(column=2,row=10,sticky='EW')

        labelZoom1 = Tkinter.Label(self,anchor='w',text=u"These set N and Z to a zoomed in range.")
        labelZoom1.grid(column=3,row=9,sticky='EW')
        labelZoom2 = Tkinter.Label(self,anchor='w',text=u"Can show P(xn) or Ratio values when zoomed in.")
        labelZoom2.grid(column=3,row=10,sticky='EW')
        
        # buttons for inputting N and Z plot range
        button1 = Tkinter.Button(self,text=u"N (minimum)") #add button widget
        button1.grid(column=0,row=12) #place button in grid
        entryVariable1 = Tkinter.IntVar() #sets variable for N min
        TextEntry1 = Tkinter.Entry(self,textvariable=entryVariable1) 
        TextEntry1.grid(column=1,row=12,sticky='EW') #add to grid layout

        button2 = Tkinter.Button(self,text=u"Z (minimum)") #add button widget
        button2.grid(column=2,row=12) #place button in grid
        entryVariable2 = Tkinter.IntVar()
        TextEntry2 = Tkinter.Entry(self,textvariable=entryVariable2) #create first widget, an Entry widget
        TextEntry2.grid(column=3,row=12,sticky='EW')

        button3 = Tkinter.Button(self,text=u"N (maximum)") #add button widget
        button3.grid(column=0,row=13) #place button in grid   
        entryVariable3 = Tkinter.IntVar()
        TextEntry3 = Tkinter.Entry(self,textvariable=entryVariable3) #create first widget, an Entry widget
        TextEntry3.grid(column=1,row=13,sticky='EW')

        button4 = Tkinter.Button(self,text=u"Z (maximum)") #add button widget
        button4.grid(column=2,row=13) #place button in grid
        entryVariable4 = Tkinter.IntVar()
        TextEntry4 = Tkinter.Entry(self,textvariable=entryVariable4) #create first widget, an Entry widget
        TextEntry4.grid(column=3,row=13,sticky='EW')

        def NextButton(): #event for when Next button clicked to highlight display options
            N_low_user = entryVariable1.get()
            N_high_user = entryVariable3.get()
            Z_low_user = entryVariable2.get()
            Z_high_user = entryVariable4.get()

            Delta_N = N_high_user-N_low_user
            Delta_Z = Z_high_user-Z_low_user

            # determines what display options are highlighted based on user choices
            if (checkButtonCHOICE_EXP.get() == 1 and checkButtonCHOICE_THEO.get() == 0):
                check_PxnEXP = checkButtonPxn_EXP.get();check_NORMEXP = checkButtonNORM_EXP.get()
                check_R = checkButtonRatio.get()
                
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    cPxnEXP.configure(state='normal');cNORMEXP.configure(state='normal');cR.configure(state='normal')          
                    cPxnTHEO.configure(state='disabled');cNORMTHEO.configure(state='disabled')
                    cP1nC.configure(state='disabled');cP2nC.configure(state='disabled');cP3nC.configure(state='disabled')
                    
                    cPxnEXP.deselect();cNORMEXP.deselect();cR.deselect()
                    cPxnTHEO.deselect();cNORMTHEO.deselect();cP1nC.deselect();cP2nC.deselect();cP3nC.deselect()
                
                if (Delta_N != 10 or Delta_Z != 10) and (Delta_N != 7 or Delta_Z != 7) and (Delta_N != 4 or Delta_Z != 4) and (Delta_N != 0 or Delta_Z != 0):
                    cPxnEXP.configure(state='disabled');cNORMEXP.configure(state='normal');cR.configure(state='disabled')
                    cPxnTHEO.configure(state='disabled');cNORMTHEO.configure(state='disabled')
                    cP1nC.configure(state='disabled');cP2nC.configure(state='disabled');cP3nC.configure(state='disabled')
                    cXnEXP1.configure(state='normal');cXnEXP2.configure(state='normal')
                    cXnEXP3.configure(state='normal');cXnEXP4.configure(state='normal')
                    
                    cNORMEXP.select();cPxnEXP.deselect();cR.deselect()
                    cPxnTHEO.deselect();cNORMTHEO.deselect();cP1nC.deselect();cP2nC.deselect();cP3nC.deselect()

            if (checkButtonCHOICE_THEO.get() == 1 and checkButtonCHOICE_EXP.get() == 0):
                check_PxnTHEO = checkButtonPxn_THEO.get();check_NORMTHEO = checkButtonNORM_THEO.get()
                check_P1nC = checkButtonP1nC_THEO.get();check_P2nC = checkButtonP2nC_THEO.get();check_P3nC = checkButtonP3nC_THEO.get()
                
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    cPxnTHEO.configure(state='normal');cNORMTHEO.configure(state='normal')
                    cP1nC.configure(state='normal');cP2nC.configure(state='normal');cP3nC.configure(state='normal')
                    cPxnEXP.configure(state='disabled');cNORMEXP.configure(state='disabled');cR.configure(state='disabled')

                    cPxnEXP.deselect();cNORMEXP.deselect();cR.deselect()
                    cPxnTHEO.deselect();cNORMTHEO.deselect();cP1nC.deselect();cP2nC.deselect();cP3nC.deselect()
                    
                if (Delta_N != 10 or Delta_Z != 10) and (Delta_N != 7 or Delta_Z != 7) and (Delta_N != 4 or Delta_Z != 4) and (Delta_N != 0 or Delta_Z != 0):
                    cPxnTHEO.configure(state='disabled');cNORMTHEO.configure(state='normal')
                    cP1nC.configure(state='normal');cP2nC.configure(state='normal');cP3nC.configure(state='normal')                
                    cPxnEXP.configure(state='disabled');cNORMEXP.configure(state='disabled');cR.configure(state='disabled')

                    cPxnEXP.deselect();cNORMEXP.deselect();cR.deselect()
                    cPxnTHEO.deselect();cNORMTHEO.deselect();cP1nC.deselect();cP2nC.deselect();cP3nC.deselect()

        NextButton = Tkinter.Button(self,text=u"NEXT",command=NextButton)
        NextButton.grid(column=5,row=13)

        label6 = Tkinter.Label(self,anchor='w',text=u"*This option might not show all information due to space constraints.")
        label6.grid(column=0,row=14,sticky='EW',columnspan=5)

        # display options for Experimental Database
        label7 = Tkinter.Label(self,anchor='w',text=u"")
        label7.grid(column=0,row=15,columnspan=5,sticky='EW') #label widget

        label8 = Tkinter.Label(self,anchor='w',text=u"Evaluated Database (Only check ONE box before proceeding): ")
        label8.grid(column=0,row=16,columnspan=5,sticky='EW') #label widget

        def OncheckButtonPxn_EXP():
            N_low_user = entryVariable1.get()
            N_high_user = entryVariable3.get()
            Z_low_user = entryVariable2.get()
            Z_high_user = entryVariable4.get()

            Delta_N = N_high_user-N_low_user
            Delta_Z = Z_high_user-Z_low_user
            
            if checkButtonXn_EXP.get() == 1 and ((Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0)):
                cNORMEXP.configure(state='disabled')
                cR.configure(state='disabled')
                cXnEXP1.configure(state='normal');cXnEXP2.configure(state='normal')
                cXnEXP3.configure(state='normal');cXnEXP4.configure(state='normal')
            if checkButtonXn_EXP.get() == 0 and ((Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0)):
                cNORMEXP.configure(state='normal')
                cR.configure(state='normal')
                cXnEXP1.configure(state='disabled');cXnEXP2.configure(state='disabled')
                cXnEXP3.configure(state='disabled');cXnEXP4.configure(state='disabled')
                checkButtonXn_EXP_1n.set(0);checkButtonXn_EXP_2n.set(0)
                checkButtonXn_EXP_3n.set(0);checkButtonXn_EXP_4n.set(0)

        checkButtonPxn_EXP = Tkinter.IntVar()
        cPxnEXP = Tkinter.Checkbutton(self,text="Show P(xn)-Values",variable=checkButtonPxn_EXP,state='disabled',command=OncheckButtonPxn_EXP)
        cPxnEXP.grid(column=1,row=18,sticky='EW')

        def OncheckButtonXn_EXP_1n():
            if checkButtonXn_EXP_1n.get() == 1:
                cXnEXP2.configure(state='disabled');checkButtonXn_EXP_2n.set(0)
                cXnEXP3.configure(state='disabled');checkButtonXn_EXP_3n.set(0)
                cXnEXP4.configure(state='disabled');checkButtonXn_EXP_4n.set(0)
            if checkButtonXn_EXP_1n.get() == 0:
                cXnEXP2.configure(state='normal');checkButtonXn_EXP_2n.set(0)
                cXnEXP3.configure(state='normal');checkButtonXn_EXP_3n.set(0)
                cXnEXP4.configure(state='normal');checkButtonXn_EXP_4n.set(0)

        def OncheckButtonXn_EXP_2n():
            if checkButtonXn_EXP_2n.get() == 1:
                cXnEXP1.configure(state='disabled');checkButtonXn_EXP_1n.set(0)
                cXnEXP3.configure(state='disabled');checkButtonXn_EXP_3n.set(0)
                cXnEXP4.configure(state='disabled');checkButtonXn_EXP_4n.set(0)
            if checkButtonXn_EXP_2n.get() == 0:
                cXnEXP1.configure(state='normal');checkButtonXn_EXP_1n.set(0)
                cXnEXP3.configure(state='normal');checkButtonXn_EXP_3n.set(0)
                cXnEXP4.configure(state='normal');checkButtonXn_EXP_4n.set(0)

        def OncheckButtonXn_EXP_3n():
            if checkButtonXn_EXP_3n.get() == 1:
                cXnEXP2.configure(state='disabled');checkButtonXn_EXP_2n.set(0)
                cXnEXP1.configure(state='disabled');checkButtonXn_EXP_1n.set(0)
                cXnEXP4.configure(state='disabled');checkButtonXn_EXP_4n.set(0)
            if checkButtonXn_EXP_3n.get() == 0:
                cXnEXP2.configure(state='normal');checkButtonXn_EXP_2n.set(0)
                cXnEXP1.configure(state='normal');checkButtonXn_EXP_1n.set(0)
                cXnEXP4.configure(state='normal');checkButtonXn_EXP_4n.set(0)

        def OncheckButtonXn_EXP_4n():
            if checkButtonXn_EXP_4n.get() == 1:
                cXnEXP2.configure(state='disabled');checkButtonXn_EXP_2n.set(0)
                cXnEXP3.configure(state='disabled');checkButtonXn_EXP_3n.set(0)
                cXnEXP1.configure(state='disabled');checkButtonXn_EXP_1n.set(0)
            if checkButtonXn_EXP_4n.get() == 0:
                cXnEXP2.configure(state='normal');checkButtonXn_EXP_2n.set(0)
                cXnEXP3.configure(state='normal');checkButtonXn_EXP_3n.set(0)
                cXnEXP1.configure(state='normal');checkButtonXn_EXP_1n.set(0)
        
        checkButtonXn_EXP_1n = Tkinter.IntVar()
        cXnEXP1 = Tkinter.Checkbutton(self,text="1n",variable=checkButtonXn_EXP_1n,state='disabled',command=OncheckButtonXn_EXP_1n)
        cXnEXP1.grid(column=2,row=17,sticky='EW')
        checkButtonXn_EXP_2n = Tkinter.IntVar()
        cXnEXP2 = Tkinter.Checkbutton(self,text="2n",variable=checkButtonXn_EXP_2n,state='disabled',command=OncheckButtonXn_EXP_2n)
        cXnEXP2.grid(column=3,row=17,sticky='EW')
        checkButtonXn_EXP_3n = Tkinter.IntVar()
        cXnEXP3 = Tkinter.Checkbutton(self,text="3n",variable=checkButtonXn_EXP_3n,state='disabled',command=OncheckButtonXn_EXP_3n)
        cXnEXP3.grid(column=2,row=18,sticky='EW')
        checkButtonXn_EXP_4n = Tkinter.IntVar()
        cXnEXP4 = Tkinter.Checkbutton(self,text="4n",variable=checkButtonXn_EXP_4n,state='disabled',command=OncheckButtonXn_EXP_4n)
        cXnEXP4.grid(column=3,row=18,sticky='EW')

        def OncheckButtonNORM_EXP():
            N_low_user = entryVariable1.get()
            N_high_user = entryVariable3.get()
            Z_low_user = entryVariable2.get()
            Z_high_user = entryVariable4.get()

            Delta_N = N_high_user-N_low_user
            Delta_Z = Z_high_user-Z_low_user

            if checkButtonNORM_EXP.get() == 1 and ((Delta_N != 10 and Delta_Z != 10) or (Delta_N != 7 and Delta_Z != 7) or (Delta_N != 4 and Delta_Z != 4) or (Delta_N != 0 and Delta_Z != 0)):
                cXnEXP1.configure(state='normal');cXnEXP2.configure(state='normal')
                cXnEXP3.configure(state='normal');cXnEXP4.configure(state='normal')
            if checkButtonNORM_EXP.get() == 0 and ((Delta_N != 10 and Delta_Z != 10) or (Delta_N != 7 and Delta_Z != 7) or (Delta_N != 4 and Delta_Z != 4) or (Delta_N != 0 and Delta_Z != 0)):
                cXnEXP1.configure(state='disabled');cXnEXP2.configure(state='disabled')
                cXnEXP3.configure(state='disabled');cXnEXP4.configure(state='disabled')
                checkButtonXn_EXP_1n.set(0);checkButtonXn_EXP_2n.set(0)
                checkButtonXn_EXP_3n.set(0);checkButtonXn_EXP_4n.set(0)
                
            if checkButtonNORM_EXP.get() == 1 and ((Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0)):
                cPxnEXP.configure(state='disabled')
                cR.configure(state='disabled')
                cXnEXP1.configure(state='normal');cXnEXP2.configure(state='normal')
                cXnEXP3.configure(state='normal');cXnEXP4.configure(state='normal')
            if checkButtonNORM_EXP.get() == 0 and ((Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0)):
                cPxnEXP.configure(state='normal')
                cR.configure(state='normal')
                cXnEXP1.configure(state='disabled');cXnEXP2.configure(state='disabled')
                cXnEXP3.configure(state='disabled');cXnEXP4.configure(state='disabled')
                checkButtonXn_EXP_1n.set(0);checkButtonXn_EXP_2n.set(0)
                checkButtonXn_EXP_3n.set(0);checkButtonXn_EXP_4n.set(0)

        checkButtonNORM_EXP = Tkinter.IntVar()
        cNORMEXP = Tkinter.Checkbutton(self,text="Normal",variable=checkButtonNORM_EXP,state='disabled',
                                       command=OncheckButtonNORM_EXP)
        cNORMEXP.grid(column=1,row=17,sticky='EW')

        def OncheckButtonRatio(): #event when Ratio button is clicked
            choice_user_Ratio = checkButtonRatio.get()

            if choice_user_Ratio == 1:
                cREEXP.configure(state='normal')
                cRUEXP.configure(state='disabled')
                TextEntryRUE.configure(state='normal')
                cRMTHEO.configure(state='normal')
                cRUTHEO.configure(state='disabled')
                TextEntryRUT.configure(state='normal')
                cPxnEXP.configure(state='disabled')
                cNORMEXP.configure(state='disabled')

                cREEXP.select();cRMTHEO.select()
                
            if choice_user_Ratio == 0:
                cREEXP.configure(state='disabled')
                cRUEXP.configure(state='disabled')
                TextEntryRUE.configure(state='disabled')
                cRMTHEO.configure(state='disabled')
                cRUTHEO.configure(state='disabled')
                TextEntryRUT.configure(state='disabled')
                cPxnEXP.configure(state='normal')
                cNORMEXP.configure(state='normal')

                cREEXP.deselect();cRMTHEO.deselect()
                cRUEXP.deselect();cRUTHEO.deselect()

        # buttons for displaying options for Ratio
        checkButtonRatio = Tkinter.IntVar()
        cR = Tkinter.Checkbutton(self,text="Show Ratio [Pxn(Exp.)/Pxn(Theo.)]",variable=checkButtonRatio,state='disabled',
                                 command=OncheckButtonRatio)
        cR.grid(column=1,row=19,sticky='EW')

        label9 = Tkinter.Label(self,anchor='w',text=u"            P(xn) Values for Ratio (Exp.): ")
        label9.grid(column=1,row=20,columnspan=5,sticky='EW') #label widget

        def OncheckButtonREEXP():
            if checkButtonRatio_ENSDF_EXP.get() == 0:
                cRUEXP.configure(state='normal');cRUEXP.select();cREEXP.configure(state='disabled')

        checkButtonRatio_ENSDF_EXP = Tkinter.IntVar()
        cREEXP = Tkinter.Checkbutton(self,text="ENSDF",variable=checkButtonRatio_ENSDF_EXP,state='disabled',
                                     command=OncheckButtonREEXP)
        cREEXP.grid(column=2,row=20,sticky='EW')

        def OncheckButtonRUEXP():
            if checkButtonRatio_USER_EXP.get() == 0:
                cREEXP.configure(state='normal');cREEXP.select();cRUEXP.configure(state='disabled')

        checkButtonRatio_USER_EXP = Tkinter.IntVar()
        cRUEXP = Tkinter.Checkbutton(self,text="Upload Experimental P(xn) Data",variable=checkButtonRatio_USER_EXP,state='disabled',
                                     command=OncheckButtonRUEXP)
        cRUEXP.grid(column=2,row=21,sticky='EW')

        ratioUSERFILEEXP = Tkinter.StringVar()
        TextEntryRUE = Tkinter.Entry(self,textvariable=ratioUSERFILEEXP,state='disabled') #create first widget, an Entry widget
        TextEntryRUE.grid(column=3,row=21,sticky='EW')

        label10 = Tkinter.Label(self,anchor='w',text=u"            P(xn) Values for Ratio (Theo.): ")
        label10.grid(column=1,row=22,columnspan=5,sticky='EW') #label widget

        def OncheckButtonRMTHEO():
            if checkButtonRatio_MOE_THEO.get() == 0:
                cRUTHEO.configure(state='normal');cRUTHEO.select();cRMTHEO.configure(state='disabled')

        checkButtonRatio_MOE_THEO = Tkinter.IntVar()
        cRMTHEO = Tkinter.Checkbutton(self,text="MOELLER 2003",variable=checkButtonRatio_MOE_THEO,state='disabled',
                                      command=OncheckButtonRMTHEO)
        cRMTHEO.grid(column=2,row=22,sticky='EW')

        def OncheckButtonRUTHEO():
            if checkButtonRatio_USER_THEO.get() == 0:
                cRMTHEO.configure(state='normal');cRMTHEO.select();cRUTHEO.configure(state='disabled')

        checkButtonRatio_USER_THEO = Tkinter.IntVar()
        cRUTHEO = Tkinter.Checkbutton(self,text="Upload Theoretical P(xn) Data",variable=checkButtonRatio_USER_THEO,state='disabled',
                                      command=OncheckButtonRUTHEO)
        cRUTHEO.grid(column=2,row=23,sticky='EW')

        ratioUSERFILETHEO = Tkinter.StringVar()
        TextEntryRUT = Tkinter.Entry(self,textvariable=ratioUSERFILETHEO,state='disabled') #create first widget, an Entry widget
        TextEntryRUT.grid(column=3,row=23,sticky='EW')

        # display options for theoretical database
        label11 = Tkinter.Label(self,anchor='w',text=u"Theoretical Database (Only check ONE box before proceeding): ")
        label11.grid(column=0,row=24,columnspan=5,sticky='EW') #label widget

        def OncheckButtonPxn_THEO():
            N_low_user = entryVariable1.get()
            N_high_user = entryVariable3.get()
            Z_low_user = entryVariable2.get()
            Z_high_user = entryVariable4.get()

            Delta_N = N_high_user-N_low_user
            Delta_Z = Z_high_user-Z_low_user

            if checkButtonPxn_THEO.get() == 1 and ((Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0)):
                cNORMTHEO.configure(state='disabled')
                cP1nC.configure(state='disabled')
                cP2nC.configure(state='disabled')
                cP3nC.configure(state='disabled')
                cPxnTHEOA.configure(state='normal');cPxnTHEO2.configure(state='normal')
                cPxnTHEO1.configure(state='normal');cPxnTHEO3.configure(state='normal')
            if checkButtonPxn_THEO.get() == 0 and ((Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0)):
                cNORMTHEO.configure(state='normal')
                cP1nC.configure(state='normal')
                cP2nC.configure(state='normal')
                cP3nC.configure(state='normal')
                cPxnTHEOA.configure(state='disabled');cPxnTHEO2.configure(state='disabled')
                cPxnTHEO1.configure(state='disabled');cPxnTHEO3.configure(state='disabled')
                checkButtonPxn_THEO_ALL.set(0);checkButtonPxn_THEO_1n.set(0)
                checkButtonPxn_THEO_2n.set(0);checkButtonPxn_THEO_3n.set(0)

        checkButtonPxn_THEO = Tkinter.IntVar()
        cPxnTHEO = Tkinter.Checkbutton(self,text="Show P(xn)-Values",variable=checkButtonPxn_THEO,state='disabled',command=OncheckButtonPxn_THEO)
        cPxnTHEO.grid(column=1,row=26,sticky='EW')

        def OncheckButtonPxn_THEO_ALL():
            if checkButtonPxn_THEO_ALL.get() == 1:
                cPxnTHEO1.configure(state='disabled');cPxnTHEO2.configure(state='disabled')
                cPxnTHEO3.configure(state='disabled')
            if checkButtonPxn_THEO_ALL.get() == 0:
                cPxnTHEO1.configure(state='normal');cPxnTHEO2.configure(state='normal')
                cPxnTHEO3.configure(state='normal')
                
        def OncheckButtonPxn_THEO_xn():
            if checkButtonPxn_THEO_1n.get() == 1 or checkButtonPxn_THEO_2n.get() == 1 or checkButtonPxn_THEO_3n.get() == 1:
                cPxnTHEOA.configure(state='disabled')
            if checkButtonPxn_THEO_1n.get() == 0 and checkButtonPxn_THEO_2n.get() == 0 and checkButtonPxn_THEO_3n.get() == 0:
                cPxnTHEOA.configure(state='normal')
        
        checkButtonPxn_THEO_ALL = Tkinter.IntVar()
        cPxnTHEOA = Tkinter.Checkbutton(self,text="ALL",variable=checkButtonPxn_THEO_ALL,state='disabled',command=OncheckButtonPxn_THEO_ALL)
        cPxnTHEOA.grid(column=2,row=25,sticky='EW')
        checkButtonPxn_THEO_1n = Tkinter.IntVar()
        cPxnTHEO1 = Tkinter.Checkbutton(self,text="P(1n)",variable=checkButtonPxn_THEO_1n,state='disabled',command=OncheckButtonPxn_THEO_xn)
        cPxnTHEO1.grid(column=3,row=25,sticky='EW')
        checkButtonPxn_THEO_2n = Tkinter.IntVar()
        cPxnTHEO2 = Tkinter.Checkbutton(self,text="P(2n)",variable=checkButtonPxn_THEO_2n,state='disabled',command=OncheckButtonPxn_THEO_xn)
        cPxnTHEO2.grid(column=2,row=26,sticky='EW')
        checkButtonPxn_THEO_3n = Tkinter.IntVar()
        cPxnTHEO3 = Tkinter.Checkbutton(self,text="P(3n)",variable=checkButtonPxn_THEO_3n,state='disabled',command=OncheckButtonPxn_THEO_xn)
        cPxnTHEO3.grid(column=3,row=26,sticky='EW')

        def OncheckButtonNORM_THEO():
            N_low_user = entryVariable1.get()
            N_high_user = entryVariable3.get()
            Z_low_user = entryVariable2.get()
            Z_high_user = entryVariable4.get()

            Delta_N = N_high_user-N_low_user
            Delta_Z = Z_high_user-Z_low_user
            
            if checkButtonNORM_THEO.get() == 1:
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    cPxnTHEO.configure(state='disabled')
                cP1nC.configure(state='disabled')
                cP2nC.configure(state='disabled')
                cP3nC.configure(state='disabled')
                cPxnTHEOA.configure(state='normal');cPxnTHEO2.configure(state='normal')
                cPxnTHEO1.configure(state='normal');cPxnTHEO3.configure(state='normal')
                
            if checkButtonNORM_THEO.get() == 0:
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    cPxnTHEO.configure(state='normal')
                cP1nC.configure(state='normal')
                cP2nC.configure(state='normal')
                cP3nC.configure(state='normal')
                cPxnTHEOA.configure(state='disabled');cPxnTHEO2.configure(state='disabled')
                cPxnTHEO1.configure(state='disabled');cPxnTHEO3.configure(state='disabled')
                checkButtonPxn_THEO_ALL.set(0);checkButtonPxn_THEO_1n.set(0)
                checkButtonPxn_THEO_2n.set(0);checkButtonPxn_THEO_3n.set(0)
                

        checkButtonNORM_THEO = Tkinter.IntVar()
        cNORMTHEO = Tkinter.Checkbutton(self,text="Normal",variable=checkButtonNORM_THEO,state='disabled',
                                        command=OncheckButtonNORM_THEO)
        cNORMTHEO.grid(column=1,row=25,sticky='EW')

        def OncheckButtonP1nC_THEO():
            N_low_user = entryVariable1.get()
            N_high_user = entryVariable3.get()
            Z_low_user = entryVariable2.get()
            Z_high_user = entryVariable4.get()

            Delta_N = N_high_user-N_low_user
            Delta_Z = Z_high_user-Z_low_user
            
            if checkButtonP1nC_THEO.get() == 1:
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    cPxnTHEO.configure(state='disabled')
                cNORMTHEO.configure(state='disabled')
                cP2nC.configure(state='disabled')
                cP3nC.configure(state='disabled')
            if checkButtonP1nC_THEO.get() == 0:
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    cPxnTHEO.configure(state='normal')
                cNORMTHEO.configure(state='normal')
                cP2nC.configure(state='normal')
                cP3nC.configure(state='normal')

        checkButtonP1nC_THEO = Tkinter.IntVar()
        cP1nC = Tkinter.Checkbutton(self,text="Show P(1n) Color Bar Gradient",variable=checkButtonP1nC_THEO,state='disabled',
                                    command=OncheckButtonP1nC_THEO)
        cP1nC.grid(column=1,row=27,sticky='EW')

        def OncheckButtonP2nC_THEO():
            N_low_user = entryVariable1.get()
            N_high_user = entryVariable3.get()
            Z_low_user = entryVariable2.get()
            Z_high_user = entryVariable4.get()

            Delta_N = N_high_user-N_low_user
            Delta_Z = Z_high_user-Z_low_user
            
            if checkButtonP2nC_THEO.get() == 1:
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    cPxnTHEO.configure(state='disabled')
                cNORMTHEO.configure(state='disabled')
                cP1nC.configure(state='disabled')
                cP3nC.configure(state='disabled')
            if checkButtonP2nC_THEO.get() == 0:
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    cPxnTHEO.configure(state='normal')
                cNORMTHEO.configure(state='normal')
                cP1nC.configure(state='normal')
                cP3nC.configure(state='normal')

        checkButtonP2nC_THEO = Tkinter.IntVar()
        cP2nC = Tkinter.Checkbutton(self,text="Show P(2n) Color Bar Gradient",variable=checkButtonP2nC_THEO,state='disabled',
                                    command=OncheckButtonP2nC_THEO)
        cP2nC.grid(column=2,row=27,sticky='EW')

        def OncheckButtonP3nC_THEO():
            N_low_user = entryVariable1.get()
            N_high_user = entryVariable3.get()
            Z_low_user = entryVariable2.get()
            Z_high_user = entryVariable4.get()

            Delta_N = N_high_user-N_low_user
            Delta_Z = Z_high_user-Z_low_user
            
            if checkButtonP3nC_THEO.get() == 1:
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    cPxnTHEO.configure(state='disabled')
                cNORMTHEO.configure(state='disabled')
                cP2nC.configure(state='disabled')
                cP1nC.configure(state='disabled')
            if checkButtonP3nC_THEO.get() == 0:
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    cPxnTHEO.configure(state='normal')
                cNORMTHEO.configure(state='normal')
                cP2nC.configure(state='normal')
                cP1nC.configure(state='normal')

        checkButtonP3nC_THEO = Tkinter.IntVar()
        cP3nC = Tkinter.Checkbutton(self,text="Show P(3n) Color Bar Gradient",variable=checkButtonP3nC_THEO,state='disabled',
                                    command=OncheckButtonP3nC_THEO)
        cP3nC.grid(column=3,row=27,sticky='EW')

        def PLOT(): # event when PLOT button clicked; will display the visualization based on user options
            # obtains all relevant variable values from GUI
            choice_user_EXP = checkButtonCHOICE_EXP.get()
            choice_user_THEO = checkButtonCHOICE_THEO.get()
            
            N_low_user = entryVariable1.get()
            N_high_user = entryVariable3.get()
            Z_low_user = entryVariable2.get()
            Z_high_user = entryVariable4.get()
            Delta_N = N_high_user-N_low_user
            Delta_Z = Z_high_user-Z_low_user

            if choice_user_EXP == 1 and choice_user_THEO == 0:
                choice_USERFILE_EXP = checkButtonUSER_EXP.get()
                if choice_USERFILE_EXP == 1:
                    userFile_EXP = userFileEXP.get()

                Pxn_EXP = checkButtonPxn_EXP.get()
                Xn_EXP1 = checkButtonXn_EXP_1n.get();Xn_EXP2 = checkButtonXn_EXP_2n.get()
                Xn_EXP3 = checkButtonXn_EXP_3n.get();Xn_EXP4 = checkButtonXn_EXP_4n.get()
                NORM_EXP = checkButtonNORM_EXP.get()

                if Xn_EXP1 == 1:
                    leg_EXP_4 = "%"+r'$\beta$'+"-1n Measured" #red
                    leg_EXP_5 = "%"+r'$\beta$'+"-1n Upper Limit Determined" #blue
                if Xn_EXP2 == 1:
                    leg_EXP_4 = "%"+r'$\beta$'+"-2n Measured" #red
                    leg_EXP_5 = "%"+r'$\beta$'+"-2n Upper Limit Determined" #blue
                if Xn_EXP3 == 1:
                    leg_EXP_4 = "%"+r'$\beta$'+"-3n Measured" #red
                    leg_EXP_5 = "%"+r'$\beta$'+"-3n Upper Limit Determined" #blue
                if Xn_EXP4 == 1:
                    leg_EXP_4 = "%"+r'$\beta$'+"-4n Measured" #red
                    leg_EXP_5 = "%"+r'$\beta$'+"-4n Upper Limit Determined" #blue
                
                Ratio = checkButtonRatio.get()
                if Ratio == 1:
                    Ratio_ENSDF_EXP = checkButtonRatio_ENSDF_EXP.get()
                    Ratio_USER_EXP = checkButtonRatio_USER_EXP.get()
                    if Ratio_USER_EXP == 1 and Ratio_ENSDF_EXP == 0:
                        Ratio_USERFILE_EXP = ratioUSERFILEEXP.get()

                    Ratio_MOE_THEO = checkButtonRatio_MOE_THEO.get()
                    Ratio_USER_THEO = checkButtonRatio_USER_THEO.get()
                    if Ratio_USER_THEO == 1 and Ratio_MOE_THEO == 0:
                        Ratio_USERFILE_THEO = ratioUSERFILETHEO.get()
                    

            if choice_user_THEO == 1 and choice_user_EXP == 0:
                choice_USERFILE_THEO = checkButtonUSER_THEO.get()
                if choice_USERFILE_THEO == 1:
                    userFile_THEO = userFileTHEO.get()

                Pxn_THEO = checkButtonPxn_THEO.get()
                PxnTHEOA = checkButtonPxn_THEO_ALL.get();PxnTHEO1 = checkButtonPxn_THEO_1n.get()
                PxnTHEO2 = checkButtonPxn_THEO_2n.get();PxnTHEO3 = checkButtonPxn_THEO_3n.get()
                NORM_THEO = checkButtonNORM_THEO.get()
                P1nC_THEO = checkButtonP1nC_THEO.get()
                P2nC_THEO = checkButtonP2nC_THEO.get()
                P3nC_THEO = checkButtonP3nC_THEO.get()
                
            USER_filename_EXP = '';USER_filename_THEO = ''

            # determines if running on a Windows or a Unix machine and yields the required directory deliminator
            if os.name == "nt":
                dirDelim = "\\"
            else:
                dirDelim = "/"
                mpl.rcParams['backend'] = "TkAgg"
            #print mpl.rcParams['backend']
                
            if choice_user_THEO == 1 and choice_user_EXP == 0: #theoretical database
                # reads in values from text files and stores all of the data columns into arrays
                filename_MOE = os.getcwd() + dirDelim + "Data_Files" + dirDelim + "ChartNuclides_DataTable_MOELLER.txt"        
                user_P = 0
                    
                if choice_USERFILE_THEO == 1:
                    filename_THEORY_USER = os.getcwd() + dirDelim + "Data_Files" + dirDelim + userFile_THEO

                    ELE_names_THEORY = np.genfromtxt(filename_THEORY_USER,skip_header=1,usecols=(5),dtype=str,unpack=True)
                    N_P_USER,Z_P_USER,P1n_USER,P2n_USER,P3n_USER = np.loadtxt(filename_THEORY_USER,skiprows=1,usecols=(0, 1, 2, 3, 4),unpack=True)
                    size_P_USER = len(N_P_USER) ; user_P = 1

                N_stable,Z_stable = np.loadtxt(filename_MOE,skiprows=1,usecols=(0, 1),unpack=True)
                s1 = len(N_stable)

                N,Z = np.loadtxt(filename_MOE,skiprows=1,usecols=(2, 3),unpack=True)
                s2 = len(N)

                ELE_names_MOE = np.genfromtxt(filename_MOE,skip_header=1,usecols=(9),dtype=str,unpack=True)
                N_P,Z_P,P1n,P2n,P3n = np.loadtxt(filename_MOE,skiprows=1,usecols=(4, 5, 6, 7, 8),unpack=True)
                size_P = len(N_P)

                #-------------------------------------------------------------------------
                # list of text in order to properly set up the legend            
                N_high_user=N_high_user+1
                N_low_user=N_low_user-1
                #-----------------------------------------------------------------------------           
                # this part of the code makes an array for only the N and Z values that denote a stable nuclei from the basic data files
                N_stable_Bound = [];Z_stable_Bound = [];blank = 0
                append_NstableB = N_stable_Bound.append;append_ZstableB = Z_stable_Bound.append

                for i in xrange(0,s1):
                    if Z_stable[i] >= Z_low_user and Z_stable[i] <= Z_high_user:
                        if Z_stable[i] == 0 and N_stable[i] == 0:
                            blank = 1
                        else:
                            append_NstableB(N_stable[i])
                            append_ZstableB(Z_stable[i])
                #------------------------------------------------------------------------------
                # makes an array of the nuclei that are within the user bounds from the basic data files
                N_Bound = []; Z_Bound = [] ; blank = 0
                append_NB = N_Bound.append;append_ZB = Z_Bound.append

                for i in xrange(0,len(N)):
                    if Z[i] >= Z_low_user and Z[i] <= Z_high_user:
                        if Z[i] == 0 and N[i] == 0:
                            blank == 1
                        else:
                            append_NB(N[i])
                            append_ZB(Z[i])

                #------------------------------------------------------------------------------

                # this part of the code makes an array for the N and Z values of the magic number lines from the basic data files
                # also makes an array for all nuclei found in the user bounds
                N_P_Bound = [] ; Z_P_Bound = []
                append_NPB = N_P_Bound.append;append_ZPB = Z_P_Bound.append
                N_Bound_magic = [] ; Z_Bound_magic = []
                append_NBM = N_Bound_magic.append ; append_ZBM = Z_Bound_magic.append

                append_NBM(N_low_user) ; append_ZBM(Z_low_user-1)
                append_NBM(N_high_user) ; append_ZBM(Z_high_user+1)
                N_Bound_magic = np.array(N_Bound_magic) ; Z_Bound_magic = np.array(Z_Bound_magic)

                for i in xrange(0,size_P):
                    if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user:
                        append_NPB(N_P[i])
                        append_ZPB(Z_P[i])

                #-----------------------------------------------------------------------------
                #for loop that determines the size of an array based on isotopes that have probability of beta-delayed emission
                #greater than 0 (measured probability) and determines array of P values that should be displayed on the plot

                # initializes all arrays required to use based on user input
                N_P1n = [];append_NP1 = N_P1n.append
                Z_P1n = [];append_ZP1 = Z_P1n.append
                N_P2n = [];append_NP2 = N_P2n.append
                Z_P2n = [];append_ZP2 = Z_P2n.append
                N_P3n = [];append_NP3 = N_P3n.append
                Z_P3n = [];append_ZP3 = Z_P3n.append

                if P1nC_THEO == 1 and P2nC_THEO == 0 and P3nC_THEO == 0 and NORM_THEO == 0:
                    P1n_Color = [];append_P1NC = P1n_Color.append
                    N_P1n_Color = [];append_NP1C = N_P1n_Color.append
                    Z_P1n_Color = [];append_ZP1C = Z_P1n_Color.append

                if P2nC_THEO == 1 and P1nC_THEO == 0 and P3nC_THEO == 0 and NORM_THEO == 0:
                    P2n_Color = [];append_P2NC = P2n_Color.append
                    N_P2n_Color = [];append_NP2C = N_P2n_Color.append
                    Z_P2n_Color = [];append_ZP2C = Z_P2n_Color.append

                if P3nC_THEO == 1 and P1nC_THEO == 0 and P2nC_THEO == 0 and NORM_THEO == 0:
                    P3n_Color = [];append_P3NC = P3n_Color.append
                    N_P3n_Color = [];append_NP3C = N_P3n_Color.append
                    Z_P3n_Color = [];append_ZP3C = Z_P3n_Color.append

                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    if Pxn_THEO == 1 and P1nC_THEO == 0 and P2nC_THEO == 0 and P3nC_THEO == 0 and NORM_THEO == 0:
                        N_P1n_Bound = [];append_NP1B = N_P1n_Bound.append
                        Z_P1n_Bound = [];append_ZP1B = Z_P1n_Bound.append
                        P1n_Bound = [];append_P1B = P1n_Bound.append
                        N_P2n_Bound = [];append_NP2B = N_P2n_Bound.append
                        Z_P2n_Bound = [];append_ZP2B = Z_P2n_Bound.append
                        P2n_Bound = [];append_P2B = P2n_Bound.append
                        N_P3n_Bound = [];append_NP3B = N_P3n_Bound.append
                        Z_P3n_Bound = [];append_ZP3B = Z_P3n_Bound.append
                        P3n_Bound = [];append_P3B = P3n_Bound.append

                        N_ELE = [];Z_ELE = []
                        append_NELE = N_ELE.append;append_ZELE = Z_ELE.append
                        A_ELE = [];ELE_name = []
                        append_AELE = A_ELE.append;append_ELEn = ELE_name.append

                if user_P == 1:
                    N_P1n_USER = [];append_NP1U = N_P1n_USER.append
                    Z_P1n_USER = [];append_ZP1U = Z_P1n_USER.append
                    N_P2n_USER = [];append_NP2U = N_P2n_USER.append
                    Z_P2n_USER = [];append_ZP2U = Z_P2n_USER.append
                    N_P3n_USER = [];append_NP3U = N_P3n_USER.append
                    Z_P3n_USER = [];append_ZP3U = Z_P3n_USER.append

                    if P1nC_THEO == 1 and P2nC_THEO == 0 and P3nC_THEO == 0 and NORM_THEO == 0:
                        P1n_Color_USER = [];append_P1NCU = P1n_Color_USER.append
                        N_P1n_Color_USER = [];append_NP1CU = N_P1n_Color_USER.append
                        Z_P1n_Color_USER = [];append_ZP1CU = Z_P1n_Color_USER.append

                    if P2nC_THEO == 1 and P1nC_THEO == 0 and P3nC_THEO == 0 and NORM_THEO == 0:
                        P2n_Color_USER = [];append_P2NCU = P2n_Color_USER.append
                        N_P2n_Color_USER = [];append_NP2CU = N_P2n_Color_USER.append
                        Z_P2n_Color_USER = [];append_ZP2CU = Z_P2n_Color_USER.append

                    if P3nC_THEO == 1 and P1nC_THEO == 0 and P2nC_THEO == 0 and NORM_THEO == 0:
                        P3n_Color_USER = [];append_P3NCU = P3n_Color_USER.append
                        N_P3n_Color_USER = [];append_NP3CU = N_P3n_Color_USER.append
                        Z_P3n_Color_USER = [];append_ZP3CU = Z_P3n_Color_USER.append

                    if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                        if Pxn_THEO == 1 and P1nC_THEO == 0 and P2nC_THEO == 0 and P3nC_THEO == 0 and NORM_THEO == 0:
                            N_P1n_Bound_USER = [];append_NP1BU = N_P1n_Bound_USER.append
                            Z_P1n_Bound_USER = [];append_ZP1BU = Z_P1n_Bound_USER.append
                            P1n_Bound_USER = [];append_P1BU = P1n_Bound_USER.append
                            N_P2n_Bound_USER = [];append_NP2BU = N_P2n_Bound_USER.append
                            Z_P2n_Bound_USER = [];append_ZP2BU = Z_P2n_Bound_USER.append
                            P2n_Bound_USER = [];append_P2BU = P2n_Bound_USER.append
                            N_P3n_Bound_USER = [];append_NP3BU = N_P3n_Bound_USER.append
                            Z_P3n_Bound_USER = [];append_ZP3BU = Z_P3n_Bound_USER.append
                            P3n_Bound_USER = [];append_P3BU = P3n_Bound_USER.append

                            N_ELE_USER = [];Z_ELE_USER = []
                            append_NELEU = N_ELE_USER.append;append_ZELEU = Z_ELE_USER.append
                            A_ELE_USER = [];ELE_name_USER = []
                            append_AELEU = A_ELE_USER.append;append_ELEnU = ELE_name_USER.append
                            
                for i in xrange(0,size_P):
                    if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] >= N_low_user and N_P[i] <= N_high_user:
                        if P1n[i] != 0 and P1n[i] > P2n[i] and P1n[i] > P3n[i]:
                            append_NP1(N_P[i]);append_ZP1(Z_P[i]) #makes array of nuclei with dominant P1n values

                        if P1n[i] != 0 and P1nC_THEO == 1 and P2nC_THEO == 0 and P3nC_THEO == 0 and NORM_THEO == 0:
                            append_NP1C(N_P[i]);append_ZP1C(Z_P[i]) #makes an array for the color bar version

                            # determines which color a nuclei will be highlighted as using the color bar
                            if P1n[i] <= 50:
                                if P1n[i] > 0 and P1n[i] <= 10:
                                    append_P1NC('yellow')
                                if P1n[i] > 10 and P1n[i] <= 20:
                                    append_P1NC('orange')
                                if P1n[i] > 20 and P1n[i] <= 30:
                                    append_P1NC('red')
                                if P1n[i] > 30 and P1n[i] <= 40:
                                    append_P1NC('maroon')
                                if P1n[i] > 40:
                                    append_P1NC('lime')
                            if P1n[i] > 50:
                                if P1n[i] <= 60:
                                    append_P1NC('green')
                                if P1n[i] > 60 and P1n[i] <= 70:
                                    append_P1NC('DeepSkyBlue')
                                if P1n[i] > 70 and P1n[i] <= 80:
                                    append_P1NC('blue')
                                if P1n[i] > 80 and P1n[i] <= 90:
                                    append_P1NC('violet')
                                if P1n[i] > 90 and P1n[i] <= 100:
                                    append_P1NC('purple')

                        if P2n[i] != 0 and P2n[i] > P1n[i] and P2n[i] > P3n[i]:
                            append_NP2(N_P[i]);append_ZP2(Z_P[i]) #nuclei with dominant P2n values

                        if P2n[i] != 0 and P2nC_THEO == 1 and P1nC_THEO == 0 and P3nC_THEO == 0 and NORM_THEO == 0:
                            append_NP2C(N_P[i]);append_ZP2C(Z_P[i])

                            if P2n[i] <= 50:
                                if P2n[i] > 0 and P2n[i] <= 10:
                                    append_P2NC('yellow')
                                if P2n[i] > 10 and P2n[i] <= 20:
                                    append_P2NC('orange')
                                if P2n[i] > 20 and P2n[i] <= 30:
                                    append_P2NC('red')
                                if P2n[i] > 30 and P2n[i] <= 40:
                                    append_P2NC('maroon')
                                if P2n[i] > 40:
                                    append_P2NC('lime')
                            if P2n[i] > 50:
                                if P2n[i] <= 60:
                                    append_P2NC('green')
                                if P2n[i] > 60 and P2n[i] <= 70:
                                    append_P2NC('DeepSkyBlue')
                                if P2n[i] > 70 and P2n[i] <= 80:
                                    append_P2NC('blue')
                                if P2n[i] > 80 and P2n[i] <= 90:
                                    append_P2NC('violet')
                                if P2n[i] > 90 and P2n[i] <= 100:
                                    append_P2NC('purple')

                        if P3n[i] != 0 and P3n[i] > P1n[i] and P3n[i] > P2n[i]:
                            append_NP3(N_P[i]);append_ZP3(Z_P[i]) # nuclei with dominant P3n values

                        if P3n[i] != 0 and P3nC_THEO == 1 and P1nC_THEO == 0 and P2nC_THEO == 0 and NORM_THEO == 0:
                            append_NP3C(N_P[i]);append_ZP3C(Z_P[i]) 

                            if P3n[i] <= 50:
                                if P3n[i] > 0 and P3n[i] <= 10:
                                    append_P3NC('yellow')
                                if P3n[i] > 10 and P3n[i] <= 20:
                                    append_P3NC('orange')
                                if P3n[i] > 20 and P3n[i] <= 30:
                                    append_P3NC('red')
                                if P3n[i] > 30 and P3n[i] <= 40:
                                    append_P3NC('maroon')
                                if P3n[i] > 40:
                                    append_P3NC('lime')
                            if P3n[i] > 50:
                                if P3n[i] <= 60:
                                    append_P3NC('green')
                                if P3n[i] > 60 and P3n[i] <= 70:
                                    append_P3NC('DeepSkyBlue')
                                if P3n[i] > 70 and P3n[i] <= 80:
                                    append_P3NC('blue')
                                if P3n[i] > 80 and P3n[i] <= 90:
                                    append_P3NC('violet')
                                if P3n[i] > 90 and P3n[i] <= 100:
                                    append_P3NC('purple')

                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    if Pxn_THEO == 1 and P1nC_THEO == 0 and P2nC_THEO == 0 and P3nC_THEO == 0 and NORM_THEO == 0:
                        for i in xrange(0,size_P):
                            if P1n[i] != 0 and Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                                append_NP1B(N_P[i]);append_ZP1B(Z_P[i]) #makes array for nuclei which will have Pxn data displayed about them
                                append_P1B(P1n[i])
                            if P2n[i] != 0 and Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                                append_NP2B(N_P[i]);append_ZP2B(Z_P[i])
                                append_P2B(P2n[i])
                            if P3n[i] != 0 and Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                                append_NP3B(N_P[i]);append_ZP3B(Z_P[i])
                                append_P3B(P3n[i])
                            if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                                append_NELE(N_P[i])
                                append_ZELE(Z_P[i])
                                append_ELEn(ELE_names_MOE[i])
                                append_AELE(N_P[i]+Z_P[i]) # makes all the arrays used to display element name and mass number, A

                if user_P == 1: #if the user has uploaded their own data, this section of the code will analyze that data to display
                    for i in xrange(0,size_P_USER):
                        if Z_P_USER[i] >= Z_low_user and Z_P_USER[i] <= Z_high_user and N_P_USER[i] >= N_low_user and N_P_USER[i] <= N_high_user:
                            if P1n_USER[i] != 0 and P1n_USER[i] > P2n_USER[i] and P1n_USER[i] > P3n_USER[i]:
                                append_NP1U(N_P_USER[i]);append_ZP1U(Z_P_USER[i]) #makes array of nuclei with dominant P1n values

                            if P1n_USER[i] != 0 and P1nC_THEO == 1 and P2nC_THEO == 0 and P3nC_THEO == 0 and NORM_THEO == 0:
                                append_NP1CU(N_P_USER[i]);append_ZP1CU(Z_P_USER[i]) #makes an array for the color bar version

                                # determines which color a nuclei will be highlighted as using the color bar
                                if P1n_USER[i] <= 50:
                                    if P1n_USER[i] > 0 and P1n_USER[i] <= 10:
                                        append_P1NCU('yellow')
                                    if P1n[i] > 10 and P1n[i] <= 20:
                                        append_P1NCU('orange')
                                    if P1n[i] > 20 and P1n[i] <= 30:
                                        append_P1NCU('red')
                                    if P1n[i] > 30 and P1n[i] <= 40:
                                        append_P1NCU('maroon')
                                    if P1n[i] > 40:
                                        append_P1NCU('lime')
                                if P1n_USER[i] > 50:
                                    if P1n_USER[i] <= 60:
                                        append_P1NCU('green')
                                    if P1n_USER[i] > 60 and P1n_USER[i] <= 70:
                                        append_P1NCU('DeepSkyBlue')
                                    if P1n_USER[i] > 70 and P1n_USER[i] <= 80:
                                        append_P1NCU('blue')
                                    if P1n_USER[i] > 80 and P1n_USER[i] <= 90:
                                        append_P1NCU('violet')
                                    if P1n_USER[i] > 90 and P1n_USER[i] <= 100:
                                        append_P1NCU('purple')

                            if P2n_USER[i] != 0 and P2n_USER[i] > P1n_USER[i] and P2n_USER[i] > P3n_USER[i]:
                                append_NP2U(N_P_USER[i]);append_ZP2U(Z_P_USER[i]) #nuclei with dominant P2n values

                            if P2n_USER[i] != 0 and P2nC_THEO == 1 and P1nC_THEO == 0 and P3nC_THEO == 0 and NORM_THEO == 0:
                                append_NP2CU(N_P_USER[i]);append_ZP2CU(Z_P_USER[i])

                                if P2n_USER[i] <= 50:
                                    if P2n_USER[i] > 0 and P2n_USER[i] <= 10:
                                        append_P2NCU('yellow')
                                    if P2n_USER[i] > 10 and P2n_USER[i] <= 20:
                                        append_P2NCU('orange')
                                    if P2n_USER[i] > 20 and P2n_USER[i] <= 30:
                                        append_P2NCU('red')
                                    if P2n_USER[i] > 30 and P2n_USER[i] <= 40:
                                        append_P2NCU('maroon')
                                    if P2n_USER[i] > 40:
                                        append_P2NCU('lime')
                                if P2n_USER[i] > 50:
                                    if P2n_USER[i] <= 60:
                                        append_P2NCU('green')
                                    if P2n_USER[i] > 60 and P2n_USER[i] <= 70:
                                        append_P2NCU('DeepSkyBlue')
                                    if P2n_USER[i] > 70 and P2n_USER[i] <= 80:
                                        append_P2NCU('blue')
                                    if P2n_USER[i] > 80 and P2n_USER[i] <= 90:
                                        append_P2NCU('violet')
                                    if P2n_USER[i] > 90 and P2n_USER[i] <= 100:
                                        append_P2NCU('purple')

                            if P3n_USER[i] != 0 and P3n_USER[i] > P1n_USER[i] and P3n_USER[i] > P2n_USER[i]:
                                append_NP3U(N_P_USER[i]);append_ZP3U(Z_P_USER[i]) # nuclei with dominant P3n values

                            if P3n_USER[i] != 0 and P3nC_THEO == 1 and P1nC_THEO == 0 and P2nC_THEO == 0 and NORM_THEO == 0:
                                append_NP3CU(N_P_USER[i]);append_ZP3CU(Z_P_USER[i]) 

                                if P3n_USER[i] <= 50:
                                    if P3n_USER[i] > 0 and P3n_USER[i] <= 10:
                                        append_P3NCU('yellow')
                                    if P3n_USER[i] > 10 and P3n_USER[i] <= 20:
                                        append_P3NCU('orange')
                                    if P3n_USER[i] > 20 and P3n_USER[i] <= 30:
                                        append_P3NCU('red')
                                    if P3n_USER[i] > 30 and P3n_USER[i] <= 40:
                                        append_P3NCU('maroon')
                                    if P3n_USER[i] > 40:
                                        append_P3NCU('lime')
                                if P3n_USER[i] > 50:
                                    if P3n_USER[i] <= 60:
                                        append_P3NCU('green')
                                    if P3n_USER[i] > 60 and P3n_USER[i] <= 70:
                                        append_P3NCU('DeepSkyBlue')
                                    if P3n_USER[i] > 70 and P3n_USER[i] <= 80:
                                        append_P3NCU('blue')
                                    if P3n_USER[i] > 80 and P3n_USER[i] <= 90:
                                        append_P3NCU('violet')
                                    if P3n_USER[i] > 90 and P3n_USER[i] <= 100:
                                        append_P3NCU('purple')

                    if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                        if Pxn_THEO == 1 and P1nC_THEO == 0 and P2nC_THEO == 0 and P3nC_THEO == 0 and NORM_THEO == 0:
                            for i in xrange(0,size_P_USER):
                                if P1n_USER[i] != 0 and Z_P_USER[i] >= Z_low_user and Z_P_USER[i] <= Z_high_user and N_P_USER[i] > N_low_user and N_P_USER[i] < N_high_user:
                                    append_NP1BU(N_P_USER[i]);append_ZP1BU(Z_P_USER[i]) #makes array for nuclei which will have Pxn data displayed about them
                                    append_P1BU(P1n_USER[i])
                                if P2n_USER[i] != 0 and Z_P_USER[i] >= Z_low_user and Z_P_USER[i] <= Z_high_user and N_P_USER[i] > N_low_user and N_P_USER[i] < N_high_user:
                                    append_NP2BU(N_P_USER[i]);append_ZP2BU(Z_P_USER[i])
                                    append_P2BU(P2n_USER[i])
                                if P3n_USER[i] != 0 and Z_P_USER[i] >= Z_low_user and Z_P_USER[i] <= Z_high_user and N_P_USER[i] > N_low_user and N_P_USER[i] < N_high_user:
                                    append_NP3BU(N_P_USER[i]);append_ZP3BU(Z_P_USER[i])
                                    append_P3BU(P3n_USER[i])
                                if Z_P_USER[i] >= Z_low_user and Z_P_USER[i] <= Z_high_user and N_P_USER[i] > N_low_user and N_P_USER[i] < N_high_user:
                                    append_NELEU(N_P_USER[i])
                                    append_ZELEU(Z_P_USER[i])
                                    append_ELEnU(ELE_names_THEORY[i])
                                    append_AELEU(N_P_USER[i]+Z_P_USER[i]) # makes all the arrays used to display element name and mass number, A

                #---------------------------------------------------------------------------
                
                color1='black'
                color2='Tomato'
                color3='DeepSkyBlue'
                color4='Orange'
                c1=0;c2=0;c3=0;c4=0;c5=0;c6=0
                
                # all variables necessary to tweak the plots for optimal viewing
                #if (Delta_N != 10 and Delta_Z != 10) or (Delta_N != 7 and Delta_Z != 7) or (Delta_N != 4 and Delta_Z != 4) or (Delta_N != 0 and Delta_Z != 0):
                if (Delta_N > 80) or (Delta_Z > 80):
                    msize = 2.7
                    mew = 0.5;ms1=1
                    lw1 = 0.5;lw2 = 1
                    ax1_1=0.93;ax1_2=0.1;ax1_3=0.02;ax1_4=0.8
                    Cred_N = -0.3;Cred_Z1=-0.4;Cred_Z2=0
                    
                if ((Delta_N > 10) and Delta_N <= 80) and ((Delta_Z > 10) and Delta_Z <= 80):
                    msize = 9
                    mew = 1.0;ms1=1
                    lw1 = 0.5;lw2 = 1
                    ax1_1=0.93;ax1_2=0.1;ax1_3=0.02;ax1_4=0.8
                    Cred_N = -0.3;Cred_Z1=-0.4;Cred_Z2=0

                if ((Delta_N != 7 and Delta_Z != 7) or (Delta_N != 4 and Delta_Z != 4) or (Delta_N != 0 and Delta_Z != 0)) and (Delta_N <= 10 and Delta_Z <= 10):
                    msize = 35
                    mew = 1.5;ms1=0.2;ms2=0
                    lw1 = 2.0;lw2 = 2.5
                    Cred_N = -0.3 
                    Cred_Z1=-0.4;Cred_Z2=0;Cred_Z3=0.4 
                    Cred_Z4=0.8;Cred_Z5=1.2;Cred_Z6=1.6
                    if (P1nC_THEO == 1 or P2nC_THEO == 1 or P3nC_THEO == 1):
                        Cred_N = 2
                        Cred_Z1=1.8;Cred_Z2=2.2
                    N_ELE_adj1=0.37;Z_ELE_adj1=0.15
                    fontsize_set_1=9;fontsize_set_2=9;fontsize_set_3=8
                    N_adj=0.28;N_adj_r=0.28
                    Z_adj_1=-0.06;Z_adj_2=-0.3
                    ax1_1=0.75;ax1_2=0.1;ax1_3=0.02;ax1_4=0.8

                if (Delta_N == 7 and Delta_Z == 7):
                    msize = 45
                    mew = 3.0;ms1=0.2;ms2=0
                    lw1 = 2.0;lw2 = 2.5
                    Cred_N = -0.2
                    Cred_Z1=0.2;Cred_Z2=0.4;Cred_Z3=0.6 
                    Cred_Z4=0.8;Cred_Z5=1;Cred_Z6=1.2
                    if (P1nC_THEO == 1 or P2nC_THEO == 1 or P3nC_THEO == 1):
                        Cred_N = 1.5
                        Cred_Z1=1.6;Cred_Z2=1.8
                    N_ELE_adj1=0.3;Z_ELE_adj1=0.2
                    fontsize_set_1=10;fontsize_set_2=9;fontsize_set_3=8
                    N_adj=0.25;N_adj_r=0.25
                    Z_adj_1=0.05;Z_adj_2=-0.1;Z_adj_3=-0.25;Z_adj_4=-0.4
                    ax1_1=0.75;ax1_2=0.1;ax1_3=0.02;ax1_4=0.8

                if (Delta_N == 4 and Delta_Z == 4):
                    msize = 70
                    mew = 4.0;ms1=0.1;ms2=0
                    lw1 = 3.0;lw2 = 3.5
                    Cred_N = -0.1 
                    Cred_Z1=0.2;Cred_Z2=0.4;Cred_Z3=0.6
                    Cred_Z4=0.8;Cred_Z5=1.0;Cred_Z6=1.2
                    if (P1nC_THEO == 1 or P2nC_THEO == 1 or P3nC_THEO == 1):
                        Cred_N = 1
                        Cred_Z1=1.3;Cred_Z2=1.5
                    N_ELE_adj1=0.3;Z_ELE_adj1=0.3
                    fontsize_set_1=12;fontsize_set_2=11;fontsize_set_3=8.5
                    N_adj=0.4;N_adj_i=0;N_adj_r=0.25
                    Z_adj_1=0.15;Z_adj_2=0.05;Z_adj_3=-0.05;Z_adj_4=-0.16
                    ax1_1=0.75;ax1_2=0.1;ax1_3=0.02;ax1_4=0.8

                if Delta_N == 0 and Delta_Z == 0:
                    msize = 200
                    mew = 4.0;ms1=0.05;ms2=0
                    lw1 = 3.0;lw2 = 3.5
                    Cred_N = -0.1 
                    Cred_Z1=0.9;Cred_Z2=0.95;Cred_Z3=1
                    Cred_Z4=1.05;Cred_Z5=1.1;Cred_Z6=1.15
                    if (P1nC_THEO == 1 or P2nC_THEO == 1 or P3nC_THEO == 1):
                        Cred_N = 0.5
                        Cred_Z1=1.1;Cred_Z2=1.15
                    N_ELE_adj1=0.1;Z_ELE_adj1=0.3
                    fontsize_set_1=20;fontsize_set_2=4;fontsize_set_3=18
                    N_adj=0.1;N_adj_i=0;N_adj_r=0.25
                    Z_adj_1=0.2;Z_adj_2=0.1;Z_adj_3=0;Z_adj_4=-0.1
                    ax1_1=0.75;ax1_2=0.1;ax1_3=0.02;ax1_4=0.8
                    
                # if statement which determines which Chart type will be displayed
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    if NORM_THEO == 1 or Pxn_THEO == 1:
                        plt.figure(figsize=(16.5,8))
                        plt.axis('scaled')
                        g=plt.gca()
                        plt.xlim(N_low_user,N_high_user)
                        plt.ylim(Z_low_user-1,Z_high_user+1)

                        Num_xticks = np.arange(N_low_user+1,N_high_user,1)
                        label_xticks = [];append_lx = label_xticks.append
                        for i in xrange(N_low_user+1,N_high_user):
                            c = i%2
                            if c == 0:
                                label_xticks.append(i)
                            else:
                                label_xticks.append("")
                        plt.xticks(Num_xticks,label_xticks)
                        plt.xticks(size=8)
                        
                        Num_yticks = np.arange(Z_low_user,Z_high_user+1,1)
                        label_yticks = [];append_ly = label_yticks.append
                        for i in xrange(Z_low_user,Z_high_user+1):
                            c = i%2
                            if c == 0:
                                label_yticks.append(i)
                            else:
                                label_yticks.append("")
                        plt.yticks(Num_yticks,label_yticks)
                        plt.yticks(size=8)

                        plt.xlabel(xlabel)
                        plt.ylabel(ylabel)

                        # Credits 
                        plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z1,CreditTextTHEO_1,fontsize=10)
                        plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z2,CreditTextTHEO_2,fontsize=10)
                        plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z3,CreditTextTHEO_3,fontsize=10)
                        plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z4,CreditTextTHEO_4,fontsize=10) 


                        plt.title(Title_THEO)
                        leg_entries = []
                        leg_text = []

                        # plots nuclei in user bounds and stable nuclei using basic data files
                        if len(N_P_Bound) != 0:
                            plt.plot(N_P_Bound,Z_P_Bound,marker='s',color='0.85',markersize=msize,markeredgewidth=0,linestyle='')
                        if len(N_Bound) != 0:
                            t0, = plt.plot(N_Bound,Z_Bound,marker='s',color='0.8',markersize=msize,markeredgewidth=mew,linestyle='');c1=1
                        if len(N_stable_Bound) != 0:
                            t1, = plt.plot(N_stable_Bound,Z_stable_Bound,marker='s',color=color1,markersize=msize,markeredgewidth=0,linestyle='');c2=1

                        # highlights nuclei with Pxn values in user bounds using basic data files                                       
                        if len(N_P1n) != 0 and (PxnTHEO1 == 1 or PxnTHEOA == 1):
                            t2, = plt.plot(N_P1n,Z_P1n,marker='s',color=color2,markersize=msize,markeredgewidth=0,linestyle='');c3=1
                        if len(N_P2n) != 0 and (PxnTHEO2 == 1 or PxnTHEOA == 1):
                            t3, = plt.plot(N_P2n,Z_P2n,marker='s',color=color3,markersize=msize,markeredgewidth=0,linestyle='');c4=1
                        if len(N_P3n) != 0 and (PxnTHEO3 == 1 or PxnTHEOA == 1):
                            t4, = plt.plot(N_P3n,Z_P3n,marker='s',color=color4,markersize=msize,markeredgewidth=0,linestyle='');c5=1
                            
                        # highlights nuclei with Pxn values in user bounds using user data files 
                        if user_P == 1:    
                            if len(N_P1n_USER) != 0 and (PxnTHEO1 == 1 or PxnTHEOA == 1):
                                plt.plot(N_P1n_USER,Z_P1n_USER,marker='s',color=color2,markersize=msize,markeredgewidth=0,linestyle='');c3=1
                            if len(N_P2n_USER) != 0 and (PxnTHEO2 == 1 or PxnTHEOA == 1):
                                plt.plot(N_P2n_USER,Z_P2n_USER,marker='s',color=color3,markersize=msize,markeredgewidth=0,linestyle='');c4=1
                            if len(N_P3n_USER) != 0 and (PxnTHEO3 == 1 or PxnTHEOA == 1):
                                plt.plot(N_P3n_USER,Z_P3n_USER,marker='s',color=color4,markersize=msize,markeredgewidth=0,linestyle='');c5=1

                        # determines which magic number lines are necessary to display
                        if N_high_user >= 8 and N_low_user <= 8:  
                            plt.plot(N_Bound_magic*0.+8.5,Z_Bound_magic,color=color1,linewidth=lw1)  
                            plt.plot(N_Bound_magic*0.+7.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 20 and N_low_user <= 20:
                            plt.plot(N_Bound_magic*0.+20.5,Z_Bound_magic,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic*0.+19.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 28 and N_low_user <= 28:
                            plt.plot(N_Bound_magic*0.+28.5,Z_Bound_magic,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic*0.+27.5,Z_Bound_magic,color=color1,linewidth=lw1)     

                        if N_high_user >= 50 and N_low_user <= 50:
                            plt.plot(N_Bound_magic*0.+50.5,Z_Bound_magic,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic*0.+49.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 82 and N_low_user <= 82:
                            plt.plot(N_Bound_magic*0.+82.5,Z_Bound_magic,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic*0.+81.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 126 and N_low_user <= 126:
                            plt.plot(N_Bound_magic*0.+126.5,Z_Bound_magic,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic*0.+125.5,Z_Bound_magic,color=color1,linewidth=lw1) 

                        if Z_high_user >= 8 and Z_low_user <= 8:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+8.5,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+7.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 20 and Z_low_user <= 20:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+20.5,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+19.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 28 and Z_low_user <= 28:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+28.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+27.5,color=color1,linewidth=lw1)             

                        if Z_high_user >= 50 and Z_low_user <= 50:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+50.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+49.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 82 and Z_low_user <= 82:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+82.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+81.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 126 and Z_low_user <= 126:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+126.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+125.5,color=color1,linewidth=lw1)

                        # builds legend
                        if c1 == 1:
                            leg_entries.append(t0);leg_text.append(leg_THEO_1)
                        if c2 == 1:
                            leg_entries.append(t1);leg_text.append(leg_THEO_2)
                        if c3 == 1:
                            leg_entries.append(t2);leg_text.append(leg_THEO_3)
                        if c4 == 1:
                            leg_entries.append(t3);leg_text.append(leg_THEO_4)
                        if c5 == 1:
                            leg_entries.append(t4);leg_text.append(leg_THEO_5)
                            
                        if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                            l1 = plt.legend(leg_entries,leg_text,loc=2,bbox_to_anchor=[1.02,0.98],borderaxespad=0.,markerscale=ms1,numpoints=1)
                            if NORM_THEO == 0 and Delta_Z <= 10 and Delta_N <= 10 and Delta_N > 7 and Delta_Z > 7:
                                l2 = plt.legend((leg_ValueLabels1_THEO,leg_ValueLabels2_THEO,leg_ValueLabels3_THEO),loc=6,bbox_to_anchor=[1.02,0.4],numpoints=1,markerscale=ms2)
                                g.add_artist(l1)
                            if NORM_THEO == 0 and Delta_Z <= 7 and Delta_N <= 7:
                                l2 = plt.legend((leg_ValueLabels1_THEO,leg_ValueLabels2_THEO,leg_ValueLabels3_THEO,leg_ValueLabels4_THEO),loc=6,bbox_to_anchor=[1.02,0.4],numpoints=1,markerscale=ms2)
                                g.add_artist(l1)
                        else:
                            l1 = plt.legend(leg_entries,leg_text,loc=4,markerscale=ms1,numpoints=1)

                        if Pxn_THEO == 1 and NORM_THEO == 0:
                            # outputs Element information (name, Pxn values, etc.) when the user bounds are a certain size
                            if (len(N_ELE) != 0 and len(ELE_name) != 0): 
                                for i in xrange(0,len(N_ELE)):
                                    if user_P == 0: # if no user uploaded files, only use basic data files
                                        ELE_info = ' '.join([ELE_name[i].rstrip('\n'),str(int(A_ELE[i]))])
                                        plt.text(N_ELE[i]-N_ELE_adj1,Z_ELE[i]+Z_ELE_adj1,ELE_info,fontsize=fontsize_set_1)
                                    else: # if user uploaded files exist, give priority to user uploaded files over basic files in what is displayed
                                        for ii in xrange(0,len(N_ELE_USER)):
                                            if N_ELE[i] == N_ELE_USER[ii] and Z_ELE[i] == Z_ELE_USER[ii]:
                                                PriorityCheck = 0
                                                break
                                            else:
                                                PriorityCheck = 1
                                        if PriorityCheck == 1:
                                            ELE_info = ' '.join([ELE_name[i].rstrip('\n'),str(int(A_ELE[i]))])
                                            plt.text(N_ELE[i]-N_ELE_adj1,Z_ELE[i]+Z_ELE_adj1,ELE_info,fontsize=fontsize_set_1)                           

                                if (PxnTHEO1 == 1 or PxnTHEOA == 1) and len(N_P1n_Bound) != 0 and Delta_Z <= 10 and Delta_N <= 10: #for displaying P1n values
                                    for i in xrange(0,len(N_P1n_Bound)):
                                        if user_P == 0:
                                            str_P1n="{0:.2f}".format(P1n_Bound[i])
                                            plt.text(N_P1n_Bound[i]-N_adj,Z_P1n_Bound[i]+Z_adj_1,str_P1n,fontsize=fontsize_set_3)
                                        else:
                                            for ii in xrange(0,len(N_P1n_Bound_USER)):
                                                if N_P1n_Bound[i] == N_P1n_Bound_USER[ii] and Z_P1n_Bound[i] == Z_P1n_Bound_USER[ii]:
                                                    PriorityCheck = 0
                                                    break
                                                else:
                                                    PriorityCheck = 1
                                            if PriorityCheck == 1:
                                                str_P1n="{0:.2f}".format(P1n_Bound[i])
                                                plt.text(N_P1n_Bound[i]-N_adj,Z_P1n_Bound[i]+Z_adj_1,str_P1n,fontsize=fontsize_set_3)

                                if (PxnTHEO2 == 1 or PxnTHEOA == 1) and len(N_P2n_Bound) != 0 and Delta_Z <= 10 and Delta_N <= 10: #for displaying P2n values
                                    for i in xrange(0,len(N_P2n_Bound)):
                                        if user_P == 0:
                                            str_P2n="{0:.2f}".format(P2n_Bound[i])
                                            plt.text(N_P2n_Bound[i]-N_adj,Z_P2n_Bound[i]+Z_adj_2,str_P2n,fontsize=fontsize_set_3)
                                        else:
                                            for ii in xrange(0,len(N_P2n_Bound_USER)):
                                                if N_P2n_Bound[i] == N_P2n_Bound_USER[ii] and Z_P2n_Bound[i] == Z_P2n_Bound_USER[ii]:
                                                    PriorityCheck = 0
                                                    break
                                                else:
                                                    PriorityCheck = 1
                                            if PriorityCheck == 1:
                                                str_P2n="{0:.2f}".format(P2n_Bound[i])
                                                plt.text(N_P2n_Bound[i]-N_adj,Z_P2n_Bound[i]+Z_adj_2,str_P2n,fontsize=fontsize_set_3)

                                if (PxnTHEO3 == 1 or PxnTHEOA == 1) and len(N_P3n_Bound) != 0 and Delta_Z <= 7 and Delta_N <= 7: #for displaying P3n values
                                    for i in xrange(0,len(N_P3n_Bound)):
                                        if user_P == 0:
                                            str_P3n="{0:.2f}".format(P3n_Bound[i])
                                            plt.text(N_P3n_Bound[i]-N_adj,Z_P3n_Bound[i]+Z_adj_3,str_P3n,fontsize=fontsize_set_3)
                                        else:
                                            for ii in xrange(0,len(N_P3n_Bound_USER)):
                                                if N_P3n_Bound[i] != N_P3n_Bound_USER[ii] and Z_P3n_Bound[i] != Z_P3n_Bound_USER[ii]:
                                                    PriorityCheck = 1
                                                else:
                                                    PriorityCheck = 0
                                                    break
                                            if PriorityCheck == 1:
                                                str_P3n="{0:.2f}".format(P3n_Bound[i])
                                                plt.text(N_P3n_Bound[i]-N_adj,Z_P3n_Bound[i]+Z_adj_3,str_P3n,fontsize=fontsize_set_3)

                            if user_P == 1: # displays all info about user uploaded data on nuclei
                                for i in xrange(0,len(N_ELE_USER)):
                                    ELE_info = ' '.join([ELE_name_USER[i].rstrip('\n'),str(int(A_ELE_USER[i]))])
                                    plt.text(N_ELE_USER[i]-N_ELE_adj1,Z_ELE_USER[i]+Z_ELE_adj1,ELE_info,fontsize=fontsize_set_1)

                                if (PxnTHEO1 == 1 or PxnTHEOA == 1) and len(N_P1n_Bound_USER) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                                    for i in xrange(0,len(N_P1n_Bound_USER)):
                                        str_P1nU="{0:.2f}".format(P1n_Bound_USER[i])
                                        plt.text(N_P1n_Bound_USER[i]-N_adj,Z_P1n_Bound_USER[i]+Z_adj_1,str_P1nU,fontsize=fontsize_set_3)

                                if (PxnTHEO2 == 1 or PxnTHEOA == 1) and len(N_P2n_Bound_USER) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                                    for i in xrange(0,len(N_P2n_Bound_USER)):
                                        str_P2nU="{0:.2f}".format(P2n_Bound_USER[i])
                                        plt.text(N_P2n_Bound_USER[i]-N_adj,Z_P2n_Bound_USER[i]+Z_adj_2,str_P2nU,fontsize=fontsize_set_3)

                                if (PxnTHEO3 == 1 or PxnTHEOA == 1) and len(N_P3n_Bound_USER) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                                    for i in xrange(0,len(N_P3n_Bound_USER)):
                                        str_P3nU="{0:.2f}".format(P3n_Bound_USER[i])
                                        plt.text(N_P3n_Bound_USER[i]-N_adj,Z_P3n_Bound_USER[i]+Z_adj_3,str_P3nU,fontsize=fontsize_set_3)

                        plt.show(block=False)
                        
                    if P1nC_THEO == 1 or P2nC_THEO == 1 or P3nC_THEO == 1: # for color bar gradient plots
                        fig = plt.figure(figsize=(16.5,8))

                        plt.axis('scaled')
                        g=plt.gca()
                        plt.xlim(N_low_user,N_high_user)
                        plt.ylim(Z_low_user-1,Z_high_user+1)

                        Num_xticks = np.arange(N_low_user+1,N_high_user,1)
                        label_xticks = [];append_lx = label_xticks.append
                        for i in xrange(N_low_user+1,N_high_user):
                            c = i%2
                            if c == 0:
                                label_xticks.append(i)
                            else:
                                label_xticks.append("")
                        plt.xticks(Num_xticks,label_xticks)
                        plt.xticks(size=8)
                        
                        Num_yticks = np.arange(Z_low_user,Z_high_user+1,1)
                        label_yticks = [];append_ly = label_yticks.append
                        for i in xrange(Z_low_user,Z_high_user+1):
                            c = i%2
                            if c == 0:
                                label_yticks.append(i)
                            else:
                                label_yticks.append("")
                        plt.yticks(Num_yticks,label_yticks)
                        plt.yticks(size=8)

                        plt.xlabel(xlabel)
                        plt.ylabel(ylabel)

                        # plots nuclei, stable nuclei, and color highlights the Pxn values within user bounds using basic data files
                        if len(N_P_Bound) != 0:
                            plt.plot(N_P_Bound,Z_P_Bound,marker='s',color='0.85',markersize=msize,markeredgewidth=0,linestyle='')
                        if len(N_Bound) != 0:
                            plt.plot(N_Bound,Z_Bound,marker='s',color='0.8',markersize=msize,markeredgewidth=mew,linestyle='')
                        if len(N_stable_Bound) != 0:
                            plt.plot(N_stable_Bound,Z_stable_Bound,marker='s',color=color1,markersize=msize,markeredgewidth=0,linestyle='')

                        if P1nC_THEO == 1 and P2nC_THEO == 0 and P3nC_THEO == 0:
                            plt.title(THEO_ColorTitle_1)                           
                            if len(N_P1n_Color) != 0:
                                for i in xrange(0,len(N_P1n_Color)):
                                    plt.plot(N_P1n_Color[i],Z_P1n_Color[i],marker='s',color=P1n_Color[i],markersize=msize,markeredgewidth=0,linestyle='')

                        if P2nC_THEO == 1 and P1nC_THEO == 0 and P3nC_THEO == 0:
                            plt.title(THEO_ColorTitle_2)
                            if len(N_P2n_Color) != 0: 
                                for i in xrange(0,len(N_P2n_Color)):
                                    plt.plot(N_P2n_Color[i],Z_P2n_Color[i],marker='s',color=P2n_Color[i],markersize=msize,markeredgewidth=0,linestyle='')

                        if P3nC_THEO == 1 and P1nC_THEO == 0 and P2nC_THEO == 0:
                            plt.title(THEO_ColorTitle_3)
                            if len(N_P3n_Color) != 0:
                                for i in xrange(0,len(N_P3n_Color)):
                                    plt.plot(N_P3n_Color[i],Z_P3n_Color[i],marker='s',color=P3n_Color[i],markersize=msize,markeredgewidth=0,linestyle='')
                        # plots nuclei,stable nuclei, and color highlights the Pn values within user bounds using user uploaded data files
                        if user_P == 1:
                            if P1nC_THEO == 1 and P2nC_THEO == 0 and P3nC_THEO == 0:
                                plt.title(THEO_ColorTitle_1)
                                if len(N_P1n_Color_USER) != 0:
                                    for i in xrange(0,len(N_P1n_Color_USER)):
                                        plt.plot(N_P1n_Color_USER[i],Z_P1n_Color_USER[i],marker='s',color=P1n_Color_USER[i],markersize=msize,markeredgewidth=0,linestyle='')

                            if P2nC_THEO == 1 and P1nC_THEO == 0 and P3nC_THEO == 0:
                                plt.title(THEO_ColorTitle_2)
                                if len(N_P2n_Color_USER) != 0: 
                                    for i in xrange(0,len(N_P2n_Color_USER)):
                                        plt.plot(N_P2n_Color_USER[i],Z_P2n_Color_USER[i],marker='s',color=P2n_Color_USER[i],markersize=msize,markeredgewidth=0,linestyle='')

                            if P3nC_THEO == 1 and P1nC_THEO == 0 and P2nC_THEO == 0:
                                plt.title(THEO_ColorTitle_3)
                                if len(N_P3n_Color_USER) != 0:
                                    for i in xrange(0,len(N_P3n_Color_USER)):
                                        plt.plot(N_P3n_Color_USER[i],Z_P3n_Color_USER[i],marker='s',color=P3n_Color_USER[i],markersize=msize,markeredgewidth=0,linestyle='')

                        # Credits 
                        plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z1,CreditTextTHEO_ColorBar_1,fontsize=10)
                        plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z2,CreditTextTHEO_ColorBar_2,fontsize=10)

                        # determines which magic number lines are necessary to display
                        if N_high_user >= 8 and N_low_user <= 8:  
                            plt.plot(N_Bound_magic*0.+8.5,Z_Bound_magic,color=color1,linewidth=lw1)  
                            plt.plot(N_Bound_magic*0.+7.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 20 and N_low_user <= 20:
                            plt.plot(N_Bound_magic*0.+20.5,Z_Bound_magic,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic*0.+19.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 28 and N_low_user <= 28:
                            plt.plot(N_Bound_magic*0.+28.5,Z_Bound_magic,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic*0.+27.5,Z_Bound_magic,color=color1,linewidth=lw1)     

                        if N_high_user >= 50 and N_low_user <= 50:
                            plt.plot(N_Bound_magic*0.+50.5,Z_Bound_magic,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic*0.+49.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 82 and N_low_user <= 82:
                            plt.plot(N_Bound_magic*0.+82.5,Z_Bound_magic,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic*0.+81.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 126 and N_low_user <= 126:
                            plt.plot(N_Bound_magic*0.+126.5,Z_Bound_magic,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic*0.+125.5,Z_Bound_magic,color=color1,linewidth=lw1) 

                        if Z_high_user >= 8 and Z_low_user <= 8:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+8.5,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+7.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 20 and Z_low_user <= 20:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+20.5,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+19.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 28 and Z_low_user <= 28:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+28.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+27.5,color=color1,linewidth=lw1)             

                        if Z_high_user >= 50 and Z_low_user <= 50:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+50.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+49.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 82 and Z_low_user <= 82:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+82.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+81.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 126 and Z_low_user <= 126:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+126.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+125.5,color=color1,linewidth=lw1)

                        # outputs color bar
                        ax1 = fig.add_axes([ax1_1,ax1_2,ax1_3,ax1_4])

                        cmap = mpl.colors.ListedColormap(['yellow','orange','red','maroon','lime','green','DeepSkyBlue','blue','violet','purple'])
                        bounds = [0,10,20,30,40,50,60,70,80,90,100]
                        norm = mpl.colors.BoundaryNorm(bounds,cmap.N)
                        cb1 = mpl.colorbar.ColorbarBase(ax1,cmap=cmap,norm=norm,boundaries=bounds,ticks=bounds,orientation='vertical')
                        cb1.set_label(ColorBarLabel)

                        plt.show(block=False)
                        
                else:
                    if NORM_THEO == 1 and P1nC_THEO == 0 and P2nC_THEO == 0 and P3nC_THEO == 0: #normal display
                        plt.figure(figsize=(16.5,8))
                        plt.axis('scaled')
                        g=plt.gca()
                        plt.xlim(N_low_user,N_high_user)
                        plt.ylim(Z_low_user-1,Z_high_user+1)

                        Num_xticks = np.arange(N_low_user+1,N_high_user,1)
                        label_xticks = [];append_lx = label_xticks.append
                        for i in xrange(N_low_user+1,N_high_user):
                            c = i%2
                            if c == 0:
                                label_xticks.append(i)
                            else:
                                label_xticks.append("")
                        if Delta_N >= 100:
                            label_xticks = []
                        plt.xticks(Num_xticks,label_xticks)
                        plt.xticks(size=8)
                        
                        Num_yticks = np.arange(Z_low_user,Z_high_user+1,1)
                        label_yticks = [];append_ly = label_yticks.append
                        for i in xrange(Z_low_user,Z_high_user+1):
                            c = i%2
                            if c == 0:
                                label_yticks.append(i)
                            else:
                                label_yticks.append("")
                        if Delta_Z >= 100:
                            label_yticks = []
                        plt.yticks(Num_yticks,label_yticks)
                        plt.yticks(size=8)
                        
                        plt.xlabel(xlabel1,fontsize=8)
                        plt.ylabel(ylabel,fontsize=8)

                        plt.title(Title_THEO)          
                        leg_entries = []
                        leg_text = []

                        # plots nuclei in user bounds and stable nuclei using basic data files
                        if len(N_P_Bound) != 0:
                            plt.plot(N_P_Bound,Z_P_Bound,marker='s',color='0.85',markersize=msize,markeredgewidth=0,linestyle='')
                        if len(N_Bound) != 0:
                            t0, = plt.plot(N_Bound,Z_Bound,marker='s',color='0.8',markersize=msize,markeredgewidth=mew,linestyle='');c1=1
                        if len(N_stable_Bound) != 0:
                            t1, = plt.plot(N_stable_Bound,Z_stable_Bound,marker='s',color=color1,markersize=msize,markeredgewidth=0,linestyle='');c2=1

                        # highlights nuclei with Pxn values in user bounds using basic data files                                       
                        if len(N_P1n) != 0 and (PxnTHEO1 == 1 or PxnTHEOA == 1):
                            t2, = plt.plot(N_P1n,Z_P1n,marker='s',color=color2,markersize=msize,markeredgewidth=0,linestyle='');c3=1
                        if len(N_P2n) != 0 and (PxnTHEO2 == 1 or PxnTHEOA == 1):
                            t3, = plt.plot(N_P2n,Z_P2n,marker='s',color=color3,markersize=msize,markeredgewidth=0,linestyle='');c4=1
                        if len(N_P3n) != 0 and (PxnTHEO3 == 1 or PxnTHEOA == 1):
                            t4, = plt.plot(N_P3n,Z_P3n,marker='s',color=color4,markersize=msize,markeredgewidth=0,linestyle='');c5=1
                        # highlights nuclei with Pxn values in user bounds using user data files 
                        if user_P == 1:    
                            if len(N_P1n_USER) != 0 and (PxnTHEO1 == 1 or PxnTHEOA == 1):
                                plt.plot(N_P1n_USER,Z_P1n_USER,marker='s',color=color2,markersize=msize,markeredgewidth=0,linestyle='');c3=1
                            if len(N_P2n_USER) != 0 and (PxnTHEO2 == 1 or PxnTHEOA == 1):
                                plt.plot(N_P2n_USER,Z_P2n_USER,marker='s',color=color3,markersize=msize,markeredgewidth=0,linestyle='');c4=1
                            if len(N_P3n_USER) != 0 and (PxnTHEO3 == 1 or PxnTHEOA == 1):
                                plt.plot(N_P3n_USER,Z_P3n_USER,marker='s',color=color4,markersize=msize,markeredgewidth=0,linestyle='');c5=1

                        # determines which magic number lines are necessary to display
                        if N_high_user >= 8 and N_low_user <= 8:  
                            plt.plot(N_Bound_magic*0.+8.5,Z_Bound_magic,color=color1,linewidth=lw1)  
                            plt.plot(N_Bound_magic*0.+7.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 20 and N_low_user <= 20:
                            plt.plot(N_Bound_magic*0.+20.5,Z_Bound_magic,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic*0.+19.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 28 and N_low_user <= 28:
                            plt.plot(N_Bound_magic*0.+28.5,Z_Bound_magic,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic*0.+27.5,Z_Bound_magic,color=color1,linewidth=lw1)     

                        if N_high_user >= 50 and N_low_user <= 50:
                            plt.plot(N_Bound_magic*0.+50.5,Z_Bound_magic,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic*0.+49.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 82 and N_low_user <= 82:
                            plt.plot(N_Bound_magic*0.+82.5,Z_Bound_magic,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic*0.+81.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 126 and N_low_user <= 126:
                            plt.plot(N_Bound_magic*0.+126.5,Z_Bound_magic,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic*0.+125.5,Z_Bound_magic,color=color1,linewidth=lw1) 

                        if Z_high_user >= 8 and Z_low_user <= 8:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+8.5,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+7.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 20 and Z_low_user <= 20:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+20.5,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+19.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 28 and Z_low_user <= 28:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+28.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+27.5,color=color1,linewidth=lw1)             

                        if Z_high_user >= 50 and Z_low_user <= 50:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+50.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+49.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 82 and Z_low_user <= 82:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+82.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+81.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 126 and Z_low_user <= 126:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+126.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+125.5,color=color1,linewidth=lw1)

                        # builds legend
                        if c1 == 1:
                            leg_entries.append(t0);leg_text.append(leg_THEO_1)
                        if c2 == 1:
                            leg_entries.append(t1);leg_text.append(leg_THEO_2)
                        if c3 == 1:
                            leg_entries.append(t2);leg_text.append(leg_THEO_3)
                        if c4 == 1:
                            leg_entries.append(t3);leg_text.append(leg_THEO_4)
                        if c5 == 1:
                            leg_entries.append(t4);leg_text.append(leg_THEO_5)
                        
                        if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                            l1 = plt.legend(leg_entries,leg_text,loc=2,bbox_to_anchor=[1.02,0.98],borderaxespad=0.,markerscale=ms1,numpoints=1)
                        else:
                            l1 = plt.legend(leg_entries,leg_text,loc=4,markerscale=ms1,numpoints=1)

                        plt.show(block=False)
                        
                    if P1nC_THEO == 1 or P2nC_THEO == 1 or P3nC_THEO== 1: # color bar gradient for non-zoom in ranges
                        fig = plt.figure(figsize=(16.5,8))

                        plt.axis('scaled')
                        g=plt.gca()
                        plt.xlim(N_low_user,N_high_user)
                        plt.ylim(Z_low_user-1,Z_high_user+1)

                        Num_xticks = np.arange(N_low_user+1,N_high_user,1)
                        label_xticks = [];append_lx = label_xticks.append
                        for i in xrange(N_low_user+1,N_high_user):
                            c = i%2
                            if c == 0:
                                label_xticks.append(i)
                            else:
                                label_xticks.append("")
                        if Delta_N >= 100:
                            label_xticks = []
                        plt.xticks(Num_xticks,label_xticks)
                        plt.xticks(size=8)
                        
                        Num_yticks = np.arange(Z_low_user,Z_high_user+1,1)
                        label_yticks = [];append_ly = label_yticks.append
                        for i in xrange(Z_low_user,Z_high_user+1):
                            c = i%2
                            if c == 0:
                                label_yticks.append(i)
                            else:
                                label_yticks.append("")
                        if Delta_Z >= 100:
                            label_yticks = []
                        plt.yticks(Num_yticks,label_yticks)
                        plt.yticks(size=8)

                        plt.xlabel(xlabel1,fontsize=8)
                        plt.ylabel(ylabel,fontsize=8)

                        # plots nuclei,stable nuclei, and color highlights the Pxn values within user bounds using basic data files
                        if len(N_P_Bound) != 0:
                            plt.plot(N_P_Bound,Z_P_Bound,marker='s',color='0.85',markersize=msize,markeredgewidth=0,linestyle='')
                        if len(N_Bound) != 0:
                            plt.plot(N_Bound,Z_Bound,marker='s',color='0.8',markersize=msize,markeredgewidth=mew,linestyle='')
                        if len(N_stable_Bound) != 0:
                            plt.plot(N_stable_Bound,Z_stable_Bound,marker='s',color=color1,markersize=msize,markeredgewidth=0,linestyle='')

                        if P1nC_THEO == 1 and P2nC_THEO == 0 and P3nC_THEO == 0:
                            plt.title(THEO_ColorTitle_1)            
                            if len(N_P1n_Color) != 0:
                                for i in xrange(0,len(N_P1n_Color)):
                                    plt.plot(N_P1n_Color[i],Z_P1n_Color[i],marker='s',color=P1n_Color[i],markersize=msize,markeredgewidth=0,linestyle='')

                        if P2nC_THEO == 1 and P1nC_THEO == 0 and P3nC_THEO == 0:
                            plt.title(THEO_ColorTitle_2)
                            if len(N_P2n_Color) != 0: 
                                for i in xrange(0,len(N_P2n_Color)):
                                    plt.plot(N_P2n_Color[i],Z_P2n_Color[i],marker='s',color=P2n_Color[i],markersize=msize,markeredgewidth=0,linestyle='')

                        if P3nC_THEO == 1 and P1nC_THEO == 0 and P2nC_THEO == 0:
                            plt.title(THEO_ColorTitle_3)
                            if len(N_P3n_Color) != 0:
                                for i in xrange(0,len(N_P3n_Color)):
                                    plt.plot(N_P3n_Color[i],Z_P3n_Color[i],marker='s',color=P3n_Color[i],markersize=msize,markeredgewidth=0,linestyle='')
                        # plots nuclei,stable nuclei, and color highlights the Pxn values within user bounds using user uploaded data files
                        if user_P == 1:
                            if P1nC_THEO == 1 and P2nC_THEO == 0 and P3nC_THEO == 0:
                                plt.title(THEO_ColorTitle_1)
                                if len(N_P1n_Color_USER) != 0:
                                    for i in xrange(0,len(N_P1n_Color_USER)):
                                        plt.plot(N_P1n_Color_USER[i],Z_P1n_Color_USER[i],marker='s',color=P1n_Color_USER[i],markersize=msize,markeredgewidth=0,linestyle='')

                            if P2nC_THEO == 1 and P1nC_THEO == 0 and P3nC_THEO == 0:
                                plt.title(THEO_ColorTitle_2)
                                if len(N_P2n_Color_USER) != 0: 
                                    for i in xrange(0,len(N_P2n_Color_USER)):
                                        plt.plot(N_P2n_Color_USER[i],Z_P2n_Color_USER[i],marker='s',color=P2n_Color_USER[i],markersize=msize,markeredgewidth=0,linestyle='')

                            if P3nC_THEO == 1 and P1nC_THEO == 0 and P2nC_THEO == 0:
                                plt.title(THEO_ColorTitle_3)
                                if len(N_P3n_Color_USER) != 0:
                                    for i in xrange(0,len(N_P3n_Color_USER)):
                                        plt.plot(N_P3n_Color_USER[i],Z_P3n_Color_USER[i],marker='s',color=P3n_Color_USER[i],markersize=msize,markeredgewidth=0,linestyle='')
                        
                        # determines which magic number lines are necessary to display
                        if N_high_user >= 8 and N_low_user <= 8:  
                            plt.plot(N_Bound_magic*0.+8.5,Z_Bound_magic,color=color1,linewidth=lw1)  
                            plt.plot(N_Bound_magic*0.+7.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 20 and N_low_user <= 20:
                            plt.plot(N_Bound_magic*0.+20.5,Z_Bound_magic,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic*0.+19.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 28 and N_low_user <= 28:
                            plt.plot(N_Bound_magic*0.+28.5,Z_Bound_magic,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic*0.+27.5,Z_Bound_magic,color=color1,linewidth=lw1)     

                        if N_high_user >= 50 and N_low_user <= 50:
                            plt.plot(N_Bound_magic*0.+50.5,Z_Bound_magic,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic*0.+49.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 82 and N_low_user <= 82:
                            plt.plot(N_Bound_magic*0.+82.5,Z_Bound_magic,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic*0.+81.5,Z_Bound_magic,color=color1,linewidth=lw1)

                        if N_high_user >= 126 and N_low_user <= 126:
                            plt.plot(N_Bound_magic*0.+126.5,Z_Bound_magic,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic*0.+125.5,Z_Bound_magic,color=color1,linewidth=lw1) 

                        if Z_high_user >= 8 and Z_low_user <= 8:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+8.5,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+7.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 20 and Z_low_user <= 20:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+20.5,color=color1,linewidth=lw1) 
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+19.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 28 and Z_low_user <= 28:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+28.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+27.5,color=color1,linewidth=lw1)             

                        if Z_high_user >= 50 and Z_low_user <= 50:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+50.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+49.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 82 and Z_low_user <= 82:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+82.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+81.5,color=color1,linewidth=lw1)

                        if Z_high_user >= 126 and Z_low_user <= 126:
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+126.5,color=color1,linewidth=lw1)
                            plt.plot(N_Bound_magic,Z_Bound_magic*0.+125.5,color=color1,linewidth=lw1)

                        # outputs color bar
                        ax1 = fig.add_axes([ax1_1,ax1_2,ax1_3,ax1_4])

                        cmap = mpl.colors.ListedColormap(['yellow','orange','red','maroon','lime','green','DeepSkyBlue','blue','violet','purple'])
                        bounds = [0,10,20,30,40,50,60,70,80,90,100]
                        norm = mpl.colors.BoundaryNorm(bounds,cmap.N)
                        cb1 = mpl.colorbar.ColorbarBase(ax1,cmap=cmap,norm=norm,boundaries=bounds,ticks=bounds,orientation='vertical')
                        cb1.set_label(ColorBarLabel)

                        plt.show(block=False)
                        
            if choice_user_EXP == 1 and choice_user_THEO == 0: #experimental database      
                #reads in values from text files and stores all of the data columns into arrays
                filename_ENSDF_1 = os.getcwd() + dirDelim + "Data_Files" + dirDelim + "ChartNuclides_DataTable_ENSDF_Stable-QValues.txt"
                filename_ENSDF_2 = os.getcwd() + dirDelim + "Data_Files" + dirDelim + "ChartNuclides_DataTable_ENSDF_PValues.txt"

                user_P = 0 ; user_Q = 0 ; user_i = 0
                if choice_USERFILE_EXP == 1:
                    filename_EXP_USER = os.getcwd() + dirDelim + "Data_Files" + dirDelim + userFile_EXP

                    # checks # of columns in uploaded data files
                    with open(filename_EXP_USER) as ColCheck:
                        reader = csv.reader(ColCheck,delimiter='\t',skipinitialspace=True)
                        first_row = next(reader)
                        ncol = len(first_row)

                    if ncol == 7:
                        ELE_names_USER = np.genfromtxt(filename_EXP_USER,skip_header=1,usecols=(6),dtype=str,unpack=True)
                        N_USER,Z_USER,P1n_USER,P2n_USER,P3n_USER,P4n_USER = np.loadtxt(filename_EXP_USER,skiprows=1,usecols=(0,1,2,3,4,5),unpack=True)
                        size_P_USER = len(N_USER); user_P = 1               
                    if ncol == 11:
                        ELE_names_USER = np.genfromtxt(filename_EXP_USER,skip_header=1,usecols=(10),dtype=str,unpack=True)
                        N_USER,Z_USER,P1n_USER,P2n_USER,P3n_USER,P4n_USER = np.loadtxt(filename_EXP_USER,skiprows=1,usecols=(0,1,2,3,4,5),unpack=True)
                        size_P_USER = len(N_USER)
                        Qbn_USER,Qb2n_USER,Qb3n_USER,Qb4n_USER = np.loadtxt(filename_EXP_USER,skiprows=1,usecols=(6,7,8,9),unpack=True)
                        size_Q_USER = len(Qbn_USER); user_Q = 1
                    if ncol == 15:
                        ELE_names_USER = np.genfromtxt(filename_EXP_USER,skip_header=1,usecols=(14),dtype=str,unpack=True)
                        N_USER,Z_USER,P1n_USER,P2n_USER,P3n_USER,P4n_USER = np.loadtxt(filename_EXP_USER,skiprows=1,usecols=(0,1,2,3,4,5),unpack=True)
                        size_P_USER = len(N_USER)

                        Qbn_USER,Qb2n_USER,Qb3n_USER,Qb4n_USER = np.loadtxt(filename_EXP_USER,skiprows=1,usecols=(6,7,8,9),unpack=True)
                        P1n_iso1_USER,P2n_iso1_USER,P1n_iso2_USER,P2n_iso2_USER = np.loadtxt(filename_EXP_USER,skiprows=1,usecols=(10,11,12,13),unpack=True)
                        size_iso_USER = len(P1n_iso1_USER); user_i = 1

                N_stable,Z_stable = np.loadtxt(filename_ENSDF_1,skiprows=1,usecols=(0, 1),unpack=True)
                s2 = len(N_stable)

                N,Z = np.loadtxt(filename_ENSDF_1,skiprows=1,usecols=(2, 3),unpack=True)
                s1 = len(N)
                
                Snlt0,Qbn,Qb2n,Qb3n,Qb4n = np.genfromtxt(filename_ENSDF_1,skip_header=1,usecols=(4,5,6,7,8),dtype=str,unpack=True)

                ELE_names_EXP = np.genfromtxt(filename_ENSDF_2,skip_header=1,usecols=(0),dtype=str,unpack=True)
                N_P,Z_P,P1n,P2n,P3n,P4n,P1SP,P2SP,P3SP,P4SP = np.loadtxt(filename_ENSDF_2,skiprows=1,usecols=(1, 2, 3, 6, 9, 10, 11, 12, 13 ,14),unpack=True)
                size_P = len(N_P)

                N_P_iso1,Z_P_iso1,P1n_iso1,P2n_iso1,N_P_iso2,Z_P_iso2,P1n_iso2,P2n_iso2 = np.loadtxt(filename_ENSDF_2,skiprows=1,usecols=(1,2,4,7,1,2,5,8),unpack=True)
                size_P_iso1 = len(N_P_iso1);size_P_iso2 = len(N_P_iso2)
            #----------------------------------------------------------------------------

                # list of text in order to properly set up the legend and special symbols
                Special_sym = ['<','>','ca.','?']
                N_high_user=N_high_user+1
                N_low_user=N_low_user-1
            #----------------------------------------------------------------------------
            
                # choice to display ratio info instead and assembly of ratio arrays based on user choice 
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    if Ratio == 1 and Pxn_EXP == 0 and NORM_EXP == 0:
                        R1n_USER = []; append_R1nUSER = R1n_USER.append
                        R2n_USER = []; append_R2nUSER = R2n_USER.append
                        R3n_USER = []; append_R3nUSER = R3n_USER.append
                        R4n_USER = []; append_R4nUSER = R4n_USER.append

                        N_R1n_USER = []; append_NR1nUSER = N_R1n_USER.append
                        Z_R1n_USER = []; append_ZR1nUSER = Z_R1n_USER.append
                        N_R2n_USER = []; append_NR2nUSER = N_R2n_USER.append
                        Z_R2n_USER = []; append_ZR2nUSER = Z_R2n_USER.append

                        N_R3n_USER = []; append_NR3nUSER = N_R3n_USER.append
                        Z_R3n_USER = []; append_ZR3nUSER = Z_R3n_USER.append
                        N_R4n_USER = []; append_NR4nUSER = N_R4n_USER.append
                        Z_R4n_USER = []; append_ZR4nUSER = Z_R4n_USER.append

                        ELE_names_Ratio = []; append_EnR = ELE_names_Ratio.append
                        A_Ratio_USER = []; append_ARU = A_Ratio_USER.append
                        N_Ratio_USER = []; append_NRU = N_Ratio_USER.append
                        Z_Ratio_USER = []; append_ZRU = Z_Ratio_USER.append

                        if Ratio_USER_EXP == 1 and Ratio_ENSDF_EXP == 0: #for USER EXP data for Ratio
                            user_EXPR = 0;
                            filename_EXPR_USER = os.getcwd() + dirDelim + "Data_Files" + dirDelim + Ratio_USERFILE_EXP

                            # checks # of columns in uploaded data files
                            with open(filename_EXPR_USER) as ColCheck:
                                reader = csv.reader(ColCheck,delimiter='\t',skipinitialspace=True)
                                first_row = next(reader)
                                ncol = len(first_row)

                            if ncol == 7:
                                ELE_names_EXPR = np.genfromtxt(filename_EXPR_USER,skip_header=1,usecols=(6),dtype=str,unpack=True)
                                N_EXPR,Z_EXPR,P1n_EXPR,P2n_EXPR,P3n_EXPR,P4n_EXPR = np.loadtxt(filename_EXPR_USER,skiprows=1,usecols=(0,1,2,3,4,5),unpack=True)
                                size_P_EXPR = len(N_EXPR); user_EXPR = 1

                        if Ratio_USER_THEO == 1 and Ratio_MOE_THEO == 0: # for USER THEO data for Ratio
                            user_THEOR = 0;
                            filename_THEOR_USER = os.getcwd() + dirDelim + "Data_Files" + dirDelim + Ratio_USERFILE_THEO

                            # checks # of columns in uploaded data files
                            with open(filename_THEOR_USER) as ColCheck:
                                reader = csv.reader(ColCheck,delimiter='\t',skipinitialspace=True)
                                first_row = next(reader)
                                ncol = len(first_row)

                            if ncol == 7:
                                ELE_names_THEOR = np.genfromtxt(filename_THEOR_USER,skip_header=1,usecols=(6),dtype=str,unpack=True)
                                N_THEOR,Z_THEOR,P1n_THEOR,P2n_THEOR,P3n_THEOR,P4n_THEOR = np.loadtxt(filename_THEOR_USER,skiprows=1,usecols=(0,1,2,3,4,5),unpack=True)
                                size_P_THEOR = len(N_THEOR); user_THEOR = 1

                            if Ratio_ENSDF_EXP == 1 and Ratio_USER_EXP == 0:
                                # forms array of Ratio values based on User Theoretical Pn values & ENSDF EXP Pn values within user range
                                for i in xrange(0,size_P_THEOR):
                                    for ii in xrange(0,size_P):
                                        if N_THEOR[i] == N_P[ii] and Z_THEOR[i] == Z_P[ii]:
                                            if N_THEOR[i] < N_high_user and N_THEOR[i] > N_low_user and Z_THEOR[i] <= Z_high_user and Z_THEOR[i] >= Z_low_user:
                                                append_EnR(ELE_names_EXPR[ii])
                                                append_ARU(N_THEOR[i]+Z_THEOR[i])
                                                append_NRU(N_THEOR[i]);append_ZRU(Z_THEOR[i])
                                                if P1n_THEOR[i] != 0 and P1n[ii] != 0:
                                                    append_R1nUSER(P1n[ii]/P1n_THEOR[i]);append_NR1nUSER(N_THEOR[i]);append_ZR1nUSER(Z_THEOR[i])
                                                if P2n_THEOR[i] != 0 and P2n[ii] != 0:
                                                    append_R2nUSER(P2n[ii]/P2n_THEOR[i]);append_NR2nUSER(N_THEOR[i]);append_ZR2nUSER(Z_THEOR[i])
                                                if P3n_THEOR[i] != 0 and P3n[ii] != 0:
                                                    append_R3nUSER(P3n[ii]/P3n_THEOR[i]);append_NR3nUSER(N_THEOR[i]);append_ZR3nUSER(Z_THEOR[i])
                                                if P4n_THEOR[i] != 0 and P4n[ii] != 0:
                                                    append_R4nUSER(P4n[ii]/P4n_THEOR[i]);append_NR4nUSER(N_THEOR[i]);append_ZR4nUSER(Z_THEOR[i])

                            if Ratio_USER_EXP == 1 and Ratio_ENSDF_EXP == 0:
                                # forms array of Ratio values based on User Theoretical Pn values & User EXP Pn values within user range
                                for i in xrange(0,size_P_THEOR):
                                    for ii in xrange(0,size_P_EXPR):
                                        if N_THEOR[i] == N_EXPR[ii] and Z_THEOR[i] == Z_EXPR[ii]:
                                            if N_THEOR[i] < N_high_user and N_THEOR[i] > N_low_user and Z_THEOR[i] <= Z_high_user and Z_THEOR[i] >= Z_low_user:
                                                append_EnR(ELE_names_EXPR[ii])
                                                append_ARU(N_THEOR[i]+Z_THEOR[i])
                                                append_NRU(N_THEOR[i]);append_ZRU(Z_THEOR[i])
                                                if P1n_THEOR[i] != 0 and P1n_EXPR[ii] != 0:
                                                    append_R1nUSER(P1n_EXPR[ii]/P1n_THEOR[i]);append_NR1nUSER(N_THEOR[i]);append_ZR1nUSER(Z_THEOR[i])
                                                if P2n_THEOR[i] != 0 and P2n_EXPR[ii] != 0:
                                                    append_R2nUSER(P2n_EXPR[ii]/P2n_THEOR[i]);append_NR2nUSER(N_THEOR[i]);append_ZR2nUSER(Z_THEOR[i])
                                                if P3n_THEOR[i] != 0 and P3n_EXPR[ii] != 0:
                                                    append_R3nUSER(P3n_EXPR[ii]/P3n_THEOR[i]);append_NR3nUSER(N_THEOR[i]);append_ZR3nUSER(Z_THEOR[i])
                                                if P4n_THEOR[i] != 0 and P4n_EXPR[ii] != 0:
                                                    append_R4nUSER(P4n_EXPR[ii]/P4n_THEOR[i]);append_NR4nUSER(N_THEOR[i]);append_ZR4nUSER(Z_THEOR[i])


                        if Ratio_MOE_THEO == 1 and Ratio_USER_THEO == 0:
                            filename_MOE = os.getcwd() + dirDelim + "Data_Files" + dirDelim + "ChartNuclides_DataTable_MOELLER.txt"

                            N_P_MOE,Z_P_MOE,P1n_MOE_full,P2n_MOE_full,P3n_MOE_full = np.loadtxt(filename_MOE,skiprows=1,usecols=(4, 5, 6, 7, 8),unpack=True)
                            size_P_MOE = len(N_P_MOE)

                            if Ratio_ENSDF_EXP == 1 and Ratio_USER_EXP == 0:
                                # forms array of Ratio values based on MOELLER Pn values & ENSDF Pn values within user range
                                for i in xrange(0,size_P_MOE):
                                    for ii in xrange(0,size_P):
                                        if N_P_MOE[i] == N_P[ii] and Z_P_MOE[i] == Z_P[ii]:
                                            if N_P_MOE[i] < N_high_user and N_P_MOE[i] > N_low_user and Z_P_MOE[i] <= Z_high_user and Z_P_MOE[i] >= Z_low_user:
                                                append_EnR(ELE_names_EXP[ii])
                                                append_ARU(N_P_MOE[i]+Z_P_MOE[i])
                                                append_NRU(N_P_MOE[i]);append_ZRU(Z_P_MOE[i])
                                                if P1n_MOE_full[i] != 0 and P1n[ii] != 0:
                                                    append_R1nUSER(P1n[ii]/P1n_MOE_full[i]);append_NR1nUSER(N_P_MOE[i]);append_ZR1nUSER(Z_P_MOE[i])
                                                if P2n_MOE_full[i] != 0 and P2n[ii] != 0:
                                                    append_R2nUSER(P2n[ii]/P2n_MOE_full[i]);append_NR2nUSER(N_P_MOE[i]);append_ZR2nUSER(Z_P_MOE[i])
                                                if P3n_MOE_full[i] != 0 and P3n[ii] != 0:
                                                    append_R3nUSER(P3n[ii]/P3n_MOE_full[i]);append_NR3nUSER(N_P_MOE[i]);append_ZR3nUSER(Z_P_MOE[i])

                            if Ratio_USER_EXP == 1  and Ratio_ENSDF_EXP == 0:
                                # forms array of Ratio values based on MOELLER Pn values & User EXP Pn values within user range
                                for i in xrange(0,size_P_MOE):
                                    for ii in xrange(0,size_P_EXPR):
                                        if N_P_MOE[i] == N_EXPR[ii] and Z_P_MOE[i] == Z_EXPR[ii]:
                                            if N_P_MOE[i] < N_high_user and N_P_MOE[i] > N_low_user and Z_P_MOE[i] <= Z_high_user and Z_P_MOE[i] >= Z_low_user:
                                                append_EnR(ELE_names_EXPR[ii])
                                                append_ARU(N_P_MOE[i]+Z_P_MOE[i])
                                                append_NRU(N_P_MOE[i]);append_ZRU(Z_P_MOE[i])
                                                if P1n_MOE_full[i] != 0  and P1n_EXPR[ii] != 0:
                                                    append_R1nUSER(P1n_EXPR[ii]/P1n_MOE_full[i]);append_NR1nUSER(N_P_MOE[i]);append_ZR1nUSER(Z_P_MOE[i])
                                                if P2n_MOE_full[i] != 0 and P2n_EXPR[ii] != 0:
                                                    append_R2nUSER(P2n_EXPR[ii]/P2n_MOE_full[i]);append_NR2nUSER(N_P_MOE[i]);append_ZR2nUSER(Z_P_MOE[i])
                                                if P3n_MOE_full[i] != 0 and P3n_EXPR[ii] != 0:
                                                    append_R3nUSER(P3n_EXPR[ii]/P3n_MOE_full[i]);append_NR3nUSER(N_P_MOE[i]);append_ZR3nUSER(Z_P_MOE[i])
        #-----------------------------------------------------------------------------

                N_Bound = [];Z_Bound = [];blank = 0
                Snlt0_N = [];Snlt0_Z = []
                N_Bound_magic = [] ; Z_Bound_magic = []
                append_NBM = N_Bound_magic.append ; append_ZBM = Z_Bound_magic.append

                N_Qbn_Bound = [];Z_Qbn_Bound = []
                N_Qb2n_Bound = [];Z_Qb2n_Bound = []
                N_Qb3n_Bound = [];Z_Qb3n_Bound = []
                N_Qb4n_Bound = [];Z_Qb4n_Bound = []

                if user_Q == 1 or user_i == 1:
                    N_Qbn_Bound_USER = [];Z_Qbn_Bound_USER = []
                    N_Qb2n_Bound_USER = [];Z_Qb2n_Bound_USER = []
                    N_Qb3n_Bound_USER = [];Z_Qb3n_Bound_USER = []
                    N_Qb4n_Bound_USER = [];Z_Qb4n_Bound_USER = []

                append_NBM(N_low_user) ; append_ZBM(Z_low_user-1)
                append_NBM(N_high_user) ; append_ZBM(Z_high_user+1)
                N_Bound_magic = np.array(N_Bound_magic) ; Z_Bound_magic = np.array(Z_Bound_magic)

                # for loop that assigns the values of N and Z to each array within user bounds using the basic data files
                for i in xrange(0,s1):
                    if Z[i] >= Z_low_user and Z[i] <= Z_high_user and N[i] >= N_low_user and N[i] <= N_high_user:
                        if N[i] == 0 and Z[i] == 0:
                            blank = 1
                        else:
                            N_Bound = np.append(N_Bound,N[i])
                            Z_Bound = np.append(Z_Bound,Z[i])
                        if Snlt0[i] == str(1):
                            Snlt0_N = np.append(Snlt0_N,N[i])
                            Snlt0_Z = np.append(Snlt0_Z,Z[i])

                    # for loop that assigns N and Z values to the arrays only if the isotopes have a Qbxn greater than 0 and the Qbxn value is not equal to '--------'
                    #(a random number denoting isotopes with unknown Qbxn values) at that N and Z value using the basic data files

                    if Z[i] >= Z_low_user and Z[i] <= Z_high_user and N[i] >= N_low_user and N[i] <= N_high_user and Qbn[i] != '--------':
                        if float(Qbn[i]) > 0:
                            N_Qbn_Bound = np.append(N_Qbn_Bound,N[i])
                            Z_Qbn_Bound = np.append(Z_Qbn_Bound,Z[i])

                    if Z[i] >= Z_low_user and Z[i] <= Z_high_user and N[i] >= N_low_user and N[i] <= N_high_user and Qb2n[i] != '--------':
                        if float(Qb2n[i]) > 0:
                            N_Qb2n_Bound = np.append(N_Qb2n_Bound,N[i])
                            Z_Qb2n_Bound = np.append(Z_Qb2n_Bound,Z[i])

                    if Z[i] >= Z_low_user and Z[i] <= Z_high_user and N[i] >= N_low_user and N[i] <= N_high_user and Qb3n[i] != '--------':
                        if float(Qb3n[i]) > 0:
                            N_Qb3n_Bound = np.append(N_Qb3n_Bound,N[i])
                            Z_Qb3n_Bound = np.append(Z_Qb3n_Bound,Z[i])

                    if Z[i] >= Z_low_user and Z[i] <= Z_high_user and N[i] >= N_low_user and N[i] <= N_high_user and Qb4n[i] != '--------':
                        if float(Qb4n[i]) > 0:
                            N_Qb4n_Bound = np.append(N_Qb4n_Bound,N[i]) 
                            Z_Qb4n_Bound = np.append(Z_Qb4n_Bound,Z[i])

                # for loop that assigns N and Z values to the arrays only if the isotopes have a Qbxn greater than 0 using user files
                if user_Q == 1 or user_i == 1:
                    for i in range(0,size_P_USER):
                            if Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] >= N_low_user and N_USER[i] <= N_high_user and Qbn_USER[i] > 0: 
                                N_Qbn_Bound_USER = np.append(N_Qbn_Bound_USER,N_USER[i])
                                Z_Qbn_Bound_USER = np.append(Z_Qbn_Bound_USER,Z_USER[i])

                            if Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] >= N_low_user and N_USER[i] <= N_high_user and Qb2n_USER[i] > 0: 
                                N_Qb2n_Bound_USER = np.append(N_Qb2n_Bound_USER,N_USER[i])
                                Z_Qb2n_Bound_USER = np.append(Z_Qb2n_Bound_USER,Z_USER[i])

                            if Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] >= N_low_user and N_USER[i] <= N_high_user and Qb3n_USER[i] > 0:  
                                N_Qb3n_Bound_USER = np.append(N_Qb3n_Bound_USER,N_USER[i])
                                Z_Qb3n_Bound_USER = np.append(Z_Qb3n_Bound_USER,Z_USER[i])

                            if Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] >= N_low_user and N_USER[i] <= N_high_user and Qb4n_USER[i] > 0:  
                                N_Qb4n_Bound_USER = np.append(N_Qb4n_Bound_USER,N_USER[i]) 
                                Z_Qb4n_Bound_USER = np.append(Z_Qb4n_Bound_USER,Z_USER[i])
        #----------------------------------------------------------------------------
                # this part of the code makes an array for only the N and Z values that denote a stable nuclei using basic data files
                N_stable_Bound = [];Z_stable_Bound = [];blank = 0

                for i in xrange(0,s2):
                    if Z_stable[i] >= Z_low_user and Z_stable[i] <= Z_high_user and N_stable[i] >= N_low_user and N_stable[i] <= N_high_user:
                        if Z_stable[i] == 0 and N_stable[i] == 0:
                            blank = 1
                        else:
                            N_stable_Bound = np.append(N_stable_Bound,N_stable[i])
                            Z_stable_Bound = np.append(Z_stable_Bound,Z_stable[i])
        #----------------------------------------------------------------------------    

                # assigns the N and Z values of the isotopes with probability > 0
                N_P1n_Bound = [];Z_P1n_Bound = [] ; N_P1n_UL = [];Z_P1n_UL = [] ; N_P1n_NO = [];Z_P1n_NO = []
                N_P2n_Bound = [];Z_P2n_Bound = [] ; N_P2n_UL = [];Z_P2n_UL = [] ; N_P2n_NO = [];Z_P2n_NO = []      
                N_P3n_Bound = [];Z_P3n_Bound = [] ; N_P3n_UL = [];Z_P3n_UL = [] ; N_P3n_NO = [];Z_P3n_NO = []        
                N_P4n_Bound = [];Z_P4n_Bound = [] ; N_P4n_UL = [];Z_P4n_UL = [] ; N_P4n_NO = [];Z_P4n_NO = []

                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    if (Pxn_EXP == 1 or Ratio == 1) and NORM_EXP == 0:
                        ELE_name = []
                        N_ELE = [];Z_ELE = [];A_ELE = []

                        N_P1n_Bound_value = [];Z_P1n_Bound_value = []
                        P1n_Bound = []
                        N_P2n_Bound_value = [];Z_P2n_Bound_value = []
                        P2n_Bound = []
                        N_P3n_Bound_value = [];Z_P3n_Bound_value = []
                        P3n_Bound = []
                        N_P4n_Bound_value = [];Z_P4n_Bound_value = []
                        P4n_Bound = []

                        N_P1n_Bound_value_iso1 = [];Z_P1n_Bound_value_iso1 = []
                        N_P2n_Bound_value_iso1 = [];Z_P2n_Bound_value_iso1 = []
                        P1n_Bound_iso1 = [];P2n_Bound_iso1 = []

                        N_P1n_Bound_value_iso2 = [];Z_P1n_Bound_value_iso2 = []
                        N_P2n_Bound_value_iso2 = [];Z_P2n_Bound_value_iso2 = []
                        P1n_Bound_iso2 = [];P2n_Bound_iso2 = []

                if user_P == 1 or user_Q == 1 or user_i == 1:
                    N_P1n_Bound_USER = [];Z_P1n_Bound_USER = []
                    N_P2n_Bound_USER = [];Z_P2n_Bound_USER = []
                    N_P3n_Bound_USER = [];Z_P3n_Bound_USER = [] 
                    N_P4n_Bound_USER = [];Z_P4n_Bound_USER = []

                    if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                        if (Pxn_EXP == 1 or Ratio == 1) and NORM_EXP == 0:
                            ELE_name_USER = []
                            N_ELE_USER = [];Z_ELE_USER = [];A_ELE_USER = []
                            N_P1n_Bound_USER_value = [];Z_P1n_Bound_USER_value = []
                            P1n_Bound_USER = []
                            N_P2n_Bound_USER_value = [];Z_P2n_Bound_USER_value = []
                            P2n_Bound_USER = []
                            N_P3n_Bound_USER_value = [];Z_P3n_Bound_USER_value = []
                            P3n_Bound_USER = []
                            N_P4n_Bound_USER_value = [];Z_P4n_Bound_USER_value = []
                            P4n_Bound_USER = []

                            if user_i == 1:
                                N_P1n_Bound_USER_value_iso1 = [];Z_P1n_Bound_USER_value_iso1 = []
                                N_P2n_Bound_USER_value_iso1 = [];Z_P2n_Bound_USER_value_iso1 = []
                                P1n_Bound_USER_iso1 = [];P2n_Bound_USER_iso1 = []
                                N_P1n_Bound_USER_value_iso2 = [];Z_P1n_Bound_USER_value_iso2 = []
                                N_P2n_Bound_USER_value_iso2 = [];Z_P2n_Bound_USER_value_iso2 = []
                                P1n_Bound_USER_iso2 = [];P2n_Bound_USER_iso2 = []
                                
                # sets arrays for the nuclei with Pxn values within user bounds using the basic data files
                for i in xrange(0,size_P):
                    if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user:
                        
                        if Xn_EXP1 == 1 and P1SP[i] == 3:
                            N_P1n_NO = np.append(N_P1n_NO,N_P[i])
                            Z_P1n_NO = np.append(Z_P1n_NO,Z_P[i])
                        if Xn_EXP2 == 1 and P2SP[i] == 3:
                            N_P2n_NO = np.append(N_P2n_NO,N_P[i])
                            Z_P2n_NO = np.append(Z_P2n_NO,Z_P[i])
                        if Xn_EXP3 == 1 and P3SP[i] == 3:
                            N_P3n_NO = np.append(N_P3n_NO,N_P[i])
                            Z_P3n_NO = np.append(Z_P3n_NO,Z_P[i])
                        if Xn_EXP4 == 1 and P4SP[i] == 3:
                            N_P4n_NO = np.append(N_P4n_NO,N_P[i])
                            Z_P4n_NO = np.append(Z_P4n_NO,Z_P[i])
                        
                        if P1n[i] > 0: 
                            N_P1n_Bound = np.append(N_P1n_Bound,N_P[i]) 
                            Z_P1n_Bound = np.append(Z_P1n_Bound,Z_P[i])

                            if Xn_EXP1 == 1 and P1SP[i] == 1:
                                N_P1n_UL = np.append(N_P1n_UL,N_P[i])
                                Z_P1n_UL = np.append(Z_P1n_UL,Z_P[i])

                            if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                                if Pxn_EXP == 1 and NORM_EXP == 0 and Ratio == 0 and Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                                    N_P1n_Bound_value = np.append(N_P1n_Bound_value,N_P[i])
                                    Z_P1n_Bound_value = np.append(Z_P1n_Bound_value,Z_P[i])
                                    P1n_Bound = np.append(P1n_Bound,P1n[i])

                        if P2n[i] > 0: 
                            N_P2n_Bound = np.append(N_P2n_Bound,N_P[i])
                            Z_P2n_Bound = np.append(Z_P2n_Bound,Z_P[i])

                            if Xn_EXP2 == 1 and P2SP[i] == 1:
                                N_P2n_UL = np.append(N_P2n_UL,N_P[i])
                                Z_P2n_UL = np.append(Z_P2n_UL,Z_P[i])

                            if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                                if Pxn_EXP == 1 and NORM_EXP == 0 and Ratio == 0 and Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                                    N_P2n_Bound_value = np.append(N_P2n_Bound_value,N_P[i])
                                    Z_P2n_Bound_value = np.append(Z_P2n_Bound_value,Z_P[i])
                                    P2n_Bound = np.append(P2n_Bound,P2n[i])

                        if P3n[i] > 0: 
                            N_P3n_Bound = np.append(N_P3n_Bound,N_P[i])
                            Z_P3n_Bound = np.append(Z_P3n_Bound,Z_P[i])

                            if Xn_EXP3 == 1 and P3SP[i] == 1:
                                N_P3n_UL = np.append(N_P3n_UL,N_P[i])
                                Z_P3n_UL = np.append(Z_P3n_UL,Z_P[i])

                            if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                                if Pxn_EXP == 1 and NORM_EXP == 0 and Ratio == 0 and Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                                    N_P3n_Bound_value = np.append(N_P3n_Bound_value,N_P[i])
                                    Z_P3n_Bound_value = np.append(Z_P3n_Bound_value,Z_P[i])
                                    P3n_Bound = np.append(P3n_Bound,P3n[i]) 

                        if P4n[i] > 0: 
                            N_P4n_Bound = np.append(N_P4n_Bound,N_P[i])
                            Z_P4n_Bound = np.append(Z_P4n_Bound,Z_P[i])

                            if Xn_EXP4 == 1 and P4SP[i] == 1:
                                N_P4n_UL = np.append(N_P4n_UL,N_P[i])
                                Z_P4n_UL = np.append(Z_P4n_UL,Z_P[i])

                            if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                                if Pxn_EXP == 1 and NORM_EXP == 0 and Ratio == 0 and Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                                    N_P4n_Bound_value = np.append(N_P4n_Bound_value,N_P[i])
                                    Z_P4n_Bound_value = np.append(Z_P4n_Bound_value,Z_P[i])
                                    P4n_Bound = np.append(P4n_Bound,P4n[i])

                    if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                        if (Pxn_EXP == 1 or Ratio == 1) and NORM_EXP == 0 and Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user and (P1n[i] != 0 or P2n[i] != 0 or P3n[i] != 0 or P4n[i] != 0): 
                            N_ELE = np.append(N_ELE,N_P[i])
                            Z_ELE = np.append(Z_ELE,Z_P[i])
                            A_calc = N_P[i] + Z_P[i]
                            ELE_name = np.append(ELE_name,ELE_names_EXP[i])
                            A_ELE = np.append(A_ELE,A_calc)
                            
                # sets arrays for the nuclei with Pxn values within user bounds using the user data files
                if user_P == 1 or user_Q == 1 or user_i == 1:
                    for i in xrange(0,size_P_USER):
                        if Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user:
                            if P1n_USER[i] != 0: 
                                N_P1n_Bound_USER = np.append(N_P1n_Bound_USER,N_USER[i]) 
                                Z_P1n_Bound_USER = np.append(Z_P1n_Bound_USER,Z_USER[i])

                                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                                    if Pxn_EXP == 1 and NORM_EXP == 0 and Ratio == 0 and Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user:
                                        N_P1n_Bound_USER_value = np.append(N_P1n_Bound_USER_value,N_USER[i])
                                        Z_P1n_Bound_USER_value = np.append(Z_P1n_Bound_USER_value,Z_USER[i])
                                        P1n_Bound_USER = np.append(P1n_Bound_USER,P1n_USER[i])

                            if P2n_USER[i] != 0: 
                                N_P2n_Bound_USER = np.append(N_P2n_Bound_USER,N_USER[i])
                                Z_P2n_Bound_USER = np.append(Z_P2n_Bound_USER,Z_USER[i])

                                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                                    if Pxn_EXP == 1 and NORM_EXP == 0 and Ratio == 0 and Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user:
                                        N_P2n_Bound_USER_value = np.append(N_P2n_Bound_USER_value,N_USER[i])
                                        Z_P2n_Bound_USER_value = np.append(Z_P2n_Bound_USER_value,Z_USER[i])
                                        P2n_Bound_USER = np.append(P2n_Bound_USER,P2n_USER[i])

                            if P3n_USER[i] != 0: 
                                N_P3n_Bound_USER = np.append(N_P3n_Bound_USER,N_USER[i])
                                Z_P3n_Bound_USER = np.append(Z_P3n_Bound_USER,Z_USER[i])

                                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                                    if Pxn_EXP == 1 and NORM_EXP == 0 and Ratio == 0 and Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user:
                                        N_P3n_Bound_USER_value = np.append(N_P3n_Bound_USER_value,N_USER[i])
                                        Z_P3n_Bound_USER_value = np.append(Z_P3n_Bound_USER_value,Z_USER[i])
                                        P3n_Bound_USER = np.append(P3n_Bound_USER,P3n_USER[i]) 

                            if P4n_USER[i] != 0: 
                                N_P4n_Bound_USER = np.append(N_P4n_Bound_USER,N_USER[i])
                                Z_P4n_Bound_USER = np.append(Z_P4n_Bound_USER,Z_USER[i])

                                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                                    if Pxn_EXP == 1 and NORM_EXP == 0 and Ratio == 0 and Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user:
                                        N_P4n_Bound_USER_value = np.append(N_P4n_Bound_USER_value,N_USER[i])
                                        Z_P4n_Bound_USER_value = np.append(Z_P4n_Bound_USER_value,Z_USER[i])
                                        P4n_Bound_USER = np.append(P4n_Bound_USER,P4n_USER[i])

                        if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                            if (Ratio == 1 or Pxn_EXP == 1) and NORM_EXP == 0 and Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user and (P1n_USER[i] != 0 or P2n_USER[i] != 0 or P3n_USER[i] != 0 or P4n_USER[i] != 0): 

                                N_ELE_USER= np.append(N_ELE_USER,N_USER[i])
                                Z_ELE_USER = np.append(Z_ELE_USER,Z_USER[i])
                                A_calc_USER = N_USER[i] + Z_USER[i]
                                ELE_name_USER = np.append(ELE_name_USER,ELE_names_USER[i])
                                A_ELE_USER = np.append(A_ELE_USER,A_calc_USER)

                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    if Pxn_EXP == 1 and NORM_EXP == 0 and Ratio == 0:
                        for i in xrange(0,size_P_iso1):
                            if Z_P_iso1[i] >= Z_low_user and Z_P_iso1[i] <= Z_high_user and N_P_iso1[i] > N_low_user and N_P_iso1[i] < N_high_user:
                                if P1n_iso1[i] != 0:
                                    N_P1n_Bound_value_iso1 = np.append(N_P1n_Bound_value_iso1,N_P_iso1[i]) 
                                    Z_P1n_Bound_value_iso1 = np.append(Z_P1n_Bound_value_iso1,Z_P_iso1[i])
                                    P1n_Bound_iso1 = np.append(P1n_Bound_iso1,P1n_iso1[i])

                                if P2n_iso1[i] != 0: 
                                    N_P2n_Bound_value_iso1 = np.append(N_P2n_Bound_value_iso1,N_P_iso1[i])
                                    Z_P2n_Bound_value_iso1 = np.append(Z_P2n_Bound_value_iso1,Z_P_iso1[i])
                                    P2n_Bound_iso1 = np.append(P2n_Bound_iso1,P2n_iso1[i])

                        for i in xrange(0,size_P_iso2):
                            if Z_P_iso2[i] >= Z_low_user and Z_P_iso2[i] <= Z_high_user and N_P_iso2[i] > N_low_user and N_P_iso2[i] < N_high_user:
                                if P1n_iso2[i] != 0:
                                    N_P1n_Bound_value_iso2 = np.append(N_P1n_Bound_value_iso2,N_P_iso2[i])
                                    Z_P1n_Bound_value_iso2 = np.append(Z_P1n_Bound_value_iso2,Z_P_iso2[i])
                                    P1n_Bound_iso2 = np.append(P1n_Bound_iso2,P1n_iso2[i])

                                if P2n_iso2[i] != 0: 
                                    N_P2n_Bound_value_iso2 = np.append(N_P2n_Bound_value_iso2,N_P_iso2[i])
                                    Z_P2n_Bound_value_iso2 = np.append(Z_P2n_Bound_value_iso2,Z_P_iso2[i])
                                    P2n_Bound_iso2 = np.append(P2n_Bound_iso2,P2n_iso2[i])

                        if user_i == 1:
                            for i in xrange(0,size_iso_USER): 
                                if Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user:
                                    if P1n_iso1_USER[i] != 0:
                                        N_P1n_Bound_USER_value_iso1 = np.append(N_P1n_Bound_USER_value_iso1,N_USER[i]) 
                                        Z_P1n_Bound_USER_value_iso1 = np.append(Z_P1n_Bound_USER_value_iso1,Z_USER[i])
                                        P1n_Bound_USER_iso1 = np.append(P1n_Bound_USER_iso1,P1n_iso1_USER[i])

                                    if P2n_iso1_USER[i] != 0: 
                                        N_P2n_Bound_USER_value_iso1 = np.append(N_P2n_Bound_USER_value_iso1,N_USER[i])
                                        Z_P2n_Bound_USER_value_iso1 = np.append(Z_P2n_Bound_USER_value_iso1,Z_USER[i])
                                        P2n_Bound_USER_iso1 = np.append(P2n_Bound_USER_iso1,P2n_iso1_USER[i])

                            for i in xrange(0,size_iso_USER):
                                if Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user:
                                    if P1n_iso2_USER[i] != 0:
                                        N_P1n_Bound_USER_value_iso2 = np.append(N_P1n_Bound_USER_value_iso2,N_USER[i])
                                        Z_P1n_Bound_USER_value_iso2 = np.append(Z_P1n_Bound_USER_value_iso2,Z_USER[i])
                                        P1n_Bound_USER_iso2 = np.append(P1n_Bound_USER_iso2,P1n_iso2_USER[i])

                                    if P2n_iso2_USER[i] != 0: 
                                        N_P2n_Bound_USER_value_iso2 = np.append(N_P2n_Bound_USER_value_iso2,N_USER[i])
                                        Z_P2n_Bound_USER_value_iso2 = np.append(Z_P2n_Bound_USER_value_iso2,Z_USER[i])
                                        P2n_Bound_USER_iso2 = np.append(P2n_Bound_USER_iso2,P2n_iso2_USER[i])
        #----------------------------------------------------------------------------

                # builds the chart that will be displayed
                color1='black'
                color2='Yellow'
                color3='DarkOrange'
                color4='Red'
                color5='Blue'
                color6='Green'
                color7='White'
                leg_list = []
                c1=0;c2=0;c3=0;c4=0;c5=0
                c6=0;c7=0;c8=0;c9=0;c10=0;c11=0

                plt.figure(figsize=(16.5,8))

                # declares all necessary variables that tweak the chart for optimal viewing
                if (Delta_N > 80) or (Delta_Z > 80):
                    msize = 4
                    mew = 1.5;ms1=1
                    lw1 = 0.5;lw2 = 1
                    
                if (Delta_N > 10 and Delta_N <= 80) and (Delta_Z > 10 and Delta_Z <= 80):
                    msize = 9
                    mew = 2.0;ms1=1
                    lw1 = 0.5;lw2 = 1

                if ((Delta_N != 10 and Delta_Z != 10) or (Delta_N != 7 and Delta_Z != 7) or (Delta_N != 4 and Delta_Z != 4) or (Delta_N != 0 and Delta_Z != 0)) and (Delta_N <= 10 and Delta_Z <= 10):
                    msize = 35
                    mew = 3.0;ms1=0.2;ms2=0
                    lw1 = 2.0;lw2 = 2.5
                    Cred_N = -0.3 
                    Cred_Z1=-0.3;Cred_Z2=0;Cred_Z3=0.3 
                    Cred_Z4=0.6;Cred_Z5=0.9;Cred_Z6=1.2
                    N_ELE_adj1=0.37;Z_ELE_adj1=0.15
                    fontsize_set_1=9;fontsize_set_2=9;fontsize_set_3=8
                    N_adj=0.34;N_adj_r=0.28
                    Z_adj_1=-0.06;Z_adj_2=-0.3
                    Z_adj_5=-0.08;Z_adj_6=-0.34

                if (Delta_N == 7 and Delta_Z == 7):
                    msize = 45
                    mew = 4.0;ms1=0.2;ms2=0
                    lw1 = 2.0;lw2 = 2.5
                    Cred_N = -0.2
                    Cred_Z1=0.2;Cred_Z2=0.4;Cred_Z3=0.6 
                    Cred_Z4=0.8;Cred_Z5=1;Cred_Z6=1.2
                    N_ELE_adj1=0.3;Z_ELE_adj1=0.2
                    fontsize_set_1=10;fontsize_set_2=9;fontsize_set_3=8
                    N_adj=0.25;N_adj_r=0.25
                    Z_adj_1=0.05;Z_adj_2=-0.1;Z_adj_3=-0.25;Z_adj_4=-0.4
                    Z_adj_5=0.04;Z_adj_6=-0.12;Z_adj_7=-0.28;Z_adj_8=-0.44

                if (Delta_N == 4 and Delta_Z == 4):
                    msize = 70
                    mew = 5.0;ms1=0.1;ms2=0
                    lw1 = 3.0;lw2 = 3.5
                    Cred_N = -0.15 
                    Cred_Z1=0.2;Cred_Z2=0.35;Cred_Z3=0.5
                    Cred_Z4=0.65;Cred_Z5=0.8;Cred_Z6=0.95
                    N_ELE_adj1=0.3;Z_ELE_adj1=0.28
                    fontsize_set_1=12;fontsize_set_2=10;fontsize_set_3=8.5
                    N_adj=0.4;N_adj_i=0;N_adj_r=0.25
                    Z_adj_1=0.15;Z_adj_2=0.05;Z_adj_3=-0.05;Z_adj_4=-0.16
                    Z_adj_5=0.14;Z_adj_6=0.02;Z_adj_7=-0.1;Z_adj_8=-0.22

                if Delta_N == 0 and Delta_Z == 0:
                    msize = 200
                    mew = 5.0;ms1=0.05;ms2=0
                    lw1 = 3.0;lw2 = 3.5
                    Cred_N = -0.1 
                    Cred_Z1=0.9;Cred_Z2=0.95;Cred_Z3=1
                    Cred_Z4=1.05;Cred_Z5=1.1;Cred_Z6=1.15
                    N_ELE_adj1=0.1;Z_ELE_adj1=0.3
                    fontsize_set_1=20;fontsize_set_2=19;fontsize_set_3=18
                    N_adj=0.3;N_adj_i=0;N_adj_r=0.1
                    Z_adj_1=0.2;Z_adj_2=0.1;Z_adj_3=0;Z_adj_4=-0.1
                    Z_adj_5=0.18;Z_adj_6=0.06;Z_adj_7=-0.08;Z_adj_8=-0.22
                    ax1_1=0.75;ax1_2=0.1;ax1_3=0.02;ax1_4=0.8

                leg_entries = []
                leg_text = []
                # outputs highlighted nuclei based on Qbxn values and Pxn values
                if len(N_Bound) != 0:
                    e2, = plt.plot(N_Bound,Z_Bound,marker='s',color=color2,markersize=msize,linestyle='');c2=1
                if len(N_stable_Bound) != 0:
                    e1, = plt.plot(N_stable_Bound,Z_stable_Bound,marker='s',color=color1,markersize=msize,linestyle='');c1=1

                if Xn_EXP1 == 1 and len(N_Qbn_Bound) != 0:
                    e3, = plt.plot(N_Qbn_Bound,Z_Qbn_Bound,marker='s',color=color3,markersize=msize,linestyle='');c3=1
                if Xn_EXP2 == 1 and len(N_Qb2n_Bound) != 0:
                    e3, = plt.plot(N_Qb2n_Bound,Z_Qb2n_Bound,marker='s',color=color3,markersize=msize,linestyle='');c3=1
                if Xn_EXP3 == 1 and len(N_Qb3n_Bound) != 0:
                    e3, = plt.plot(N_Qb3n_Bound,Z_Qb3n_Bound,marker='s',color=color3,markersize=msize,linestyle='');c3=1
                if Xn_EXP4 == 1 and len(N_Qb4n_Bound) != 0:
                    e3, = plt.plot(N_Qb4n_Bound,Z_Qb4n_Bound,marker='s',color=color3,markersize=msize,linestyle='');c3=1

                if len(N_P1n_Bound) != 0 and (Xn_EXP1 == 1):
                    e4, = plt.plot(N_P1n_Bound,Z_P1n_Bound,marker='s',color=color4,markersize=msize,linestyle='');c4=1
                if len(N_P2n_Bound) != 0 and (Xn_EXP2 == 1):
                    e4, = plt.plot(N_P2n_Bound,Z_P2n_Bound,marker='s',color=color4,markersize=msize,linestyle='');c4=1
                if len(N_P3n_Bound) != 0 and (Xn_EXP3 == 1):
                    e4, = plt.plot(N_P3n_Bound,Z_P3n_Bound,marker='s',color=color4,markersize=msize,linestyle='');c4=1
                if len(N_P4n_Bound) != 0 and (Xn_EXP4 == 1):
                    e4, = plt.plot(N_P4n_Bound,Z_P4n_Bound,marker='s',color=color4,markersize=msize,linestyle='');c4=1

                if len(N_P1n_UL) != 0 and (Xn_EXP1 == 1):
                    e5, = plt.plot(N_P1n_UL,Z_P1n_UL,marker='s',color=color5,markersize=msize,linestyle='');c5=1
                if len(N_P2n_UL) != 0 and (Xn_EXP2 == 1):
                    e5, = plt.plot(N_P2n_UL,Z_P2n_UL,marker='s',color=color5,markersize=msize,linestyle='');c5=1
                if len(N_P3n_UL) != 0 and (Xn_EXP3 == 1):
                    e5, = plt.plot(N_P3n_UL,Z_P3n_UL,marker='s',color=color5,markersize=msize,linestyle='');c5=1
                if len(N_P4n_UL) != 0 and (Xn_EXP4 == 1):
                    e5, = plt.plot(N_P4n_UL,Z_P4n_UL,marker='s',color=color5,markersize=msize,linestyle='');c5=1

                if len(Snlt0_N) != 0:
                    e6, = plt.plot(Snlt0_N,Snlt0_Z,marker='s',color=color6,markersize=msize,linestyle='');c6=1

##                if len(N_P1n_NO) != 0 and (Xn_EXP1 == 1):
##                    e7, = plt.plot(N_P1n_NO,Z_P1n_NO,marker='s',color=color7,markeredgewidth=1,markersize=msize,linestyle='');c7=1
##                if len(N_P2n_NO) != 0 and (Xn_EXP2 == 1):
##                    e7, = plt.plot(N_P2n_NO,Z_P2n_NO,marker='s',color=color7,markeredgewidth=1,markersize=msize,linestyle='');c7=1
##                if len(N_P3n_NO) != 0 and (Xn_EXP3 == 1):
##                    e7, = plt.plot(N_P3n_NO,Z_P3n_NO,marker='s',color=color7,markeredgewidth=1,markersize=msize,linestyle='');c7=1
##                if len(N_P4n_NO) != 0 and (Xn_EXP4 == 1):
##                    e7, = plt.plot(N_P4n_NO,Z_P4n_NO,marker='s',color=color7,markeredgewidth=1,markersize=msize,linestyle='');c7=1

                # if user uploaded data files, output is analyzed here
                if user_Q == 1 or user_i == 1:
                    if Xn_EXP1 == 1 and len(N_Qbn_Bound_USER) != 0:
                        plt.plot(N_Qbn_Bound_USER,Z_Qbn_Bound_USER,marker='s',color=color3,markersize=msize,linestyle='');c3=1
                    if Xn_EXP2 == 1 and len(N_Qb2n_Bound_USER) != 0:
                        plt.plot(N_Qb2n_Bound_USER,Z_Qb2n_Bound_USER,marker='s',color=color3,markersize=msize,linestyle='');c3=1   
                    if Xn_EXP3 == 1 and len(N_Qb3n_Bound_USER) != 0:
                        plt.plot(N_Qb3n_Bound_USER,Z_Qb3n_Bound_USER,marker='s',color=color3,markersize=msize,linestyle='');c3=1
                    if Xn_EXP4 == 1 and len(N_Qb4n_Bound_USER) != 0:
                        plt.plot(N_Qb4n_Bound_USER,Z_Qb4n_Bound_USER,marker='s',color=color3,markersize=msize,linestyle='');c3=1

                if user_P == 1 or user_Q == 1 or user_i == 1:
                    if len(N_P1n_Bound_USER) != 0 and (Xn_EXP1 == 1):
                        plt.plot(N_P1n_Bound_USER,Z_P1n_Bound_USER,marker='s',color=color4,markersize=msize,linestyle='');c4=1
                    if len(N_P2n_Bound_USER) != 0 and (Xn_EXP2 == 1):
                        plt.plot(N_P2n_Bound_USER,Z_P2n_Bound_USER,marker='s',color=color4,markersize=msize,linestyle='');c4=1
                    if len(N_P3n_Bound_USER) != 0 and (Xn_EXP3 == 1):
                        plt.plot(N_P3n_Bound_USER,Z_P3n_Bound_USER,marker='s',color=color4,markersize=msize,linestyle='');c4=1
                    if len(N_P4n_Bound_USER) != 0 and (Xn_EXP4 == 1):
                        plt.plot(N_P4n_Bound_USER,Z_P4n_Bound_USER,marker='s',color=color4,markersize=msize,linestyle='');c4=1
                        
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    if (Ratio == 1 or Pxn_EXP == 1) and NORM_EXP == 0 and len(N_ELE) != 0 and len(ELE_name) != 0:
                        #checks priority of user data over basic data for displaying values
                        for i in xrange(0,len(N_ELE)):
                            if user_P != 1 or user_Q != 1 or user_i != 1:
                                ELE_info = ' '.join([ELE_name[i].rstrip('\n'),str(int(A_ELE[i]))])
                                plt.text(N_ELE[i]-N_ELE_adj1,Z_ELE[i]+Z_ELE_adj1,ELE_info,fontsize=fontsize_set_1)
                            else:
                                for ii in xrange(0,len(N_ELE_USER)):
                                    if N_ELE[i] == N_ELE_USER[ii] and Z_ELE[i] == Z_ELE_USER[ii]:
                                        PriorityCheck = 0
                                        break
                                    else:
                                        PriorityCheck = 1
                                if PriorityCheck == 1:
                                    ELE_info = ' '.join([ELE_name[i].rstrip('\n'),str(int(A_ELE[i]))])
                                    plt.text(N_ELE[i]-N_ELE_adj1,Z_ELE[i]+Z_ELE_adj1,ELE_info,fontsize=fontsize_set_1)

                # outputs element info from user data files
                if user_P == 1 or user_Q == 1 or user_i == 1:
                    if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                        if (Ratio == 1 or Pxn_EXP == 1) and NORM_EXP == 0 and len(N_USER) != 0 and len(ELE_name_USER) != 0:
                            for i in xrange(0,len(N_ELE_USER)):
                                ELE_info = ' '.join([ELE_name_USER[i].rstrip('\n'),str(int(A_ELE_USER[i]))])
                                plt.text(N_ELE_USER[i]-N_ELE_adj1,Z_ELE_USER[i]+Z_ELE_adj1,ELE_info,fontsize=fontsize_set_1)

                # displays Ratio values from arrays formed prior
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    if Ratio == 1 and Pxn_EXP == 0 and NORM_EXP == 0:
                        for i in xrange(0,len(N_Ratio_USER)):
                            ELE_info = ' '.join([ELE_names_Ratio[i].rstrip('\n'),str(int(A_Ratio_USER[i]))])
                            plt.text(N_Ratio_USER[i]-N_ELE_adj1,Z_Ratio_USER[i]+Z_ELE_adj1,ELE_info,fontsize=fontsize_set_1)

                        if len(N_R1n_USER) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                            for i in xrange(0,len(N_R1n_USER)):
                                str_ratio="{0:.2f}".format(R1n_USER[i])
                                plt.text(N_R1n_USER[i]-N_adj_r,Z_R1n_USER[i]+Z_adj_5,str_ratio,fontsize=fontsize_set_2)
                                plt.plot(N_R1n_USER,Z_R1n_USER,marker='s',color=color1,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')

                        if len(N_R2n_USER) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                            for i in xrange(0,len(N_R2n_USER)):
                                str_ratio="{0:.2f}".format(R2n_USER[i])
                                plt.text(N_R2n_USER[i]-N_adj_r,Z_R2n_USER[i]+Z_adj_6,str_ratio,fontsize=fontsize_set_2)
                                plt.plot(N_R2n_USER,Z_R2n_USER,marker='s',color=color6,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')

                        if len(N_R3n_USER) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                            for i in xrange(0,len(N_R3n_USER)):
                                str_ratio="{0:.2f}".format(R3n_USER[i])
                                plt.text(N_R3n_USER[i]-N_adj_r,Z_R3n_USER[i]+Z_adj_7,str_ratio,fontsize=fontsize_set_2)
                                plt.plot(N_R3n_USER,Z_R3n_USER,marker='s',color=color7,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')

                        if Ratio_USER_THEO == 1 and Ratio_MOE_THEO == 0:
                            if len(N_R4n_USER) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                                for i in xrange(0,len(N_R4n_USER)):
                                    str_ratio="{0:.2f}".format(R4n_USER[i])
                                    plt.text(N_R4n_USER[i]-N_adj_r,Z_R4n_USER[i]+Z_adj_8,str_ratio,fontsize=fontsize_set_2)
                                    plt.plot(N_R4n_USER,Z_R4n_USER,marker='s',color=color8,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')

                    # outputs Pxn values and does priority check if user data files uploaded
                    if Pxn_EXP == 1 and NORM_EXP == 0 and Ratio == 0:
                        if (Xn_EXP1 == 1) and len(N_P1n_Bound_value) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                            for i in xrange(0,len(N_P1n_Bound_value)):
                                if user_P != 1 or user_Q != 1 or user_i != 1:
                                    str_ratio="{0:.2f}".format(P1n_Bound[i])
                                    plt.text(N_P1n_Bound_value[i]-N_adj,Z_P1n_Bound_value[i]+Z_adj_1,str_ratio,fontsize=fontsize_set_3)
                                else:
                                    for ii in xrange(0,len(N_P1n_Bound_USER_value)):
                                        if N_P1n_Bound_value[i] == N_P1n_Bound_USER_value[ii] and Z_P1n_Bound_value[i] == Z_P1n_Bound_USER_value[ii]:
                                            PriorityCheck = 0
                                            break
                                        else:
                                            PriorityCheck = 1
                                    if PriorityCheck == 1:
                                        str_ratio="{0:.2f}".format(P1n_Bound[i])
                                        plt.text(N_P1n_Bound_value[i]-N_adj,Z_P1n_Bound_value[i]+Z_adj_1,str_ratio,fontsize=fontsize_set_3)        

                        if (Xn_EXP2 == 1) and len(N_P2n_Bound_value) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                            for i in xrange(0,len(N_P2n_Bound_value)):
                                if user_P != 1 or user_Q != 1 or user_i != 1:
                                    str_ratio="{0:.2f}".format(P2n_Bound[i])
                                    plt.text(N_P2n_Bound_value[i]-N_adj,Z_P2n_Bound_value[i]+Z_adj_2,str_ratio,fontsize=fontsize_set_3)
                                else:
                                    for ii in xrange(0,len(N_P2n_Bound_USER_value)):
                                        if N_P2n_Bound_value[i] == N_P2n_Bound_USER_value[ii] and Z_P2n_Bound_value[i] == Z_P2n_Bound_USER_value[ii]:
                                            PriorityCheck = 0
                                            break
                                        else:
                                            PriorityCheck = 1
                                    if PriorityCheck == 1:
                                        str_ratio="{0:.2f}".format(P2n_Bound[i])
                                        plt.text(N_P2n_Bound_value[i]-N_adj,Z_P2n_Bound_value[i]+Z_adj_2,str_ratio,fontsize=fontsize_set_3)

                        if (Xn_EXP3 == 1) and len(N_P3n_Bound_value) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                            for i in xrange(0,len(N_P3n_Bound_value)):
                                if user_P != 1 or user_Q != 1 or user_i != 1:
                                    str_ratio="{0:.2f}".format(P3n_Bound[i])
                                    plt.text(N_P3n_Bound_value[i]-N_adj,Z_P3n_Bound_value[i]+Z_adj_3,str_ratio,fontsize=fontsize_set_3)
                                else:
                                    for ii in xrange(0,len(N_P3n_Bound_USER_value)):
                                        if N_P3n_Bound_value[i] == N_P3n_Bound_USER_value[ii] and Z_P3n_Bound_value[i] == Z_P3n_Bound_USER_value[ii]:
                                            PriorityCheck = 0
                                            break
                                        else:
                                            PriorityCheck = 1
                                    if PriorityCheck == 1:
                                        str_ratio="{0:.2f}".format(P3n_Bound[i])
                                        plt.text(N_P3n_Bound_value[i]-N_adj,Z_P3n_Bound_value[i]+Z_adj_3,str_ratio,fontsize=fontsize_set_3)    

                        if (Xn_EXP4 == 1) and len(N_P4n_Bound_value) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                            for i in xrange(0,len(N_P4n_Bound_value)):
                                if user_P != 1 or user_Q != 1 or user_i != 1:
                                    str_ratio="{0:.2f}".format(P4n_Bound[i])
                                    plt.text(N_P4n_Bound_value[i]-N_adj,Z_P4n_Bound_value[i]+Z_adj_4,str_ratio,fontsize=fontsize_set_3)
                                else:
                                    for ii in xrange(0,len(N_P4n_Bound_USER_value)):
                                        if N_P4n_Bound_value[i] == N_P4n_Bound_USER_value[ii] and Z_P4n_Bound_value[i] == Z_P4n_Bound_USER_value[ii]:
                                            PriorityCheck = 0
                                            break
                                        else:
                                            PriorityCheck = 1
                                    if PriorityCheck == 1:
                                        str_ratio="{0:.2f}".format(P4n_Bound[i])
                                        plt.text(N_P4n_Bound_value[i]-N_adj,Z_P4n_Bound_value[i]+Z_adj_4,str_ratio,fontsize=fontsize_set_3)

                        if (Xn_EXP1 == 1) and len(N_P1n_Bound_value_iso1) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                            for i in xrange(0,len(N_P1n_Bound_value_iso1)):
                                if user_i != 1:
                                    str_ratio="{0:.2f}".format(P1n_Bound_iso1[i])
                                    plt.text(N_P1n_Bound_value_iso1[i]-N_adj_i,Z_P1n_Bound_value_iso1[i]+Z_adj_1,'| '+str_ratio,fontsize=fontsize_set_3)
                                else:
                                    for ii in xrange(0,len(N_P1n_Bound_USER_value_iso1)):
                                        if N_P1n_Bound_value_iso1[i] == N_P1n_Bound_USER_value_iso1[ii] and Z_P1n_Bound_value_iso1[i] == Z_P1n_Bound_USER_value_iso1[ii]:
                                            PriorityCheck = 0
                                            break
                                        else:
                                            PriorityCheck = 1
                                    if PriorityCheck == 1:
                                        str_ratio="{0:.2f}".format(P1n_Bound_iso1[i])
                                        plt.text(N_P1n_Bound_value_iso1[i]-N_adj_i,Z_P1n_Bound_value_iso1[i]+Z_adj_1,'| '+str_ratio,fontsize=fontsize_set_3)

                        if (Xn_EXP2 == 1) and len(N_P2n_Bound_value_iso1) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                            for i in xrange(0,len(N_P2n_Bound_value_iso1)):
                                if user_i != 1:
                                    str_ratio="{0:.2f}".format(P2n_Bound_iso1[i])
                                    plt.text(N_P2n_Bound_value_iso1[i]-N_adj_i,Z_P2n_Bound_value_iso1[i]+Z_adj_2,'| '+str_ratio,fontsize=fontsize_set_3)
                                else:
                                    for ii in xrange(0,len(N_P2n_Bound_USER_value_iso1)):
                                        if N_P2n_Bound_value_iso1[i] == N_P2n_Bound_USER_value_iso1[ii] and Z_P2n_Bound_value_iso1[i] == Z_P2n_Bound_USER_value_iso1[ii]:
                                            PriorityCheck = 0
                                            break
                                        else:
                                            PriorityCheck = 1
                                    if PriorityCheck == 1:
                                        str_ratio="{0:.2f}".format(P2n_Bound_iso1[i])
                                        plt.text(N_P2n_Bound_value_iso1[i]-N_adj_i,Z_P2n_Bound_value_iso1[i]+Z_adj_2,'| '+str_ratio,fontsize=fontsize_set_3)

                        if (Xn_EXP1 == 1) and len(N_P1n_Bound_value_iso2) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                            for i in xrange(0,len(N_P1n_Bound_value_iso2)):
                                if user_i != 1:
                                    str_ratio="{0:.2f}".format(P1n_Bound_iso2[i])
                                    plt.text(N_P1n_Bound_value_iso2[i]-N_adj_i,Z_P1n_Bound_value_iso2[i]+Z_adj_3,'| '+str_ratio,fontsize=fontsize_set_3)
                                else:
                                    for ii in xrange(0,len(N_P1n_Bound_USER_value_iso2)):
                                        if N_P1n_Bound_value_iso2[i] == N_P1n_Bound_USER_value_iso2[ii] and Z_P1n_Bound_value_iso2[i] == Z_P1n_Bound_USER_value_iso2[ii]:
                                            PriorityCheck = 0
                                            break
                                        else:
                                            PriorityCheck = 1
                                    if PriorityCheck == 1:
                                        str_ratio="{0:.2f}".format(P1n_Bound_iso2[i])
                                        plt.text(N_P1n_Bound_value_iso2[i]-N_adj_i,Z_P1n_Bound_value_iso2[i]+Z_adj_3,'| '+str_ratio,fontsize=fontsize_set_3)

                        if (Xn_EXP2 == 1) and len(N_P2n_Bound_value_iso2) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                            for i in xrange(0,len(N_P2n_Bound_value_iso2)):
                                if user_i != 1:
                                    str_ratio="{0:.2f}".format(P2n_Bound_iso2[i])
                                    plt.text(N_P2n_Bound_value_iso2[i]-N_adj_i,Z_P2n_Bound_value_iso2[i]+Z_adj_4,'| '+str_ratio,fontsize=fontsize_set_3)
                                else:
                                    for ii in xrange(0,len(N_P2n_Bound_USER_value_iso2)):
                                        if N_P2n_Bound_value_iso2[i] == N_P2n_Bound_USER_value_iso2[ii] and Z_P2n_Bound_value_iso2[i] == Z_P2n_Bound_USER_value_iso2[ii]:
                                            PriorityCheck = 0
                                            break
                                        else:
                                            PriorityCheck = 1
                                    if PriorityCheck == 1:
                                        str_ratio="{0:.2f}".format(P2n_Bound_iso2[i])
                                        plt.text(N_P2n_Bound_value_iso2[i]-N_adj_i,Z_P2n_Bound_value_iso2[i]+Z_adj_4,'| '+str_ratio,fontsize=fontsize_set_3)

                        # outputs Pxn values from user data files 
                        if user_P == 1 or user_Q == 1 or user_i == 1:
                            if (Xn_EXP1 == 1) and len(N_P1n_Bound_USER_value) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                                for i in xrange(0,len(N_P1n_Bound_USER_value)):
                                    str_ratio="{0:.2f}".format(P1n_Bound_USER[i])
                                    plt.text(N_P1n_Bound_USER_value[i]-N_adj,Z_P1n_Bound_USER_value[i]+Z_adj_1,str_ratio,fontsize=fontsize_set_3)

                            if (Xn_EXP2 == 1) and len(N_P2n_Bound_USER_value) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                                for i in xrange(0,len(N_P2n_Bound_USER_value)):
                                    str_ratio="{0:.2f}".format(P2n_Bound_USER[i])
                                    plt.text(N_P2n_Bound_USER_value[i]-N_adj,Z_P2n_Bound_USER_value[i]+Z_adj_2,str_ratio,fontsize=fontsize_set_3)

                            if (Xn_EXP3 == 1) and len(N_P3n_Bound_USER_value) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                                for i in xrange(0,len(N_P3n_Bound_USER_value)):
                                    str_ratio="{0:.2f}".format(P3n_Bound_USER[i])
                                    plt.text(N_P3n_Bound_USER_value[i]-N_adj,Z_P3n_Bound_USER_value[i]+Z_adj_3,str_ratio,fontsize=fontsize_set_3)

                            if (Xn_EXP4 == 1) and len(N_P4n_Bound_USER_value) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                                for i in xrange(0,len(N_P4n_Bound_USER_value)):
                                    str_ratio="{0:.2f}".format(P4n_Bound_USER[i])
                                    plt.text(N_P4n_Bound_USER_value[i]-N_adj,Z_P4n_Bound_USER_value[i]+Z_adj_4,str_ratio,fontsize=fontsize_set_3)

                        if user_i == 1:    
                            if (Xn_EXP1 == 1) and len(N_P1n_Bound_USER_value_iso1) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                                for i in xrange(0,len(N_P1n_Bound_USER_value_iso1)):
                                    str_ratio="{0:.2f}".format(P1n_Bound_USER_iso1[i])
                                    plt.text(N_P1n_Bound_USER_value_iso1[i]-N_adj_i,Z_P1n_Bound_USER_value_iso1[i]+Z_adj_1,'| '+str_ratio,fontsize=fontsize_set_3)

                            if (Xn_EXP2 == 1) and len(N_P2n_Bound_USER_value_iso1) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                                for i in xrange(0,len(N_P2n_Bound_USER_value_iso1)):
                                    str_ratio="{0:.2f}".format(P2n_Bound_USER_iso1[i])
                                    plt.text(N_P2n_Bound_USER_value_iso1[i]-N_adj_i,Z_P2n_Bound_USER_value_iso1[i]+Z_adj_2,'| '+str_ratio,fontsize=fontsize_set_3)

                            if (Xn_EXP1 == 1) and len(N_P1n_Bound_USER_value_iso2) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                                for i in xrange(0,len(N_P1n_Bound_USER_value_iso2)):
                                    str_ratio="{0:.2f}".format(P1n_Bound_USER_iso2[i])
                                    plt.text(N_P1n_Bound_USER_value_iso2[i]-N_adj_i,Z_P1n_Bound_USER_value_iso2[i]+Z_adj_3,'| '+str_ratio,fontsize=fontsize_set_3)

                            if (Xn_EXP2 == 1) and len(N_P2n_Bound_USER_value_iso2) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                                for i in xrange(0,len(N_P2n_Bound_USER_value_iso2)):
                                    str_ratio="{0:.2f}".format(P2n_Bound_USER_iso2[i])
                                    plt.text(N_P2n_Bound_USER_value_iso2[i]-N_adj_i,Z_P2n_Bound_USER_value_iso2[i]+Z_adj_4,'| '+str_ratio,fontsize=fontsize_set_3)
                                    
                plt.axis('scaled')
                g=plt.gca()
                plt.xlim(N_low_user,N_high_user)
                plt.ylim(Z_low_user-1,Z_high_user+1)

                Num_xticks = np.arange(N_low_user+1,N_high_user,1)
                label_xticks = [];append_lx = label_xticks.append
                for i in xrange(N_low_user+1,N_high_user):
                    c = i%2
                    if c == 0:
                        label_xticks.append(i)
                    else:
                        label_xticks.append("")
                if Delta_N >= 100:
                    label_xticks = []
                plt.xticks(Num_xticks,label_xticks)
                plt.xticks(size=8)
                    
                Num_yticks = np.arange(Z_low_user,Z_high_user+1,1)
                label_yticks = [];append_ly = label_yticks.append
                for i in xrange(Z_low_user,Z_high_user+1):
                    c = i%2
                    if c == 0:
                        label_yticks.append(i)
                    else:
                        label_yticks.append("")
                if Delta_N >= 100:
                    label_xticks = []
                plt.yticks(Num_yticks,label_yticks)
                plt.yticks(size=8)

                if Ratio == 1 and Pxn_EXP == 0 and NORM_EXP == 0:
                    plt.title(Title_Ratio)
                if Ratio == 0:
                    plt.title(Title_EXP)

                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    plt.xlabel(xlabel)
                    plt.ylabel(ylabel)          
                else:
                    plt.xlabel(xlabel2,fontsize=14)
                    plt.ylabel(ylabel,fontsize=14)

                # determines which magic number lines are necessary to display
                if N_high_user >= 8 and N_low_user <= 8:  
                    plt.plot(N_Bound_magic*0.+8.5,Z_Bound_magic,color=color1,linewidth=lw1)  
                    plt.plot(N_Bound_magic*0.+7.5,Z_Bound_magic,color=color1,linewidth=lw1)

                if N_high_user >= 20 and N_low_user <= 20:
                    plt.plot(N_Bound_magic*0.+20.5,Z_Bound_magic,color=color1,linewidth=lw1) 
                    plt.plot(N_Bound_magic*0.+19.5,Z_Bound_magic,color=color1,linewidth=lw1)

                if N_high_user >= 28 and N_low_user <= 28:
                    plt.plot(N_Bound_magic*0.+28.5,Z_Bound_magic,color=color1,linewidth=lw1)
                    plt.plot(N_Bound_magic*0.+27.5,Z_Bound_magic,color=color1,linewidth=lw1)     

                if N_high_user >= 50 and N_low_user <= 50:
                    plt.plot(N_Bound_magic*0.+50.5,Z_Bound_magic,color=color1,linewidth=lw1)
                    plt.plot(N_Bound_magic*0.+49.5,Z_Bound_magic,color=color1,linewidth=lw1)

                if N_high_user >= 82 and N_low_user <= 82:
                    plt.plot(N_Bound_magic*0.+82.5,Z_Bound_magic,color=color1,linewidth=lw1)
                    plt.plot(N_Bound_magic*0.+81.5,Z_Bound_magic,color=color1,linewidth=lw1)

                if N_high_user >= 126 and N_low_user <= 126:
                    plt.plot(N_Bound_magic*0.+126.5,Z_Bound_magic,color=color1,linewidth=lw1) 
                    plt.plot(N_Bound_magic*0.+125.5,Z_Bound_magic,color=color1,linewidth=lw1) 

                if Z_high_user >= 8 and Z_low_user <= 8:
                    plt.plot(N_Bound_magic,Z_Bound_magic*0.+8.5,color=color1,linewidth=lw1) 
                    plt.plot(N_Bound_magic,Z_Bound_magic*0.+7.5,color=color1,linewidth=lw1)

                if Z_high_user >= 20 and Z_low_user <= 20:
                    plt.plot(N_Bound_magic,Z_Bound_magic*0.+20.5,color=color1,linewidth=lw1) 
                    plt.plot(N_Bound_magic,Z_Bound_magic*0.+19.5,color=color1,linewidth=lw1)

                if Z_high_user >= 28 and Z_low_user <= 28:
                    plt.plot(N_Bound_magic,Z_Bound_magic*0.+28.5,color=color1,linewidth=lw1)
                    plt.plot(N_Bound_magic,Z_Bound_magic*0.+27.5,color=color1,linewidth=lw1)             

                if Z_high_user >= 50 and Z_low_user <= 50:
                    plt.plot(N_Bound_magic,Z_Bound_magic*0.+50.5,color=color1,linewidth=lw1)
                    plt.plot(N_Bound_magic,Z_Bound_magic*0.+49.5,color=color1,linewidth=lw1)

                if Z_high_user >= 82 and Z_low_user <= 82:
                    plt.plot(N_Bound_magic,Z_Bound_magic*0.+82.5,color=color1,linewidth=lw1)
                    plt.plot(N_Bound_magic,Z_Bound_magic*0.+81.5,color=color1,linewidth=lw1)

                if Z_high_user >= 126 and Z_low_user <= 126:
                    plt.plot(N_Bound_magic,Z_Bound_magic*0.+126.5,color=color1,linewidth=lw1)
                    plt.plot(N_Bound_magic,Z_Bound_magic*0.+125.5,color=color1,linewidth=lw1)

                # credits
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z1,CreditTextEXP_1,fontsize=10)
                    plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z2,CreditTextEXP_2,fontsize=10)
                    plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z3,CreditTextEXP_3,fontsize=10)

                    if Ratio == 1 and Pxn_EXP == 0 and NORM_EXP == 0:
                        plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z4,CreditTextEXP_4,fontsize=10)
                        plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z5,CreditTextEXP_5,fontsize=10)
                        plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z6,CreditTextEXP_6,fontsize=10) 

                    if Ratio == 0:
                        plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z4,CreditTextEXP_4,fontsize=10)
                        plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z5,CreditTextEXP_5,fontsize=10)

                # builds legend
                if c1 == 1:
                    leg_entries.append(e1);leg_text.append(leg_EXP_1)
                if c2 == 1:
                    leg_entries.append(e2);leg_text.append(leg_EXP_2)
                if c3 == 1:
                    leg_entries.append(e3);leg_text.append(leg_EXP_3)
                if c4 == 1:
                    leg_entries.append(e4);leg_text.append(leg_EXP_4)
                if c5 == 1:
                    leg_entries.append(e5);leg_text.append(leg_EXP_5)
                if c6 == 1:
                    leg_entries.append(e6);leg_text.append(leg_EXP_6)
                if c7 == 1:
                    leg_entries.append(e7);leg_text.append(leg_EXP_7)
                    
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    l1 = plt.legend(leg_entries,leg_text,loc=2,bbox_to_anchor=[1.02,0.98],borderaxespad=0.,markerscale=ms1,numpoints=1)
                    if Ratio == 1 and Pxn_EXP == 0 and NORM_EXP == 0 and Delta_Z <= 10 and Delta_N <= 10  and Delta_N > 7 and Delta_Z > 7:
                        l2 = plt.legend((leg_ValueLabels1_EXP,leg_ValueLabels2_EXP,leg_ValueLabels3_EXP),loc=6,bbox_to_anchor=[1.02,0.4],numpoints=1,markerscale=ms2)
                        g.add_artist(l1)
                    if Ratio == 1 and Pxn_EXP == 0 and NORM_EXP == 0 and Delta_Z <= 7 and Delta_N <= 7:
                        l2 = plt.legend((leg_ValueLabels1_EXP,leg_ValueLabels2_EXP,leg_ValueLabels3_EXP,leg_ValueLabels4_EXP),loc=6,bbox_to_anchor=[1.02,0.4],numpoints=1,markerscale=ms2)
                        g.add_artist(l1)
                    if Ratio == 1 and Pxn_EXP == 0 and NORM_EXP == 0 and Delta_Z <= 4 and Delta_N <= 4:
                        l2 = plt.legend((leg_ValueLabels1_EXP,leg_ValueLabels2_EXP,leg_ValueLabels3_EXP,leg_ValueLabels4_EXP,leg_ValueLabels5_EXP),loc=6,bbox_to_anchor=[1.02,0.4],numpoints=1,markerscale=ms2)
                        g.add_artist(l1)

                    if Ratio == 0 and Pxn_EXP == 1 and NORM_EXP == 0 and Delta_Z <= 10 and Delta_N <= 10 and Delta_N > 7 and Delta_Z > 7:
                        l2 = plt.legend((leg_ValueLabels1_THEO,leg_ValueLabels2_THEO,leg_ValueLabels3_THEO),loc=6,bbox_to_anchor=[1.02,0.4],numpoints=1,markerscale=ms2)
                        g.add_artist(l1)
                    if Ratio == 0 and Pxn_EXP == 1 and NORM_EXP == 0 and Delta_Z <= 7 and Delta_N <= 7  and Delta_N > 4 and Delta_Z > 4:
                        l2 = plt.legend((leg_ValueLabels1_THEO,leg_ValueLabels2_THEO,leg_ValueLabels3_THEO,leg_ValueLabels4_THEO,leg_ValueLabels5_THEO),loc=6,bbox_to_anchor=[1.02,0.4],numpoints=1,markerscale=ms2)
                        g.add_artist(l1)
                    if Ratio == 0 and Pxn_EXP == 1 and NORM_EXP == 0 and Delta_Z <= 4 and Delta_N <= 4:
                        l2 = plt.legend((leg_ValueLabels1_iso,leg_ValueLabels2_iso,leg_ValueLabels3_iso,leg_ValueLabels4_iso,leg_ValueLabels5_iso),loc=6,bbox_to_anchor=[1.02,0.4],numpoints=1,markerscale=ms2)
                        g.add_artist(l1)
                else:
                    l1 = plt.legend(leg_entries,leg_text,loc=4,markerscale=ms1,numpoints=1)

                plt.show(block=False)

        PLOT_Button = Tkinter.Button(self,text=u"PLOT",command=PLOT) # PLOT button
        PLOT_Button.grid(column=2,row=28)

        self.grid_columnconfigure(0,weight=1) #resize columns when window is resized
        self.grid_columnconfigure(1,weight=1) #resize columns when window is resized
        self.grid_columnconfigure(2,weight=1) #resize columns when window is resized
        self.grid_columnconfigure(3,weight=1) #resize columns when window is resized
        self.grid_columnconfigure(4,weight=1) #resize columns when window is resized

        self.resizable(True,False) #enables horizontal resizing, prevents vertical resizing
        self.update()
        self.geometry(self.geometry())  

# opens and starts GUI for visualization
if __name__ == "__main__":
    app = BDNE_GUI(None) #first GUI element so no parent, 'None'
    app.title('Beta-Delayed Neutron Emission Visualization Program - Version 2')
    app.mainloop() #program loops indefinitely, waiting for events, until user closes window
