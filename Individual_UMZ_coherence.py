# --- 
# aims: reads data on number of UMZs and calcualtes how long individual UMZs are coherent for
# calls: none
# modefication history: gmalik, July, 2021; 

# --------------------------------
# import libraries 

from itertools import count
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl 
from num2words import num2words

# --------------------------------
# find closest values
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx,array[idx] #returns tuple of index and value

# --------------------------------
# find index of same value
def find_tracker(value):
    idx = np.where(tracker == value)
    if np.shape(idx) == 1:
        return idx[0]
    if np.shape(idx) == 0:
        return 7 #7 means not present in tracker
    if np.shape(idx) >1:
        print("tracker error")    

# --------------------------------
# find next available counter space
def find_counter_space():
    for index in range(np.shape(tracker)):
        if tracker[index] == 0:
            return index
        else:
            print("no space in counter")
    
# --------------------------------
# main

fname = r'''C:\Users\gagan\Documents\Work\Results\Temporal Coherence\cumulative_peaks_mean.txt'''
f = open (fname, mode = 'r')
tol = 0.02

peaks_old = []
peaks_current = []

counter = np.array((0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0))  #(0: first velocity) (1: # of frames)
tracker = np.array([(0,False), (0,False), (0,False), (0,False), (0,False), (0,False), (0,False)]) #(0: last recorded velocity) (1: if recently changed)

labels = []
for i in range(55):
    line = f.readline()
    if (line.startswith("z") or line.startswith("t"))  == True: # store label and counter and reset everything
        label  = line
        
        
        
        
        peaks_old = []
        counter = np.array([(0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0)])
        tracker = np.array([(0,False), (0,False), (0,False), (0,False), (0,False), (0,False), (0,False)])

    else:
        lst = line.split()
        UMZs_str = int(lst[0])
        std = lst[1]
        for ii in range(2,2+UMZs_str):
            peaks_current.append(float(lst[ii]))
        nearest_old_peaks = []

        for j in range(len(peaks_current)):
            nearest_old_peaks.append(find_nearest(peaks_old, peaks_current[j])[1])

            if np.abs(peaks_current[j] - nearest_old_peaks[j])< tol: #If it a coherent peak
                count_index = find_tracker(nearest_old_peaks[j]) #Checks if already counting
                if count_index != 7: 
                    counter[count_index,1] +=1 #Add 1 to the location of counter
                    tracker[count_index,0] = peaks_current[j] #Put in current velocity in the tracker
                    tracker[count_index,1] = True
                
                elif count_index == 7: #Creates new counter and start counting
                    new_space = find_counter_space()
                    counter[new_space,0] = nearest_old_peaks[j]
                    counter[new_space,1] = 2
                    tracker[new_space,0] = peaks_current[j]
                    tracker[new_space,1] = True
            
            else: #If not a coherent peak do nothing?
                pass
        for jj in range(len(tracker[:,0])): # Someway to reset the counter if stops being coherent
            if tracker[jj,1] == False:
                



                
        
        
        #if len(new_peaks)<1:
            #new_peaks.append(np.abs(np.asarray(peaks_current) - np.asarray(nearest_old_peaks)).argmax()) #includes new close peaks
        
        peaks_old = peaks_current.copy()
        peaks_current = []