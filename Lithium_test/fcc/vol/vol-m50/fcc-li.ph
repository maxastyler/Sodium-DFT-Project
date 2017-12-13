phonons of Li in a 8x8x8 mesh
 &inputph
  tr2_ph=1.0d-16,
  reduce_io = .true.
  ldisp = .true.
  nq1 = 8 , nq2 = 8 , nq3 = 8
  prefix='li-fcc',
  outdir='./tmp/',
  fildyn='fcc-li.dyn',
  !start_q = 24
  max_seconds = 10200
  recover = .false.
 /
