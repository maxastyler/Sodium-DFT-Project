import numpy as np
from scipy.interpolate import griddata
import xml.etree.ElementTree as ET
from os import listdir
from os.path import join
from fnmatch import fnmatch
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

#The target values to plot over
p_interp = np.linspace(-0.5, 5, 500)
t_interp = np.linspace(0, 175, 500)

#Extracts the values as a dictionary indexed by: vals[structure][temperature][pressure] = enthalpy
vals={}

for i in ["bcc", "fcc", "hcp"]:
    temps={}
    if i == "bcc": folder = "Na_BCC/phonons/"
    elif i == "fcc": folder = "Na_FCC/phonons/"
    else: folder = "Na_HCP/phonons/"
    for f in listdir(join(folder, "pt_fits")):
        if fnmatch(f, "*.xml"):
            temp = float(f.split(".")[2]+"."+f.split(".")[3])
            tree=ET.parse(join(folder, "pt_fits", f))
            pressures={}
            for line in tree.find("FIT_CHECK").find("VOL_ENE_EFIT_DELTA_P_GIBBS").text.splitlines():
                split=line.split()
                if split!=[]:
                    if i=="hcp":
                        pressures[float(split[4])/10.0]=float(split[5])/2
                    else:
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
#bcc_lower = np.vectorize(lambda x: int(x))(vals["bcc"]["e_interp"]<vals["fcc"]["e_interp"])
#hcp_lower = np.vectorize(lambda x: int(x))(vals["hcp"]["e_interp"]<vals["fcc"]["e_interp"])
for k in vals:
    #vals[k]["e_interp"] = np.vectorize(lambda x: float('inf') if x == np.NaN
    vals[k]["e_interp"] = np.nan_to_num(vals[k]["e_interp"])
hcp_lower = ((vals["hcp"]["e_interp"]<vals["fcc"]["e_interp"]) & (vals["hcp"]["e_interp"]<vals["bcc"]["e_interp"]))
bcc_lower = ((vals["bcc"]["e_interp"]<vals["fcc"]["e_interp"]) & (vals["bcc"]["e_interp"]<vals["hcp"]["e_interp"]))
fcc_lower = ((vals["fcc"]["e_interp"]<vals["bcc"]["e_interp"]) & (vals["fcc"]["e_interp"]<vals["hcp"]["e_interp"]))
hcp_lower = np.vectorize(lambda x: 1*int(x))(hcp_lower)
bcc_lower = np.vectorize(lambda x: 2*int(x))(bcc_lower)
fcc_lower = np.vectorize(lambda x: 3*int(x))(fcc_lower)
total = hcp_lower+bcc_lower+fcc_lower
bcc_lower = np.vectorize(lambda x: int(x))(vals["bcc"]["e_interp"]<vals["fcc"]["e_interp"])
cm = LinearSegmentedColormap.from_list("rb", [(1, 0, 0), (0, 0, 1)])

plt.title(r"Sodium PT Diagram")
plt.contourf(p_interp, t_interp, bcc_lower, 1, cmap = cm)
plt.xlabel(r'Pressure $(GPa)$')
plt.ylabel(r'Temperature $(K)$')
plt.gca().text(0, 20, r'FCC', color=(1, 1, 1), fontsize=19)
plt.gca().text(2, 100, r'BCC', color=(1, 1, 1), fontsize=19)
#plt.contourf(p_interp, t_interp, total, 2)
#plt.colorbar()
plt.gcf().set_size_inches(11, 5)
plt.gcf().tight_layout()
plt.savefig('../../../project_presentation/sodium_pt_diagram.png')
#plt.show()

