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

fname = r'''C:\Users\gagan\Documents\Work\Results\Temporal Coherence\cumulative_peaks_mean.txt'''
f = open (fname, mode = 'r')
tol = 0.05
peaks_old = []
peaks_new = []
for i in range(31):
    if (line.startswith("z") or line.startswith("t"))  == True:
        time = 1
        for i in range(len(UMZ_order)):
            if i!=0 and UMZ_order[i] == UMZ_order[i-1]:
                time+=1
            if ((UMZ_order[i] != UMZ_order[i-1] or i==(len(UMZ_order)-1)) and time!=1):
                eval(num2words(UMZ_order[i-1])).append(time)
                time = 1

        UMZ_order = []
        pass 
    else:
        lst = line.split()
        UMZs_str = lst[0]
        std = lst[1]
        for ii in range(2,2+UMZ_str):


        UMZ_order.append(int(UMZs_str))