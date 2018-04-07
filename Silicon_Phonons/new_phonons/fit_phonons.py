import subprocess
import glob
import math
from functools import reduce

TEMP_MIN = 0
TEMP_MAX = 700
TEMP_STEP = 10

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

for lat in lats: run_fqha(lat)
format_for_ev(get_energies(lats))
pt_fit(get_energies(lats).keys())
