#!/bin/python3
#Argument should be run number
import sys
import os
import pathlib

try:
    run_no=int(sys.argv[1])
except:
    print("No run number as argument!")
    sys.exit()

def replace_run_pressure(run, pres):
    run_folder = "run_" + str(run)
    in_file = "na.fcc.vcrelax." + str(pres) + ".in"
    out_file = "na.fcc.vcrelax." + str(pres) + ".out"
    final_coords = False
    next_line = False
    with open(os.path.join(run_folder, out_file)) as f:
        for line in f.readlines():
            if "End final coordinates" in line:
                final_coords = False
            if next_line:
                next_line = False
                new_param = original_lat*abs(float(line.split()[0]))/0.5
            if final_coords:
                if  "CELL_PARAMETERS" in line: 
                    next_line = True
                    original_lat = float(line.split()[2].strip(")"))
            if "Begin final coordinates" in line:
                final_coords = True

    with open(os.path.join(run_folder, in_file)) as f:
        new_file=""
        for line in f.readlines():
            if "celldm(1)" in line:
                new_file+="\tcelldm(1) = {},\n".format(new_param)
            else:
                new_file+=line
    new_run_folder = "run_" + str(run+1)
    pathlib.Path(new_run_folder).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(new_run_folder, in_file), 'w') as f:
            f.write(new_file)

#for p in range(-10, 101, 10):
#    replace_run_pressure(run_no, p)
replace_run_pressure(run_no, 0)
    
