import fnmatch
import os
vols = []
for f in os.listdir('./'):
    if fnmatch.fnmatch(f, "na.bcc.vcrelax.*.out"):
        with open(f) as fi:
            pressure = float(f.split('.')[3])
            in_final=False
            old_lat = 0
            ratio = 0
            next_line=False
            for line in fi.readlines():
                if "Begin final coordinates" in line: in_final = True
                if "End final coordinates" in line: in_final = False
                if in_final:
                    if next_line:
                        next_line = False
                        ratio = abs(float(line.split()[0]))
                    if "CELL_PARAMETERS" in line:
                        old_lat = float(line.split()[2].strip(")"))
                        next_line=True
            new_lat = old_lat*(ratio/0.5)
            print(new_lat, ratio, pressure)
            vols.append((pressure, new_lat))
with open("p-v-output", "w") as f:
    for (p, v) in vols:
        f.write("{} {}\n".format(p, v))
