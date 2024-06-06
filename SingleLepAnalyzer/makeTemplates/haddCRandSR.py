import os,sys

masslist = ['600','700','800','900','1000','1100','1200','1300','1400','1500','1600']
postTag='2024_5_25'
postTag2='2024_5_25'
postTag3='2024_6_4'

# Combine:
os.system('hadd -f kinematicsSRCR_R16_final/templates_XGB1300_SR1_16p81fb_wNegBinsCorrec__rebinned_stat0p2.root'+' kinematics_R16_final_CR_'+postTag+'/templates_XGB1300_SR1_16p81fb_wNegBinsCorrec__rebinned_stat0p2.root'+'  kinematics_R16_final_SR_'+postTag+'/'+'templates_XGB1300_SR1_16p81fb_wNegBinsCorrec__rebinned_stat0p2.root')
os.system('hadd -f kinematicsSRCR_R16APV_final/templates_XGB1300_SR1_19p52fb_wNegBinsCorrec__rebinned_stat0p2.root'+' kinematics_R16APV_final_CR_'+postTag+'/templates_XGB1300_SR1_19p52fb_wNegBinsCorrec__rebinned_stat0p2.root'+'  kinematics_R16APV_final_SR_'+postTag+'/templates_XGB1300_SR1_19p52fb_wNegBinsCorrec__rebinned_stat0p2.root')
os.system('hadd -f kinematicsSRCR_R17_final/templates_XGB1300_SR1_41p48fb_wNegBinsCorrec__rebinned_stat0p2.root'+' kinematics_R17_final_CR_'+postTag3+'/templates_XGB1300_SR1_41p48fb_wNegBinsCorrec__rebinned_stat0p2.root'+'  kinematics_R17_final_SR_'+postTag3+'/templates_XGB1300_SR1_41p48fb_wNegBinsCorrec__rebinned_stat0p2.root')
os.system('hadd -f kinematicsSRCR_R18_final/templates_XGB1300_SR1_59p83fb_wNegBinsCorrec__rebinned_stat0p2.root'+' kinematics_R18_final_CR_'+postTag+'/templates_XGB1300_SR1_59p83fb_wNegBinsCorrec__rebinned_stat0p2.root'+'  kinematics_R18_final_SR_'+postTag2+'/templates_XGB1300_SR1_59p83fb_wNegBinsCorrec__rebinned_stat0p2.root')

masslistH = ['200','400','600','800']

for massH in masslistH:
	os.system('hadd -f kinematicsSRCR_R16_final/templates_XGB'+massH+'_SR1_16p81fb_wNegBinsCorrec__rebinned_stat0p2.root'+' kinematics_R16_final_CR_'+postTag+'/templates_XGB'+massH+'_SR1_16p81fb_wNegBinsCorrec__rebinned_stat0p2.root'+'  kinematics_R16_final_SR_'+postTag+'/'+'templates_XGB'+massH+'_SR1_16p81fb_wNegBinsCorrec__rebinned_stat0p2.root')
	os.system('hadd -f kinematicsSRCR_R16APV_final/templates_XGB'+massH+'_SR1_19p52fb_wNegBinsCorrec__rebinned_stat0p2.root'+' kinematics_R16APV_final_CR_'+postTag+'/templates_XGB'+massH+'_SR1_19p52fb_wNegBinsCorrec__rebinned_stat0p2.root'+'  kinematics_R16APV_final_SR_'+postTag+'/templates_XGB'+massH+'_SR1_19p52fb_wNegBinsCorrec__rebinned_stat0p2.root')
	os.system('hadd -f kinematicsSRCR_R17_final/templates_XGB'+massH+'_SR1_41p48fb_wNegBinsCorrec__rebinned_stat0p2.root'+' kinematics_R17_final_CR_'+postTag3+'/templates_XGB'+massH+'_SR1_41p48fb_wNegBinsCorrec__rebinned_stat0p2.root'+'  kinematics_R17_final_SR_'+postTag3+'/templates_XGB'+massH+'_SR1_41p48fb_wNegBinsCorrec__rebinned_stat0p2.root')
	os.system('hadd -f kinematicsSRCR_R18_final/templates_XGB'+massH+'_SR1_59p83fb_wNegBinsCorrec__rebinned_stat0p2.root'+' kinematics_R18_final_CR_'+postTag+'/templates_XGB'+massH+'_SR1_59p83fb_wNegBinsCorrec__rebinned_stat0p2.root'+'  kinematics_R18_final_SR_'+postTag2+'/templates_XGB'+massH+'_SR1_59p83fb_wNegBinsCorrec__rebinned_stat0p2.root')
