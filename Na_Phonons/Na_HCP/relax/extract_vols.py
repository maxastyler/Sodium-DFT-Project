import glob

for fname in glob.glob('*.out'):
    with open(fname) as f:
        ln = 0
        lines = f.readlines()
        for (i, line) in enumerate(lines):
            if "Begin final coordinates" in line:
                ln = i
        old_lat = float(lines[ln+3].split()[-1][:-1])
        new_vec = float(lines[ln+4].split()[0])
        new_ca = float(lines[ln+6].split()[2])
        ca = new_ca/new_vec
        print(fname)
        print(new_vec*old_lat)
        print(ca)
