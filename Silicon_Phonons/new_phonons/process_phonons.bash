#!/bin/bash
for v in `seq 10.28 0.012 10.316`; do
	echo "$v"
	mpirun -np 4 q2r.x > si.q2r.$v.out << EOF
&input
	fildyn = 'silicon.$v.dyn',
	flfrc = 'silicon.$v.fc',
	zasr = 'simple',
/
EOF

	mpirun -np 4 matdyn.x > si.dos.$v.out << EOF
&input
	asr = 'simple',
	flfrc = 'silicon.$v.fc',
	dos = .true.,
	nk1 = 30, nk2 = 30, nk3 = 30,
	fldos = 'silicon.$v.dos',
/
EOF
done
