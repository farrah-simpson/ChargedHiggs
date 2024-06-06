source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /uscms/home/fsimpson/nobackup/scratch/FWLJMETstuff/CMSSW_11_3_4/src/ChargedHiggs/SingleLepAnalyzer/makeTemplates
eval `scramv1 runtime -sh`

for i in 700 800 900 1000 1100 1200 1300 1400 1500 1600 
    do combineCards.py R17=limits_X53RHM${i}_kinematics_R17_final_CR_2024_6_4/cmb/combined.txt.cmb R18=limits_X53RHM${i}_kinematics_R18_final_CR_2024_5_25/cmb/combined.txt.cmb R16=limits_X53RHM${i}_kinematics_R16_final_CR_2024_5_25/cmb/combined.txt.cmb R16APV=limits_X53RHM${i}_kinematics_R16APV_final_CR_2024_5_25/cmb/combined.txt.cmb > limits_CR_combine_X53/workspace_M${i}.txt
    done

for i in 700 800 900 1000 1100 1200 1300 1400 1500 1600 
    do text2workspace.py limits_CR_combine_X53/workspace_M${i}.txt --channel-masks -o limits_CR_combine_X53/cmb/${i}/workspace.root
    python ../../../CombineHarvester/CombineTools/scripts/ValidateDatacards.py limits_CR_combine_X53/cmb/${i}/workspace.root
done

#for i in 700 800 900 1000 1100 1200 1300 1400 1500 1600 
#    do combineCards.py R17=limits_X53RHM${i}_kinematicsSRCR_R17_final/cmb/combined.txt.cmb R18=limits_X53RHM${i}_kinematicsSRCR_R18_final/cmb/combined.txt.cmb R16=limits_X53RHM${i}_kinematicsSRCR_R16_final/cmb/combined.txt.cmb R16APV=limits_X53RHM${i}_kinematicsSRCR_R16APV_final/cmb/combined.txt.cmb > limits_SRCR_combine_X53/workspace_M${i}.txt
#    done
#
#for i in 700 800 900 1000 1100 1200 1300 1400 1500 1600 
#    do text2workspace.py limits_SRCR_combine_X53/workspace_M${i}.txt --channel-masks -o limits_SRCR_combine_X53/cmb/${i}/workspace.root
#    python ../../../CombineHarvester/CombineTools/scripts/ValidateDatacards.py limits_SRCR_combine_X53/cmb/${i}/workspace.root
#done

for i in 700 800 900 1000 1100 1200 1300 1400 1500 1600 
    do combineCards.py R17=limits_X53RHM${i}_kinematics_R17_final_SR_2024_6_4/cmb/combined.txt.cmb R18=limits_X53RHM${i}_kinematics_R18_final_SR_2024_5_25/cmb/combined.txt.cmb R16=limits_X53RHM${i}_kinematics_R16_final_SR_2024_5_25/cmb/combined.txt.cmb R16APV=limits_X53RHM${i}_kinematics_R16APV_final_SR_2024_5_25/cmb/combined.txt.cmb > limits_combine_X53/workspace_M${i}.txt
    done

for i in 700 800 900 1000 1100 1200 1300 1400 1500 1600 
    do text2workspace.py limits_combine_X53/workspace_M${i}.txt --channel-masks -o limits_combine_X53/cmb/${i}/workspace.root
    python ../../../CombineHarvester/CombineTools/scripts/ValidateDatacards.py limits_combine_X53/cmb/${i}/workspace.root
done
