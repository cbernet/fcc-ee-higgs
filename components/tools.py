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
