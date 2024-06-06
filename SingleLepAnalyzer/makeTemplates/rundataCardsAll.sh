source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /uscms/home/fsimpson/nobackup/scratch/FWLJMETstuff/CMSSW_11_3_4/src/ChargedHiggs/SingleLepAnalyzer/makeTemplates
eval `scramv1 runtime -sh`

for Mass in 700 800 900 1000 1100 1200 1300 1400 1500 1600 
    do 
	python combineLimits/dataCard_XXnew.py kinematics_R16APV_final_CR_2024_5_25/ R16APV XGB1300_SR1 ${Mass}
	python combineLimits/dataCard_XXnew.py kinematics_R16_final_CR_2024_5_25/ R16 XGB1300_SR1 ${Mass}
	python combineLimits/dataCard_XXnew.py kinematics_R17_final_CR_2024_6_4/ R17 XGB1300_SR1 ${Mass}
	python combineLimits/dataCard_XXnew.py kinematics_R18_final_CR_2024_5_25/ R18 XGB1300_SR1 ${Mass}
    done

#for Mass in 700 800 900 1000 1100 1200 1300 1400 1500 1600 
#    do 
#	python combineLimits/dataCard_XXnew.py kinematicsSRCR_R16APV_final/ R16APV XGB1300_SR1 ${Mass}
#	python combineLimits/dataCard_XXnew.py kinematicsSRCR_R16_final/ R16 XGB1300_SR1 ${Mass}
#	python combineLimits/dataCard_XXnew.py kinematicsSRCR_R17_final/ R17 XGB1300_SR1 ${Mass}
#	python combineLimits/dataCard_XXnew.py kinematicsSRCR_R18_final/ R18 XGB1300_SR1 ${Mass}
#    done

for Mass in 700 800 900 1000 1100 1200 1300 1400 1500 1600 
    do 
	#python combineLimits/dataCard_XXnew.py kinematics_R16APV_final_SR_2024_5_25/ R16APV XGB1300_SR1 ${Mass}
	#python combineLimits/dataCard_XXnew.py kinematics_R16_final_SR_2024_5_25/ R16 XGB1300_SR1 ${Mass}
	python combineLimits/dataCard_XXnew.py kinematics_R17_final_SR_2024_6_4/ R17 XGB1300_SR1 ${Mass}
	#python combineLimits/dataCard_XXnew.py kinematics_R18_final_SR_2024_5_25/ R18 XGB1300_SR1 ${Mass}
    done


