import glob
import pprint
import os
from info.basedir import basedir
from info.sampleinfo import SampleBase
import heppy.framework.config as cfg
from ROOT import TFile

base = SampleBase(basedir())
treename = 'heppy.analyzers.examples.zh.ZHTreeProducer.ZHTreeProducer_1/tree.root'
treename_janik = 'heppy.analyzers.examples.missE.TreeProducer.TreeProducer_1/tree.root'
components = dict()

print 'loading all components:'
for name in sorted(base.keys()):
    info = base[name]
    name = info.name
    files = []
    sampledir = info['sample']['directory']
    jobs = glob.glob('/'.join([sampledir, 'Job_*']))
    heppys = glob.glob('/'.join([sampledir, 'heppy.*']))
    if len(jobs):
        files = glob.glob('/'.join([sampledir, 'Job_*/*.root']))
    elif len(heppys):
        abstreename = '/'.join([sampledir,treename])
        if not os.path.isfile(abstreename):
            abstreename = '/'.join([sampledir,treename_janik])
            if not os.path.isfile(abstreename):
                raise ValueError('cannot find tree root file in '+sampledir)
        files = [abstreename]
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
    if comp is None:
        print 'comp is none'
    comp.rootfile = TFile(comp.files[0])
    comp.tree = comp.rootfile.Get('events')        
    components[name] = comp
    print name 
    

