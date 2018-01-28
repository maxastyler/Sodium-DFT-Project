import os
import fnmatch
import matplotlib.pyplot as plt
ecuts = []
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, "na.bcc.scf.*.out"):
        ecuts.append(int(file.split(".")[3]))
ecuts.sort()
energies = []
pressures = []
for cut in ecuts:
    with open("na.bcc.scf."+str(cut)+".out") as f:
        for line in f.readlines():
            if "!" in line:
                energies.append(float(line.split()[4])) 
            if "(kbar)" in line:
                pressures.append(float(line.split()[5]))

plt.semilogy(ecuts, [abs(pressures[-1]-i) for i in pressures])
plt.semilogy(ecuts, [abs(energies[-1]-i) for i in energies])
plt.show()
