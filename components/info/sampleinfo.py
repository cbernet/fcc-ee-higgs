
import os
import glob
import yaml
import networkx as nx
import pprint

class SampleInfo(dict):
    
    def __init__(self, dirname):
        self.dirname = dirname
        self.info, self.info_fname = self.load(self.dirname)
        self.name = self.info['sample']['name']
        self.id = self.info['sample']['id']
        super(SampleInfo, self).__init__(self.info.items())

    #----------------------------------------------------------------------
    def load(self, dirname):
        """load info from the single yaml file in dirname"""
        info_fname = None
        if not os.path.isdir(dirname):
            raise ValueError('directory {} does not exist'.format(dirname))
        info_fnames = glob.glob(dirname+'/*.yaml')
        if len(info_fnames) > 1:
            raise ValueError('more than one yaml file in '+dirname)
        elif len(info_fnames) == 0:
            raise ValueError('no yaml file in '+dirname)                    
        info_fname = info_fnames[0]
        with open(info_fname) as tmp:
            info = yaml.load(tmp) 
        tmp.close()
        return info, info_fname
    
    #----------------------------------------------------------------------
    def mothers(self):
        """return list of mother ids, or empty list if no mother"""
        return self['sample'].get('mothers', [])

    def __str__(self):
        lines = [self.info_fname]
        lines.append(pprint.pformat(self))
        return '\n'.join(lines)

class SampleInfoGraph(dict):
    
    def __init__(self, sample_infos):
        self.graph = nx.DiGraph()
        self.nodes = dict()
        map(self._add_node, sample_infos)

    def _add_node(self, sample_info):
        self[sample_info.name] = sample_info
        self.nodes[sample_info.id] = sample_info
        for mid in sample_info.mothers():
            self.graph.add_edge(sample_info.id, mid)
            
    def oldest_ancestor(self, sample_info):
        ancestors = list(nx.dfs_preorder_nodes(self.graph, sample_info.id))
        print ancestors
        return self.nodes[ancestors[-1]]
        
