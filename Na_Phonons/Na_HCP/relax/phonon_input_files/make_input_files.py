vals = [
(6.976382950545051,
1.6318208112624575),
(6.998233353524401,
1.6313562922319813),
(6.993850699385001,
1.6305066519493348),
(6.98348186215975,
1.6317016015146895),
(6.99410908717325,
1.6306300703090453)]

f_s = "&control\n\
       calculation='scf',\n\
       wf_collect=.true.,\n\
       prefix='na_hcp_{a}',\n\
       pseudo_dir='./',\n\
       outdir='./na_hcp_{a}/',\n\
       disk_io='low',\n\
       tstress=.true.,\n\
/\n\
&system\n\
        ibrav = 4,\n\
        celldm(1) = {a},\n\
       celldm(3) = {ca},\n\
        nat = 2,\n\
        ntyp = 1,\n\
        ecutwfc = 40,\n\
        ecutrho = 320,\n\
        occupations = 'smearing',\n\
        smearing = 'm-v',\n\
        degauss = 0.02,\n\
/\n\
&electrons\n\
        mixing_beta = 0.7,\n\
        conv_thr = 1.0d-10,\n\
/\n\
ATOMIC_SPECIES\n\
 Na 22.99 Na_pbe_v1.uspp.F.UPF\n\
ATOMIC_POSITIONS (crystal)\n\
 Na  0.0 0.0 0.0\n\
 Na  0.6666666 0.3333333 0.5\n\
K_POINTS automatic\n\
 24 24 12 0 0 1\n\
EOF"

for (a, ca) in vals:
    with open("na_hcp_{:.3f}_in".format(a), "w") as f:
    	f.write(f_s.format(a=a, ca = ca))
