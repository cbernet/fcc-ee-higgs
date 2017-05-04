
import sys
import os
import shutil
import subprocess

args = sys.argv
if len(args) != 4:
    print "usage : pythia_prod.py <card> <number_of_samples> <outdir>"
    sys.exit(1)
card, n_samples, outdir = sys.argv[1:]
if not os.path.isdir(outdir):
    os.mkdir(outdir)
rootfilename = card.replace('.txt', '.root')
for sample in range( int(n_samples) ):
    cmd_py = 'fcc-pythia8-generate {}'.format(card)
    print cmd_py
    py = subprocess.Popen(cmd_py.split())
    py.communicate()
    destfile = '{}/{}'.format(
        outdir,
        rootfilename.replace('.root',
                             '_{}.root'.format(sample))
                             )
    print destfile
    shutil.copyfile(rootfilename, destfile)
    
    
