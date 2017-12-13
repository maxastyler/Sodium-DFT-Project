phonons of Li in a 10x mesh
 &inputph
  tr2_ph=1.0d-18,
  reduce_io = .true.
  ldisp = .true.
  nq1 = 10, nq2 = 10, nq3 = 10
  prefix='li-bcc',
  outdir='./tmp/',
  fildyn='bcc-li.dyn',
  start_q = 2
  last_q  = 5
  max_seconds = 1100
  recover = .false.
 /
