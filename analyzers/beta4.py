import numpy as np
import math

def beta4(jets, sqrts):        
    rows = []
    for i in range(4):
        rows.append([])
    for jet in jets:
        rows[0].append(jet.p4().Px()/jet.e())
        rows[1].append(jet.p4().Py()/jet.e())
        rows[2].append(jet.p4().Pz()/jet.e())
        rows[3].append(jet.e()/jet.e())        
    constraint = [0.,0.,0., sqrts]
    d2 = np.array(rows)
    d = np.array(constraint)
    #print d2
    #print d
    energies = np.linalg.solve(d2,d)
    #print energies
    chi2 = 0.
    for i,jet in enumerate(jets):
        if energies[i] > 0. :
            uncert = 0.5*math.sqrt(jet.e()) + 0.05*jet.e()
            delta = (jet.e()-energies[i])/uncert
            if delta > 0. : 
                chi2 += delta*delta
            else:
                chi2 += delta*delta/4.
        else:
            chi2 += 1000.
        p4 = jet.p4()
        scale_factor = energies[i]/jet.e()
        p4.SetPxPyPzE(jet.p4().Px()*scale_factor,
                      jet.p4().Py()*scale_factor,
                      jet.p4().Pz()*scale_factor,
                      energies[i])
        jet._tlv = p4
    return chi2

