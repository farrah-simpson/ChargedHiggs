#!/bin/bash
	source /cvmfs/cms.cern.ch/cmsset_default.sh
	cd /uscms/home/fsimpson/nobackup/scratch/FWLJMETstuff/CMSSW_10_2_10/src
	eval `scramv1 runtime -sh`
	cd /uscms_data/d3/fsimpson/scratch/FWLJMETstuff/CMSSW_10_2_10/src/ChargedHiggs/SingleLepAnalyzer/makeTemplates/combineLimits
	python dataCard.py kinematics_PS_2021_11_16 R17 HT lep100_MET100_DR1_HT510_jet1Pt200_jet2Pt100
	cd limits_R17_kinematics_PS_2021_11_16_lep100_MET100_DR1_HT510_jet1Pt200_jet2Pt100
	combineTool.py -M Significance -d cmb/*/workspace.root --there -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 -n .sig --parallel 4
	combineTool.py -M AsymptoticLimits -d cmb/*/workspace.root --there --run=blind --cminDefaultMinimizerStrategy 0 -n .limit --parallel 4
    combineTool.py -M CollectLimits */*/*.limit.* --use-dirs -o limits.json
    combineTool.py -M CollectLimits */*/*.sig.* --use-dirs -o sigs.json
	cd ..
