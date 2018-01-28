import numpy as np
from scipy.interpolate import griddata
import xml.etree.ElementTree as ET
from os import listdir
from os.path import join
from fnmatch import fnmatch
import matplotlib.pyplot as plt

#The target values to plot over
p_interp = np.linspace(0, 10, 500)
t_interp = np.linspace(0, 180, 500)

#Extracts the values as a dictionary indexed by: vals[structure][temperature][pressure] = enthalpy
vals={}

for i in ["bcc", "fcc"]:
    temps={}
    if i == "bcc": folder = "BCC_relaxation/phonons/"
    else: folder = "FCC_relaxation/phonons/"
    for f in listdir(join(folder, "pt_fits")):
        if fnmatch(f, "*.xml"):
            temp = float(f.split(".")[2]+"."+f.split(".")[3])
            tree=ET.parse(join(folder, "pt_fits", f))
            pressures={}
            for line in tree.find("FIT_CHECK").find("VOL_ENE_EFIT_DELTA_P_GIBBS").text.splitlines():
                split=line.split()
                if split!=[]:
                    pressures[float(split[4])/10.0]=float(split[5])
            temps[temp]=pressures
    vals[i]=temps

#Perform the interpolation
for s in vals.keys():
    xs = []
    ys = []
    zs = []
    for t in vals[s].keys():
        for p in vals[s][t].keys():
            xs.append(p)
            ys.append(t)
            zs.append(vals[s][t][p])
    vals[s]["p_interp"], vals[s]["t_interp"] = np.meshgrid(p_interp, t_interp)
    vals[s]["e_interp"] = griddata((xs, ys), zs, (vals[s]["p_interp"], vals[s]["t_interp"]), method="cubic")

#Check which value has a lower energy at each point
bcc_lower = np.vectorize(lambda x: int(x))(vals["bcc"]["e_interp"]<vals["fcc"]["e_interp"])
print(bcc_lower)
plt.contourf(p_interp, t_interp, bcc_lower, 1)
plt.show()

