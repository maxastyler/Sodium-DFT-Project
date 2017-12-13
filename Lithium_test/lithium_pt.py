import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from os import listdir
from os.path import join
from fnmatch import fnmatch

#Extracts the values as a dictionary indexed by: vals[structure][temperature][pressure] = enthalpy

vals={}

for i in ["bcc", "fcc"]:
    temps={}
    for f in listdir(join(i, "pt_fits")):
        if fnmatch(f, "*.xml"):
            temp = float(f.split(".")[2]+"."+f.split(".")[3])
            print(temp)
            tree=ET.parse(join(i, "pt_fits", f))
            pressures={}
            for line in tree.find("FIT_CHECK").find("VOL_ENE_EFIT_DELTA_P_GIBBS").text.splitlines():
                split=line.split()
                if split!=[]:
                    pressures[float(split[4])]=float(split[5])
            temps[temp]=pressures
    vals[i]=temps

for struc in vals:
    print(struc)
    for temp in vals[struc]:
        print(temp)
        for pressure in vals[struc][temp]:
            print(pressure, vals[struc][temp][pressure])


#Turning the dict into an array
