# Synchronization of the ZH->nunubb (missing energy channel)

The file `tree.root` contains a TTree called `events`, resulting from Colin's analysis sequence. Among other things, it contains the four vector of the two jets:

- jet1_px
- jet1_py
- jet1_pz
- jet1_e

And the value of the acoplanarity computed by Colin: 

- higgs_acop

The macro `acoplanarity.py` recomputes the acoplanarity and checks that for all events in the tree, the recomputed acoplanarity is equal to the one computed earlier. 

To run this script, just do:

```
python acoplanarity.py
```

You may now simply insert your acoplanarity code to make sure why it matches.
If not, you may use `pdb` for interactive debugging.

