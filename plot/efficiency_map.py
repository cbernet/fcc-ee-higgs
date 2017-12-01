class EfficiencyMap(list):
    
    def add(self, weight, ptmin, ptmax, etamin=None, etamax=None):
        assert(weight > 0 and weight < 1)
        assert(ptmin < ptmax)
        assert(etamin is not None and etamax is not None or (etamin is None and etamax is None))
        if(etamin and etamax):
            assert(etamin < etamax)
        self.append((weight, ptmin, ptmax, etamin, etamax))
        
    def __call__(self, ptc):
        regions = []
        for weight, ptmin, ptmax, etamin, etamax in self:
            ptcut = '{ptmin}<{ptc}_pt && {ptc}_pt<{ptmax}'.format(ptc=ptc,
                                                                  ptmin=ptmin,
                                                                  ptmax=ptmax)
            etacut = ''
            if etamin or etamax:
                etacut = '&& {etamin}<abs({ptc}_eta) && abs({ptc}_eta)<{etamax}'.format(ptc=ptc,
                                                                                        etamin=etamin,
                                                                                        etamax=etamax)
            regions.append('{weight}*({ptcut} {etacut})'.format(weight=weight,
                                                                ptcut=ptcut,
                                                                etacut=etacut))      
        regions_str = ' + '.join(regions)
        regions_str = '({regstr})'.format(regstr=regions_str)
        return regions_str

if __name__ == '__main__':
    
    effmap = EfficiencyMap()
    effmap.add(0.2, 0, 10)
    effmap.add(0.5, 10, 20)
    effmap.add(0.9, 20, 10000)
    print effmap('zeds_1')
    
    effmu_delphes = EfficiencyMap()
    effmu_delphes.add(0.95, 10, 1000, 0, 2.4)
    
    effe_delphes = EfficiencyMap()
    effe_delphes.add(0.95, 10, 1000, 0, 1.5)
    effe_delphes.add(0.85, 10, 1000, 1.5, 2.5)
