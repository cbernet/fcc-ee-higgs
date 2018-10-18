from ROOT import TFile, TTree
import shutil, os

tmpname = 'tmp.root'
f = TFile(tmpname)
tree = f.Get('events')

tree.SetBranchStatus('mva', 0)

newf = TFile('tmp2.root', 'recreate')
newtree = tree.CloneTree()
newtree.Write()

f.Close()
newf.Close()
