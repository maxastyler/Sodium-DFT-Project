from subprocess import run, PIPE
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def create_string(ecutwfc, lattice_parameter):
    return "&control\n\
    	calculation = 'scf',\n\
    	outdir='/home/max/quantum_espresso/qe-6.1/tempdir/',\n\
    /\n\
    &system\n\
    	ibrav = 3,\n\
    	celldm(1) = {},\n\
    	nat = 1,\n\
    	ntyp = 1,\n\
    	ecutwfc = {},\n\
        occupations = 'smearing',\n\
        degauss = 0.05,\n\
    /\n\
    &electrons\n\
    	mixing_beta = 0.7,\n\
    	conv_thr = 1.0d-8\n\
    /\n\
    ATOMIC_SPECIES\n\
     Al	26.982	Al.pbe-n-kjpaw_psl.1.0.0.UPF\n\
    ATOMIC_POSITIONS\n\
     Al 0.00 0.00 0.00\n\
    K_POINTS automatic\n\
     5 5 5   1 1 1".format(lattice_parameter, ecutwfc)
def get_energy(lattice_param, ecutwfc):
    p=run(['pw.x'], stdout=PIPE, input=create_string(ecutwfc, lattice_param), encoding='ascii')
    print(ecutwfc)
    for line in p.stdout.splitlines():
        if "!    total energy" in line:
            return float(line.split()[-2])
lat_params = np.linspace(6, 6.3, 40)
ecut_params = np.linspace(10, 20, 30)
#lat_energies = [get_energy(i, 13) for i in lat_params]
#np.save("lattice_energies_bcc", lat_energies)
lat_energies = np.load("lattice_energies_bcc.npy")
#ecut_energies = [get_energy(7.655, i) for i in ecut_params]
#ecut_energy_differences=[ecut_energies[i]-ecut_energies[i-1] for i in range(1, len(ecut_params))]
fitted_values=curve_fit(lambda x, a, b, c: a*(x-b)**2+c, lat_params, lat_energies)
a=fitted_values[0][0]
b=fitted_values[0][1]
c=fitted_values[0][2]
print(b, c)
plt.title("Energy (Ry) vs Lattice Parameter (A?) for Si")
plt.plot(lat_params, lat_energies)
#plt.plot(ecut_params, ecut_energies)
#plt.plot(ecut_params[1:], ecut_energy_differences)
#plt.show()
