# ExtractESynapseData

This program is intended for use with the RECONSTRUCT software developed by the Harris Lab.

This program extracts data from a CSV generated by RECONSTRUCT.
This CSV file should contain data on names, count, flat area, and volume of each object.

The following naming convention is assumed:

1) Every synapse of interest has a dendrite number, a synapse number, and axe number on the c-trace
ex. d01c01axe001, d123c45Aaxe678.
Branched naming conventions are accounted for up to quadruply branched protrusions
2) For mitochondria:
ex. d01c01axe001_mito1, d123c45Aaxe678_mito1.
3) For vesicles:
ex. d01c01axe001_ssvr, d123c45Aaxe678_ssvd.
4) For glia:
ex. d01g01_ASI, d123g45_pre.

For MSBs, the program will identify any c-traces with axon numbers that match any synapse on the dendrite of interest.
The user will then be prompted to check if the the two synapses are on the same bouton.
