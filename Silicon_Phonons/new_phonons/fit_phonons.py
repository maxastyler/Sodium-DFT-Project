import subprocess
import glob
import math
from functools import reduce
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

TEMP_MIN = 0
TEMP_MAX = 700
TEMP_STEP = 10
a1 = np.array([-0.5, 0, 0.5])
a2 = np.array([0, 0.5, 0.5])
a3 = np.array([-0.5, 0.5, 0])
volume = np.cross(a1, a2).dot(a3)
print(volume)

def vinet_d(v, v0, e0, b0, db0):
    eta = ((v/v0)**(1/3))
    e = np.exp((3/2)*(db0-1)*(1-eta)) 
    return -3*b0*v0*(1-eta)*e*(v0**(-1/3))*(v**(-2/3))

def vinet(v, v0, e0, b0, db0):
    eta = ((v/v0)**(1/3))
    bovo_eta = b0*v0/((db0-1)**2)
    exp_br = (3/2)*(db0-1)*(1-eta)
    other_br = 3*(db0-1)*(1-eta)-2
    return e0 + 4*bovo_eta + 2*bovo_eta*np.exp(exp_br)*other_br

def fname_to_latparam(fname):
    nums = fname.split('.')[1:3]
    return float(nums[0]+"."+nums[1])
lats = list(sorted(map(fname_to_latparam ,glob.glob("silicon.*.dos"))))

def run_fqha(lat):
    tempstr = reduce(lambda a, b: "{}\n{}".format(a, b), range(TEMP_MIN, TEMP_MAX, TEMP_STEP))
    fqha_string = "silicon.{lat:.3f}.dos\nsilicon.{lat:.3f}.fe\n".format(lat=lat)+tempstr
    subprocess.run(['fqha.x'], input= fqha_string.encode())

def energy_from_scf(v):
    with open("si.scf.{:.3f}.out".format(v)) as f:
        e_l = list(filter(lambda x: "!" in x, f.readlines()))[0].split()[-2]
    return float(e_l)

def energies_from_fe(v):
    with open("silicon.{:.3f}.fe".format(v)) as f:
        ts = {} 
        for line in f.readlines():
            (t, e) = list(map(lambda x: float(x), line.split()))
            ts[t] = e
    return ts

def get_energies(lats):
    energies = {}
    for v in lats:
        e_scf = energy_from_scf(v)
        e_fe = energies_from_fe(v)
        for t in e_fe: 
            if t not in energies:
                energies[t] = {}
            energies[t][v] = e_fe[t] + e_scf
    return energies

def format_for_ev(energies):
    for t in energies:
        es = [energies[t][v] for v in sorted(lats)]
        ev_str = reduce(lambda s, x: s + "{} {}\n".format(x[0], x[1]), zip(lats, es), "")
        with open("silicon.{:.1f}.ev".format(t), 'w') as f:
            f.write(ev_str) 

def pt_fit(temperatures):
    for t in temperatures:
        input_str = "au\nfcc\n1\nsilicon.{:.1f}.ev\nsilicon.{:.1f}.pt".format(t, t)
        subprocess.run(['ev.x'], input = input_str.encode())

#put in dictionary of energy[temp][lat] and get fit[temp][fit]
def get_fits(energies):
    fits = {}
    for t, e_lat in energies.items():
        vols = [l**3*volume for l in sorted(e_lat.keys())]
        fits[t] = curve_fit(vinet, vols, [e_lat[lat] for lat in lats], p0 = [277, -19, 0.005, 12])[0]
    return fits

def load_frequencies(lat):
    full = np.loadtxt("silicon.{:.3f}.freq.gp".format(lat))
    ks = full[:, 0]
    ws = full[:, 1:]
    return ks, ws

#for lat in lats: run_fqha(lat)
#format_for_ev(get_energies(lats))
#pt_fit(get_energies(lats).keys())
energies = get_energies(lats)
fits = get_fits(energies)
ts = sorted(fits.keys())
vs = [(fits[t][0]/0.25)**(1/3) for t in ts]

def data_for_t(t):
    ls = sorted(energies[t].keys())
    return ls, [energies[t][l] for l in ls]

def plot_pressure():
    print(fits[0])
    xs = np.linspace(9.8, 10.5, 20)
    #ls, _ = data_for_t(0)
    es = [vinet(l**3*0.25, *fits[0]) for l in xs]
    ps = [-vinet_d(l**3*0.25, *fits[0]) for l in xs]
    es = [x for _, x in sorted(zip(ps, es))]
    ps = sorted(ps)
    plt.plot(ps, es)
    plt.show()

def plot_two():
    fig, ax1 = plt.subplots()
    plt.ticklabel_format(useOffset=False)
    ax1.get_yaxis().get_major_formatter().set_scientific(False)
    #x1 = plt.subplots()
    plt.title(r'Free Energy vs Lattice Parameter in Silicon at $T=0K, T=500K$')
    ls, es = data_for_t(0)
    xs = np.linspace(ls[0], ls[-1], 100)
    ys = [vinet(l**3*0.25, *fits[0]) for l in xs]
    ax1.scatter(ls, es, c=(0, 0.5, 1), marker='.')
    ax1.plot(xs, ys, 'b')
    ax1.set_xlabel('Lattice Paramter (Bohr)')
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel(r'Free energy at $T=0K$ $(Ry)$', color='b')
    ax1.tick_params('y', colors='b')
    ax1.set_ylim((-19.18457, -19.18417))
    
    ax2 = ax1.twinx()
    plt.ticklabel_format(useOffset=False)
    ax2.get_yaxis().get_major_formatter().set_scientific(False)
    ls, es = data_for_t(500)
    xs = np.linspace(ls[0], ls[-1], 100)
    ys = [vinet(l**3*0.25, *fits[500]) for l in xs]
    ax2.scatter(ls, es, c=(1, 0.5, 0), marker='.')
    ax2.plot(xs, ys, 'r')
    ax2.set_ylabel(r'Free energy at $T=500K$ $(Ry)$', color='r')
    ax2.tick_params('y', colors='r')
    ax2.set_ylim((-19.19626, -19.1958))
    
    fig.set_size_inches(11, 5)
    fig.tight_layout()
    plt.show()

#plot_two()
def plot_bands():
    ks, ws = load_frequencies(10.352)
    dos = np.loadtxt('./silicon.10.352.dos').transpose()
    special_point_strs = [r"$\Gamma$", r"$X$", r"$W$", r"$K$", r"$\Gamma$", r"$L$"]
    special_point_dists = [40, 20, 20, 40, 40]
    special_point_dists = [ks[sum(special_point_dists[:i])] for i in range(len(special_point_dists)+1)]
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, gridspec_kw = {'width_ratios':[3, 1]})
    print(ks)
    for i in [0, 1, 2]:
        ax1.plot(ks, ws.transpose()[i], color = 'blue')
    for i in [3, 4, 5]:
        ax1.plot(ks, ws.transpose()[i], color= 'red')
    ax1.set_xticklabels(special_point_strs)
    ax1.set_xticks(special_point_dists)
    ax2.set_xticklabels([])
    ax2.set_xticks([])
    ax1.set_ylabel(r"Phonon frequency $\omega$ ($cm^{-1}$)")
    ax1.set_xlabel(r"Brillouin zone position")
    ax2.set_xlabel(r"Density of states $g(\omega)$")
    for p in special_point_dists:
        ax1.axvline(p, color = 'black')
    f.subplots_adjust(wspace=0, hspace=0)
    print(dos[1])
    ax2.plot(dos[1], dos[0])
    ax1.set_xlim(special_point_dists[0], special_point_dists[-1])
    ax1.set_ylim(0, 510)
    ax2.set_xlim(0, 0.1)
    plt.tight_layout()
    plt.savefig('../../project_report/figures/si_band_structure.png')
    plt.show()

def expansion_func(x, a, b, c, d, e):
    return a*x**4+b*x**3+c*x**2+d*x+e

def linear_expansion(x, a, b, c, d, e):
    return 4*a*x**3+3*b*x**2+2*c*x+d

def plot_lat_thermal_expansion():
    ts = sorted(fits.keys())
    vs = [fits[t][0] for t in ts]
    vol_fit = curve_fit(expansion_func, ts, vs)[0]
    alphas = [expansion_func(t, *vol_fit)-vs[i] for i, t in enumerate(ts)]
    #plt.plot(ts, vs)
    plt.plot(ts, alphas)
    plt.show()
#plot_bands()
plot_lat_thermal_expansion()
