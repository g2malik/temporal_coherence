# --- 
# aims: implement the GMM and the KDE to snapshots while changing the frame of reference
# calls: kde_plus_gmm
# modefication history: gmalik, June, 2021; 

# --------------------------------
# import libraries 

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl 
import time 
from scipy.interpolate import griddata 
from pylab import *
from kde_plus_gmm import kde_plus_gmm
# --------------------------------
# ------ Read data from file ------
path = '/gpfs/fs0/scratch/j/jphickey/jphickey/Boundary_Layer_PNAS_2017/'
testing_file = '/gpfs/fs0/scratch/j/jphickey/g2malik/working_code/temporal_coherence/No_UMZs2.dat' # temporary file for debugging
t = open(testing_file, "w")
total_snaps = 0
coherent_snaps = 0
start_t = 0
for xx in range(2,3):
    for zz in range(1,513,50):    
        t.write("t:%d "%(start_t))
        t.write("z:%d "%(zz))
        t.write("x:%d"%(xx+1))
        t.write("\n")
        x_shift = 0
        for time in range (start_t,37):
            time_stamp = '%02d' %(time)
            fname = path + 'restart_010' + time_stamp + '_ydelta_adrian_scalar_omega_uvw_08240_10565.dat'
            f = open (fname, mode = 'r') 
            print('--- the %d th snapshot in time ---'%time)

            # ----- choose the starting position/parameters -----
            btfti = 0.04 # see Wu, Wallace and Hickey 2019, PoF 
            binbin = 50 

            first_z = 1     # start from the position at Z-label = ? {1...513}
            last_z = 513
            first_x = 0     # start from the position at X-label = ? {0...2326}
            last_x = 2326
            first_y = 105   # [1,400] skip the buffer layer -- 100 wall units 
            last_y = 400    

            y_interval = last_y - first_y + 1

            wall_length = 2000 
            x_interval = int(0.22 * wall_length) #0.29 ACCORDING TO SUMMARY BUT 440 POINTS IN CODE
            total_x_planes = int((last_x-first_x)/x_interval)
            # --------------------------------

            # ------ Calculate x_cordinates -----
            z_plane = zz
            x_plane = xx
            
            stax = first_x + x_shift + (x_interval * x_plane)
            skpx = last_x - x_interval 
            endx = stax + x_interval 
            # --------------------------------

            # ----skip / go to certain index -----
            for i in range(3):
                data = f.readline()
            for ii in range(stax-1):
                data = f.readline()
            for jj in range(first_y-1):
                for ii in range(last_x):
                    data = f.readline()
            for kk in range(z_plane-1):
                for jj in range(last_y):
                    for ii in range(last_x):
                        data = f.readline()
            # --------------------------------

            # ------- get velocity etc -------
            xy    = [[],[]] # computational grid
            uu    = []      # computational grid
            delta = []
            tt    = []
            small = 1e-15

            for j in range(y_interval):
                ylb = first_y + j + 1 # y-label grid 
                for i in range(x_interval):
                    data = f.readline()
                    lst = data.split()
                    x = float(lst[0]) - 10842.4  # minus the starting position at re_theta = 1800 
                    y = float(lst[1])
                    yod = float(lst[3])
                    xod = x / (y+small) * yod
                    if yod != 0:
                        d = y/yod #Calculates boundary layer thickness
                        delta.append(d)
                    tl = float(lst[5]) # passive scalar, index of btfti 
                    u = float(lst[7])
                    xy[0].append(xod)
                    xy[1].append(yod)
                    uu.append(u)
                    tt.append(tl)
                for i in range(skpx): # skip the x that we don't need 
                    data = f.readline()
            # --------------------------------

            # --------------------------------
            # interpolation to uniform grid    
            xmax = xy[0][-1]
            xmin = xy[0][0]
            ymax = xy[1][-1]
            ymin = xy[1][0]

            interpx = 400  # number of pts 
            interpy = 400
            xi=np.linspace(xmin,xmax,interpx)
            yi=np.linspace(ymin,ymax,interpy)

            XY  = np.meshgrid(xi,yi)
            UU  = griddata((xy[0],xy[1]), uu, (XY[0],XY[1]), method =  'cubic')
            TT  = griddata((xy[0],xy[1]), tt, (XY[0],XY[1]), method =  'cubic')
            if ymax ==0:
                break
            delta_points = int(interpy/ymax) #Finds the number of points that gives a yod value of 1

            # ----------------------------------
            # prepare the data for the histogram 
            uhis = []
            u_free = []

            for i in range(interpx):
                for j in range(interpy):
                    # detection of the turbultent region; BTFTI 
                    lll = TT[i][j]
                    if lll > btfti :
                        uhis.append(UU[i][j]) #uhis doesnt include turbulent region but UU does
            # --------------------------------
            # GMM - main 
            model = kde_plus_gmm(XY,UU,uhis,z_plane,binbin,x_plane+1,time_stamp,testing_file, delta_points, btfti, TT)
            if model.coherent == True:
                coherent_snaps+=1
            t.write("%d "%(model.N_best))
            t.write("%.7f"%(np.mean(model.cov_g)))
            for mean in model.means_g:
                t.write(" %.3f"%(mean))
            t.write("\n")
            total_snaps += 1

            # --------------------------------
            # Calculate next frame)
            x_interval = 1.316070556640625 #x distance between adjascent indices
            dt = 112.5

            u_shift = np.mean(uhis)

            displacement = u_shift * dt

            x_shift = x_shift + int(displacement/x_interval)
print("coherent ratio = ", (coherent_snaps/total_snaps))
t.close()
print ('--- End of all ---')