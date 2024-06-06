#!/bin/bash

Mass=${1}
source /cvmfs/cms.cern.ch/cmsset_default.sh

cd /uscms/home/fsimpson/nobackup/scratch/FWLJMETstuff/CMSSW_10_2_10/src/ChargedHiggs/SingleLepAnalyzer/makeTemplates

eval `scramv1 runtime -sh`

python combineLimits/dataCard_XXH.py kinematics_R16APV_final_SR_2024_4_5/ R16APV XGB${Mass}_SR1 ${Mass}
python combineLimits/dataCard_XXH.py kinematics_R16_final_SR_2024_4_5/ R16 XGB${Mass}_SR1 ${Mass}
python combineLimits/dataCard_XXH.py kinematics_R17_final_SR_2024_4_5/ R17 XGB${Mass}_SR1 ${Mass}
python combineLimits/dataCard_XXH.py kinematics_R18_final_SR_2024_4_7/ R18 XGB${Mass}_SR1 ${Mass}
