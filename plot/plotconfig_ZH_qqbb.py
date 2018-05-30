from fcc_ee_higgs.plot.plotconfig_ZH_ll import cut_hbb, bins, detector, lumi, xtitle

var = 'higgsmass'
##var = 'mZedJet'
##var = 'deltaWW'
##var = 'vismass'

channel = 'qqbb'

from fcc_ee_higgs.components.ZH_qqbb_CLD_May30 import ZH, ZZ, ffbar, WW
from fcc_ee_higgs.components.tools import load
comps = [ZZ, ZH, ffbar, WW]
ZH.name =  'ZH' 
ZZ.name =  'ZZ'
ffbar.name =  'ffbar'
WW.name = 'WW'
load(comps)

from fcc_ee_higgs.plot.cuts import Cuts

cut = "n_iso_leptons<=2 && hadjet1_n_constituents >= 5 && \
hadjet1_n_charged_hadrons>0 && hadjet2_n_constituents >= 5 && \
hadjet2_n_charged_hadrons>0 && hadjet3_n_constituents >= 5 && \
hadjet3_n_charged_hadrons>0 && hadjet4_n_constituents >= 5 && \
hadjet4_n_charged_hadrons>0&&n_jets>=4 && vismass>=180 && chi2>=0   && \
deltaWW>10 && deltaZZ > 10 &&  (hadjet1_higgsmaker*hadjet1_b + \
hadjet2_higgsmaker*hadjet2_b + hadjet3_higgsmaker*hadjet3_b + \
hadjet4_higgsmaker*hadjet4_b)==2 && mHJet > 100 && mZedJet > 80 && \
mZedJet < 110"

# no_lep = '(n_iso_leptons<=2)'
no_lep = '(n_iso_leptons==0)'
njets = '(n_jets>=4)'
jet_id = '(hadjet1_n_constituents >= 5 && \
hadjet1_n_charged_hadrons>0 && hadjet2_n_constituents >= 5 && \
hadjet2_n_charged_hadrons>0 && hadjet3_n_constituents >= 5 && \
hadjet3_n_charged_hadrons>0 && hadjet4_n_constituents >= 5)'
vismass = '(vismass>=180)'
chi2 = '(chi2>=0)'
deltaWW = '(deltaWW>10)'
deltaZZ = '(deltaZZ>10)'
btag = '((hadjet1_higgsmaker*hadjet1_b + \
hadjet2_higgsmaker*hadjet2_b + hadjet3_higgsmaker*hadjet3_b + \
hadjet4_higgsmaker*hadjet4_b)==2)'
mZ = '(mZedJet > 80 && mZedJet < 110)'
# mZ = '(mZedJet > 82 && mZedJet < 102)'
# mZ = '(mZedJet > 85 && mZedJet < 115)'
mH = '(mHJet > 100)'

cuts = Cuts([
    ('no_lep', no_lep),
    ('njets', njets), 
    ('jet_id', jet_id), 
    ('vismass', vismass), 
    ('chi2', chi2), 
    ('deltaWW', deltaWW), 
    ('deltaZZ', deltaZZ), 
    ('btag', btag), 
    ('mZ', mZ), 
    # ('mH', mH), 
    ])

if var == 'mZedJet':
    del cuts['mZ']
elif var == 'deltaWW':
    del cuts['deltaWW']
    bins = 50, 0, 100
elif var == 'deltaZZ':
    del cuts['deltaZZ']
    bins = 50, 0, 100
elif var == 'vismass':
    del cuts['vismass']
    bins = 50, 0, 250

cut = str(cuts)
