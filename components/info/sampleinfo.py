
import os
import fnmatch
import glob
import yaml
import re
import networkx as nx
import pprint

# fix bug in yaml 
# https://stackoverflow.com/questions/30458977/yaml-loads-5e-6-as-string-and-not-a-number
loader = yaml.SafeLoader
loader.add_implicit_resolver(
    u'tag:yaml.org,2002:float',
    re.compile(u'''^(?:
     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
    |\\.[0-9_]+(?:[eE][-+][0-9]+)?
    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
    |[-+]?\\.(?:inf|Inf|INF)
    |\\.(?:nan|NaN|NAN))$''', re.X),
    list(u'-+0123456789.'))

########################################################################
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
            info = yaml.load(tmp, Loader=loader) 
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

def find_samples(dirname, pattern):
    '''Find all samples with a yaml files in dirname'''
    matches = []
    for root, dirnames, filenames in os.walk(dirname):
        if len(fnmatch.filter(filenames, '*.yaml')):
            if pattern is None or fnmatch.fnmatch(root, pattern):
                matches.append(root)
    return matches


########################################################################
class SampleBase(dict):
    
    def __init__(self, basedirname, pattern=None):
        self.parent_graph = nx.DiGraph()
        self.child_graph = nx.DiGraph()
        self.nodes = dict()
        sampledirs = find_samples(basedirname, pattern)
        for sampledir in sampledirs:
            info = SampleInfo(sampledir)
            # adding the sample directory to the sample info
            info['sample']['directory'] = sampledir
            self._add_node(info)
            self[info.name] = info

    def _add_node(self, sample_info):
        self[sample_info.name] = sample_info
        self.nodes[sample_info.id] = sample_info
        for mid in sample_info.mothers():
            self.parent_graph.add_edge(sample_info.id, mid)
            self.child_graph.add_edge(mid, sample_info.id)
            
    def oldest_ancestor(self, sample_info):
        if not sample_info.id in self.parent_graph:
            return sample_info
        ancestors = list(nx.dfs_preorder_nodes(self.parent_graph, sample_info.id))
        return self.nodes[ancestors[-1]]
    
    def ancestors(self, sample_info):
        if not sample_info.id in self.parent_graph:
            return [sample_info]
        ancestors = list(nx.dfs_preorder_nodes(self.parent_graph, sample_info.id))
        return [self.nodes[i] for i in ancestors]
    
    def descendants(self, sample_info):
        if not sample_info.id in self.child_graph:
            return [sample_info]
        descendants = list(nx.dfs_preorder_nodes(self.child_graph, sample_info.id)) 
        return [self.nodes[i] for i in descendants]
        
