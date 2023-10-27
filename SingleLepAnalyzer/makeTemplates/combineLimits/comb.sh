#!/bin/bash

Mass=${1}

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /home/jluo48/ChargedHiggs/CMSSW_10_2_10/src/ChargedHiggs/SingleLepAnalyzer/makeTemplates/combineLimits/limits_Hptb${Mass}_M500_2023_5_14_topPtRW_NOHTWeight_Full_FixTrig_forlimit_XGB${Mass}  #/home/jluo48/CMSSW_10_2_13/src
eval `scramv1 runtime -sh`
#cd ChargedHiggs/SingleLepAnalyzer/makeTemplates/combineLimits/limits_Hptb${Mass}_M500_2023_5_14_topPtRW_NOHTWeight_Full_FixTrig_forlimit_XGB${Mass}   #limits_Hptb${Mass}_M500_2021_3_2_topPtRW_allweights_UL17_Reshape_ReNorm2D_HTnj_XGBs_split_XGB${Mass}
#combine -M AsymptoticLimits cmb/workspace.root --cminDefaultMinimizerStrategy 0 &> asy_m${Mass}.txt
combine -M AsymptoticLimits cmb/workspace.root --run=blind --cminDefaultMinimizerStrategy 0 &> asy_m${Mass}.txt
