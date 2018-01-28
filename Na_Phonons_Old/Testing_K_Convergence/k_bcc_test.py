import os
import fnmatch
import matplotlib.pyplot as plt
ks = []
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, "na.bcc.scf.*.out"):
        ks.append(int(file.split(".")[3]))
ks.sort()
energies = []
pressures = []
for cut in ks:
    with open("na.bcc.scf."+str(cut)+".out") as f:
        for line in f.readlines():
            if "!" in line:
                energies.append(float(line.split()[4])) 
            if "(kbar)" in line:
                pressures.append(float(line.split()[5]))

plt.semilogy(ks, [abs(pressures[-1]-i) for i in pressures])
plt.semilogy(ks, [abs(energies[-1]-i) for i in energies])
plt.show()
