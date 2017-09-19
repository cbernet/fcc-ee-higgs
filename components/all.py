import glob
import pprint
import os
from info.basedir import basedir
from info.sampleinfo import SampleBase
import heppy.framework.config as cfg
from ROOT import TFile

def read_pythia(sampledir):
    jobs = glob.glob('/'.join([sampledir, 'Job_*']))
    if len(jobs):
        return glob.glob('/'.join([sampledir, 'Job_*/*.root']))
    else:
        return []
    
def read_heppy(sampledir, treename, treename_janik):
    heppys = glob.glob('/'.join([sampledir, 'heppy.*']))
    files = []
    rootfile = None
    tree = None
    if len(heppys):
        abstreename = '/'.join([sampledir,treename])
        if not os.path.isfile(abstreename):
            abstreename = '/'.join([sampledir,treename_janik])
            if not os.path.isfile(abstreename):
                raise ValueError('cannot find tree root file in '+sampledir)        
        files = [abstreename]
        rootfile = TFile(comp.files[0])
        tree = rootfile.Get('events')
    return files, rootfile, tree

def load_components(pattern=None, mode=None):
    if mode and mode not in ['pythia', 'heppy']:
        raise ValueError("if you provide mode, it should be set to 'pythia' or 'heppy'")
    print 'loading all components:'
    base = SampleBase(basedir(), pattern)
    treename = 'heppy.analyzers.examples.zh.ZHTreeProducer.ZHTreeProducer_1/tree.root'
    treename_janik = 'heppy.analyzers.examples.missE.TreeProducer.TreeProducer_1/tree.root'
    components = dict()    
    for name in sorted(base.keys()):
        info = base[name]
        name = info.name
        files = []
        rootfile = None
        tree = None
        sampledir = info['sample']['directory']
        if mode is None:
            files = read_pythia(sampledir)
            files, rootfile, tree = read_heppy(sampledir, treename, treename_janik)
        elif mode == 'pythia':
            files = read_pythia(sampledir)
        elif mode == 'heppy':
            files, rootfile, tree = read_heppy(sampledir, treename, treename_janik)
        if len(files) == 0:
            continue  # skipping heppy components in pythia mode, and vice versa
        oldest_ancestor = base.oldest_ancestor(info)
        xSection = oldest_ancestor['sample']['xsection'] * 1e9  # now in pb
        nGenEvents = oldest_ancestor['sample']['nevents']
        global_eff = 1.
        for ancestor in base.ancestors(info):
            eff = float(ancestor['sample']['njobs_ok']) / float(ancestor['sample']['njobs'])
            global_eff *= eff
        comp = cfg.MCComponent(name=name,
                               files=files,
                               xSection=xSection,
                               nGenEvents=nGenEvents,
                               effCorrFactor=global_eff)
        print comp.name
        print comp.files
        if rootfile and tree:
            comp.rootfile = rootfile
            comp.tree = tree        
        components[name] = comp
        print name
    return components
        


