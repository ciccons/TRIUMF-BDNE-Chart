#-----------------------------------------------------------------------------
# Author: Stephanie Ciccone
# Consult Chart_Program_INFO.txt for instruction on how to ensure this program properly runs on your machine
#-----------------------------------------------------------------------------

# imports all necessary libraries and functions
import gc
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# function to display Chart with theoretical data from the MOELLER(2003) paper
def MOELLER():

    # determines if running on a Windows or a Unix machine and yields the required directory deliminator
    if os.name == "nt":
        dirDelim = "\\"
    else:
        dirDelim = "/"

    # reads in values from text files and stores all of the data columns into arrays
    filename_MOE = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "ChartNuclides_DataTable_MOELLER.txt"

    print ""
    print "If you wish to include additional data, you can enter your data file name below. Data files must be in the format shown!"
    print "----------HEADER COLUMN TITLES----------"
    print "-- N values -- Z values -- P1n -- P2n -- P3n -- Nuclei Name --"
    print ""
    USER_filename = input("Enter 'pass' to skip. Enter the name of your own data file in ' ': ")

    user_P = 0
    while USER_filename != 'pass':
        filename_THEORY_USER = os.getcwd() + dirDelim + "Text_Files" + dirDelim + USER_filename
        
        ELE_names_THEORY = np.genfromtxt(filename_THEORY_USER,skip_header=1,usecols=(5),dtype=str,unpack=True)
        N_P_USER,Z_P_USER,P1n_USER,P2n_USER,P3n_USER = np.loadtxt(filename_THEORY_USER,skiprows=1,usecols=(0, 1, 2, 3, 4),unpack=True)
        size_P_USER = len(N_P_USER) ; user_P = 1

        USER_filename = input("Enter 'pass' to skip. Enter the name of your own data file in '': ")

    N_stable,Z_stable = np.loadtxt(filename_MOE,skiprows=1,usecols=(0, 1),unpack=True)
    s1 = len(N_stable)
    
    N,Z = np.loadtxt(filename_MOE,skiprows=1,usecols=(2, 3),unpack=True)
    s2 = len(N)
    
    ELE_names_MOE = np.genfromtxt(filename_MOE,skip_header=1,usecols=(9),dtype=str,unpack=True)
    N_P,Z_P,P1n,P2n,P3n = np.loadtxt(filename_MOE,skiprows=1,usecols=(4, 5, 6, 7, 8),unpack=True)
    size_P = len(N_P)

    #-------------------------------------------------------------------------

    # list of text in order to properly set up the legend
    leg_text=['','Existing Nuclei','Stable','P(1n) dominates','P(2n) dominates','P(3n) dominates']
    
    #-------------------------------------------------------------------------

    r = 0 
    while r != 1:

        # initializes the N and Z user range variables
        N_low_user = 0;N_high_user = 0
        Z_low_user = 0;Z_high_user = 0

        # Introduction Text (all text and user input options will be altered into a GUI in the future)
        print "--------------------------------------------------"
        print "Welcome to the Chart of Nuclides Output Program - MOELLER Edition."
        print ""
        print "The Chart will zoom in and display P values of the theoretical emitters only if the user inputs:"
        print " 1. An N range with a difference equal to 10 and a Z range with a difference equal to 10."
        print " 2. An N range with a difference equal to 7 and a Z range with a difference equal to 7."
        print " 3. An N range with a difference equal to 4 and a Z range with a difference equal to 4."
        print " 4. An N range with a difference equal to 0 and a Z range with a difference equal to 0."
        print "The Chart will output normally if BOTH ranges are different to these limits."
        print "You also have the option to display a color bar for either P1n, P2n, or P3n values."
        print "It is recommended to input exact differences following Options 1 to 4 above for optimal viewing results."
        print""
        print"---------------------------------------------------"
        print""

        N_low_user=input('Enter the integer value for the minimum of the N range: ')
        N_high_user=input('Enter the integer value for the maximum of the N range: ')
        Z_low_user=input('Enter the integer value for the minimum of the Z range: ')
        Z_high_user=input('Enter the integer value for the maximum of the Z range: ')

        Delta_N = N_high_user - N_low_user
        Delta_Z = Z_high_user - Z_low_user

        N_high_user=N_high_user+1
        N_low_user=N_low_user-1

        print "Analyzing Data Tables and Building Chart Arrays..."

        #-----------------------------------------------------------------------------
        
        # this part of the code makes an array for only the N and Z values that denote a stable nuclei from the basic data files
        N_stable_Bound = [];Z_stable_Bound = []
        append_NstableB = N_stable_Bound.append;append_ZstableB = Z_stable_Bound.append

        for i in xrange(0,s1):
            if Z_stable[i] >= Z_low_user and Z_stable[i] <= Z_high_user:
                append_NstableB(N_stable[i])
                append_ZstableB(Z_stable[i])

        #------------------------------------------------------------------------------

        # makes an array of the nuclei that are within the user bounds from the basic data files
        N_Bound = []; Z_Bound = []
        append_NB = N_Bound.append;append_ZB = Z_Bound.append

        for i in xrange(0,len(N)):
            if Z[i] >= Z_low_user and Z[i] <= Z_high_user:
                append_NB(N[i])
                append_ZB(Z[i])

        #------------------------------------------------------------------------------

        # this part of the code makes an array for the N and Z values of the magic number lines from the basic data files
        # also makes an array for all nuclei found in the user bounds
        N_P_Bound = [] ; Z_P_Bound = []
        append_NPB = N_P_Bound.append;append_ZPB = Z_P_Bound.append
        N_Bound_magic = [] ; Z_Bound_magic = []
        append_NmagB = N_Bound_magic.append;append_ZmagB = Z_Bound_magic.append
                
        for i in xrange(0,size_P):

            if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user:
                append_NPB(N_P[i])
                append_ZPB(Z_P[i])

            if Z_P[i] >= 0 and Z_P[i] <= Z_high_user:
                append_NmagB(N_P[i])
                append_ZmagB(Z_P[i])
        N_Bound_magic = np.array(N_Bound_magic)
        Z_Bound_magic = np.array(Z_Bound_magic)

        #-----------------------------------------------------------------------------

        #for loop that determines the size of an array based on isotopes that have probability of beta-delayed emission
        #greater than 0 (measured probability) and determines array of P values that should be displayed on the plot
        N_P1n = [];Z_P1n = []
        append_NP1 = N_P1n.append;append_ZP1 = Z_P1n.append
        N_P2n = [];Z_P2n = []
        append_NP2 = N_P2n.append;append_ZP2 = Z_P2n.append
        N_P3n = [];Z_P3n = []
        append_NP3 = N_P3n.append;append_ZP3 = Z_P3n.append

        N_P1n_Bound = [];Z_P1n_Bound = []
        append_NP1B = N_P1n_Bound.append;append_ZP1B = Z_P1n_Bound.append
        P1n_Bound = [];P1n_Color = []
        append_P1B = P1n_Bound.append;append_P1NC = P1n_Color.append
        N_P1n_Color = [];Z_P1n_Color = []
        append_NP1C = N_P1n_Color.append;append_ZP1C = Z_P1n_Color.append
        
        N_P2n_Bound = [];Z_P2n_Bound = []
        append_NP2B = N_P2n_Bound.append;append_ZP2B = Z_P2n_Bound.append
        P2n_Bound = [];P2n_Color = []
        append_P2B = P2n_Bound.append;append_P2NC = P2n_Color.append
        N_P2n_Color = [];Z_P2n_Color = []
        append_NP2C = N_P2n_Color.append;append_ZP2C = Z_P2n_Color.append
        
        N_P3n_Bound = [];Z_P3n_Bound = []
        append_NP3B = N_P3n_Bound.append;append_ZP3B = Z_P3n_Bound.append
        P3n_Bound = [];P3n_Color = []
        append_P3B = P3n_Bound.append;append_P3NC = P3n_Color.append
        N_P3n_Color = [];Z_P3n_Color = []
        append_NP3C = N_P3n_Color.append;append_ZP3C = Z_P3n_Color.append

        N_ELE = [];Z_ELE = []
        append_NELE = N_ELE.append;append_ZELE = Z_ELE.append
        A_ELE = [];ELE_name = []
        append_AELE = A_ELE.append;append_ELEn = ELE_name.append

        if user_P == 1:
            N_P1n_USER = [];Z_P1n_USER = []
            append_NP1U = N_P1n_USER.append;append_ZP1U = Z_P1n_USER.append
            N_P2n_USER = [];Z_P2n_USER = []
            append_NP2U = N_P2n_USER.append;append_ZP2U = Z_P2n_USER.append
            N_P3n_USER = [];Z_P3n_USER = []
            append_NP3U = N_P3n_USER.append;append_ZP3U = Z_P3n_USER.append

            N_P1n_Bound_USER = [];Z_P1n_Bound_USER = []
            append_NP1BU = N_P1n_Bound_USER.append;append_ZP1BU = Z_P1n_Bound_USER.append
            P1n_Bound_USER = [];P1n_Color_USER = []
            append_P1BU = P1n_Bound_USER.append;append_P1NCU = P1n_Color_USER.append
            N_P1n_Color_USER = [];Z_P1n_Color_USER = []
            append_NP1CU = N_P1n_Color_USER.append;append_ZP1CU = Z_P1n_Color_USER.append

            N_P2n_Bound_USER = [];Z_P2n_Bound_USER = []
            append_NP2BU = N_P2n_Bound_USER.append;append_ZP2BU = Z_P2n_Bound_USER.append
            P2n_Bound_USER = [];P2n_Color_USER = []
            append_P2BU = P2n_Bound_USER.append;append_P2NCU = P2n_Color_USER.append
            N_P2n_Color_USER = [];Z_P2n_Color_USER = []
            append_NP2CU = N_P2n_Color_USER.append;append_ZP2CU = Z_P2n_Color_USER.append

            N_P3n_Bound_USER = [];Z_P3n_Bound_USER = []
            append_NP3BU = N_P3n_Bound_USER.append;append_ZP3BU = Z_P3n_Bound_USER.append
            P3n_Bound_USER = [];P3n_Color_USER = []
            append_P3BU = P3n_Bound_USER.append;append_P3NCU = P3n_Color_USER.append
            N_P3n_Color_USER = [];Z_P3n_Color_USER = []
            append_NP3CU = N_P3n_Color_USER.append;append_ZP3CU = Z_P3n_Color_USER.append

            N_ELE_USER = [];Z_ELE_USER = []
            append_NELEU = N_ELE_USER.append;append_ZELEU = Z_ELE_USER.append
            A_ELE_USER = [];ELE_name_USER = []
            append_AELEU = A_ELE_USER.append;append_ELEnU = ELE_name_USER.append

        for i in xrange(0,size_P):
            if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] >= N_low_user and N_P[i] <= N_high_user:
                if P1n[i] != 0 and P1n[i] > P2n[i] and P1n[i] > P3n[i]:
                    append_NP1(N_P[i]);append_ZP1(Z_P[i]) #makes array of nuclei with dominant P1n values

                if P1n[i] != 0:
                    append_NP1C(N_P[i]);append_ZP1C(Z_P[i]) #makes an array for the color bar version

                    if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                        append_NP1B(N_P[i]);append_ZP1B(Z_P[i]) #makes array for nuclei which will have data displayed about them
                        append_P1B(P1n[i])

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
                    
                if P2n[i] != 0:
                    append_NP2C(N_P[i]);append_ZP2C(Z_P[i])

                    if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                        append_NP2B(N_P[i]);append_ZP2B(Z_P[i])
                        append_P2B(P2n[i])

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

                if P3n[i] != 0:
                    append_NP3C(N_P[i]);append_ZP3C(Z_P[i]) 
                    
                    if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                        append_NP3B(N_P[i]);append_ZP3B(Z_P[i])
                        append_P3B(P3n[i])

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

                if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:

                    append_NELE(N_P[i])
                    append_ZELE(Z_P[i])
                    append_ELEn(ELE_names_MOE[i])
                    append_AELE(N_P[i]+Z_P[i]) # makes all the arrays to display element name and mass number, A

        if user_P == 1: #if the user has uploaded their own data, this section of the code will analyze that data to display
            for i in xrange(0,size_P_USER):
                if Z_P_USER[i] >= Z_low_user and Z_P_USER[i] <= Z_high_user and N_P_USER[i] >= N_low_user and N_P_USER[i] <= N_high_user:
                    if P1n_USER[i] != 0 and P1n_USER[i] > P2n_USER[i] and P1n_USER[i] > P3n_USER[i]:
                        append_NP1U(N_P_USER[i]);append_ZP1U(Z_P_USER[i]) #makes array of nuclei with dominant P1n values

                    if P1n_USER[i] != 0:
                        append_NP1CU(N_P_USER[i]);append_ZP1CU(Z_P_USER[i]) #makes an array for the color bar version

                        if Z_P_USER[i] >= Z_low_user and Z_P_USER[i] <= Z_high_user and N_P_USER[i] > N_low_user and N_P_USER[i] < N_high_user:
                            append_NP1BU(N_P_USER[i]);append_ZP1BU(Z_P_USER[i]) #makes array for nuclei which will have data displayed about them
                            append_P1BU(P1n_USER[i])

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
                        
                    if P2n_USER[i] != 0:
                        append_NP2CU(N_P_USER[i]);append_ZP2CU(Z_P_USER[i])

                        if Z_P_USER[i] >= Z_low_user and Z_P_USER[i] <= Z_high_user and N_P_USER[i] > N_low_user and N_P_USER[i] < N_high_user:
                            append_NP2BU(N_P_USER[i]);append_ZP2BU(Z_P_USER[i])
                            append_P2BU(P2n_USER[i])

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

                    if P3n_USER[i] != 0:
                        append_NP3CU(N_P_USER[i]);append_ZP3CU(Z_P_USER[i]) 
                        
                        if Z_P_USER[i] >= Z_low_user and Z_P_USER[i] <= Z_high_user and N_P_USER[i] > N_low_user and N_P_USER[i] < N_high_user:
                            append_NP3BU(N_P_USER[i]);append_ZP3BU(Z_P_USER[i])
                            append_P3BU(P3n_USER[i])

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

                    if Z_P_USER[i] >= Z_low_user and Z_P_USER[i] <= Z_high_user and N_P_USER[i] > N_low_user and N_P_USER[i] < N_high_user:

                        append_NELEU(N_P_USER[i])
                        append_ZELEU(Z_P_USER[i])
                        append_ELEnU(ELE_names_THEORY[i])
                        append_AELEU(N_P_USER[i]+Z_P_USER[i]) # makes all the arrays in order to display element name and mass number, A
                        
        #---------------------------------------------------------------------------

        # User Chart Choice Text (will be altered into GUI in the future)
        print "Enter 0 to plot the normal chart that highlights all dominant probability values (P1n, P2n, P3n)."
        print "Enter 1, 2, or 3 to plot only the P1n, P2n, or P3n values with a color bar gradient (0%-10%, 10%-20%,etc.). "
        plot_choice = input("Enter choice: ")

        color1='black'
        color2='Tomato'
        color3='DeepSkyBlue'
        color4='orange'
        # all variables necessary to tweak the plots for optimal viewing
        if Delta_N > 10 and Delta_Z > 10:
            msize = 9
            mew = 1.0;ms1=1
            lw1 = '0.5';lw2 = '1'
            ax1_1=0.93;ax1_2=0.1;ax1_3=0.02;ax1_4=0.8
            
        if Delta_N <= 10 and Delta_Z <= 10 and Delta_N > 7 and Delta_Z > 7:
            msize = 35
            mew = 1.5;ms1=0.2;ms2=0
            lw1 = '2.0';lw2 = '2.5'
            Cred_N = -0.3 
            Cred_Z1=-0.4;Cred_Z2=0;Cred_Z3=0.4 
            Cred_Z4=0.8;Cred_Z5=1.2;Cred_Z6=1.6
            N_ELE_adj1=0.37;Z_ELE_adj1=0.15
            fontsize_set_1=9;fontsize_set_2=9;fontsize_set_3=8
            N_adj=0.28;N_adj_r=0.28
            Z_adj_1=-0.06;Z_adj_2=-0.3
            ax1_1=0.75;ax1_2=0.1;ax1_3=0.02;ax1_4=0.8
            
        if Delta_N <= 7 and Delta_Z <= 7 and Delta_N > 4 and Delta_Z > 4:
            msize = 45
            mew = 3.0;ms1=0.2;ms2=0
            lw1 = '2.0';lw2 = '2.5'
            Cred_N = -0.2
            Cred_Z1=0.2;Cred_Z2=0.4;Cred_Z3=0.6 
            Cred_Z4=0.8;Cred_Z5=1;Cred_Z6=1.2
            N_ELE_adj1=0.3;Z_ELE_adj1=0.2
            fontsize_set_1=10;fontsize_set_2=9;fontsize_set_3=8
            N_adj=0.25;N_adj_r=0.25
            Z_adj_1=0.05;Z_adj_2=-0.1;Z_adj_3=-0.25;Z_adj_4=-0.4
            ax1_1=0.75;ax1_2=0.1;ax1_3=0.02;ax1_4=0.8
            
        if Delta_N <= 4 and Delta_Z <= 4  and Delta_N > 0 and Delta_Z > 0:
            msize = 70
            mew = 4.0;ms1=0.1;ms2=0
            lw1 = '3.0';lw2 = '3.5'
            Cred_N = -0.1 
            Cred_Z1=0.2;Cred_Z2=0.4;Cred_Z3=0.6
            Cred_Z4=0.8;Cred_Z5=1.0;Cred_Z6=1.2
            N_ELE_adj1=0.3;Z_ELE_adj1=0.3
            fontsize_set_1=12;fontsize_set_2=11;fontsize_set_3=8.5
            N_adj=0.4;N_adj_i=0;N_adj_r=0.25
            Z_adj_1=0.15;Z_adj_2=0.05;Z_adj_3=-0.05;Z_adj_4=-0.16
            ax1_1=0.75;ax1_2=0.1;ax1_3=0.02;ax1_4=0.8

        if Delta_N == 0 and Delta_Z == 0:
            msize = 200
            mew = 4.0;ms1=0.05;ms2=0
            lw1 = '3.0';lw2 = '3.5'
            Cred_N = -0.1 
            Cred_Z1=0.9;Cred_Z2=0.95;Cred_Z3=1
            Cred_Z4=1.05;Cred_Z5=1.1;Cred_Z6=1.15
            N_ELE_adj1=0.1;Z_ELE_adj1=0.3
            fontsize_set_1=20;fontsize_set_2=4;fontsize_set_3=18
            N_adj=0.1;N_adj_i=0;N_adj_r=0.25
            Z_adj_1=0.2;Z_adj_2=0.1;Z_adj_3=0;Z_adj_4=-0.1
            ax1_1=0.75;ax1_2=0.1;ax1_3=0.02;ax1_4=0.8

        # if statement which determines which Chart type will be displayed
        if plot_choice == 0:
            plt.figure(figsize=(16.5,8))
            plt.axis('scaled')
            g=plt.gca()
            plt.xlim(N_low_user,N_high_user)
            plt.ylim(Z_low_user-1,Z_high_user+1)                                               
            
            plt.xlabel("N")
            plt.ylabel("Z")

            # Credits 
            if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z1,'Produced By: Ciccone, Stephanie',fontsize=10)
                plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z2,'               TRIUMF/McMaster University',fontsize=10)
                plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z3,'Masses: AME 2012 (Wang et al.)',fontsize=10)
                plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z4,'               MOELLER(2003)',fontsize=10) 

            
            plt.title("Theoretically known beta-delayed neutron emitters")          
            leg_list = []
            c1=0;c2=0;c3=0;c4=0;c5=0;c6=0

            # plots nuclei in user bounds and stable nuclei using basic data files
            if len(N_P_Bound) != 0:
                plt.plot(N_P_Bound,Z_P_Bound,marker='s',color='0.85',markersize=msize,markeredgewidth=0,linestyle='')
                c1=1
            if len(N_Bound) != 0:
                plt.plot(N_Bound,Z_Bound,marker='s',color='0.8',markersize=msize,markeredgewidth=mew,linestyle='')
                c2=1
            if len(N_stable_Bound) != 0:
                plt.plot(N_stable_Bound,Z_stable_Bound,marker='s',color=color1,markersize=msize,markeredgewidth=0,linestyle='')
                c3=1

            # highlights nuclei with Pn values in user bounds using basic data files                                       
            if len(N_P1n_Bound) != 0:
                plt.plot(N_P1n_Bound,Z_P1n_Bound,marker='s',color=color2,markersize=msize,markeredgewidth=0,linestyle='')
                c4=1
            if len(N_P2n_Bound) != 0:
                plt.plot(N_P2n_Bound,Z_P2n_Bound,marker='s',color=color3,markersize=msize,markeredgewidth=0,linestyle='')
                c5=1
            if len(N_P3n_Bound) != 0:
                plt.plot(N_P3n_Bound,Z_P3n_Bound,marker='s',color=color4,markersize=msize,markeredgewidth=0,linestyle='')
                c6=1
            # highlights nuclei with Pn values in user bounds using user data files 
            if user_P == 1:    
                if len(N_P1n_Bound_USER) != 0:
                    plt.plot(N_P1n_Bound_USER,Z_P1n_Bound_USER,marker='s',color=color2,markersize=msize,markeredgewidth=0,linestyle='')
                if len(N_P2n_Bound_USER) != 0:
                    plt.plot(N_P2n_Bound_USER,Z_P2n_Bound_USER,marker='s',color=color3,markersize=msize,markeredgewidth=0,linestyle='')
                if len(N_P3n_Bound_USER) != 0:
                    plt.plot(N_P3n_Bound_USER,Z_P3n_Bound_USER,marker='s',color=color4,markersize=msize,markeredgewidth=0,linestyle='')

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
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+8.5,color=color1,linewidth=lw2) 
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+7.5,color=color1,linewidth=lw2)
                  
            if Z_high_user >= 20 and Z_low_user <= 20:
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+20.5,color=color1,linewidth=lw2) 
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+19.5,color=color1,linewidth=lw2)
                 
            if Z_high_user >= 28 and Z_low_user <= 28:
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+28.5,color=color1,linewidth=lw2)
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+27.5,color=color1,linewidth=lw2)             

            if Z_high_user >= 50 and Z_low_user <= 50:
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+50.5,color=color1,linewidth=lw2)
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+49.5,color=color1,linewidth=lw2)

            if Z_high_user >= 82 and Z_low_user <= 82:
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+82.5,color=color1,linewidth=lw2)
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+81.5,color=color1,linewidth=lw2)

            if Z_high_user >= 126 and Z_low_user <= 126:
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+126.5,color=color1,linewidth=lw2)
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+125.5,color=color1,linewidth=lw2)

            # outputs Element information (name, Pn values, etc.) when the user bounds are a certain size
            if (len(N_ELE) != 0 and len(ELE_name) != 0):
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0): 
                    #xyouts,N_spec-0.35,Z_spec+0.28,Special_user,charsize=1,color=color1
                    for i in xrange(0,len(N_ELE)):
                        if size_P_USER == 'none': # if no user uploaded files, only use basic data files
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

                    if len(N_P1n_Bound) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                        for i in xrange(0,len(N_P1n_Bound)):
                            if size_P_USER == 'none':
                                str_P1n="{0:.1f}".format(P1n_Bound[i])
                                plt.text(N_P1n_Bound[i]-N_adj,Z_P1n_Bound[i]+Z_adj_1,str_P1n+'%',fontsize=fontsize_set_3)
                            else:
                                for ii in xrange(0,len(N_P1n_USER)):
                                    if N_P1n_Bound[i] == N_P1n_USER[ii] and Z_P1n_Bound[i] == Z_P1n_USER[ii]:
                                        PriorityCheck = 0
                                        break
                                    else:
                                        PriorityCheck = 1
                                if PriorityCheck == 1:
                                    str_P1n="{0:.1f}".format(P1n_Bound[i])
                                    plt.text(N_P1n_Bound[i]-N_adj,Z_P1n_Bound[i]+Z_adj_1,str_P1n+'%',fontsize=fontsize_set_3)
                                    
                    if len(N_P2n_Bound) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                        for i in xrange(0,len(N_P2n_Bound)):
                            if size_P_USER == 'none':
                                str_P2n="{0:.1f}".format(P2n_Bound[i])
                                plt.text(N_P2n_Bound[i]-N_adj,Z_P2n_Bound[i]+Z_adj_2,str_P2n+'%',fontsize=fontsize_set_3)
                            else:
                                for ii in xrange(0,len(N_P2n_USER)):
                                    if N_P2n_Bound[i] == N_P2n_USER[ii] and Z_P2n_Bound[i] == Z_P2n_USER[ii]:
                                        PriorityCheck = 0
                                        break
                                    else:
                                        PriorityCheck = 1
                                if PriorityCheck == 1:
                                    str_P2n="{0:.1f}".format(P2n_Bound[i])
                                    plt.text(N_P2n_Bound[i]-N_adj,Z_P2n_Bound[i]+Z_adj_2,str_P2n+'%',fontsize=fontsize_set_3)

                    if len(N_P3n_Bound) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                        for i in xrange(0,len(N_P3n_Bound)):
                            if size_P_USER == 'none':
                                str_P3n="{0:.1f}".format(P3n_Bound[i])
                                plt.text(N_P3n_Bound[i]-N_adj,Z_P3n_Bound[i]+Z_adj_3,str_P3n+'%',fontsize=fontsize_set_3)
                            else:
                                for ii in xrange(0,len(N_P3n_USER)):
                                    if N_P3n_Bound[i] != N_P3n_USER[ii] and Z_P3n_Bound[i] != Z_P3n_USER[ii]:
                                        PriorityCheck = 1
                                    else:
                                        PriorityCheck = 0
                                        break
                                if PriorityCheck == 1:
                                    str_P3n="{0:.1f}".format(P3n_Bound[i])
                                    plt.text(N_P3n_Bound[i]-N_adj,Z_P3n_Bound[i]+Z_adj_3,str_P3n+'%',fontsize=fontsize_set_3)

            if user_P == 1: # displays all info about user uploaded data on nuclei 
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0): 
                    #xyouts,N_spec-0.35,Z_spec+0.28,Special_user,charsize=1,color=color1
                    for i in xrange(0,len(N_ELE_USER)):
                        ELE_info = ' '.join([ELE_name_USER[i].rstrip('\n'),str(int(A_ELE_USER[i]))])
                        plt.text(N_ELE_USER[i]-N_ELE_adj1,Z_ELE_USER[i]+Z_ELE_adj1,ELE_info,fontsize=fontsize_set_1)

                    if len(N_P1n_USER) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                        for i in xrange(0,len(N_P1n_USER)):
                            str_P1nU="{0:.1f}".format(P1n_USER[i])
                            plt.text(N_P1n_USER[i]-N_adj,Z_P1n_USER[i]+Z_adj_1,str_P1nU+'%',fontsize=fontsize_set_3)
                                
                    if len(N_P2n_USER) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                        for i in xrange(0,len(N_P2n_USER)):
                            str_P2nU="{0:.1f}".format(P2n_USER[i])
                            plt.text(N_P2n_USER[i]-N_adj,Z_P2n_USER[i]+Z_adj_2,str_P2nU+'%',fontsize=fontsize_set_3)

                    if len(N_P3n_USER) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                        for i in xrange(0,len(N_P3n_USER)):
                            str_P3nU="{0:.1f}".format(P3n_USER[i])
                            plt.text(N_P3n_USER[i]-N_adj,Z_P3n_USER[i]+Z_adj_3,str_P3nU+'%',fontsize=fontsize_set_3)

            # builds legend 
            if c1 == 1:
                leg_list = np.append(leg_list,leg_text[0])
            if c2 == 1:
                leg_list = np.append(leg_list,leg_text[1])
            if c3 == 1:
                leg_list = np.append(leg_list,leg_text[2])
                                                     
            if c4 == 1:
                leg_list = np.append(leg_list,leg_text[3])
            if c5 == 1:
                leg_list = np.append(leg_list,leg_text[4])
            if c6 == 1:
                leg_list = np.append(leg_list,leg_text[5])

            if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                l1 = plt.legend(leg_list,loc=2,bbox_to_anchor=[1.02,0.98],borderaxespad=0.,markerscale=ms1,numpoints=1)
                if Delta_Z <= 10 and Delta_N <= 10 and Delta_N > 7 and Delta_Z > 7:
                    l2 = plt.legend(('  Isotope  ','  P1n','  P2n'),loc=6,bbox_to_anchor=[1.02,0.4],numpoints=1,markerscale=ms2)
                    g.add_artist(l1)
                if Delta_Z <= 7 and Delta_N <= 7:
                    l2 = plt.legend(('  Isotope  ','  P1n','  P2n','  P3n'),loc=6,bbox_to_anchor=[1.02,0.4],numpoints=1,markerscale=ms2)
                    g.add_artist(l1)
            else:
                l1 = plt.legend(leg_list,loc=4,markerscale=ms1,numpoints=1)

            plt.show()
            
        if plot_choice == 1 or plot_choice == 2 or plot_choice == 3:
            fig = plt.figure(figsize=(16.5,8))

            plt.axis('scaled')
            g=plt.gca()
            plt.xlim(N_low_user,N_high_user)
            plt.ylim(Z_low_user-1,Z_high_user+1)                                               
            
            plt.xlabel("N")
            plt.ylabel("Z")

            # plots nuclei,stable nuclei, and color highlights the Pn values within user bounds using basic data files
            if len(N_P_Bound) != 0:
                plt.plot(N_P_Bound,Z_P_Bound,marker='s',color='0.85',markersize=msize,markeredgewidth=0,linestyle='')
                c1=1
            if len(N_Bound) != 0:
                plt.plot(N_Bound,Z_Bound,marker='s',color='0.8',markersize=msize,markeredgewidth=mew,linestyle='')
                c2=1
            if len(N_stable_Bound) != 0:
                plt.plot(N_stable_Bound,Z_stable_Bound,marker='s',color=color1,markersize=msize,markeredgewidth=0,linestyle='')
                c3=1
                                                     
            if len(N_P1n_Color) != 0 and plot_choice == 1:
                plt.title("Theoretically known beta-delayed neutron emitters: P1n Color Bar")
                for i in range(0,len(N_P1n_Color)):
                    plt.plot(N_P1n_Color[i],Z_P1n_Color[i],marker='s',color=P1n_Color[i],markersize=msize,markeredgewidth=0,linestyle='')
                    c4=1

            if len(N_P2n_Color) != 0 and plot_choice == 2:
                plt.title("Theoretically known beta-delayed neutron emitters: P2n Color Bar") 
                for i in range(0,len(N_P2n_Color)):
                    plt.plot(N_P2n_Color[i],Z_P2n_Color[i],marker='s',color=P2n_Color[i],markersize=msize,markeredgewidth=0,linestyle='')
                    c5=1

            if len(N_P3n_Color) != 0 and plot_choice == 3:
                plt.title("Theoretically known beta-delayed neutron emitters: P3n Color Bar")
                for i in range(0,len(N_P3n_Color)):
                    plt.plot(N_P3n_Color[i],Z_P3n_Color[i],marker='s',color=P3n_Color[i],markersize=msize,markeredgewidth=0,linestyle='')
                    c6=1
            # plots nuclei,stable nuclei, and color highlights the Pn values within user bounds using user uploaded data files
            if user_P == 1:
                if len(N_P1n_Color_USER) != 0 and plot_choice == 1:
                    plt.title("Theoretically known beta-delayed neutron emitters: P1n Color Bar")
                    for i in range(0,len(N_P1n_Color_USER)):
                        plt.plot(N_P1n_Color_USER[i],Z_P1n_Color_USER[i],marker='s',color=P1n_Color_USER[i],markersize=msize,markeredgewidth=0,linestyle='')
                        c4=1

                if len(N_P2n_Color_USER) != 0 and plot_choice == 2:
                    plt.title("Theoretically known beta-delayed neutron emitters: P2n Color Bar") 
                    for i in range(0,len(N_P2n_Color_USER)):
                        plt.plot(N_P2n_Color_USER[i],Z_P2n_Color_USER[i],marker='s',color=P2n_Color_USER[i],markersize=msize,markeredgewidth=0,linestyle='')
                        c5=1

                if len(N_P3n_Color_USER) != 0 and plot_choice == 3:
                    plt.title("Theoretically known beta-delayed neutron emitters: P3n Color Bar")
                    for i in range(0,len(N_P3n_Color_USER)):
                        plt.plot(N_P3n_Color_USER[i],Z_P3n_Color_USER[i],marker='s',color=P3n_Color_USER[i],markersize=msize,markeredgewidth=0,linestyle='')
                        c6=1

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
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+8.5,color=color1,linewidth=lw2) 
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+7.5,color=color1,linewidth=lw2)
                  
            if Z_high_user >= 20 and Z_low_user <= 20:
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+20.5,color=color1,linewidth=lw2) 
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+19.5,color=color1,linewidth=lw2)
                 
            if Z_high_user >= 28 and Z_low_user <= 28:
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+28.5,color=color1,linewidth=lw2)
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+27.5,color=color1,linewidth=lw2)             

            if Z_high_user >= 50 and Z_low_user <= 50:
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+50.5,color=color1,linewidth=lw2)
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+49.5,color=color1,linewidth=lw2)

            if Z_high_user >= 82 and Z_low_user <= 82:
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+82.5,color=color1,linewidth=lw2)
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+81.5,color=color1,linewidth=lw2)

            if Z_high_user >= 126 and Z_low_user <= 126:
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+126.5,color=color1,linewidth=lw2)
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+125.5,color=color1,linewidth=lw2)

            # outputs color bar
            ax1 = fig.add_axes([ax1_1,ax1_2,ax1_3,ax1_4])
            
            cmap = mpl.colors.ListedColormap(['yellow','orange','red','maroon','lime','green','DeepSkyBlue','blue','violet','purple'])
            bounds = [0,10,20,30,40,50,60,70,80,90,100]
            norm = mpl.colors.BoundaryNorm(bounds,cmap.N)
            cb1 = mpl.colorbar.ColorbarBase(ax1,cmap=cmap,norm=norm,boundaries=bounds,ticks=bounds,orientation='vertical')
            cb1.set_label('Beta-Delayed Neutron Emission Probability')

            plt.show()
            
        r=input("If r = 1, program will stop. If r = 0, program continues. Enter r: ")
#------------------------------------------------------------------------------------------------------------

def main():

    # will be altered to GUI in future
    choice_user = 0
    choice_user = input("Enter any number to display the experimental version; Enter 2 to display the theoretical version: ")

    # determines if running on a Windows or a Unix machine and yields the required directory deliminator
    if os.name == "nt":
        dirDelim = "\\"
    else:
        dirDelim = "/"

    if choice_user == 2:
        MOELLER() # runs theoretical MOELLER version
    else:
        #reads in values from text files and stores all of the data columns into arrays
        filename_ENSDF = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "ChartNuclides_DataTable_ENSDF.txt"

        print ""
        print "If you wish to include additional data, you can enter your data file name below. Data files must be in the format shown!"
        print "---------- HEADER COLUMN TITLES ----------"
        print "-- N -- Z -- P1n -- P2n -- P3n -- P4n -- Nuclei Name --"
        print "------------ OR ------------"
        print "-- N -- Z -- P1n -- P2n -- P3n -- P4n -- Qbn -- Qb2n -- Qb3n -- Qb4n -- Nuclei Name --"
        print "------------ OR ------------"
        print "-- N -- Z -- P1n -- P2n -- P3n -- P4n -- Qbn -- Qb2n -- Qb3n -- Qb4n -- P1n_iso1 -- P2n_iso1 -- P1n_iso2 -- P2n_iso2 -- Nuclei Name --"
        print "------------ OR ------------"
        print "-- N -- Z -- P1n -- P2n -- P3n -- P4n -- Qbn -- Qb2n -- Qb3n -- Qb4n -- Ratio1n -- Ratio2n -- Ratio3n -- Ratio4n -- Nuclei Name -- THEORY Source for Ratio --" 
        print ""

        user_R = 0 ; user_P = 0 ; user_Q = 0 ; user_i = 0
        USER_filename = input("Enter 'pass' to skip. Enter the name of your own data file in ' ': ")
        while USER_filename != 'pass':
            filename_EXP_USER = os.getcwd() + dirDelim + "Text_Files" + dirDelim + USER_filename

            # checks # of columns in uploaded data files
            with open(filename_EXP_USER) as ColCheck:
                reader = csv.reader(ColCheck,delimiter='\t',skipinitialspace=True)
                first_row = next(reader)
                ncol = len(first_row)
            print ncol

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
            if ncol == 16:
                ELE_names_USER = np.genfromtxt(filename_EXP_USER,skip_header=1,usecols=(14),dtype=str,unpack=True)
                N_USER,Z_USER,P1n_USER,P2n_USER,P3n_USER,P4n_USER = np.loadtxt(filename_EXP_USER,skiprows=1,usecols=(0,1,2,3,4,5),unpack=True)
                size_P_USER = len(N_USER)
                Qbn_USER,Qb2n_USER,Qb3n_USER,Qb4n_USER = np.loadtxt(filename_EXP_USER,skiprows=1,usecols=(6,7,8,9),unpack=True)
                size_Q_USER = len(Qbn_USER)
                
                R1n_USER,R2n_USER,R3n_USER,R4n_USER = np.loadtxt(filename_EXP_USER,skiprows=1,usecols=(10,11,12,13),unpack=True)
                size_R_USER = len(R1n_USER);user_R = 1
                
            USER_filename = input("Enter 'pass' to skip. Enter the name of your own data file in '': ")
            
        N_stable,Z_stable = np.loadtxt(filename_ENSDF,skiprows=1,usecols=(0, 1),unpack=True)
        s2 = len(N_stable)
        
        N,Z = np.loadtxt(filename_ENSDF,skiprows=1,usecols=(2, 3),unpack=True)
        s1 = len(N)

        Qbn,Qb2n,Qb3n,Qb4n = np.loadtxt(filename_ENSDF,skiprows=1,usecols=(4, 5, 6, 7),unpack=True)
        
        ELE_names_EXP = np.genfromtxt(filename_ENSDF,skip_header=1,usecols=(8),dtype=str,unpack=True)
        N_P,Z_P,P1n,P2n,P3n,P4n = np.loadtxt(filename_ENSDF,skiprows=1,usecols=(9, 10, 11, 12, 13, 14),unpack=True)
        size_P = len(N_P)

        N_P_iso1,Z_P_iso1,P1n_iso1,P2n_iso1,P3n_iso1,P4n_iso1,N_P_iso2,Z_P_iso2,P1n_iso2,P2n_iso2,P3n_iso2,P4n_iso2 = np.loadtxt(filename_ENSDF,skiprows=1,usecols=(15,16,17,18,19,20,21,22,23,24,25,26),unpack=True)
        size_P_iso1 = len(N_P_iso1);size_P_iso2 = len(N_P_iso2)

        filename_MOE = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "ChartNuclides_DataTable_MOELLER.txt"

        N_P_MOE,Z_P_MOE,P1n_MOE_full,P2n_MOE_full,P3n_MOE_full = np.loadtxt(filename_MOE,skiprows=1,usecols=(4, 5, 6, 7, 8),unpack=True)
        size_P_MOE = len(N_P_MOE)

        P1n_MOE = []; append_P1nMOE = P1n_MOE.append
        P2n_MOE = []; append_P2nMOE = P2n_MOE.append
        P3n_MOE = []; append_P3nMOE = P3n_MOE.append

        # forms array of MOELLER Pn values that correspond to the EXP Pn values in the basic data files
        for i in xrange(0,size_P_MOE):
            for ii in xrange(0,size_P):
                if N_P_MOE[i] == N_P[ii] and Z_P_MOE[i] == Z_P[ii]:
                    append_P1nMOE(P1n_MOE_full[i])
                    append_P2nMOE(P2n_MOE_full[i])
                    append_P3nMOE(P3n_MOE_full[i])
    #----------------------------------------------------------------------------

        # list of text in order to properly set up the legend and special symbols
        Special_sym = ['<','>','ca.','?']
        leg_text = ['Known','Stable','Q(b1n) > 0 keV','Q(b2n) > 0 keV','Q(b3n) > 0 keV','Q(b4n) > 0 keV','Measured P(1n)','Measured P(2n)','Measured P(3n)','Measured P(4n)']

    #----------------------------------------------------------------------------

        r = 0
        while r != 1:

            N_low_user = 0;N_high_user = 0
            Z_low_user = 0;Z_high_user = 0
            ratio_user = 0

            # intro text and input (will be altered into GUI in the future)
            print "--------------------------------------------------"
            print "Welcome to the Chart of Nuclides Output Program - ENSDF Edition."
            print ""
            print "The Chart will zoom in and display P values of the measured, known emitters only if the user inputs: "
            print " 1. An N range with a difference equal to 0 and a Z range with a difference equal to 0."
            print " 2. An N range with a difference equal to 4 and a Z range with a difference equal to 4."
            print " 3. An N range with a difference equal to 7 and a Z range with a difference equal to 7."
            print " 4. An N range with a difference equal to 10 and a Z range with a difference equal to 10."
            print "The Chart will output normally if BOTH ranges are different to these limits."
            print "You also have the option to display the ratio difference between the experimentally known and theoretically known emitters."
            print "It is recommended to input exact differences following Options 1 to 4 above for optimal viewing results."
            print ""
            print "---------------------------------------------------"
            print ""

            N_low_user=input("Enter the integer value for the minimum of the N range: ")
            N_high_user=input("Enter the integer value for the maximum of the N range: ") 
            Z_low_user=input("Enter the integer value for the minimum of the Z range: ")
            Z_high_user=input("Enter the integer value for the maximum of the Z range: ")

            Delta_N = N_high_user - N_low_user
            Delta_Z = Z_high_user - Z_low_user

            # choice to display ratio info instead
            if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                ratio_user=input("Enter 1 to display the ratio difference instead-(P exp.)/(P theory). Enter anything else to proceed without the ratio: ")

            N_high_user=N_high_user+1
            N_low_user=N_low_user-1

            print "Analyzing Data Tables and Building Chart Arrays..."
    #-----------------------------------------------------------------------------

            N_Bound = [];Z_Bound = []
            N_Bound_magic = [];Z_Bound_magic = []

            N_Qbn_Bound = [];Z_Qbn_Bound = []
            N_Qb2n_Bound = [];Z_Qb2n_Bound = []
            N_Qb3n_Bound = [];Z_Qb3n_Bound = []
            N_Qb4n_Bound = [];Z_Qb4n_Bound = []

            if user_Q == 1 or user_i == 1 or user_R == 1:
                N_Qbn_Bound_USER = [];Z_Qbn_Bound_USER = []
                N_Qb2n_Bound_USER = [];Z_Qb2n_Bound_USER = []
                N_Qb3n_Bound_USER = [];Z_Qb3n_Bound_USER = []
                N_Qb4n_Bound_USER = [];Z_Qb4n_Bound_USER = []

            # for loop that assigns the values of N and Z to each array within user bounds using the basic data files
            for i in xrange(0,s1):
                if Z[i] >= Z_low_user and Z[i] <= Z_high_user and N[i] >= N_low_user and N[i] <= N_high_user: 
                    N_Bound = np.append(N_Bound,N[i])
                    Z_Bound = np.append(Z_Bound,Z[i])
      
                if Z[i] >= 0 and Z[i] <= Z_high_user+1:
                    Z_Bound_magic = np.append(Z_Bound_magic,Z[i])
                    N_Bound_magic = np.append(N_Bound_magic,N[i])

                # for loop that assigns N and Z values to the arrays only if the isotopes have a Qbn greater than 0 and the Qbn value is not equal to '1010'
                #(a random number denoting isotopes with unknown Qbn values) at that N and Z value using the basic data files

                if Z[i] >= Z_low_user and Z[i] <= Z_high_user and N[i] >= N_low_user and N[i] <= N_high_user and Qbn[i] > 0 and Qbn[i] != 1010: 
                    N_Qbn_Bound = np.append(N_Qbn_Bound,N[i])
                    Z_Qbn_Bound = np.append(Z_Qbn_Bound,Z[i])

                if Z[i] >= Z_low_user and Z[i] <= Z_high_user and N[i] >= N_low_user and N[i] <= N_high_user and Qb2n[i] > 0 and Qb2n[i] != 1010: 
                    N_Qb2n_Bound = np.append(N_Qb2n_Bound,N[i])
                    Z_Qb2n_Bound = np.append(Z_Qb2n_Bound,Z[i])

                if Z[i] >= Z_low_user and Z[i] <= Z_high_user and N[i] >= N_low_user and N[i] <= N_high_user and Qb3n[i] > 0 and Qb3n[i] != 1010:  
                    N_Qb3n_Bound = np.append(N_Qb3n_Bound,N[i])
                    Z_Qb3n_Bound = np.append(Z_Qb3n_Bound,Z[i])

                if Z[i] >= Z_low_user and Z[i] <= Z_high_user and N[i] >= N_low_user and N[i] <= N_high_user and Qb4n[i] > 0 and Qb4n[i] != 1010:  
                    N_Qb4n_Bound = np.append(N_Qb4n_Bound,N[i]) 
                    Z_Qb4n_Bound = np.append(Z_Qb4n_Bound,Z[i])

            # for loop that assigns N and Z values to the arrays only if the isotopes have a Qbn greater than 0 using user files
            if user_Q == 1 or user_i == 1 or user_R == 1:
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
            N_stable_Bound = [];Z_stable_Bound = []

            for i in xrange(0,s2):
                if Z_stable[i] >= Z_low_user and Z_stable[i] <= Z_high_user and N_stable[i] >= N_low_user and N_stable[i] <= N_high_user:
                    N_stable_Bound = np.append(N_stable_Bound,N_stable[i])
                    Z_stable_Bound = np.append(Z_stable_Bound,Z_stable[i])
    #----------------------------------------------------------------------------

            # assigns the N and Z values of the isotopes with probability > 0
            N_P1n_Bound = [];Z_P1n_Bound = []
            N_P1n_Bound_value = [];Z_P1n_Bound_value = []
            P1n_Bound = []

            P1n_ratio = []
            N_P1n_ratio = [];Z_P1n_ratio = []

            N_P2n_Bound = [];Z_P2n_Bound = []     
            N_P2n_Bound_value = [];Z_P2n_Bound_value = []
            P2n_Bound = []

            P2n_ratio = []
            N_P2n_ratio = [];Z_P2n_ratio = []

            N_P3n_Bound = [];Z_P3n_Bound = []
            N_P3n_Bound_value = [];Z_P3n_Bound_value = []
            P3n_Bound = []

            P3n_ratio = []
            N_P3n_ratio = [];Z_P3n_ratio = []

            N_P4n_Bound = [];Z_P4n_Bound = []
            N_P4n_Bound_value = [];Z_P4n_Bound_value = []
            P4n_Bound = []

            P4n_ratio = []
            N_P4n_ratio = [];Z_P4n_ratio = []

            ELE_name = []
            N_ELE = [];Z_ELE = [];A_ELE = []

            Special_user = []
            N_spec = [];Z_spec = []

            N_P1n_Bound_iso1 = [];Z_P1n_Bound_iso1 = []
            N_P2n_Bound_iso1 = [];Z_P2n_Bound_iso1 = []
            P1n_Bound_iso1 = [];P2n_Bound_iso1 = []

            N_P1n_Bound_iso2 = [];Z_P1n_Bound_iso2 = []
            N_P2n_Bound_iso2 = [];Z_P2n_Bound_iso2 = []
            P1n_Bound_iso2 = [];P2n_Bound_iso2 = []

            if user_P == 1 or user_Q == 1 or user_i == 1 or user_R == 1:
                N_P1n_Bound_USER = [];Z_P1n_Bound_USER = []
                N_P1n_Bound_USER_value = [];Z_P1n_Bound_USER_value = []
                P1n_Bound_USER = []

                N_P2n_Bound_USER = [];Z_P2n_Bound_USER = []
                N_P2n_Bound_USER_value = [];Z_P2n_Bound_USER_value = []
                P2n_Bound_USER = []

                N_P3n_Bound_USER = [];Z_P3n_Bound_USER = []
                N_P3n_Bound_USER_value = [];Z_P3n_Bound_USER_value = []
                P3n_Bound_USER = []

                N_P4n_Bound_USER = [];Z_P4n_Bound_USER = []
                N_P4n_Bound_USER_value = [];Z_P4n_Bound_USER_value = []
                P4n_Bound_USER = []

                ELE_name_USER = []
                N_ELE_USER = [];Z_ELE_USER = [];A_ELE_USER = []

            if user_i == 1:
                N_P1n_Bound_USER_iso1 = [];Z_P1n_Bound_USER_iso1 = []
                N_P2n_Bound_USER_iso1 = [];Z_P2n_Bound_USER_iso1 = []
                P1n_Bound_USER_iso1 = [];P2n_Bound_USER_iso1 = []
                N_P1n_Bound_USER_iso2 = [];Z_P1n_Bound_USER_iso2 = []
                N_P2n_Bound_USER_iso2 = [];Z_P2n_Bound_USER_iso2 = []
                P1n_Bound_USER_iso2 = [];P2n_Bound_USER_iso2 = []

            # sets arrays for the nuclei with Pn values within user bounds using the basic data files
            for i in xrange(0,size_P):
                if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user:
                    if P1n[i] != 0: 
                        N_P1n_Bound = np.append(N_P1n_Bound,N_P[i]) 
                        Z_P1n_Bound = np.append(Z_P1n_Bound,Z_P[i])

                        if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                            N_P1n_Bound_value = np.append(N_P1n_Bound_value,N_P[i])
                            Z_P1n_Bound_value = np.append(Z_P1n_Bound_value,Z_P[i])
                            P1n_Bound = np.append(P1n_Bound,P1n[i])
                            if P1n_MOE[i] != 0:
                                ratio = P1n[i]/P1n_MOE[i]
                                P1n_ratio = np.append(P1n_ratio,ratio)
                                N_P1n_ratio=np.append(N_P1n_ratio,N_P[i]) 
                                Z_P1n_ratio=np.append(Z_P1n_ratio,Z_P[i])

                    if P2n[i] != 0: 
                        N_P2n_Bound = np.append(N_P2n_Bound,N_P[i])
                        Z_P2n_Bound = np.append(Z_P2n_Bound,Z_P[i])

                        if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                            N_P2n_Bound_value = np.append(N_P2n_Bound_value,N_P[i])
                            Z_P2n_Bound_value = np.append(Z_P2n_Bound_value,Z_P[i])
                            P2n_Bound = np.append(P2n_Bound,P2n[i])
                            if P2n_MOE[i] != 0:
                                ratio=P2n[i]/P2n_MOE[i]
                                P2n_ratio=np.append(P2n_ratio,ratio)
                                N_P2n_ratio=np.append(N_P2n_ratio,N_P[i])
                                Z_P2n_ratio=np.append(Z_P2n_ratio,Z_P[i])

                    if P3n[i] != 0: 
                        N_P3n_Bound = np.append(N_P3n_Bound,N_P[i])
                        Z_P3n_Bound = np.append(Z_P3n_Bound,Z_P[i])

                        if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                            N_P3n_Bound_value = np.append(N_P3n_Bound_value,N_P[i])
                            Z_P3n_Bound_value = np.append(Z_P3n_Bound_value,Z_P[i])
                            P3n_Bound = np.append(P3n_Bound,P3n[i]) 
                            if P3n_MOE[i] != 0:
                                ratio=P3n[i]/P3n_MOE[i]
                                P3n_ratio=np.append(P3n_ratio,ratio)
                                N_P3n_ratio=np.append(N_P3n_ratio,N_P[i])
                                Z_P3n_ratio=np.append(Z_P3n_ratio,Z_P[i])

                    if P4n[i] != 0: 
                        N_P4n_Bound = np.append(N_P4n_Bound,N_P[i])
                        Z_P4n_Bound = np.append(Z_P4n_Bound,Z_P[i])

                        if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                            N_P4n_Bound_value = np.append(N_P4n_Bound_value,N_P[i])
                            Z_P4n_Bound_value = np.append(Z_P4n_Bound_value,Z_P[i])
                            P4n_Bound = np.append(P4n_Bound,P4n[i])
                        
                if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user and (P1n[i] != 0 or P2n[i] != 0 or P3n[i] != 0 or P4n[i] != 0): 

                    N_ELE = np.append(N_ELE,N_P[i])
                    Z_ELE = np.append(Z_ELE,Z_P[i])
                    A_calc = N_P[i] + Z_P[i]
                    ELE_name = np.append(ELE_name,ELE_names_EXP[i])
                    A_ELE = np.append(A_ELE,A_calc)

            # sets arrays for the nuclei with Pn values within user bounds using the user data files
            if user_P == 1 or user_Q == 1 or user_i == 1 or user_R == 1:
                for i in xrange(0,size_P_USER):
                    if Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user:
                        if P1n_USER[i] != 0: 
                            N_P1n_Bound_USER = np.append(N_P1n_Bound_USER,N_USER[i]) 
                            Z_P1n_Bound_USER = np.append(Z_P1n_Bound_USER,Z_USER[i])

                            if Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user:
                                N_P1n_Bound_USER_value = np.append(N_P1n_Bound_USER_value,N_USER[i])
                                Z_P1n_Bound_USER_value = np.append(Z_P1n_Bound_USER_value,Z_USER[i])
                                P1n_Bound_USER = np.append(P1n_Bound_USER,P1n_USER[i])

                        if P2n_USER[i] != 0: 
                            N_P2n_Bound_USER = np.append(N_P2n_Bound_USER,N_USER[i])
                            Z_P2n_Bound_USER = np.append(Z_P2n_Bound_USER,Z_USER[i])

                            if Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user:
                                N_P2n_Bound_USER_value = np.append(N_P2n_Bound_USER_value,N_USER[i])
                                Z_P2n_Bound_USER_value = np.append(Z_P2n_Bound_USER_value,Z_USER[i])
                                P2n_Bound_USER = np.append(P2n_Bound_USER,P2n_USER[i])

                        if P3n_USER[i] != 0: 
                            N_P3n_Bound_USER = np.append(N_P3n_Bound_USER,N_USER[i])
                            Z_P3n_Bound_USER = np.append(Z_P3n_Bound_USER,Z_USER[i])

                            if Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user:
                                N_P3n_Bound_USER_value = np.append(N_P3n_Bound_USER_value,N_USER[i])
                                Z_P3n_Bound_USER_value = np.append(Z_P3n_Bound_USER_value,Z_USER[i])
                                P3n_Bound_USER = np.append(P3n_Bound_USER,P3n_USER[i]) 

                        if P4n_USER[i] != 0: 
                            N_P4n_Bound_USER = np.append(N_P4n_Bound_USER,N_USER[i])
                            Z_P4n_Bound_USER = np.append(Z_P4n_Bound_USER,Z_USER[i])

                            if Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user:
                                N_P4n_Bound_USER_value = np.append(N_P4n_Bound_USER_value,N_USER[i])
                                Z_P4n_Bound_USER_value = np.append(Z_P4n_Bound_USER_value,Z_USER[i])
                                P4n_Bound_USER = np.append(P4n_Bound_USER,P4n_USER[i])
                            
                    if Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user and (P1n_USER[i] != 0 or P2n_USER[i] != 0 or P3n_USER[i] != 0 or P4n_USER[i] != 0): 

                        N_ELE_USER= np.append(N_ELE_USER,N_USER[i])
                        Z_ELE_USER = np.append(Z_ELE_USER,Z_USER[i])
                        A_calc_USER = N_USER[i] + Z_USER[i]
                        ELE_name_USER = np.append(ELE_name_USER,ELE_names_USER[i])
                        A_ELE_USER = np.append(A_ELE_USER,A_calc_USER)

##                    if Special[i] == 1: 
##                        Special_user = np.append(Special_user,Special_sym[0])
##                        N_spec = np.append(N_spec,N_P[i])
##                        Z_spec = np.append(Z_spec,Z_P[i])
##
##                    if Special[i] == 2: 
##                        Special_user = np.append(Special_user,Special_sym[1])
##                        N_spec = np.append(N_spec,N_P[i])
##                        Z_spec = np.append(Z_spec,Z_P[i])
##      
##                    if Special[i] == 3: 
##                        Special_user = np.append(Special_user,Special_sym[2])
##                        N_spec = np.append(N_spec,N_P[i])
##                        Z_spec = np.append(Z_spec,Z_P[i])
##
##                    if Special[i] == 4:
##                         Special_user = np.append(Special_user,Special_sym[3])
##                         N_spec = np.append(N_spec,N_P[i])
##                         Z_spec = np.append(Z_spec,Z_P[i])

            for i in xrange(0,size_P_iso1): 
                if Z_P_iso1[i] >= Z_low_user and Z_P_iso1[i] <= Z_high_user and N_P_iso1[i] > N_low_user and N_P_iso1[i] < N_high_user:
                    if P1n_iso1[i] != 0:
                        N_P1n_Bound_iso1 = np.append(N_P1n_Bound_iso1,N_P_iso1[i]) 
                        Z_P1n_Bound_iso1 = np.append(Z_P1n_Bound_iso1,Z_P_iso1[i])
                        P1n_Bound_iso1 = np.append(P1n_Bound_iso1,P1n_iso1[i])

                    if P2n_iso1[i] != 0: 
                        N_P2n_Bound_iso1 = np.append(N_P2n_Bound_iso1,N_P_iso1[i])
                        Z_P2n_Bound_iso1 = np.append(Z_P2n_Bound_iso1,Z_P_iso1[i])
                        P2n_Bound_iso1 = np.append(P2n_Bound_iso1,P2n_iso1[i])

            for i in xrange(0,size_P_iso2):
                if Z_P_iso2[i] >= Z_low_user and Z_P_iso2[i] <= Z_high_user and N_P_iso2[i] > N_low_user and N_P_iso2[i] < N_high_user:
                    if P1n_iso2[i] != 0:
                        N_P1n_Bound_iso2 = np.append(N_P1n_Bound_iso2,N_P_iso2[i])
                        Z_P1n_Bound_iso2 = np.append(Z_P1n_Bound_iso2,Z_P_iso2[i])
                        P1n_Bound_iso2 = np.append(P1n_Bound_iso2,P1n_iso2_USER[i])

                    if P2n_iso2[i] != 0: 
                        N_P2n_Bound_iso2 = np.append(N_P2n_Bound_iso2,N_P_iso2[i])
                        Z_P2n_Bound_iso2 = np.append(Z_P2n_Bound_iso2,Z_P_iso2[i])
                        P2n_Bound_iso2 = np.append(P2n_Bound_iso2,P2n_iso2[i])

            if user_i == 1:
                for i in xrange(0,size_iso_USER): 
                    if Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user:
                        if P1n_iso1_USER[i] != 0:
                            N_P1n_Bound_USER_iso1 = np.append(N_P1n_Bound_USER_iso1,N_USER[i]) 
                            Z_P1n_Bound_USER_iso1 = np.append(Z_P1n_Bound_USER_iso1,Z_USER[i])
                            P1n_Bound_USER_iso1 = np.append(P1n_Bound_USER_iso1,P1n_iso1_USER[i])

                        if P2n_iso1_USER[i] != 0: 
                            N_P2n_Bound_USER_iso1 = np.append(N_P2n_Bound_USER_iso1,N_USER[i])
                            Z_P2n_Bound_USER_iso1 = np.append(Z_P2n_Bound_USER_iso1,Z_USER[i])
                            P2n_Bound_USER_iso1 = np.append(P2n_Bound_USER_iso1,P2n_iso1_USER[i])

                for i in xrange(0,size_iso_USER):
                    if Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user:
                        if P1n_iso2_USER[i] != 0:
                            N_P1n_Bound_USER_iso2 = np.append(N_P1n_Bound_USER_iso2,N_USER[i])
                            Z_P1n_Bound_USER_iso2 = np.append(Z_P1n_Bound_USER_iso2,Z_USER[i])
                            P1n_Bound_USER_iso2 = np.append(P1n_Bound_USER_iso2,P1n_iso2_USER[i])

                        if P2n_iso2_USER[i] != 0: 
                            N_P2n_Bound_USER_iso2 = np.append(N_P2n_Bound_USER_iso2,N_USER[i])
                            Z_P2n_Bound_USER_iso2 = np.append(Z_P2n_Bound_USER_iso2,Z_USER[i])
                            P2n_Bound_USER_iso2 = np.append(P2n_Bound_USER_iso2,P2n_iso2_USER[i])
    #----------------------------------------------------------------------------

            # builds the chart that will be displayed
            color1='black'
            color2='Tomato'
            color3='DeepSkyBlue'
            color4='orange'
            color5='IndianRed'
            color6='Lime'
            color7='Red'
            color8='Magenta'
            leg_list = []
            c1=0;c2=0;c3=0;c4=0;c5=0
            c6=0;c7=0;c8=0;c9=0;c10=0

            plt.figure(figsize=(16.5,8))

            # declares all necessary variables that tweak the chart for optimal viewing
            if Delta_N > 10 and Delta_Z > 10:
                msize = 9
                mew = 2.0;ms1=1
                lw1 = '0.5';lw2 = '1'
                Cred_N = -0.3
                Cred_Z1=-0.8;Cred_Z2=0;Cred_Z3=0.8 
                Cred_Z4=1.6;Cred_Z5=2.4;Cred_Z6=3.2
                
            if Delta_N <= 10 and Delta_Z <= 10  and Delta_Z > 7 and Delta_Z > 7:
                msize = 35
                mew = 3.0;ms1=0.2;ms2=0
                lw1 = '2.0';lw2 = '2.5'
                Cred_N = -0.3 
                Cred_Z1=-0.3;Cred_Z2=0;Cred_Z3=0.3 
                Cred_Z4=0.6;Cred_Z5=0.9;Cred_Z6=1.2
                N_ELE_adj1=0.37;Z_ELE_adj1=0.15
                fontsize_set_1=9;fontsize_set_2=9;fontsize_set_3=8
                N_adj=0.34;N_adj_r=0.28
                Z_adj_1=-0.06;Z_adj_2=-0.3
                
            if Delta_N <= 7 and Delta_Z <= 7 and Delta_Z > 4 and Delta_Z > 4:
                msize = 45
                mew = 4.0;ms1=0.2;ms2=0
                lw1 = '2.0';lw2 = '2.5'
                Cred_N = -0.2
                Cred_Z1=0.2;Cred_Z2=0.4;Cred_Z3=0.6 
                Cred_Z4=0.8;Cred_Z5=1;Cred_Z6=1.2
                N_ELE_adj1=0.3;Z_ELE_adj1=0.2
                fontsize_set_1=10;fontsize_set_2=9;fontsize_set_3=8
                N_adj=0.25;N_adj_r=0.25
                Z_adj_1=0.05;Z_adj_2=-0.1;Z_adj_3=-0.25;Z_adj_4=-0.4
                
            if Delta_N <= 4 and Delta_Z <= 4:
                msize = 70
                mew = 5.0;ms1=0.1;ms2=0
                lw1 = '3.0';lw2 = '3.5'
                Cred_N = -0.15 
                Cred_Z1=0.2;Cred_Z2=0.35;Cred_Z3=0.5
                Cred_Z4=0.65;Cred_Z5=0.8;Cred_Z6=0.95
                N_ELE_adj1=0.3;Z_ELE_adj1=0.28
                fontsize_set_1=12;fontsize_set_2=11;fontsize_set_3=8.5
                N_adj=0.4;N_adj_i=0;N_adj_r=0.25
                Z_adj_1=0.15;Z_adj_2=0.05;Z_adj_3=-0.05;Z_adj_4=-0.16

            if Delta_N == 0 and Delta_Z == 0:
                msize = 200
                mew = 5.0;ms1=0.05;ms2=0
                lw1 = '3.0';lw2 = '3.5'
                Cred_N = -0.1 
                Cred_Z1=0.9;Cred_Z2=0.95;Cred_Z3=1
                Cred_Z4=1.05;Cred_Z5=1.1;Cred_Z6=1.15
                N_ELE_adj1=0.1;Z_ELE_adj1=0.3
                fontsize_set_1=20;fontsize_set_2=18;fontsize_set_3=18
                N_adj=0.3;N_adj_i=0;N_adj_r=0.1
                Z_adj_1=0.2;Z_adj_2=0.1;Z_adj_3=0;Z_adj_4=-0.1
                ax1_1=0.75;ax1_2=0.1;ax1_3=0.02;ax1_4=0.8

            if len(N_Bound) != 0:
                plt.plot(N_Bound,Z_Bound,marker='s',color='0.8',markersize=msize,linestyle='')
                c1=1
            if len(N_stable_Bound) != 0:
                plt.plot(N_stable_Bound,Z_stable_Bound,marker='s',color=color1,markersize=msize,linestyle='')
                c2=1

            if len(N_Qbn_Bound) != 0:
                plt.plot(N_Qbn_Bound,Z_Qbn_Bound,marker='s',color=color2,markersize=msize,linestyle='')
                c3=1
            if len(N_Qb2n_Bound) != 0:
                plt.plot(N_Qb2n_Bound,Z_Qb2n_Bound,marker='s',color=color3,markersize=msize,linestyle='')
                c4=1   
            if len(N_Qb3n_Bound) != 0:
                plt.plot(N_Qb3n_Bound,Z_Qb3n_Bound,marker='s',color=color4,markersize=msize,linestyle='')
                c5=1
            if len(N_Qb4n_Bound) != 0:
                plt.plot(N_Qb4n_Bound,Z_Qb4n_Bound,marker='s',color=color5,markersize=msize,linestyle='')
                c6=1

            if len(N_P1n_Bound) != 0:
                plt.plot(N_P1n_Bound,Z_P1n_Bound,marker='s',color=color1,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')
                c7=1
            if len(N_P2n_Bound) != 0:
                plt.plot(N_P2n_Bound,Z_P2n_Bound,marker='s',color=color6,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')
                c8=1
            if len(N_P3n_Bound) != 0:
                plt.plot(N_P3n_Bound,Z_P3n_Bound,marker='s',color=color7,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')
                c9=1
            if len(N_P4n_Bound) != 0:
                plt.plot(N_P4n_Bound,Z_P4n_Bound,marker='s',color=color8,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')
                c10=1
                
            if user_Q == 1 or user_i == 1 or user_R ==1:
                if len(N_Qbn_Bound_USER) != 0:
                    plt.plot(N_Qbn_Bound_USER,Z_Qbn_Bound_USER,marker='s',color=color2,markersize=msize,linestyle='')
                    c3=1
                if len(N_Qb2n_Bound_USER) != 0:
                    plt.plot(N_Qb2n_Bound_USER,Z_Qb2n_Bound_USER,marker='s',color=color3,markersize=msize,linestyle='')
                    c4=1   
                if len(N_Qb3n_Bound_USER) != 0:
                    plt.plot(N_Qb3n_Bound_USER,Z_Qb3n_Bound_USER,marker='s',color=color4,markersize=msize,linestyle='')
                    c5=1
                if len(N_Qb4n_Bound_USER) != 0:
                    plt.plot(N_Qb4n_Bound_USER,Z_Qb4n_Bound_USER,marker='s',color=color5,markersize=msize,linestyle='')
                    c6=1
                
            if user_P == 1 or user_Q == 1 or user_i == 1 or user_R == 1:
                if len(N_P1n_Bound_USER) != 0:
                    plt.plot(N_P1n_Bound_USER,Z_P1n_Bound_USER,marker='s',color=color1,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')
                    c7=1
                if len(N_P2n_Bound_USER) != 0:
                    plt.plot(N_P2n_Bound_USER,Z_P2n_Bound_USER,marker='s',color=color6,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')
                    c8=1
                if len(N_P3n_Bound_USER) != 0:
                    plt.plot(N_P3n_Bound_USER,Z_P3n_Bound_USER,marker='s',color=color7,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')
                    c9=1
                if len(N_P4n_Bound_USER) != 0:
                    plt.plot(N_P4n_Bound_USER,Z_P4n_Bound_USER,marker='s',color=color8,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')
                    c10=1               

            if len(N_ELE) != 0 and len(ELE_name) != 0:
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    #xyouts,N_spec-0.35,Z_spec+0.28,Special_user,charsize=1,color=color1
                    for i in xrange(0,len(N_ELE)):
                        if user_P != 1 or user_Q != 1 or user_i != 1 or user_R != 1:
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

            if user_P == 1 or user_Q == 1 or user_i == 1 or user_R == 1:
                if len(N_USER) != 0 and len(ELE_name_USER) != 0 and (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    for i in xrange(0,len(N_ELE_USER)):
                        ELE_info = ' '.join([ELE_name_USER[i].rstrip('\n'),str(int(A_ELE_USER[i]))])
                        plt.text(N_ELE_USER[i]-N_ELE_adj1,Z_ELE_USER[i]+Z_ELE_adj1,ELE_info,fontsize=fontsize_set_1)

            if ratio_user == 1:
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    if len(N_P1n_ratio) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                        for i in xrange(0,len(N_P1n_ratio)):
                            if user_R != 1:
                                str_ratio="{0:.1f}".format(P1n_ratio[i])
                                plt.text(N_P1n_ratio[i]-N_adj_r,Z_P1n_ratio[i]+Z_adj_1,str_ratio,fontsize=fontsize_set_2)
                            else:
                                for ii in xrange(0,len(N_USER)):
                                    if N_P1n_ratio[i] == N_USER[ii] and Z_P1n_ratio[i] == Z_USER[ii]:
                                        PriorityCheck = 0
                                        break
                                    else:
                                        PriorityCheck = 1
                                if PriorityCheck == 1:
                                    str_ratio="{0:.1f}".format(P1n_ratio[i])
                                    plt.text(N_P1n_ratio[i]-N_adj_r,Z_P1n_ratio[i]+Z_adj_1,str_ratio,fontsize=fontsize_set_2)    
                                    
                          
                    if len(N_P2n_ratio) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                        for i in xrange(0,len(N_P2n_ratio)):
                            if user_R != 1:
                                str_ratio="{0:.1f}".format(P2n_ratio[i])
                                plt.text(N_P2n_ratio[i]-N_adj_r,Z_P2n_ratio[i]+Z_adj_2,str_ratio,fontsize=fontsize_set_2)
                            else:
                                for ii in xrange(0,len(N_USER)):
                                    if N_P2n_ratio[i] == N_USER[ii] and Z_P2n_ratio[i] == Z_USER[ii]:
                                        PriorityCheck = 0
                                        break
                                    else:
                                        PriorityCheck = 1
                                if PriorityCheck == 1:
                                    str_ratio="{0:.1f}".format(P2n_ratio[i])
                                    plt.text(N_P2n_ratio[i]-N_adj_r,Z_P2n_ratio[i]+Z_adj_2,str_ratio,fontsize=fontsize_set_2)    

                    if len(N_P3n_ratio) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                        for i in xrange(0,len(N_P3n_ratio)):
                            if user_R != 1:
                                str_ratio="{0:.1f}".format(P3n_ratio[i])
                                plt.text(N_P3n_ratio[i]-N_adj_r,Z_P3n_ratio[i]+Z_adj_3,str_ratio,fontsize=fontsize_set_2)
                            else:
                                for ii in xrange(0,len(N_USER)):
                                    if N_P3n_ratio[i] == N_USER[ii] and Z_P3n_ratio[i] == Z_USER[ii]:
                                        PriorityCheck = 0
                                        break
                                    else:
                                        PriorityCheck = 1
                                if PriorityCheck == 1:
                                    str_ratio="{0:.1f}".format(P3n_ratio[i])
                                    plt.text(N_P3n_ratio[i]-N_adj_r,Z_P3n_ratio[i]+Z_adj_3,str_ratio,fontsize=fontsize_set_2)

                    if len(N_P4n_ratio) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                        for i in xrange(0,len(N_P4n_ratio)):
                            if user_R != 1:
                                str_ratio="{0:.1f}".format(P4n_ratio[i])
                                plt.text(N_P4n_ratio[i]-N_adj_r,Z_P4n_ratio[i]+Z_adj_4,str_ratio,fontsize=fontsize_set_2)
                            else:
                                for ii in xrange(0,len(N_USER)):
                                    if N_P4n_ratio[i] == N_USER[ii] and Z_P4n_ratio[i] == Z_USER[ii]:
                                        PriorityCheck = 0
                                        break
                                    else:
                                        PriorityCheck = 1
                                if PriorityCheck == 1:
                                    str_ratio="{0:.1f}".format(P4n_ratio[i])
                                    plt.text(N_P4n_ratio[i]-N_adj_r,Z_P4n_ratio[i]+Z_adj_4,str_ratio,fontsize=fontsize_set_2)

                    if user_R == 1:
                        for i in xrange(0,len(N_USER)):
                            if  Delta_Z <= 10 and Delta_N <= 10 and Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user:
                                str_ratio="{0:.1f}".format(R1n_USER[i])
                                plt.text(N_USER[i]-N_adj_r,Z_USER[i]+Z_adj_1,str_ratio,fontsize=fontsize_set_2)
                                str_ratio="{0:.1f}".format(R2n_USER[i])
                                plt.text(N_USER[i]-N_adj_r,Z_USER[i]+Z_adj_2,str_ratio,fontsize=fontsize_set_2)
                            if  Delta_Z <= 7 and Delta_N <= 7 and Z_USER[i] >= Z_low_user and Z_USER[i] <= Z_high_user and N_USER[i] > N_low_user and N_USER[i] < N_high_user:
                                str_ratio="{0:.1f}".format(R3n_USER[i])
                                plt.text(N_USER[i]-N_adj_r,Z_USER[i]+Z_adj_3,str_ratio,fontsize=fontsize_set_2)
                                str_ratio="{0:.1f}".format(R4n_USER[i])
                                plt.text(N_USER[i]-N_adj_r,Z_USER[i]+Z_adj_4,str_ratio,fontsize=fontsize_set_2)

            if ratio_user != 1:
                if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                    if len(N_P1n_Bound_value) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                        for i in xrange(0,len(N_P1n_Bound_value)):
                            if user_P != 1 or user_Q != 1 or user_i != 1 or user_R != 1:
                                str_ratio="{0:.1f}".format(P1n_Bound[i])
                                plt.text(N_P1n_Bound_value[i]-N_adj,Z_P1n_Bound_value[i]+Z_adj_1,str_ratio+'%',fontsize=fontsize_set_3)
                            else:
                                for ii in xrange(0,len(N_P1n_Bound_USER_value)):
                                    if N_P1n_Bound_value[i] == N_P1n_Bound_USER_value[ii] and Z_P1n_Bound_value[i] == Z_P1n_Bound_USER_value[ii]:
                                        PriorityCheck = 0
                                        break
                                    else:
                                        PriorityCheck = 1
                                if PriorityCheck == 1:
                                    str_ratio="{0:.1f}".format(P1n_Bound[i])
                                    plt.text(N_P1n_Bound_value[i]-N_adj,Z_P1n_Bound_value[i]+Z_adj_1,str_ratio+'%',fontsize=fontsize_set_3)        
                                
                    if len(N_P2n_Bound_value) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                        for i in xrange(0,len(N_P2n_Bound_value)):
                            if user_P != 1 or user_Q != 1 or user_i != 1 or user_R != 1:
                                str_ratio="{0:.1f}".format(P2n_Bound[i])
                                plt.text(N_P2n_Bound_value[i]-N_adj,Z_P2n_Bound_value[i]+Z_adj_2,str_ratio+'%',fontsize=fontsize_set_3)
                            else:
                                for ii in xrange(0,len(N_P2n_Bound_USER_value)):
                                    if N_P2n_Bound_value[i] == N_P2n_Bound_USER_value[ii] and Z_P2n_Bound_value[i] == Z_P2n_Bound_USER_value[ii]:
                                        PriorityCheck = 0
                                        break
                                    else:
                                        PriorityCheck = 1
                                if PriorityCheck == 1:
                                    str_ratio="{0:.1f}".format(P2n_Bound[i])
                                    plt.text(N_P2n_Bound_value[i]-N_adj,Z_P2n_Bound_value[i]+Z_adj_2,str_ratio+'%',fontsize=fontsize_set_3)

                    if len(N_P3n_Bound_value) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                        for i in xrange(0,len(N_P3n_Bound_value)):
                            if user_P != 1 or user_Q != 1 or user_i != 1 or user_R != 1:
                                str_ratio="{0:.1f}".format(P3n_Bound[i])
                                plt.text(N_P3n_Bound_value[i]-N_adj,Z_P3n_Bound_value[i]+Z_adj_3,str_ratio+'%',fontsize=fontsize_set_3)
                            else:
                                for ii in xrange(0,len(N_P3n_Bound_USER_value)):
                                    if N_P3n_Bound_value[i] == N_P3n_Bound_USER_value[ii] and Z_P3n_Bound_value[i] == Z_P3n_Bound_USER_value[ii]:
                                        PriorityCheck = 0
                                        break
                                    else:
                                        PriorityCheck = 1
                                if PriorityCheck == 1:
                                    str_ratio="{0:.1f}".format(P3n_Bound[i])
                                    plt.text(N_P3n_Bound_value[i]-N_adj,Z_P3n_Bound_value[i]+Z_adj_3,str_ratio+'%',fontsize=fontsize_set_3)    

                    if len(N_P4n_Bound_value) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                        for i in xrange(0,len(N_P4n_Bound_value)):
                            if user_P != 1 or user_Q != 1 or user_i != 1 or user_R != 1:
                                str_ratio="{0:.1f}".format(P4n_Bound[i])
                                plt.text(N_P4n_user_value[i]-N_adj,Z_P4n_user_value[i]+Z_adj_4,str_ratio+'%',fontsize=fontsize_set_3)
                            else:
                                for ii in xrange(0,len(N_P4n_Bound_USER_value)):
                                    if N_P4n_Bound_value[i] == N_P4n_Bound_USER_value[ii] and Z_P4n_Bound_value[i] == Z_P4n_Bound_USER_value[ii]:
                                        PriorityCheck = 0
                                        break
                                    else:
                                        PriorityCheck = 1
                                if PriorityCheck == 1:
                                    str_ratio="{0:.1f}".format(P4n_Bound[i])
                                    plt.text(N_P4n_user_value[i]-N_adj,Z_P4n_user_value[i]+Z_adj_4,str_ratio+'%',fontsize=fontsize_set_3)

                    if len(N_P1n_Bound_iso1) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                        for i in xrange(0,len(N_P1n_Bound_iso1)):
                            if user_i != 1:
                                str_ratio="{0:.1f}".format(P1n_Bound_iso1[i])
                                plt.text(N_P1n_Bound_iso1[i]-N_adj_i,Z_P1n_Bound_iso1[i]+Z_adj_1,'| '+str_ratio+'%',fontsize=fontsize_set_3)
                            else:
                                for ii in xrange(0,len(N_P1n_Bound_USER_iso1)):
                                    if N_P1n_Bound_iso1[i] == N_P1n_Bound_USER_iso1[ii] and Z_P1n_Bound_iso1[i] == Z_P1n_Bound_USER_iso1[ii]:
                                        PriorityCheck = 0
                                        break
                                    else:
                                        PriorityCheck = 1
                                if PriorityCheck == 1:
                                    str_ratio="{0:.1f}".format(P1n_Bound_iso1[i])
                                    plt.text(N_P1n_Bound_iso1[i]-N_adj_i,Z_P1n_Bound_iso1[i]+Z_adj_1,'| '+str_ratio+'%',fontsize=fontsize_set_3)
                            
                    if len(N_P2n_Bound_iso1) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                        for i in xrange(0,len(N_P2n_Bound_iso1)):
                            if user_i != 1:
                                str_ratio="{0:.1f}".format(P2n_Bound_iso1[i])
                                plt.text(N_P2n_Bound_iso1[i]-N_adj_i,Z_P2n_Bound_iso1[i]+Z_adj_2,'| '+str_ratio+'%',fontsize=fontsize_set_3)
                            else:
                                for ii in xrange(0,len(N_P2n_Bound_USER_iso1)):
                                    if N_P2n_Bound_iso1[i] == N_P2n_Bound_USER_iso1[ii] and Z_P2n_Bound_iso1[i] == Z_P2n_Bound_USER_iso1[ii]:
                                        PriorityCheck = 0
                                        break
                                    else:
                                        PriorityCheck = 1
                                if PriorityCheck == 1:
                                    str_ratio="{0:.1f}".format(P2n_Bound_iso1[i])
                                    plt.text(N_P2n_Bound_iso1[i]-N_adj_i,Z_P2n_Bound_iso1[i]+Z_adj_2,'| '+str_ratio+'%',fontsize=fontsize_set_3)

                    if len(N_P1n_Bound_iso2) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                        for i in xrange(0,len(N_P1n_Bound_iso2)):
                            if user_i != 1:
                                str_ratio="{0:.1f}".format(P1n_Bound_iso2[i])
                                plt.text(N_P1n_Bound_iso2[i]-N_adj_i,Z_P1n_Bound_iso2[i]+Z_adj_3,'| '+str_ratio+'%',fontsize=fontsize_set_3)
                            else:
                                for ii in xrange(0,len(N_P1n_Bound_USER_iso2)):
                                    if N_P1n_Bound_iso2[i] == N_P1n_Bound_USER_iso2[ii] and Z_P1n_Bound_iso2[i] == Z_P1n_Bound_USER_iso2[ii]:
                                        PriorityCheck = 0
                                        break
                                    else:
                                        PriorityCheck = 1
                                if PriorityCheck == 1:
                                    str_ratio="{0:.1f}".format(P1n_Bound_iso2[i])
                                    plt.text(N_P1n_Bound_iso2[i]-N_adj_i,Z_P1n_Bound_iso2[i]+Z_adj_3,'| '+str_ratio+'%',fontsize=fontsize_set_3)

                    if len(N_P2n_Bound_iso2) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                        for i in xrange(0,len(N_P2n_Bound_iso2)):
                            if user_i != 1:
                                str_ratio="{0:.1f}".format(P2n_Bound_iso2[i])
                                plt.text(N_P2n_Bound_iso2[i]-N_adj_i,Z_P2n_Bound_iso2[i]+Z_adj_4,'| '+str_ratio+'%',fontsize=fontsize_set_3)
                            else:
                                for ii in xrange(0,len(N_P2n_Bound_USER_iso2)):
                                    if N_P2n_Bound_iso2[i] == N_P2n_Bound_USER_iso2[ii] and Z_P2n_Bound_iso2[i] == Z_P2n_Bound_USER_iso2[ii]:
                                        PriorityCheck = 0
                                        break
                                    else:
                                        PriorityCheck = 1
                                if PriorityCheck == 1:
                                    str_ratio="{0:.1f}".format(P2n_Bound_iso2[i])
                                    plt.text(N_P2n_Bound_iso2[i]-N_adj_i,Z_P2n_Bound_iso2[i]+Z_adj_4,'| '+str_ratio+'%',fontsize=fontsize_set_3)

                    if user_P == 1 or user_Q == 1 or user_i == 1 or user_R == 1:
                        if len(N_P1n_Bound_USER_value) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                            for i in xrange(0,len(N_P1n_Bound_USER_value)):
                                str_ratio="{0:.1f}".format(P1n_Bound_USER[i])
                                plt.text(N_P1n_Bound_USER_value[i]-N_adj,Z_P1n_Bound_USER_value[i]+Z_adj_1,str_ratio+'%',fontsize=fontsize_set_3)
                                    
                        if len(N_P2n_Bound_USER_value) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                            for i in xrange(0,len(N_P2n_Bound_USER_value)):
                                str_ratio="{0:.1f}".format(P2n_Bound_USER[i])
                                plt.text(N_P2n_Bound_USER_value[i]-N_adj,Z_P2n_Bound_USER_value[i]+Z_adj_2,str_ratio+'%',fontsize=fontsize_set_3)

                        if len(N_P3n_Bound_USER_value) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                            for i in xrange(0,len(N_P3n_Bound_USER_value)):
                                str_ratio="{0:.1f}".format(P3n_Bound_USER[i])
                                plt.text(N_P3n_Bound_USER_value[i]-N_adj,Z_P3n_Bound_USER_value[i]+Z_adj_3,str_ratio+'%',fontsize=fontsize_set_3)

                        if len(N_P4n_Bound_USER_value) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                            for i in xrange(0,len(N_P4n_Bound_USER_value)):
                                str_ratio="{0:.1f}".format(P4n_Bound_USER[i])
                                plt.text(N_P4n_Bound_USER_value[i]-N_adj,Z_P4n_Bound_USER_value[i]+Z_adj_4,str_ratio+'%',fontsize=fontsize_set_3)

                    if user_i == 1:    
                        if len(N_P1n_Bound_USER_iso1) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                            for i in xrange(0,len(N_P1n_Bound_USER_iso1)):
                                str_ratio="{0:.1f}".format(P1n_Bound_USER_iso1[i])
                                plt.text(N_P1n_Bound_USER_iso1[i]-N_adj_i,Z_P1n_Bound_USER_iso1[i]+Z_adj_1,'| '+str_ratio+'%',fontsize=fontsize_set_3)
                                
                        if len(N_P2n_Bound_USER_iso1) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                            for i in xrange(0,len(N_P2n_Bound_USER_iso1)):
                                str_ratio="{0:.1f}".format(P2n_Bound_USER_iso1[i])
                                plt.text(N_P2n_Bound_USER_iso1[i]-N_adj_i,Z_P2n_Bound_USER_iso1[i]+Z_adj_2,'| '+str_ratio+'%',fontsize=fontsize_set_3)

                        if len(N_P1n_Bound_USER_iso2) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                            for i in xrange(0,len(N_P1n_Bound_USER_iso2)):
                                str_ratio="{0:.1f}".format(P1n_Bound_USER_iso2[i])
                                plt.text(N_P1n_Bound_USER_iso2[i]-N_adj_i,Z_P1n_Bound_USER_iso2[i]+Z_adj_3,'| '+str_ratio+'%',fontsize=fontsize_set_3)

                        if len(N_P2n_Bound_USER_iso2) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                            for i in xrange(0,len(N_P2n_Bound_USER_iso2)):
                                str_ratio="{0:.1f}".format(P2n_Bound_USER_iso2[i])
                                plt.text(N_P2n_Bound_USER_iso2[i]-N_adj_i,Z_P2n_Bound_USER_iso2[i]+Z_adj_4,'| '+str_ratio+'%',fontsize=fontsize_set_3)
                    
            plt.axis('scaled')
            g=plt.gca()
            plt.xlim(N_low_user,N_high_user)
            plt.ylim(Z_low_user-1,Z_high_user+1)
            
            if ratio_user == 1:
                plt.title("Ratio between theoretical & experimental data")
            if ratio_user != 1:
                plt.title("Experimentally known beta-delayed neutron emitters")
                
            plt.xlabel("N")
            plt.ylabel("Z")

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
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+8.5,color=color1,linewidth=lw2) 
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+7.5,color=color1,linewidth=lw2)
                  
            if Z_high_user >= 20 and Z_low_user <= 20:
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+20.5,color=color1,linewidth=lw2) 
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+19.5,color=color1,linewidth=lw2)
                 
            if Z_high_user >= 28 and Z_low_user <= 28:
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+28.5,color=color1,linewidth=lw2)
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+27.5,color=color1,linewidth=lw2)             

            if Z_high_user >= 50 and Z_low_user <= 50:
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+50.5,color=color1,linewidth=lw2)
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+49.5,color=color1,linewidth=lw2)

            if Z_high_user >= 82 and Z_low_user <= 82:
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+82.5,color=color1,linewidth=lw2)
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+81.5,color=color1,linewidth=lw2)

            if Z_high_user >= 126 and Z_low_user <= 126:
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+126.5,color=color1,linewidth=lw2)
                plt.plot(N_Bound_magic,Z_Bound_magic*0.+125.5,color=color1,linewidth=lw2)

            if Delta_N == 10 and Delta_Z == 10 or Delta_N == 7 and Delta_Z == 7 or Delta_N == 4 and Delta_Z == 4 or Delta_N == 0 and Delta_Z == 0:
                plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z1,'Produced By: Ciccone, Stephanie',fontsize=10)
                plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z2,'    TRIUMF/McMaster University',fontsize=10)
                plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z3,'Masses: AME 2012 (Wang et al.)',fontsize=10)

                if ratio_user == 1:
                    plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z4,'Exp.: ENSDF(June 2011), Miernik(2013)',fontsize=10)
                    plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z5,'        Hosmer(2010), Padgett(2010)',fontsize=10)
                    plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z6,'Theo.: Moeller(2003)',fontsize=10) 

                if ratio_user != 1:
                    plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z4,'Exp.: ENSDF(June 2011)',fontsize=10)
                    plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z5,'        Hosmer(2010),Padgett(2010)',fontsize=10)
                    plt.text(N_high_user-Cred_N,Z_low_user-Cred_Z6,'        Miernik(2013)',fontsize=10)

            if c1 == 1:
                leg_list = np.append(leg_list,leg_text[0])
            if c2 == 1:
                leg_list = np.append(leg_list,leg_text[1])
            if c3 == 1:
                leg_list = np.append(leg_list,leg_text[2])
            if c4 == 1:
                leg_list = np.append(leg_list,leg_text[3])
            if c5 == 1:
                leg_list = np.append(leg_list,leg_text[4])
                
            if c6 == 1:
                leg_list = np.append(leg_list,leg_text[5])
            if c7 == 1:
                leg_list = np.append(leg_list,leg_text[6])
            if c8 == 1:
                leg_list = np.append(leg_list,leg_text[7])
            if c9 == 1:
                leg_list = np.append(leg_list,leg_text[8])
            if c10 == 1:
                leg_list = np.append(leg_list,leg_text[9])

            if (Delta_N == 10 and Delta_Z == 10) or (Delta_N == 7 and Delta_Z == 7) or (Delta_N == 4 and Delta_Z == 4) or (Delta_N == 0 and Delta_Z == 0):
                l1 = plt.legend(leg_list,loc=2,bbox_to_anchor=[1.02,0.98],borderaxespad=0.,markerscale=ms1,numpoints=1)
                if ratio_user == 1 and Delta_Z <= 10 and Delta_N <= 10  and Delta_N > 7 and Delta_Z > 7:
                    l2 = plt.legend(('      Isotope','(P1n Exp./P1n Theory)','(P2n Exp./P2n Theory)'),loc=6,bbox_to_anchor=[1.02,0.4],numpoints=1,markerscale=ms2)
                    g.add_artist(l1)
                if ratio_user == 1 and Delta_Z <= 7 and Delta_N <= 7:
                    l2 = plt.legend(('      Isotope','(P1n Exp./P1n Theory)','(P2n Exp./P2n Theory)','(P3n Exp./P3n Theory)','(P4n Exp./P4n Theory)'),loc=6,bbox_to_anchor=[1.02,0.4],numpoints=1,markerscale=ms2)
                    g.add_artist(l1)

                if ratio_user != 1 and Delta_Z <= 10 and Delta_N <= 10 and Delta_N > 7 and Delta_Z > 7:
                    l2 = plt.legend(('  Isotope  ','  P1n','  P2n'),loc=6,bbox_to_anchor=[1.02,0.4],numpoints=1,markerscale=ms2)
                    g.add_artist(l1)
                if ratio_user != 1 and Delta_Z <= 7 and Delta_N <= 7  and Delta_Z > 4 and Delta_Z > 4:
                    l2 = plt.legend(('  Isotope  ','  P1n','  P2n','  P3n','  P4n'),loc=6,bbox_to_anchor=[1.02,0.4],numpoints=1,markerscale=ms2)
                    g.add_artist(l1)
                if ratio_user != 1 and Delta_Z <= 4 and Delta_N <= 4:
                    l2 = plt.legend(('     Isotope  ','  P1n-gs | P1n-iso1','  P2n-gs | P2n-iso1','  P3n-gs | P1n-iso2','  P4n-gs | P2n-iso2'),loc=6,bbox_to_anchor=[1.02,0.4],numpoints=1,markerscale=ms2)
                    g.add_artist(l1)
            else:
                l1 = plt.legend(leg_list,loc=4,markerscale=ms1,numpoints=1)

            plt.show()
            
            # user choice to continue or quit program
            r=input("If r = 1, program will stop. If r = 0, program continues. Enter r: ")
                        
main() #runs program
