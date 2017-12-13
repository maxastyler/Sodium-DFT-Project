import sys

filenames = {}
for argument in sys.argv[1:]:
    print(argument)
    v=(argument.split(".")[3:5])
    fname=argument.split("/")[2]
    filenames[fname]=float(v[0]+"."+v[1])

temps = []
with open("extracted/"+next(iter(filenames.keys()))) as f:
    for line in f:
        temps.append(float(line.split()[0]))

tempdict={}
for temp in temps:
    tempdict[temp]=[]

for filename in sorted(filenames, key=filenames.__getitem__):
    with open("extracted/fcc.fqha."+str(filenames[filename])) as f:
        with open("extracted/fcc-li.scf.out."+str(filenames[filename])) as dft:
            for line in dft:
                if "!" in line:
                    dft_fe=float(line.split()[4])
                    print(dft_fe)
            for line in f:
                temp=float(line.split()[0])
                fe=float(line.split()[1])
                tempdict[temp].append( (filenames[filename], fe+dft_fe) )

for temp in tempdict:
    with open("bm_fits/"+"li.fcc."+str(temp), "w") as f:
        for (vol, fe) in tempdict[temp]:
            f.write(str(vol)+"\t"+str(fe)+"\n")
