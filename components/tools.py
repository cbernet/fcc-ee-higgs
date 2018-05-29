from ROOT import TFile

def load(comps):
    for comp in comps:
        assert(len(comp.files) == 1)
        comp.rootfile = TFile(comp.files[0])
        comp.tree = comp.rootfile.Get("events")
        if not comp.tree:
            msg = '''
            cannot find tree "events" in comp
            {}
            '''.format(str(comp))
            raise ValueError(msg)

def get_components(mode, components, nfiles=None):
    cps = []
    if mode == 'all':
        cps = list(components)
    else:
        comp = None
        for cp in components:
            if cp.name == mode:
                comp = cp
                break
        comp.splitFactor = 1
        cps = [comp]
    if nfiles:
        for cp in cps:
            cp.files = cp.files[:nfiles]
    return cps
