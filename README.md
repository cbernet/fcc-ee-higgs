# fcc-ee-higgs
Higgs coupling analyses for FCC-ee

## Samples 

### Sample organization

Samples are placed in a base directory chosen by the user, e.g. `~/Datasets/FCC/fcc_ee_higgs/samples/`. 

The official samples are in ` /eos/experiment/fcc/ee/datasets`

Each sample is in a subdirectory, e.g. `heppy/ee_to_ZH_Z_to_ll/CLIC_FCCee/Jan30/ee_to_ZH_Oct30`. This subdirectory substring is enough to identify the sample, and is used as the sample name. 

For samples produced with `heppy (papas)`, the sample subdirectory contains: 

 - a root file `fcc_ee_higgs.analyzers.ZHTreeProducer.ZHTreeProducer_1/tree.root` containing the `events` TTree. 
 - the `info.yaml` file that contains information about data processing: 

```yaml

processing:
  nfiles: 100
  ngoodfiles: 97
sample:
  id: !!python/object:uuid.UUID
    int: 202928111438401843621742064401199831137
  jobtype: heppy
  mother: pythia/ee_to_ZH_Oct30
  nevents: 32864
  nfiles: 1
  ngoodfiles: 1
  pattern: fcc_ee_higgs.analyzers.ZHTreeProducer.ZHTreeProducer_1/tree.root
software:
  fcc_datasets: !!python/unicode 'df41188443d8b15436543f854ee7de77a6934036'
  fcc_ee_higgs: !!python/unicode 'b01b8340ea89aa7cdbfbf9ac510f0bafc8f308b0'
  heppy: !!python/unicode '7cb2d942997594a80988187d0ab50901627575b4'
```

In this file: 

 - The `processing` section gives the total number of jobs (`nfiles`) and the total number of successful jobs (`ngoodfiles`) for the production of this sample. The computing efficiency `ngoodfiles/njobs` should be accounting for in the sample normalization.
 - The `sample` section gives information about this sample, and in particular the name of its mother. 
 - The `software` section gives the github commitid for the various software packages used to process the sample. It can be used to check that the different samples used in a given analysis are indeed compatible. Please note that the commitid do not have to be the same in a given analysis. However, if the commitids are different, you should probably check with git that no change has been made to the physics of the simulation or the analysis code between these commitids.  

### Sample list

#### Pythia samples 

All `heppy (papas)` samples were produced by reading the `pythia` samples.

|Sample name |Pythia cross-section (pb) |Number of generated events|sqrts |Comments |
|---|---|---|---|---|
|`pythia/ee_to_ZH_Oct30` |0.2 |5e5 |240 |Inclusive ZH production |
|`pythia/ee_to_ZZ_Sep12_A_2`|1.35 |2e6 |240 |Inclusive ZZ production |
|`pythia/ee_to_WW_Dec6_large`|16.4 |4e6 |240 |Inclusive WW production |

#### Heppy samples

[Jan30, CLIC-FCCee](results/Jan30/clic.md)

[Jan30, CMS](results/Jan30/cms.md)


## Analyzing the TTree

The variables should be self-explanatory. 
The plotting code I use is here: 

 - [ZH->ll(bb)](https://github.com/cbernet/fcc-ee-higgs/blob/master/plot/plot_ZH_ll.py)
 - [ZH->nunubb](https://github.com/cbernet/fcc-ee-higgs/blob/master/plot/plot_ZH_nunubb.py)

For example, for the CLIC-FCCee detector, the first script in bb mode currently plots the variable:

`recoil_m`

With this selection: 

`
(zeds_1_iso_e/zeds_1_e<0.2) && (zeds_1_iso_e/zeds_1_e<0.2) && zeds_1_e>0 && zeds_2_e>0 && (abs(zeds_m-91)<4. && zeds_pt>10 && zeds_pz<50 && zeds_acol>100 && zeds_cross>10) && (zeds_1_pdgid==-zeds_2_pdgid)  && ((jets_1_e<0 || jets_1_22_e/jets_1_e<0.8) && (jets_2_e<0 || jets_2_22_e/jets_2_e<0.8)) && (((jets_1_bmatch==1 && rndm<0.8) || (jets_1_bmatch==0 && rndm<0.004))  ||  ((jets_2_bmatch==1 && rndm<0.8) || (jets_2_bmatch==0 && rndm<0.004)))
`

For the CMS detector, the selection implements a different b tagging working point:  

`
(zeds_1_iso_e/zeds_1_e<0.2) && (zeds_1_iso_e/zeds_1_e<0.2) && zeds_1_e>0 && zeds_2_e>0 && (abs(zeds_m-91)<4. && zeds_pt>10 && zeds_pz<50 && zeds_acol>100 && zeds_cross>10) && (zeds_1_pdgid==-zeds_2_pdgid)  && ((jets_1_e<0 || jets_1_22_e/jets_1_e<0.8) && (jets_2_e<0 || jets_2_22_e/jets_2_e<0.8)) && (((jets_1_bmatch==1 && rndm<0.6) || (jets_1_bmatch==0 && rndm<0.003))  ||  ((jets_2_bmatch==1 && rndm<0.6) || (jets_2_bmatch==0 && rndm<0.003)))
`

**Please note that the master commit will move overtime! If this documentation gets outdated, tell me.** 

## Analysis instructions


### lxplus

Create your working directory: 

```bash
mkdir test_ana
cd test_ana
git clone https://github.com/HEP-FCC/heppy.git
git clone https://github.com/cbernet/fcc_datasets.git
git clone https://github.com/cbernet/fcc-ee-higgs.git fcc_ee_higgs
git clone https://github.com/cbernet/cpyroot.git
git clone https://github.com/cbernet/tdr-style.git tdrstyle
```

Initialize your environment: 

```bash
source /cvmfs/fcc.cern.ch/sw/0.8.1/init_fcc_stack.sh
cd heppy
source ./init.sh
cd ..
cd fcc_datasets
source ./init.sh
cd ..
export FCCDATASETBASEOUT=/eos/experiment/fcc/ee/datasets
export PYTHONPATH=$PWD:$PYTHONPATH
```

You should now be able to use the official datasets. For example, list one of the `heppy (papas)` datasets: 

```bash
lsdataset.py heppy/ee_to_ZH_Z_to_ll/CLIC_FCCee/Jan30/ee_to_ZH_Oct30
>
heppy/ee_to_ZH_Z_to_ll/CLIC_FCCee/Jan30/ee_to_ZH_Oct30
/afs/cern.ch/user/c/cbern/work/FCC/fcc_ee_higgs/samples/heppy/ee_to_ZH_Z_to_ll/CLIC_FCCee/Jan30/ee_to_ZH_Oct30
fcc_ee_higgs.analyzers.ZHTreeProducer.ZHTreeProducer_1/tree.root : {'good': True, 'n_events': 32864, 'zero_size': False}
{'processing': {'nfiles': 100, 'ngoodfiles': 100},
 'sample': {'id': UUID('98aa885a-f206-4c87-9479-dbe5316e9861'),
            'jobtype': 'heppy',
            'mother': 'pythia/ee_to_ZH_Oct30',
            'nevents': 32864,
            'nfiles': 1,
            'ngoodfiles': 1,
            'pattern': 'fcc_ee_higgs.analyzers.ZHTreeProducer.ZHTreeProducer_1/tree.root'},
 'software': {'fcc_datasets': u'df41188443d8b15436543f854ee7de77a6934036',
              'fcc_ee_higgs': u'b01b8340ea89aa7cdbfbf9ac510f0bafc8f308b0',
              'heppy': u'7cb2d942997594a80988187d0ab50901627575b4'}}
```

Now go to the fcc_ee_higgs directory and start ipython

```bash 
cd fcc_ee_higgs
ipython
```

Plot the mass recoiling against the Z boson, which decays to two leptons: 

```python
%run plot/plot_ZH_ll.py
```
