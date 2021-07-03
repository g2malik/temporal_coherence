# --- 
# aims: reads data on number of UMZs and plots pdf
# calls: none
# modefication history: gmalik, July, 2021; 

# --------------------------------
# import libraries 

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
# main

fname = r'''C:\Users\gagan\Documents\Work\Results\Temporal Coherence\cumulative_peaks_mean.txt'''
f = open (fname, mode = 'r')
tol = 0.02
wall = 0
middle1 = 0
middle2 = 0
freestream = 0
random = 0
#UMZ_order = []
peaks_before = []
peaks_current = []

labels = []
label = ''
for line in f:
    if (line.startswith("z") or line.startswith("t"))  == True:
        #UMZ_order = []
        peaks_before = []
        label = line

    else:
        lst = line.split()
        UMZs_str = int(lst[0])
        std = lst[1]
        for ii in range(2,2+UMZs_str):
            peaks_current.append(float(lst[ii]))
        #UMZ_order.append(UMZs_str)
        destroyed_peaks = []
        nearest_current_peaks = []
        if (len(peaks_before) - len(peaks_current)) == 1 and len(peaks_current)!=0:
            for j in range(len(peaks_before)):
                nearest_current_peaks.append(find_nearest(peaks_current, peaks_before[j])[1])
                if np.abs(peaks_before[j] - nearest_current_peaks[j])> tol: #doesnt include new peaks that are close to old ones
                    destroyed_peaks.append(j)
            if len(destroyed_peaks)<1:
                destroyed_peaks.append(np.abs(np.asarray(peaks_before) - np.asarray(nearest_current_peaks)).argmax()) #includes new close peaks
            
            #print(destroyed_peaks)
            if len(destroyed_peaks)==1:
                if destroyed_peaks[0] == 0:
                    wall+=1
                    labels.append(label)
                    #print("wall")
                elif destroyed_peaks[0] == (len(peaks_before)-1):
                    freestream+=1
                    #print("free")
                elif destroyed_peaks[0] == 1:
                    middle1+=1
                    #print("middle")
                elif destroyed_peaks[0] == 2:
                    middle2+=1
                    #print("middle")
            else:
                random+=1


        peaks_before = peaks_current.copy()
        peaks_current = []

print("# of UMZs destroyed near wall: ", wall)
#print(labels)
print("# of UMZs destroyed at middle: ",middle1)
print("# of UMZs destroyed at middle: ",middle2)
print("# of UMZs destroyed near freastream: ",freestream)
print(random)