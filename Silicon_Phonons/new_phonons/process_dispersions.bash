#!/bin/bash
for v in `seq 10.28 0.012 10.4`; do
	echo "$v"
	mpirun -np 4 matdyn.x > si.disp.$v.out << EOF
&input
	asr = 'simple',
	flfrc = 'silicon.$v.fc',
	flfrq = 'silicon.$v.freq',
	q_in_band_form = .true.,
/
6
gG 40
X 20
W 20
K 40
gG 40
L 40
EOF
done
