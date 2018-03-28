#!/bin/bash
#for v in 6.976382950545051 6.998233353524401 6.993850699385001 6.98348186215975 6.99410908717325; do
for v in 6.94 6.96 7.008 7.018 7.03 7.04; do
	mpirun -np 4 q2r.x > na_hcp_q2r_$v.out << EOF
&input
	fildyn = 'na_hcp_$v.dyn',
	flfrc = 'na_hcp_$v.fc',
	zasr = 'simple',
/
EOF

	mpirun -np 4 matdyn.x > na_hcp_dos_$v.out << EOF
&input
        asr = 'simple',
        flfrc = 'na_hcp_$v.fc',
        dos = .true.,
        nk1 = 30, nk2 = 30, nk3 = 30,
        fldos = 'na_hcp_$v.dos',
/
EOF
done
