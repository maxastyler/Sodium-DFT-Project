import subprocess
import glob
import math
from functools import reduce
lats = list(map(lambda n: float(n.split('_')[-1][:-4]) ,glob.glob("na_hcp_*.dos")))

def get_volumes(lats):
    volumes = {}
    for l in lats:
        with open("na_hcp_scf_{}.in".format(l)) as f:
            ca = [float(a.split()[-1].strip(',')) for a in f.readlines() if "celldm(3)" in a][0]
            volumes[l] = ca*(l**3)*math.sin(math.pi/3)
    return volumes

volumes = get_volumes(lats)
            
def get_fqha(lats):
    tempstr = reduce(lambda a, b: "{}\n{}".format(a, b), range(0, 181, 20))
    print(tempstr)
    for v in lats:
        fqha_string = "na_hcp_{}.dos\nna_hcp_{}.fe\n".format(v, v)+tempstr
        subprocess.run(['fqha.x'], input = fqha_string.encode())

def energy_from_scf(v):
    with open("na_hcp_scf_{}.out".format(v)) as f:
        e_l = list(filter(lambda x: "!" in x, f.readlines()))[0].split()[-2]
    return float(e_l)

def energies_from_fe(v):
    with open("na_hcp_{}.fe".format(v)) as f:
        ts = {} 
        for line in f.readlines():
            (t, e) = list(map(lambda x: float(x), line.split()))
            ts[t] = e
    return ts

#returns a list of energies[temperature][volume]
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

#input a dictionary of energies indexed first by temperature, then volume, eg energies[t][v]
def format_for_ev(energies):
    for t in energies:
        vs = [volumes[i] for i in sorted(energies[t])]
        es = [energies[t][v] for v in sorted(lats)]
        ev_str = reduce(lambda s, x: s + "{} {}\n".format(x[0], x[1]), zip(vs, es), "")
        with open("na.hcp.{:.1f}.ev".format(t), 'w') as f:
            f.write(ev_str) 

def pt_fit(temperatures):
    for t in temperatures:
        input_str = "au\nnoncubic\n1\nna.hcp.{:.1f}.ev\nna.hcp.{:.1f}.pt".format(t, t)
        subprocess.run(['ev.x'], input = input_str.encode())

#get_fqha(lats)
#format_for_ev(get_energies(lats))
pt_fit(get_energies(lats).keys())
#print(get_volumes(lats))
