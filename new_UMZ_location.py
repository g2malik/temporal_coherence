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
tol = 0.025
wall = 0
middle1 = 0
middle2 = 0
freestream = 0
random = 0
UMZ_order = []
peaks_old = []
peaks_current = []
for line in f:
    if (line.startswith("z") or line.startswith("t"))  == True:
        UMZ_order = []
        peaks_old = []

    else:
        lst = line.split()
        UMZs_str = int(lst[0])
        std = lst[1]
        for ii in range(2,2+UMZs_str):
            peaks_current.append(float(lst[ii]))
        UMZ_order.append(UMZs_str)
        new_peaks = []
        nearest_old_peaks = []
        if (len(peaks_current) - len(peaks_old)) == 1 and len(peaks_old)!=0:
            for j in range(len(peaks_current)):
                nearest_old_peaks.append(find_nearest(peaks_old, peaks_current[j])[1])
                if np.abs(peaks_current[j] - nearest_old_peaks[j])> tol: #doesnt include new peaks that are close to old ones
                    new_peaks.append(j)
            if len(new_peaks)<1:
                new_peaks.append(np.abs(np.asarray(peaks_current) - np.asarray(nearest_old_peaks)).argmax()) #includes new close peaks
            
            #print(new_peaks)
            if len(new_peaks)==1:
                if new_peaks[0] == 0:
                    wall+=1
                    #print("wall")
                elif new_peaks[0] == (len(peaks_current)-1):
                    freestream+=1
                    #print("free")
                elif new_peaks[0] == 1:
                    middle1+=1
                    #print("middle")
                elif new_peaks[0] == 2:
                    middle2+=1
                    #print("middle")
            else:
                random+=1


        peaks_old = peaks_current.copy()
        peaks_current = []

print(wall)
print(middle1)
print(middle2)
print(freestream)
print(random)