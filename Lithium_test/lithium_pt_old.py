import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from os import listdir
from os.path import join
from fnmatch import fnmatch
from scipy.interpolate import interp2d, griddata
import matplotlib.pyplot as plt

#Extracts the values as a dictionary indexed by: vals[structure][temperature][pressure] = enthalpy

vals={}

for i in ["bcc", "fcc"]:
    temps={}
    for f in listdir(join(i, "pt_fits")):
        if fnmatch(f, "*.xml"):
            temp = float(f.split(".")[2]+"."+f.split(".")[3])
            tree=ET.parse(join(i, "pt_fits", f))
            pressures={}
            for line in tree.find("FIT_CHECK").find("VOL_ENE_EFIT_DELTA_P_GIBBS").text.splitlines():
                split=line.split()
                if split!=[]:
                    pressures[float(split[4])/10.0]=float(split[5])
            temps[temp]=pressures
    vals[i]=temps

#for struc in vals:
#    print(struc)
#    for temp in vals[struc]:
#        print(temp)
#        for pressure in vals[struc][temp]:
#            print(pressure, vals[struc][temp][pressure])


#Because the pressures aren't on a regular grid, we have to input each point separately to the interp2d function
#with x=[] y=[] z=[] all being 1d arrays
"""
fitting = {}
for struct in vals:
    print(struct)
    fitting[struct]={}
    fitting[struct]["e"]=[] #enthalpy
    fitting[struct]["t"]=[] #The different values of temperature
    fitting[struct]["pp"]=[] #pressure mesh
    fitting[struct]["tt"]=[] #temp mesh
    for temp in sorted(vals[struct].keys()):
        fitting[struct]["t"].append(temp)
        for pressure in sorted(vals[struct][temp].keys()):
            fitting[struct]["tt"].append(temp)
            fitting[struct]["pp"].append(pressure)
            fitting[struct]["e"].append(vals[struct][temp][pressure])
    fitting[struct]["f"]=interp2d(fitting[struct]["pp"], fitting[struct]["tt"], fitting[struct]["e"], kind='cubic')
for t in range(0, 100):
    print(fitting["fcc"]["f"](0, t))
"""
#Try the interpolation with griddata rather than interp2d
fitting = {}
for struct in vals:
    print(struct)
    fitting[struct]={}
    fitting[struct]["e"]=[] #enthalpy
    fitting[struct]["t"]=[] #The different values of temperature
    fitting[struct]["pp"]=[] #pressure mesh
    fitting[struct]["tt"]=[] #temp mesh
    for temp in sorted(vals[struct].keys()):
        fitting[struct]["t"].append(temp)
        for pressure in sorted(vals[struct][temp].keys()):
            fitting[struct]["tt"].append(temp)
            fitting[struct]["pp"].append(pressure)
            fitting[struct]["e"].append(vals[struct][temp][pressure])
    fitting[struct]["t_grid"], fitting[struct]["p_grid"] = np.mgrid[0:3:10j, 0:50:5j]
    fitting[struct]["f"]=griddata((fitting[struct]["pp"], fitting[struct]["tt"]), fitting[struct]["e"], 
            (fitting[struct]["p_grid"], fitting[struct]["t_grid"]), method="nearest")

#checking which enthalpy is lowest at a set of points:
p=np.arange(0, 10, 0.5)
t=np.arange(0, 300, 40)

"""
lowest_structure=[]
for temp in t:
    lowest_structure.append([])
    for pressure in p:
        if fitting["fcc"]["f"](pressure, temp)[0]<fitting["bcc"]["f"](pressure, temp)[0]:
            lowest_structure[-1].append(1)
        else:
            lowest_structure[-1].append(0)

i=0
lowest_structure.reverse()
print("1=fcc, 0=bcc")
for line in lowest_structure:
    print("{:03g} || {}".format(t[-i-1], line))
    i+=1
print("-"*40)
print("      ", [int(round(i)) for i in p])
"""
print(fitting["fcc"]["f"])
