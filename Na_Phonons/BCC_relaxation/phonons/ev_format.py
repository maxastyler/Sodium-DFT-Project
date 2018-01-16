from os import listdir
from os.path import join
from fnmatch import fnmatch

vals = {}

for f in listdir("./"):
    if fnmatch(f, "*.*"):
        try:
            float(f)
            with open(join("./", f, "na.bcc.scf.out")) as scf:
                for line in scf.readlines():
                    if "!" in line:
                        scf_energy = float(line.split()[-2])
            with open(join("./", f, "na.bcc.fqha.calc")) as fqha:
                for line in fqha.readlines():
                    [temp, phon_energy] = line.split()
                    temp = float(temp)
                    phon_energy = float(phon_energy)
                    if temp not in vals.keys():
                        vals[temp] = {}
                    vals[temp][float(f)]=phon_energy+scf_energy
        except: pass

def build_str(t):
    v_str = ""
    vol = sorted(vals[t].keys())
    for i in vol:
        v_str += str(i) + "\t" + str(vals[t][i]) + "\n"
    return v_str

for temp in vals.keys():
    print(temp)
    with open("ev_formatted/na.bcc."+str(temp), "w") as f:
        f.write(build_str(temp))
