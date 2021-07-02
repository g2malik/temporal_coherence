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

fname = r'''C:\Users\gagan\Documents\Work\Results\Temporal Coherence\cumulative_no_UMZ.txt'''
f = open (fname, mode = 'r')
one = []
two = []
three = []
four = []
five = []
six = []

UMZ_order = []
for line in f:
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
        UMZ_order.append(int(UMZs_str))

print(np.mean(one))
print(np.mean(two))
print(np.mean(three))
print(np.mean(four))
print(np.mean(five))







