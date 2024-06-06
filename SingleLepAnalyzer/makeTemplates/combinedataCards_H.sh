source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /uscms/home/fsimpson/nobackup/scratch/FWLJMETstuff/CMSSW_11_3_4/src/ChargedHiggs/SingleLepAnalyzer/makeTemplates
eval `scramv1 runtime -sh`

for j in 200 400 600 800
do
	for i in 600 700 800 900 1000 1100 1200 1300 1400 1500 

	do
		if [[ $(($i - $j - 173))  -gt 0 ]]
		then
  		combineCards.py R17=limits_X53M${i}_kinematics_R17_final_CR_2024_6_4MH${j}/cmb/combined.txt.cmb R18=limits_X53M${i}_kinematics_R18_CR_final_2024_5_25MH${j}/cmb/combined.txt.cmb R16=limits_X53M${i}_kinematics_R16_final_CR_2024_5_25MH${j}/cmb/combined.txt.cmb R16APV=limits_X53M${i}_kinematics_R16APV_final_CR_2024_5_25MH${j}/cmb/combined.txt.cmb > limits_CR_combine_X53MH${j}/workspace_M${i}.txt
		fi	
    	done
done

for j in 200 400 600 800
do
	for i in 600 700 800 900 1000 1100 1200 1300 1400 1500 
	do
		if [[ $(($i - $j - 173))  -gt 0 ]]
		then
  		text2workspace.py limits_CR_combine_X53MH${j}/workspace_M${i}.txt --channel-masks -o limits_CR_combine_X53MH${j}/cmb/${i}/workspace.root
		fi
	done
done

#for j in 200 400 600 800
#do
#	for i in 600 700 800 900 1000 1100 1200 1300 1400 1500 
#
#	do
#		if [[ $(($i - $j - 173))  -gt 0 ]]
#		then
#    		combineCards.py R17=limits_X53M${i}_kinematicsSRCR_R17_finalMH${j}/cmb/combined.txt.cmb R18=limits_X53M${i}_kinematicsSRCR_R18_finalMH${j}/cmb/combined.txt.cmb R16=limits_X53M${i}_kinematicsSRCR_R16_finalMH${j}/cmb/combined.txt.cmb R16APV=limits_X53M${i}_kinematicsSRCR_R16APV_finalMH${j}/cmb/combined.txt.cmb > limits_SRCR_combine_X53MH${j}/workspace_M${i}.txt
#		fi	
#    	done
#done
#
#for j in 200 400 600 800
#do
#	for i in 600 700 800 900 1000 1100 1200 1300 1400 1500 
#	do
#		if [[ $(($i - $j - 173))  -gt 0 ]]
#		then
#    		text2workspace.py limits_SRCR_combine_X53MH${j}/workspace_M${i}.txt --channel-masks -o limits_SRCR_combine_X53MH${j}/cmb/${i}/workspace.root
#		fi
#	done
#done

for j in 200 400 600 800
do
	for i in 600 700 800 900 1000 1100 1200 1300 1400 1500 

	do
		if [[ $(($i - $j - 173))  -gt 0 ]]
		then
    		combineCards.py R17=limits_X53M${i}_kinematics_R17_final_SR_2024_6_4MH${j}/cmb/combined.txt.cmb R18=limits_X53M${i}_kinematics_R18_final_SR_2024_5_25MH${j}/cmb/combined.txt.cmb R16=limits_X53M${i}_kinematics_R16_final_SR_2024_5_25MH${j}/cmb/combined.txt.cmb R16APV=limits_X53M${i}_kinematics_R16APV_final_SR_2024_5_25MH${j}/cmb/combined.txt.cmb > limits_combine_X53MH${j}/workspace_M${i}.txt
		fi	
    	done
done

for j in 200 400 600 800
do
	for i in 600 700 800 900 1000 1100 1200 1300 1400 1500 
	do
		if [[ $(($i - $j - 173))  -gt 0 ]]
		then
    		text2workspace.py limits_combine_X53MH${j}/workspace_M${i}.txt --channel-masks -o limits_combine_X53MH${j}/cmb/${i}/workspace.root
		fi
	done
done
