from ROOT import TFile, TTree, TLorentzVector, TVector3
import math

def acop_colin(jet1, jet2):
    normal = jet1.Cross(jet2).Unit()
    angle = normal.Angle( TVector3(0, 0, 1)) - math.pi / 2.    
    return angle * 180 / math.pi

f = TFile('tree.root')
events = f.Get("events")
for event in events:
    jet1 = TLorentzVector(event.jet1_px, event.jet1_py, event.jet1_pz, event.jet1_e)
    jet2 = TLorentzVector(event.jet2_px, event.jet2_py, event.jet2_pz, event.jet2_e)
    acop = acop_colin(jet1.Vect(), jet2.Vect())
    assert(acop == event.higgs_acop)
    print acop, event.higgs_acop
