#Energy differences for frequency points 10x10x10
import numpy as np
import matplotlib.pyplot as plt

ecut_energies = np.load("ecut_energies_fcc.npy")
ecut_diffs = [ecut_energies[i-1]-ecut_energies[i] for i in range(1, len(ecut_energies))]
ecut_params = np.linspace(10, 40, 20)[1:]

plt.semilogy(ecut_params, ecut_diffs)
plt.show()
