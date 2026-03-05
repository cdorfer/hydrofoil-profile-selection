import viiflow as vf
import viiflowtools.vf_tools as vft
import numpy as np
import matplotlib.pyplot as plt
import glob
from utils import re_number
from time import sleep
import pickle

import logging
logging.getLogger().setLevel(logging.WARNING)


# Read Airfoil Data

'''
S805 = vft.repanel(vft.read_selig("S805.dat"),N)
S805A = vft.repanel(vft.read_selig("S805A.dat"),N)

fig,ax = plt.subplots(1,1)
ax.plot(S805[0,:],S805[1,:],'-k',label="S805")
ax.plot(S805A[0,:],S805A[1,:],'-r',label="S805A")
ax.axis('equal')
ax.legend()
fig.show()
'''

#N = 220
#foilname = 'foils/goe398.dat'
#foil = vft.repanel(vft.read_selig(foilname),N)


AOARange = np.arange(-3, 3, 0.1)
results = {} # Dictionary of results


chord_length_m = 0.125
flow_speed_m_s = 13/3.6
Re = re_number(chord_length_m, flow_speed_m_s, temp_c=20, salt_water=False)
#Re = 1000000
print(f"Reynolds number: {Re}")
sleep(2)

ncrit = 4.5

s = vf.setup(Re=Re, Ncrit=ncrit, Alpha=AOARange[0], IterateWakes=False)
s.Silent = True
# (Maximum) internal iterations
s.Itermax = 100


#foil_profiles = list(glob.iglob('foils/*.dat'))
fails = []

N = 400

profiles = ['e230','hq010','lwk79100','n63010a','naca0010','naca001034','naca001035','naca001064','naca001065','naca001066','rae100','rae103','rae101','sc20010','rae102','e230','rae104','sd8020','fx79l100','lwk80100','fx76100','n0011sc','e297','joukowsk','nacam3','m3','n64012a','sc20012','s1012','ea61012','fx71120','j5012','naca16012','n64012','naca001264','naca001234','n0012','n63012a','e472','fx76120','ah85l120','fx79l120','lwk80120k25','naca0012h','e171','e168']

for i, foilname in enumerate(profiles):
    foilpath = f"foils/{foilname}.dat"
    print(f"Foil {i}/{len(profiles)} with path: {foilpath}")

    #if foilname in ['sc20402']:
    #    fails.append([foilname, 'excluded'])
    #    continue

    foil = vft.repanel(vft.read_selig(foilpath), N)
    results[foilname] = {}
    results[foilname]["AOA"] = []
    results[foilname]["CL"] = []
    results[foilname]["CD"] = []
    results[foilname]["CM"] = []
    results[foilname]["TRUP"] = []
    results[foilname]["TRLO"] = []
    init = True
    faults = 0

    for alpha in AOARange:
        # Set current alpha and set res/grad to None to tell viiflow that they are not valid
        s.Alpha = alpha
        res = None
        grad = None

        # Set-up and initialize based on inviscid panel solution
        # This calculates panel operator
        if init:
            #p = panel structure which contains airfoil geometries, wake geometries, viscid and invisic solutions and lift and moment coefficient
            #bl = boundary layer structure is a lift of structures of every airfoil including surface boundary layer and wake boundary layer
            #x = array used in the Newton iterator
            try:
                [p,bl,x] = vf.init([foil],s)
            except Exception as e:
                fails.append([foilname, e])
                break
            init = False



        try:
            [x,flag,res,grad,_] = vf.iter(x,bl,p,s,res,grad)
        except Exception as e:
            fails.append([foilname, e])
            break

        #if flag = True it converged
        #iterates and then overwrites p, bl and x once done



        # If converged add to cl/cd vectors (could check flag as well, but this allows custom tolerance 
        # to use the results anyways)
        if flag: 
            results[foilname]["AOA"].append(alpha)
            results[foilname]["CL"].append(p.CL)
            results[foilname]["CD"].append(bl[0].CD)
            results[foilname]["CM"].append(p.CM)
            results[foilname]["TRUP"].append(np.interp(bl[0].ST-bl[0].bl_fl.node_tr_up.xi[0],p.foils[0].S,p.foils[0].X[0,:]))
            results[foilname]["TRLO"].append(np.interp(bl[0].ST+bl[0].bl_fl.node_tr_lo.xi[0],p.foils[0].S,p.foils[0].X[0,:]))
            faults = 0
        else:
            faults+=1
            init = True

        #print(f"Assumed Mach number: {bl[0].Ma} or the invicid Mach number: {p.mach}")

        # Skip current polar if 4 unconverged results in a row
        if faults>3:
            print(f"Exiting RE {Re} polar calculation at AOA {alpha}°")
            break

pickle.dump(results, open('results.pkl', 'wb'))

print("Done")
print(fails)
'''
fix,ax = plt.subplots(3,2)
ax[0][0].plot(results["CD"],results["CL"], '--',color='r')
ax[0][1].plot(results["AOA"],results["CL"], '--',color='r')
ax[1][0].plot(results["AOA"], np.array(results["CL"])/np.array(results["CD"]), '--',color='r')
ax[1][1].plot(results["AOA"],results["CD"], '--',color='r')
ax[2][0].plot(results["AOA"],results["CM"], '--',color='r')
plt.grid(True)
plt.show()
'''


