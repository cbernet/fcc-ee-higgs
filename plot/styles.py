
import fnmatch

from cpyroot.tools.style import *

sZZ = Style(markerColor=4, markerSize=1, lineColor=4, fillColor=kBlue-9, fillStyle=3344)
sZH= Style(markerColor=2, markerSize=1, lineColor=2, fillColor=5, fillStyle=0)
sVBF= Style(markerColor=8, markerSize=1, lineColor=8, fillColor=5, fillStyle=0)
sWW= Style(markerColor=6, markerSize=1, lineColor=6, fillStyle=3003)
sffbar = Style(markerColor=1, markerSize=1, lineColor=1, fillStyle=3003)

histPref = {
    'ZZ*': {'style':sZZ, 'layer':10, 'legend':'ZZ'},
    'WW*': {'style':sWW, 'layer':5, 'legend':'WW'},
    'ZH*': {'style':sZH, 'layer':11, 'legend':'ZH'},
    'VBF*': {'style':sVBF, 'layer':12, 'legend':'VBF'},
    'ffbar': {'style':sffbar, 'layer':4, 'legend':'ffbar'},
    'qqbar': {'style':sffbar, 'layer':4, 'legend':'qqbar'},
    'll': {'style':sffbar, 'layer':4, 'legend':'ll'},
}

def set_style(comp):
    for key, pref in histPref.iteritems():
        if fnmatch.fnmatch(comp.name, key):
            comp.style = pref['style']
            found = True
    if not found:
        comp.style = sData
    
    
    
