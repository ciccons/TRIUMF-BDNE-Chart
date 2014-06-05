#-----------------------------------------------------------------------------
# Author: Stephanie Ciccone
# Consult Chart_Program_INFO.txt for instruction on how to ensure this program properly runs on your machine
#-----------------------------------------------------------------------------

# imports all necessary libraries and functions
import gc
import os
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
    filename1_MO = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "ChartNuclides_DataTable_P_MOELLER.txt"
    filename2_MO = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "ChartNuclides_DataTable_ELE_MOELLER.txt"
    filename3_MO = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "ChartNuclides_DataTable1.txt"
    filename4_MO = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "N_Z_stable.txt"

    #assigns one column of data in the text files to various specific arrays
    N_P,Z_P,P1n,P2n,P3n = np.loadtxt(filename1_MO,skiprows=1,unpack=True)
    size_P = len(N_P)

    N_stable,Z_stable = np.loadtxt(filename4_MO,skiprows=1,unpack=True)
    s1 = len(N_stable)

    N,Z,bn,b2n = np.loadtxt(filename3_MO,skiprows=1,unpack=True)
    s2 = len(N)

    f2_MO = open(filename2_MO,'r')
    header_MO = f2_MO.readline()
    
    limit = 4500
    ar = np.arange(limit) ; dt = np.dtype((str,3))
    ELE_names_MO = np.array(ar,dt)
    i_ELE=0
    
    for line in f2_MO:
        ELE_names_MO[i_ELE] = line
        i_ELE=i_ELE+1
        end=i_ELE
    ELE_names_MO = ELE_names_MO[:end]
    f2_MO.close()

    #-------------------------------------------------------------------------

    # list of text in order to properly set up the legend
    leg_text=['Known nuclei','Stable','P(1n) dominates','P(2n) dominates','P(3n) dominates']
    
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
        print "The Chart will zoom in and display P values of the theoretical emitters if the user inputs:"
        print " 1. An N range with a difference equal to 10 and a Z range with a difference equal to 10."
        print " 2. An N range with a difference equal to 7 and a Z range with a difference equal to 7."
        print " 3. An N range with a difference equal to 4 and a Z range with a difference equal to 4."
        print " 4. An N range with a difference equal to 0 and a Z range with a difference equal to 0."
        print "The Chart will output normally if BOTH ranges are greater than these limits."
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
        
        # this part of the code makes an array for only the N and Z values that denote a stable nuclei
        N_stable_user = [];Z_stable_user = []
        append_Nstable = N_stable_user.append;append_Zstable = Z_stable_user.append

        for i in xrange(0,s1):
            if Z_stable[i] >= Z_low_user and Z_stable[i] <= Z_high_user:
                append_Nstable(N_stable[i])
                append_Zstable(Z_stable[i])

        #------------------------------------------------------------------------------

        # this part of the code makes an array for the N and Z values of the magic number lines
        # also makes an array for all nuclei found in the user inputted section
        N_P_user = [] ; Z_P_user = []
        append_NP = N_P_user.append;append_ZP = Z_P_user.append
        N_user_magic = [] ; Z_user_magic = []
        append_Nmag = N_user_magic.append;append_Zmag = Z_user_magic.append
                
        for i in xrange(0,size_P):

            if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user:
                append_NP(N_P[i])
                append_ZP(Z_P[i])

            if Z_P[i] >= 0 and Z_P[i] <= Z_high_user:
                append_Nmag(N_P[i])
                append_Zmag(Z_P[i])
        N_user_magic = np.array(N_user_magic)
        Z_user_magic = np.array(Z_user_magic)

        #-----------------------------------------------------------------------------

        #for loop that determines the size of an array based on isotopes that have probability of beta-delayed emission
        #greater than 0 (measured probability) and determines array of P values that should be displayed on the plot
        N_P1n_user = [];Z_P1n_user = []
        append_NP1 = N_P1n_user.append;append_ZP1 = Z_P1n_user.append
        N_P2n_user = [];Z_P2n_user = []
        append_NP2 = N_P2n_user.append;append_ZP2 = Z_P2n_user.append
        N_P3n_user = [];Z_P3n_user = []
        append_NP3 = N_P3n_user.append;append_ZP3 = Z_P3n_user.append

        N_P1n_user_value = [];Z_P1n_user_value = []
        append_NP1V = N_P1n_user_value.append;append_ZP1V = Z_P1n_user_value.append
        P1n_user = [];P1ncolor = []
        append_P1 = P1n_user.append;append_P1ncolor = P1ncolor.append
        N_P1n_c = [];Z_P1n_c = []
        append_NP1C = N_P1n_c.append;append_ZP1C = Z_P1n_c.append
        
        N_P2n_user_value = [];Z_P2n_user_value = []
        append_NP2V = N_P2n_user_value.append;append_ZP2V = Z_P2n_user_value.append
        P2n_user = [];P2ncolor = []
        append_P2 = P2n_user.append;append_P2ncolor = P2ncolor.append
        N_P2n_c = [];Z_P2n_c = []
        append_NP2C = N_P2n_c.append;append_ZP2C = Z_P2n_c.append
        
        N_P3n_user_value = [];Z_P3n_user_value = []
        append_NP3V = N_P3n_user_value.append;append_ZP3V = Z_P3n_user_value.append
        P3n_user = [];P3ncolor = []
        append_P3 = P3n_user.append;append_P3ncolor = P3ncolor.append
        N_P3n_c = [];Z_P3n_c = []
        append_NP3C = N_P3n_c.append;append_ZP3C = Z_P3n_c.append

        N_ELE = [];Z_ELE = []
        append_NELE = N_ELE.append;append_ZELE = Z_ELE.append
        A_ELE = [];ELE_name_user = []
        append_AELE = A_ELE.append;append_ELEn = ELE_name_user.append

        for i in xrange(0,size_P):
            if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] >= N_low_user and N_P[i] <= N_high_user:
                if P1n[i] != 0 and P1n[i] > P2n[i] and P1n[i] > P3n[i]:
                    append_NP1(N_P[i]);append_ZP1(Z_P[i]) #makes array of nuclei with dominant P1n values

                if P1n[i] != 0:
                    append_NP1C(N_P[i]);append_ZP1C(Z_P[i]) #makes an array for the color bar version

                    if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                        append_NP1V(N_P[i]);append_ZP1V(Z_P[i]) #makes array for nuclei which will have data displayed about them
                        append_P1(P1n[i])

                    # determines which color a nuclei will be highlighted as using the color bar
                    if P1n[i] <= 50:
                        if P1n[i] > 0 and P1n[i] <= 10:
                            append_P1ncolor('yellow')
                        if P1n[i] > 10 and P1n[i] <= 20:
                            append_P1ncolor('orange')
                        if P1n[i] > 20 and P1n[i] <= 30:
                            append_P1ncolor('red')
                        if P1n[i] > 30 and P1n[i] <= 40:
                            append_P1ncolor('maroon')
                        if P1n[i] > 40:
                            append_P1ncolor('lime')
                    if P1n[i] > 50:
                        if P1n[i] <= 60:
                            append_P1ncolor('green')
                        if P1n[i] > 60 and P1n[i] <= 70:
                            append_P1ncolor('DeepSkyBlue')
                        if P1n[i] > 70 and P1n[i] <= 80:
                            append_P1ncolor('blue')
                        if P1n[i] > 80 and P1n[i] <= 90:
                            append_P1ncolor('violet')
                        if P1n[i] > 90 and P1n[i] <= 100:
                            append_P1ncolor('purple')

                if P2n[i] != 0 and P2n[i] > P1n[i] and P2n[i] > P3n[i]:
                    append_NP2(N_P[i]);append_ZP2(Z_P[i]) #nuclei with dominant P2n values
                    
                if P2n[i] != 0:
                    append_NP2C(N_P[i]);append_ZP2C(Z_P[i])

                    if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                        append_NP2V(N_P[i]);append_ZP2V(Z_P[i])
                        append_P2(P2n[i])

                    if P2n[i] <= 50:
                        if P2n[i] > 0 and P2n[i] <= 10:
                            append_P2ncolor('yellow')
                        if P2n[i] > 10 and P2n[i] <= 20:
                            append_P2ncolor('orange')
                        if P2n[i] > 20 and P2n[i] <= 30:
                            append_P2ncolor('red')
                        if P2n[i] > 30 and P2n[i] <= 40:
                            append_P2ncolor('maroon')
                        if P2n[i] > 40:
                            append_P2ncolor('lime')
                    if P2n[i] > 50:
                        if P2n[i] <= 60:
                            append_P2ncolor('green')
                        if P2n[i] > 60 and P2n[i] <= 70:
                            append_P2ncolor('DeepSkyBlue')
                        if P2n[i] > 70 and P2n[i] <= 80:
                            append_P2ncolor('blue')
                        if P2n[i] > 80 and P2n[i] <= 90:
                            append_P2ncolor('violet')
                        if P2n[i] > 90 and P2n[i] <= 100:
                            append_P2ncolor('purple')
                                                 
                if P3n[i] != 0 and P3n[i] > P1n[i] and P3n[i] > P2n[i]:
                    append_NP3(N_P[i]);append_ZP3(Z_P[i]) # nuclei with dominant P3n values

                if P3n[i] != 0:
                    append_NP3C(N_P[i]);append_ZP3C(Z_P[i]) 
                    
                    if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                        append_NP3V(N_P[i]);append_ZP3V(Z_P[i])
                        append_P3(P3n[i])

                    if P3n[i] <= 50:
                        if P3n[i] > 0 and P3n[i] <= 10:
                            append_P3ncolor('yellow')
                        if P3n[i] > 10 and P3n[i] <= 20:
                            append_P3ncolor('orange')
                        if P3n[i] > 20 and P3n[i] <= 30:
                            append_P3ncolor('red')
                        if P3n[i] > 30 and P3n[i] <= 40:
                            append_P3ncolor('maroon')
                        if P3n[i] > 40:
                            append_P3ncolor('lime')
                    if P3n[i] > 50:
                        if P3n[i] <= 60:
                            append_P3ncolor('green')
                        if P3n[i] > 60 and P3n[i] <= 70:
                            append_P3ncolor('DeepSkyBlue')
                        if P3n[i] > 70 and P3n[i] <= 80:
                            append_P3ncolor('blue')
                        if P3n[i] > 80 and P3n[i] <= 90:
                            append_P3ncolor('violet')
                        if P3n[i] > 90 and P3n[i] <= 100:
                            append_P3ncolor('purple')

                if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:

                    append_NELE(N_P[i])
                    append_ZELE(Z_P[i])
                    append_ELEn(ELE_names_MO[i])
                    append_AELE(N_P[i]+Z_P[i]) # makes all the arrays to display element name and mass number, A
                    
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
            mew = 2.0;ms1=1
            lw1 = '0.5';lw2 = '1'
            ax1_1=0.93;ax1_2=0.1;ax1_3=0.02;ax1_4=0.8
            
        if Delta_N <= 10 and Delta_Z <= 10 and Delta_N > 7 and Delta_Z > 7:
            msize = 35
            mew = 3.0;ms1=0.2;ms2=0
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
            mew = 4.0;ms1=0.2;ms2=0
            lw1 = '2.0';lw2 = '2.5'
            Cred_N = -0.2
            Cred_Z1=0.2;Cred_Z2=0.4;Cred_Z3=0.6 
            Cred_Z4=0.8;Cred_Z5=1;Cred_Z6=1.2
            N_ELE_adj1=0.3;Z_ELE_adj1=0.2
            fontsize_set_1=10;fontsize_set_2=9;fontsize_set_3=8
            N_adj=0.25;N_adj_r=0.25
            Z_adj_1=0.05;Z_adj_2=-0.08;Z_adj_3=-0.22;Z_adj_4=-0.36
            ax1_1=0.75;ax1_2=0.1;ax1_3=0.02;ax1_4=0.8
            
        if Delta_N <= 4 and Delta_Z <= 4  and Delta_N > 0 and Delta_Z > 0:
            msize = 70
            mew = 5.0;ms1=0.1;ms2=0
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
            mew = 5.0;ms1=0.05;ms2=0
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
            c1=0;c2=0;c3=0;c4=0;c5=0

            if len(N_P_user) != 0:
                plt.plot(N_P_user,Z_P_user,marker='s',color='0.8',markersize=msize,linestyle='')
                c1=1
            if len(N_stable_user) != 0:
                plt.plot(N_stable_user,Z_stable_user,marker='s',color=color1,markersize=msize,linestyle='')
                c2=1
                                                     
            if len(N_P1n_user) != 0:
                plt.plot(N_P1n_user,Z_P1n_user,marker='s',color=color2,markersize=msize,linestyle='')
                c3=1
            if len(N_P2n_user) != 0:
                plt.plot(N_P2n_user,Z_P2n_user,marker='s',color=color3,markersize=msize,linestyle='')
                c4=1
            if len(N_P3n_user) != 0:
                plt.plot(N_P3n_user,Z_P3n_user,marker='s',color=color4,markersize=msize,linestyle='')
                c5=1

            # determines which magic number lines are necessary to display
            if N_high_user >= 8 and N_low_user <= 8:  
                plt.plot(N_user_magic*0.+8.5,Z_user_magic,color=color1,linewidth=lw1)  
                plt.plot(N_user_magic*0.+7.5,Z_user_magic,color=color1,linewidth=lw1)
              
            if N_high_user >= 20 and N_low_user <= 20:
                plt.plot(N_user_magic*0.+20.5,Z_user_magic,color=color1,linewidth=lw1) 
                plt.plot(N_user_magic*0.+19.5,Z_user_magic,color=color1,linewidth=lw1)
                   
            if N_high_user >= 28 and N_low_user <= 28:
                plt.plot(N_user_magic*0.+28.5,Z_user_magic,color=color1,linewidth=lw1)
                plt.plot(N_user_magic*0.+27.5,Z_user_magic,color=color1,linewidth=lw1)     

            if N_high_user >= 50 and N_low_user <= 50:
                plt.plot(N_user_magic*0.+50.5,Z_user_magic,color=color1,linewidth=lw1)
                plt.plot(N_user_magic*0.+49.5,Z_user_magic,color=color1,linewidth=lw1)
                     
            if N_high_user >= 82 and N_low_user <= 82:
                plt.plot(N_user_magic*0.+82.5,Z_user_magic,color=color1,linewidth=lw1)
                plt.plot(N_user_magic*0.+81.5,Z_user_magic,color=color1,linewidth=lw1)
                       
            if N_high_user >= 126 and N_low_user <= 126:
                plt.plot(N_user_magic*0.+126.5,Z_user_magic,color=color1,linewidth=lw1) 
                plt.plot(N_user_magic*0.+125.5,Z_user_magic,color=color1,linewidth=lw1) 

            if Z_high_user >= 8 and Z_low_user <= 8:
                plt.plot(N_user_magic,Z_user_magic*0.+8.5,color=color1,linewidth=lw2) 
                plt.plot(N_user_magic,Z_user_magic*0.+7.5,color=color1,linewidth=lw2)
                  
            if Z_high_user >= 20 and Z_low_user <= 20:
                plt.plot(N_user_magic,Z_user_magic*0.+20.5,color=color1,linewidth=lw2) 
                plt.plot(N_user_magic,Z_user_magic*0.+19.5,color=color1,linewidth=lw2)
                 
            if Z_high_user >= 28 and Z_low_user <= 28:
                plt.plot(N_user_magic,Z_user_magic*0.+28.5,color=color1,linewidth=lw2)
                plt.plot(N_user_magic,Z_user_magic*0.+27.5,color=color1,linewidth=lw2)             

            if Z_high_user >= 50 and Z_low_user <= 50:
                plt.plot(N_user_magic,Z_user_magic*0.+50.5,color=color1,linewidth=lw2)
                plt.plot(N_user_magic,Z_user_magic*0.+49.5,color=color1,linewidth=lw2)

            if Z_high_user >= 82 and Z_low_user <= 82:
                plt.plot(N_user_magic,Z_user_magic*0.+82.5,color=color1,linewidth=lw2)
                plt.plot(N_user_magic,Z_user_magic*0.+81.5,color=color1,linewidth=lw2)

            if Z_high_user >= 126 and Z_low_user <= 126:
                plt.plot(N_user_magic,Z_user_magic*0.+126.5,color=color1,linewidth=lw2)
                plt.plot(N_user_magic,Z_user_magic*0.+125.5,color=color1,linewidth=lw2)

            print len(N_ELE),len(ELE_name_user)
            if len(N_ELE) != 0 and len(ELE_name_user) != 0 and Delta_Z <= 10 and Delta_N <= 10: 
                #xyouts,N_spec-0.35,Z_spec+0.28,Special_user,charsize=1,color=color1
                for i in xrange(0,len(N_ELE)):
                    ELE_info = ' '.join([ELE_name_user[i].rstrip('\n'),str(int(A_ELE[i]))])
                    plt.text(N_ELE[i]-N_ELE_adj1,Z_ELE[i]+Z_ELE_adj1,ELE_info,fontsize=fontsize_set_1)

                if len(N_P1n_user_value) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                    for i in xrange(0,len(N_P1n_user_value)):
                        str_ratio="{0:.2f}".format(P1n_user[i])
                        plt.text(N_P1n_user_value[i]-N_adj,Z_P1n_user_value[i]+Z_adj_1,str_ratio+'%',fontsize=fontsize_set_3)
                            
                if len(N_P2n_user_value) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                    for i in xrange(0,len(N_P2n_user_value)):
                        str_ratio="{0:.2f}".format(P2n_user[i])
                        plt.text(N_P2n_user_value[i]-N_adj,Z_P2n_user_value[i]+Z_adj_2,str_ratio+'%',fontsize=fontsize_set_3)

                if len(N_P3n_user_value) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                    for i in xrange(0,len(N_P3n_user_value)):
                        str_ratio="{0:.2f}".format(P3n_user[i])
                        plt.text(N_P3n_user_value[i]-N_adj,Z_P3n_user_value[i]+Z_adj_3,str_ratio+'%',fontsize=fontsize_set_3)

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

            if Delta_N <= 10 and Delta_Z <= 10:
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

            if len(N_P_user) != 0:
                plt.plot(N_P_user,Z_P_user,marker='s',color='0.8',markersize=msize,linestyle='')
                c1=1
            if len(N_stable_user) != 0:
                plt.plot(N_stable_user,Z_stable_user,marker='s',color=color1,markersize=msize,linestyle='')
                c2=1
                                                     
            if len(N_P1n_c) != 0 and plot_choice == 1:
                plt.title("Theoretically known beta-delayed neutron emitters: P1n Color Bar")
                for i in range(0,len(N_P1n_c)):
                    plt.plot(N_P1n_c[i],Z_P1n_c[i],marker='s',color=P1ncolor[i],markersize=msize,linestyle='')
                    c3=1

            if len(N_P2n_c) != 0 and plot_choice == 2:
                plt.title("Theoretically known beta-delayed neutron emitters: P2n Color Bar") 
                for i in range(0,len(N_P2n_c)):
                    plt.plot(N_P2n_c[i],Z_P2n_c[i],marker='s',color=P2ncolor[i],markersize=msize,linestyle='')
                    c3=1

            if len(N_P3n_c) != 0 and plot_choice == 3:
                plt.title("Theoretically known beta-delayed neutron emitters: P3n Color Bar")
                for i in range(0,len(N_P3n_c)):
                    plt.plot(N_P3n_c[i],Z_P3n_c[i],marker='s',color=P3ncolor[i],markersize=msize,linestyle='')
                    c3=1

            if N_high_user >= 8 and N_low_user <= 8:  
                plt.plot(N_user_magic*0.+8.5,Z_user_magic,color=color1,linewidth=lw1)  
                plt.plot(N_user_magic*0.+7.5,Z_user_magic,color=color1,linewidth=lw1)
              
            if N_high_user >= 20 and N_low_user <= 20:
                plt.plot(N_user_magic*0.+20.5,Z_user_magic,color=color1,linewidth=lw1) 
                plt.plot(N_user_magic*0.+19.5,Z_user_magic,color=color1,linewidth=lw1)
                   
            if N_high_user >= 28 and N_low_user <= 28:
                plt.plot(N_user_magic*0.+28.5,Z_user_magic,color=color1,linewidth=lw1)
                plt.plot(N_user_magic*0.+27.5,Z_user_magic,color=color1,linewidth=lw1)     

            if N_high_user >= 50 and N_low_user <= 50:
                plt.plot(N_user_magic*0.+50.5,Z_user_magic,color=color1,linewidth=lw1)
                plt.plot(N_user_magic*0.+49.5,Z_user_magic,color=color1,linewidth=lw1)
                     
            if N_high_user >= 82 and N_low_user <= 82:
                plt.plot(N_user_magic*0.+82.5,Z_user_magic,color=color1,linewidth=lw1)
                plt.plot(N_user_magic*0.+81.5,Z_user_magic,color=color1,linewidth=lw1)
                       
            if N_high_user >= 126 and N_low_user <= 126:
                plt.plot(N_user_magic*0.+126.5,Z_user_magic,color=color1,linewidth=lw1) 
                plt.plot(N_user_magic*0.+125.5,Z_user_magic,color=color1,linewidth=lw1) 

            if Z_high_user >= 8 and Z_low_user <= 8:
                plt.plot(N_user_magic,Z_user_magic*0.+8.5,color=color1,linewidth=lw2) 
                plt.plot(N_user_magic,Z_user_magic*0.+7.5,color=color1,linewidth=lw2)
                  
            if Z_high_user >= 20 and Z_low_user <= 20:
                plt.plot(N_user_magic,Z_user_magic*0.+20.5,color=color1,linewidth=lw2) 
                plt.plot(N_user_magic,Z_user_magic*0.+19.5,color=color1,linewidth=lw2)
                 
            if Z_high_user >= 28 and Z_low_user <= 28:
                plt.plot(N_user_magic,Z_user_magic*0.+28.5,color=color1,linewidth=lw2)
                plt.plot(N_user_magic,Z_user_magic*0.+27.5,color=color1,linewidth=lw2)             

            if Z_high_user >= 50 and Z_low_user <= 50:
                plt.plot(N_user_magic,Z_user_magic*0.+50.5,color=color1,linewidth=lw2)
                plt.plot(N_user_magic,Z_user_magic*0.+49.5,color=color1,linewidth=lw2)

            if Z_high_user >= 82 and Z_low_user <= 82:
                plt.plot(N_user_magic,Z_user_magic*0.+82.5,color=color1,linewidth=lw2)
                plt.plot(N_user_magic,Z_user_magic*0.+81.5,color=color1,linewidth=lw2)

            if Z_high_user >= 126 and Z_low_user <= 126:
                plt.plot(N_user_magic,Z_user_magic*0.+126.5,color=color1,linewidth=lw2)
                plt.plot(N_user_magic,Z_user_magic*0.+125.5,color=color1,linewidth=lw2)

            # outputs color bar
            ax1 = fig.add_axes([ax1_1,ax1_2,ax1_3,ax1_4])
            
            cmap = mpl.colors.ListedColormap(['yellow','orange','red','maroon','lime','green','DeepSkyBlue','blue','violet','purple'])
            bounds = [0,10,20,30,40,50,60,70,80,90,100]
            norm = mpl.colors.BoundaryNorm(bounds,cmap.N)
            cb1 = mpl.colorbar.ColorbarBase(ax1,cmap=cmap,norm=norm,boundaries=bounds,ticks=bounds,orientation='vertical')
            cb1.set_label('%')

            plt.show()
            
        r=input("If r = 1, program will stop. If r = 0, program continues. Enter r: ")
#------------------------------------------------------------------------------------------------------------

def main():

    # will be altered to GUI in future
    choice_user = 0
    choice_user = input("Enter 1 to display the experimental version; Enter 2 to display the theoretical version: ")

    # determines if running on a Windows or a Unix machine and yields the required directory deliminator
    if os.name == "nt":
        dirDelim = "\\"
    else:
        dirDelim = "/"

    if choice_user == 2:
        MOELLER() # runs theoretical MOELLER version
    else:
        #reads in values from text files and stores all of the data columns into arrays
        #filename1 = "C:\Users\Stephanie_2\Documents\GitHub\TRIUMF-BDNE-Chart\Text_Files\ChartNuclides_DataTable1.txt"
        
        filename1 = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "ChartNuclides_DataTable1.txt"
        filename2 = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "N_Z_stable.txt"
        
        filename3 = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "ChartNuclides_DataTable_Qbn.txt"
        filename4 = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "ChartNuclides_DataTable_Qb2n.txt"
        filename5 = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "ChartNuclides_DataTable_Qb3n.txt"
        filename6 = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "ChartNuclides_DataTable_Qb4n.txt"
        
        filename7 = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "ChartNuclides_DataTable_P_ENSDF.txt"
        filename8 = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "ChartNuclides_DataTable_ELE_ENSDF.txt"
        filename9 = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "ChartNuclides_DataTable_iso1_ENSDF.txt"
        filename10 = os.getcwd() + dirDelim + "Text_Files" + dirDelim + "ChartNuclides_DataTable_iso2_ENSDF.txt"

        N,Z,bn,b2n = np.loadtxt(filename1,skiprows=1,unpack=True)
        s1 = len(N)
        
        N_stable,Z_stable= np.loadtxt(filename2,skiprows=1,unpack=True)
        s2 = len(N_stable)

        N_bn,Z_bn,Qbn = np.loadtxt(filename3,skiprows=1,unpack=True)
        N_b2n,Z_b2n,Qb2n = np.loadtxt(filename4,skiprows=1,unpack=True)
        N_b3n,Z_b3n,Qb3n = np.loadtxt(filename5,skiprows=1,unpack=True)
        N_b4n,Z_b4n,Qb4n = np.loadtxt(filename6,skiprows=1,unpack=True)

        N_P,Z_P,Special,P1n,P2n,P3n,P4n,P1n_MOE,P2n_MOE,P3n_MOE = np.loadtxt(filename7,skiprows=1,unpack=True)
        size_P = len(N_P)

        f8 = open(filename8,'r')
        header = f8.readline()
        ELE_names = []
        for line in f8:
            ELE_names = np.append(ELE_names,line)
        f8.close()
        
        N_P_iso1,Z_P_iso1,Special_iso1,P1n_iso1,P2n_iso1,P3n_iso1,P4n_iso1 = np.loadtxt(filename9,skiprows=1,unpack=True)
        size_P_iso1 = len(N_P_iso1)
        N_P_iso2,Z_P_iso2,Special_iso2,P1n_iso2,P2n_iso2,P3n_iso2,P4n_iso2 = np.loadtxt(filename10,skiprows=1,unpack=True)
        size_P_iso2 = len(N_P_iso2)
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
            print "The Chart will zoom in and display P values of the measured, known emitters if the user inputs: "
            print " 1. An N range with a difference equal to 0 and a Z range with a difference equal to 0."
            print " 2. An N range with a difference equal to 4 and a Z range with a difference equal to 4."
            print " 3. An N range with a difference equal to 7 and a Z range with a difference equal to 7."
            print " 4. An N range with a difference equal to 10 and a Z range with a difference equal to 10."
            print "The Chart will output normally if BOTH ranges are greater than 10."
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
            if Delta_N <= 10 and Delta_Z <= 10:
                ratio_user=input("Enter 1 to display the ratio difference instead-(P exp.)/(P theory). Enter anything else to proceed without the ratio: ")

            N_high_user=N_high_user+1
            N_low_user=N_low_user-1

            print "Analyzing Data Tables and Building Chart Arrays..."
    #-----------------------------------------------------------------------------

            N_user = []
            Z_user = []

            N_user_magic = []
            Z_user_magic = []

            N_Qbn_user = []
            Z_Qbn_user = []
            N_Qb2n_user = []
            Z_Qb2n_user = []
            
            N_Qb3n_user = []
            Z_Qb3n_user = []
            N_Qb4n_user = []
            Z_Qb4n_user = []

            # for loop that assigns the values of N and Z to each array
            for i in xrange(0,s1):

                if Z[i] >= Z_low_user and Z[i] <= Z_high_user and N[i] >= N_low_user and N[i] <= N_high_user: 
                    N_user = np.append(N_user,N[i])
                    Z_user = np.append(Z_user,Z[i])
      
                if Z[i] >= 0 and Z[i] <= Z_high_user+1:
                    Z_user_magic = np.append(Z_user_magic,Z[i])
                    N_user_magic = np.append(N_user_magic,N[i])

                # for loop that assigns N and Z values to the arrays only if the isotopes have a Qbn greater than 0 and the Qbn value is not equal to '1010'
                #(a random number denoting isotopes with unknown Qbn values) at that N and Z value

                if Z[i] >= Z_low_user and Z[i] <= Z_high_user and N[i] >= N_low_user and N[i] <= N_high_user and Qbn[i] > 0 and Qbn[i] != 1010: 
                    N_Qbn_user = np.append(N_Qbn_user,N[i])
                    Z_Qbn_user = np.append(Z_Qbn_user,Z[i])

                if Z[i] >= Z_low_user and Z[i] <= Z_high_user and N[i] >= N_low_user and N[i] <= N_high_user and Qb2n[i] > 0 and Qb2n[i] != 1010: 
                    N_Qb2n_user = np.append(N_Qb2n_user,N[i])
                    Z_Qb2n_user = np.append(Z_Qb2n_user,Z[i])

                if Z[i] >= Z_low_user and Z[i] <= Z_high_user and N[i] >= N_low_user and N[i] <= N_high_user and Qb3n[i] > 0 and Qb3n[i] != 1010:  
                    N_Qb3n_user = np.append(N_Qb3n_user,N[i])
                    Z_Qb3n_user = np.append(Z_Qb3n_user,Z[i])

                if Z[i] >= Z_low_user and Z[i] <= Z_high_user and N[i] >= N_low_user and N[i] <= N_high_user and Qb4n[i] > 0 and Qb4n[i] != 1010:  
                    N_Qb4n_user = np.append(N_Qb4n_user,N[i]) 
                    Z_Qb4n_user = np.append(Z_Qb4n_user,Z[i])
    #----------------------------------------------------------------------------

            # this part of the code makes an array for only the N and Z values that denote a stable nuclei
            N_stable_user = []
            Z_stable_user = []

            for i in xrange(0,s2):

                if Z_stable[i] >= Z_low_user and Z_stable[i] <= Z_high_user and N_stable[i] >= N_low_user and N_stable[i] <= N_high_user:
                    N_stable_user = np.append(N_stable_user,N_stable[i])
                    Z_stable_user = np.append(Z_stable_user,Z_stable[i])
    #----------------------------------------------------------------------------

            # assigns the N and Z values of the isotopes with probability > 0
            N_P1n_user = []
            Z_P1n_user = []
            
            N_P1n_user_value = []
            Z_P1n_user_value = []
            P1n_user = []

            P1n_ratio = []
            N_P1n_ratio = []
            Z_P1n_ratio = []

            N_P2n_user = []
            Z_P2n_user = []
            
            N_P2n_user_value = []
            Z_P2n_user_value = []
            P2n_user = []

            P2n_ratio = []
            N_P2n_ratio = []
            Z_P2n_ratio = []

            N_P3n_user = []
            Z_P3n_user = []
            
            N_P3n_user_value = []
            Z_P3n_user_value = []
            P3n_user = []

            P3n_ratio = []
            N_P3n_ratio = []
            Z_P3n_ratio = []

            N_P4n_user = []
            Z_P4n_user = []
            
            N_P4n_user_value = []
            Z_P4n_user_value = []
            P4n_user = []

            P4n_ratio = []
            N_P4n_ratio = []
            Z_P4n_ratio = []

            ELE_name_user = []
            N_ELE = []
            Z_ELE = []
            A_ELE = []

            Special_user = []
            N_spec = []
            Z_spec = []

            N_P1n_user_iso1 = []
            Z_P1n_user_iso1 = []
            N_P2n_user_iso1 = []
            Z_P2n_user_iso1 = []

            P1n_user_iso1 = []
            P2n_user_iso1 = []

            N_P1n_user_iso2 = []
            Z_P1n_user_iso2 = []
            N_P2n_user_iso2 = []
            Z_P2n_user_iso2 = []

            P1n_user_iso2 = []
            P2n_user_iso2 = []
            
            for i in xrange(0,size_P):

                if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and P1n[i] != 0 and Special[i] <= 5: 
                    N_P1n_user = np.append(N_P1n_user,N_P[i]) 
                    Z_P1n_user = np.append(Z_P1n_user,Z_P[i])

                    if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                        N_P1n_user_value = np.append(N_P1n_user_value,N_P[i])
                        Z_P1n_user_value = np.append(Z_P1n_user_value,Z_P[i])
                        P1n_user = np.append(P1n_user,P1n[i])
                        if P1n_MOE[i] != 0:
                            ratio = P1n[i]/P1n_MOE[i]
                            P1n_ratio = np.append(P1n_ratio,ratio)
                            N_P1n_ratio=np.append(N_P1n_ratio,N_P[i]) 
                            Z_P1n_ratio=np.append(Z_P1n_ratio,Z_P[i])

                    if P2n[i] != 0: 
                        N_P2n_user = np.append(N_P2n_user,N_P[i])
                        Z_P2n_user = np.append(Z_P2n_user,Z_P[i])

                        if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                            N_P2n_user_value = np.append(N_P2n_user_value,N_P[i])
                            Z_P2n_user_value = np.append(Z_P2n_user_value,Z_P[i])
                            P2n_user = np.append(P2n_user,P2n[i])
                            if P2n_MOE[i] != 0:
                                ratio=P2n[i]/P2n_MOE[i]
                                P2n_ratio=np.append(P2n_ratio,ratio)
                                N_P2n_ratio=np.append(N_P2n_ratio,N_P[i])
                                Z_P2n_ratio=np.append(Z_P2n_ratio,Z_P[i])

                    if P3n[i] != 0: 
                        N_P3n_user = np.append(N_P3n_user,N_P[i])
                        Z_P3n_user = np.append(Z_P3n_user,Z_P[i])

                        if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                            N_P3n_user_value = np.append(N_P3n_user_value,N_P[i])
                            Z_P3n_user_value = np.append(Z_P3n_user_value,Z_P[i])
                            P3n_user = np.append(P3n_user,P3n[i]) 
                            if P3n_MOE[i] != 0:
                                ratio=P3n[i]/P3n_MOE[i]
                                P3n_ratio=np.append(P3n_ratio,ratio)
                                N_P3n_ratio=np.append(N_P3n_ratio,N_P[i])
                                Z_P3n_ratio=np.append(Z_P3n_ratio,Z_P[i])

                    if P4n[i] != 0: 
                        N_P4n_user = np.append(N_P4n_user,N_P[i])
                        Z_P4n_user = np.append(Z_P4n_user,Z_P[i])

                        if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user:
                            N_P4n_user_value = np.append(N_P4n_user_value,N_P[i])
                            Z_P4n_user_value = np.append(Z_P4n_user_value,Z_P[i])
                            P4n_user = np.append(P4n_user,P4n[i])
                        
                if Z_P[i] >= Z_low_user and Z_P[i] <= Z_high_user and N_P[i] > N_low_user and N_P[i] < N_high_user and P1n[i] != 0: 

                    N_ELE = np.append(N_ELE,N_P[i])
                    Z_ELE = np.append(Z_ELE,Z_P[i])
                    A_calc = N_P[i] + Z_P[i]
                    ELE_name_user = np.append(ELE_name_user,ELE_names[i])
                    A_ELE = np.append(A_ELE,A_calc)

                    if Special[i] == 1: 
                        Special_user = np.append(Special_user,Special_sym[0])
                        N_spec = np.append(N_spec,N_P[i])
                        Z_spec = np.append(Z_spec,Z_P[i])

                    if Special[i] == 2: 
                        Special_user = np.append(Special_user,Special_sym[1])
                        N_spec = np.append(N_spec,N_P[i])
                        Z_spec = np.append(Z_spec,Z_P[i])
      
                    if Special[i] == 3: 
                        Special_user = np.append(Special_user,Special_sym[2])
                        N_spec = np.append(N_spec,N_P[i])
                        Z_spec = np.append(Z_spec,Z_P[i])

                    if Special[i] == 4:
                         Special_user = np.append(Special_user,Special_sym[3])
                         N_spec = np.append(N_spec,N_P[i])
                         Z_spec = np.append(Z_spec,Z_P[i])

            for i in xrange(0,size_P_iso1): 
                if Z_P_iso1[i] >= Z_low_user and Z_P_iso1[i] <= Z_high_user and N_P_iso1[i] > N_low_user and N_P_iso1[i] < N_high_user and Special_iso1[i] > 5 and P1n_iso1[i] != 0:
                    N_P1n_user_iso1 = np.append(N_P1n_user_iso1,N_P_iso1[i]) 
                    Z_P1n_user_iso1 = np.append(Z_P1n_user_iso1,Z_P_iso1[i])
                    P1n_user_iso1 = np.append(P1n_user_iso1,P1n_iso1[i])

                    if P2n_iso1[i] != 0: 
                        N_P2n_user_iso1 = np.append(N_P2n_user_iso1,N_P_iso1[i])
                        Z_P2n_user_iso1 = np.append(Z_P2n_user_iso1,Z_P_iso1[i])
                        P2n_user_iso1 = np.append(P2n_user_iso1,P2n_iso1[i])

            for i in xrange(0,size_P_iso2):
                if Z_P_iso2[i] >= Z_low_user and Z_P_iso2[i] <= Z_high_user and N_P_iso2[i] > N_low_user and N_P_iso2[i] < N_high_user and Special_iso2[i] > 5 and P1n_iso2[i] != 0:
                    N_P1n_user_iso2 = np.append(N_P1n_user_iso2,N_P_iso2[i])
                    Z_P1n_user_iso2 = np.append(Z_P1n_user_iso2,Z_P_iso2[i])
                    P1n_user_iso2 = np.append(P1n_user_iso2,P1n_iso2[i])

                    if P2n_iso2[i] != 0: 
                        N_P2n_user_iso2 = np.append(N_P2n_user_iso2,N_P_iso2[i])
                        Z_P2n_user_iso2 = np.append(Z_P2n_user_iso2,Z_P_iso2[i])
                        P2n_user_iso2 = np.append(P2n_user_iso2,P2n_iso2[i])
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

            if len(N_user) != 0:
                plt.plot(N_user,Z_user,marker='s',color='0.8',markersize=msize,linestyle='')
                c1=1
            if len(N_stable_user) != 0:
                plt.plot(N_stable_user,Z_stable_user,marker='s',color=color1,markersize=msize,linestyle='')
                c2=1

            if len(N_Qbn_user) != 0:
                plt.plot(N_Qbn_user,Z_Qbn_user,marker='s',color=color2,markersize=msize,linestyle='')
                c3=1
            if len(N_Qb2n_user) != 0:
                plt.plot(N_Qb2n_user,Z_Qb2n_user,marker='s',color=color3,markersize=msize,linestyle='')
                c4=1
                
            if len(N_Qb3n_user) != 0:
                plt.plot(N_Qb3n_user,Z_Qb3n_user,marker='s',color=color4,markersize=msize,linestyle='')
                c5=1
            if len(N_Qb4n_user) != 0:
                plt.plot(N_Qb4n_user,Z_Qb4n_user,marker='s',color=color5,markersize=msize,linestyle='')
                c6=1

            if len(N_P1n_user) != 0:
                plt.plot(N_P1n_user,Z_P1n_user,marker='s',color=color1,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')
                c7=1
            if len(N_P2n_user) != 0:
                plt.plot(N_P2n_user,Z_P2n_user,marker='s',color=color6,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')
                c8=1
            if len(N_P3n_user) != 0:
                plt.plot(N_P3n_user,Z_P3n_user,marker='s',color=color7,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')
                c9=1
            if len(N_P4n_user) != 0:
                plt.plot(N_P4n_user,Z_P4n_user,marker='s',color=color8,markeredgewidth=mew,markersize=msize,fillstyle='none',linestyle='')
                c10=1

            if len(N_ELE) != 0 and len(ELE_name_user) != 0 and Delta_Z <= 10: 
                #xyouts,N_spec-0.35,Z_spec+0.28,Special_user,charsize=1,color=color1
                for i in range(0,len(N_ELE)):
                    ELE_info = ' '.join([ELE_name_user[i].rstrip('\n'),str(int(A_ELE[i]))])
                    plt.text(N_ELE[i]-N_ELE_adj1,Z_ELE[i]+Z_ELE_adj1,ELE_info,fontsize=fontsize_set_1)

            if ratio_user == 1: 
                if len(N_P1n_ratio) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                    for i in xrange(0,len(N_P1n_ratio)):
                        str_ratio="{0:.2f}".format(P1n_ratio[i])
                        plt.text(N_P1n_ratio[i]-N_adj_r,Z_P1n_ratio[i]+Z_adj_1,str_ratio,fontsize=fontsize_set_2)
                      
                if len(N_P2n_ratio) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                    for i in xrange(0,len(N_P2n_ratio)):
                        str_ratio="{0:.2f}".format(P2n_ratio[i])
                        plt.text(N_P2n_ratio[i]-N_adj_r,Z_P2n_ratio[i]+Z_adj_2,str_ratio,fontsize=fontsize_set_2)

                if len(N_P3n_ratio) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                    for i in xrange(0,len(N_P3n_ratio)):
                        str_ratio="{0:.2f}".format(P3n_ratio[i])
                        plt.text(N_P3n_ratio[i]-N_adj_r,Z_P3n_ratio[i]+Z_adj_3,str_ratio,fontsize=fontsize_set_2)

                if len(N_P4n_ratio) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                    for i in xrange(0,len(N_P4n_ratio)):
                        str_ratio="{0:.2f}".format(P4n_ratio[i])
                        plt.text(N_P4n_ratio[i]-N_adj_r,Z_P4n_ratio[i]+Z_adj_4,str_ratio,fontsize=fontsize_set_2)

            if ratio_user != 1:
                if len(N_P1n_user_value) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                    for i in xrange(0,len(N_P1n_user_value)):
                        str_ratio="{0:.2f}".format(P1n_user[i])
                        plt.text(N_P1n_user_value[i]-N_adj,Z_P1n_user_value[i]+Z_adj_1,str_ratio+'%',fontsize=fontsize_set_3)
                            
                if len(N_P2n_user_value) != 0 and Delta_Z <= 10 and Delta_N <= 10:
                    for i in xrange(0,len(N_P2n_user_value)):
                        str_ratio="{0:.2f}".format(P2n_user[i])
                        plt.text(N_P2n_user_value[i]-N_adj,Z_P2n_user_value[i]+Z_adj_2,str_ratio+'%',fontsize=fontsize_set_3)

                if len(N_P3n_user_value) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                    for i in xrange(0,len(N_P3n_user_value)):
                        str_ratio="{0:.2f}".format(P3n_user[i])
                        plt.text(N_P3n_user_value[i]-N_adj,Z_P3n_user_value[i]+Z_adj_3,str_ratio+'%',fontsize=fontsize_set_3)

                if len(N_P4n_user_value) != 0 and Delta_Z <= 7 and Delta_N <= 7:
                    for i in xrange(0,len(N_P4n_user_value)):
                        str_ratio="{0:.2f}".format(P4n_user[i])
                        plt.text(N_P4n_user_value[i]-N_adj,Z_P4n_user_value[i]+Z_adj_4,str_ratio+'%',fontsize=fontsize_set_3)

                if len(N_P1n_user_iso1) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                    for i in xrange(0,len(N_P1n_user_iso1)):
                        str_ratio="{0:.2f}".format(P1n_user_iso1[i])
                        plt.text(N_P1n_user_iso1[i]-N_adj_i,Z_P1n_user_iso1[i]+Z_adj_1,'| '+str_ratio+'%',fontsize=fontsize_set_3)
                        
                if len(N_P2n_user_iso1) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                    for i in xrange(0,len(N_P2n_user_iso1)):
                        str_ratio="{0:.2f}".format(P2n_user_iso1[i])
                        plt.text(N_P2n_user_iso1[i]-N_adj_i,Z_P2n_user_iso1[i]+Z_adj_2,'| '+str_ratio+'%',fontsize=fontsize_set_3)

                if len(N_P1n_user_iso2) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                    for i in xrange(0,len(N_P1n_user_iso2)):
                        str_ratio="{0:.2f}".format(P1n_user_iso2[i])
                        plt.text(N_P1n_user_iso2[i]-N_adj_i,Z_P1n_user_iso2[i]+Z_adj_3,'| '+str_ratio+'%',fontsize=fontsize_set_3)

                if len(N_P2n_user_iso2) != 0 and Delta_Z <= 4 and Delta_N <= 4:
                    for i in xrange(0,len(N_P2n_user_iso2)):
                        str_ratio="{0:.2f}".format(P2n_user_iso2[i])
                        plt.text(N_P2n_user_iso2[i]-N_adj_i,Z_P2n_user_iso2[i]+Z_adj_4,'| '+str_ratio+'%',fontsize=fontsize_set_3)
                
            plt.axis('scaled')
            g=plt.gca()
            plt.xlim(N_low_user,N_high_user)
            plt.ylim(Z_low_user-1,Z_high_user+1)
            
            if ratio_user == 1:
                plt.title("Ratio between theoretical & experimental data")
            if ratio_user != 1 and Delta_Z > 10 and Delta_N > 10:
                plt.title("Experimentally known beta-delayed neutron emitters")
            if ratio_user != 1 and Delta_Z <= 10 and Delta_Z <= 10:
                plt.title("Experimentally known beta-delayed neutron emitters")
                
            plt.xlabel("N")
            plt.ylabel("Z")

            if N_high_user >= 8 and N_low_user <= 8:  
                plt.plot(N_user_magic*0.+8.5,Z_user_magic,color=color1,linewidth=lw1)  
                plt.plot(N_user_magic*0.+7.5,Z_user_magic,color=color1,linewidth=lw1)
                  
            if N_high_user >= 20 and N_low_user <= 20:
                plt.plot(N_user_magic*0.+20.5,Z_user_magic,color=color1,linewidth=lw1) 
                plt.plot(N_user_magic*0.+19.5,Z_user_magic,color=color1,linewidth=lw1)
                   
            if N_high_user >= 28 and N_low_user <= 28:
                plt.plot(N_user_magic*0.+28.5,Z_user_magic,color=color1,linewidth=lw1)
                plt.plot(N_user_magic*0.+27.5,Z_user_magic,color=color1,linewidth=lw1)     

            if N_high_user >= 50 and N_low_user <= 50:
                plt.plot(N_user_magic*0.+50.5,Z_user_magic,color=color1,linewidth=lw1)
                plt.plot(N_user_magic*0.+49.5,Z_user_magic,color=color1,linewidth=lw1)
                     
            if N_high_user >= 82 and N_low_user <= 82:
                plt.plot(N_user_magic*0.+82.5,Z_user_magic,color=color1,linewidth=lw1)
                plt.plot(N_user_magic*0.+81.5,Z_user_magic,color=color1,linewidth=lw1)
                       
            if N_high_user >= 126 and N_low_user <= 126:
                plt.plot(N_user_magic*0.+126.5,Z_user_magic,color=color1,linewidth=lw1) 
                plt.plot(N_user_magic*0.+125.5,Z_user_magic,color=color1,linewidth=lw1) 

            if Z_high_user >= 8 and Z_low_user <= 8:
                plt.plot(N_user_magic,Z_user_magic*0.+8.5,color=color1,linewidth=lw2) 
                plt.plot(N_user_magic,Z_user_magic*0.+7.5,color=color1,linewidth=lw2)
                  
            if Z_high_user >= 20 and Z_low_user <= 20:
                plt.plot(N_user_magic,Z_user_magic*0.+20.5,color=color1,linewidth=lw2) 
                plt.plot(N_user_magic,Z_user_magic*0.+19.5,color=color1,linewidth=lw2)
                 
            if Z_high_user >= 28 and Z_low_user <= 28:
                plt.plot(N_user_magic,Z_user_magic*0.+28.5,color=color1,linewidth=lw2)
                plt.plot(N_user_magic,Z_user_magic*0.+27.5,color=color1,linewidth=lw2)             

            if Z_high_user >= 50 and Z_low_user <= 50:
                plt.plot(N_user_magic,Z_user_magic*0.+50.5,color=color1,linewidth=lw2)
                plt.plot(N_user_magic,Z_user_magic*0.+49.5,color=color1,linewidth=lw2)

            if Z_high_user >= 82 and Z_low_user <= 82:
                plt.plot(N_user_magic,Z_user_magic*0.+82.5,color=color1,linewidth=lw2)
                plt.plot(N_user_magic,Z_user_magic*0.+81.5,color=color1,linewidth=lw2)

            if Z_high_user >= 126 and Z_low_user <= 126:
                plt.plot(N_user_magic,Z_user_magic*0.+126.5,color=color1,linewidth=lw2)
                plt.plot(N_user_magic,Z_user_magic*0.+125.5,color=color1,linewidth=lw2)

            if Delta_N == 10 and Delta_Z == 10 or Delta_N == 7 and Delta_Z == 7 or Delta_N == 4 and Delta_Z == 4:
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

            if Delta_N <= 10 and Delta_Z <= 10:
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
