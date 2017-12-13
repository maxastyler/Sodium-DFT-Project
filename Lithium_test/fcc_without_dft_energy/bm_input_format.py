import sys

filenames = {}
for argument in sys.argv[1:]:
    v=(argument.split(".")[2:4])
    filenames[argument]=float(v[0]+"."+v[1])

temps = []
with open("extracted/"+next(iter(filenames.keys()))) as f:
    for line in f:
        temps.append(float(line.split()[0]))

tempdict={}
for temp in temps:
    tempdict[temp]=[]

for filename in filenames:
    with open("extracted/"+filename) as f:
        for line in f:
            temp=float(line.split()[0])
            fe=float(line.split()[1])
            tempdict[temp].append( (filenames[filename], fe) )

for temp in tempdict:
    with open("bm_fits/"+"li.fcc."+str(temp), "w") as f:
        for (vol, fe) in tempdict[temp]:
            f.write(str(vol)+"\t"+str(fe)+"\n")
