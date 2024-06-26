import os,sys,datetime,itertools,shutil
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from utils import *

thisDir = os.getcwd()
outputDir = thisDir+'/'

region= 'SR'#'TTCR' #WJCR,SR --> matters only when plotting kinematics
categorize=0#1 #==categorize into t/W/b/j, 0==only split into flavor
#sigTrainedList=['500']#['300', '500', '800', '1000', '1500']#,'500','1000']

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)

iPlotList = [#distribution name as defined in "doHists.py"
'XGB200_SR1',
#'XGB400_SR1',
#'XGB600_SR1',
#'XGB800_SR1',
###'XGB1000_SR1',
#'XGB1300_SR1',
#'lepEta',
# 'lepPt',
# 'lepPhi',

#'ST',
#'JetPt',
#'JetEta',
#'theLeadJetPt',
#'JetPhi',
#'MET',
#'NWJets',
#'NTJets',
#'deltaRjet2',
#'NJets',
#'NBJets',
#'HT',
######'aveBBdr',
###### 'FW_momentum_0',
######'FW_momentum_1',
######'FW_momentum_2',
######'FW_momentum_3',
#######'FW_momentum_4',
######'FW_momentum_5',
######'FW_momentum_6',
######'mass_maxJJJpt',
######'Bjet1Pt',
######'deltaR_minBB',
######'deltaR',
######'MTlmet',
######'hemiout',
######'masslepJets0',
######'masslepJets1',
######'masslepJets2',
######'MT2bb',
######'masslepBJets0',
#####'mass_lepBJet_mindr',
######'secondJetPt',
######'fifthJetPt',
######'sixthJetPt',
######'PtFifthJet',
######'mass_minLLdr',
######'mass_maxBBmass',
######'deltaR_lepJetInMinMljet',
######'deltaPhi_lepJetInMinMljet',
######'deltaR_lepbJetInMinMlb',
######'deltaPhi_lepbJetInMinMlb',
######'M_allJet_W',
######'HT_bjets',
######'HTpt40',
######'ratio_HTdHT4leadjets',
######'csvJet1',
######'csvJet2',
######'csvJet3',
######'csvJet4',
######'firstcsvb_bb',
######'secondcsvb_bb',
######'thirdcsvb_bb',
######'fourthcsvb_bb',
######'NBJetsNoSF',
#####'HT_2m',
######'Sphericity',
######'Aplanarity',
######'BestTop_Disc', 
######'BestTop_Pt', 
#####'NoTop_Jet1_CSV', 
######'NoTop_Jet1_Pt', 
######'NoTop_Jet2_CSV', 
######'NoTop_Jet2_Pt',
####'XGB700_SR1', 
#######'XGB800_SR1', 
#######'XGB900_SR1', 
####'XGB1000_SR1',
#######'XGB1100_SR1',
#######'XGB1400_SR1',
#######'XGB1500_SR1',
######'XGB1600_SR1',
#######
######'XGB700_SR2', 
#######'XGB800_SR2', 
#######'XGB900_SR2', 
#######'XGB1000_SR2',
#######'XGB1100_SR2',
#######'XGB1200_SR2',
######'XGB1300_SR2',
#######'XGB1400_SR2',
#######'XGB1500_SR2',
######'XGB1600_SR2',
#######
#######'XGB700_SR3', 
#######'XGB800_SR3', 
#######'XGB900_SR3', 
######'XGB1000_SR3',
#######'XGB1100_SR3',
#######'XGB1200_SR3',
######'XGB1300_SR3',
#######'XGB1400_SR3',
#######'XGB1500_SR3',
######'XGB1600_SR3',
######
###### 			'minBBdr',
###### 			'aveBBdr',
###### 			'deltaEta_maxBB',
###### 			'FW_momentum_2',
###### 			'centrality',
###### 			'aveCSVpt',
###### 			'HT',
## 			'minMlb',
###### 			'Bjet1Pt',
###### 			'mass_maxJJJpt',
###### 			'MTlmet',
###### 			'lepDR_minBBdr',
###### 			'MET',
###### #  
###### 			'NPV',
###### 			'NJets',
###### 			'NBJets',
###### 			'HTpBDT',
###### 			'deltaPhi_METjets',
######			'min_deltaPhi_METjets'
######
###### 			'HTpDNN',	
			]

isEMlist = ['E','M']
if region=='SR' or region=='CR': nttaglist=['0','1p']
else: nttaglist = ['0p']
if region=='TTCR': nWtaglist = ['0p']
else: nWtaglist = ['0','1p']
if region=='WJCR': nbtaglist = ['0']
else: nbtaglist = ['1','2p']
if region=='PS': njetslist=['3p']
elif region=='CR': njetslist = ['4p']
else: njetslist = ['4p']
if not categorize:
    nttaglist = ['0p']
    nWtaglist = ['0p']
    nbtaglist = ['1p']
    njetslist = ['4p']
if not categorize and region=='PS':
    nttaglist = ['0p']
    nWtaglist = ['0p']
    nbtaglist = ['1p']
    njetslist = ['3p']

catList = list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist))


count=0
#for sigTrained in sigTrainedList:
if 1==1:

	pfix='templates_R17_final_'+region
	if not categorize: pfix='kinematics_R17_final_'+region#'kinematics_'+region
	pfix+='_'+date#+'_'+time
	outDir = outputDir+pfix
	if not os.path.exists(outDir): os.system('mkdir '+outDir)
	os.chdir(outputDir)
	#os.system('cp ../analyze.py doHists.py ../utils.py ../weights.py ../samples.py doCondorTemplates.py doCondorTemplates.sh '+outDir+'/')
        shutil.copy('../analyze.py', outDir+'/')
        shutil.copy('doHists.py', outDir+'/')
        shutil.copy('../utils.py', outDir+'/')
        shutil.copy('../weights.py', outDir+'/')
        shutil.copy('../samples.py', outDir+'/')
	os.chdir(outDir)

	for iplot in iPlotList:

		for cat in catList:
			#if skip(cat[4],cat[3]) and categorize: continue #DO YOU WANT TO HAVE THIS??
			catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]
#			print "Training: "+sigTrained+", iPlot: "+iplot+", cat: "+catDir
			if not os.path.exists(outDir+'/'+catDir): os.system('mkdir '+catDir)
			os.chdir(catDir)
			os.system('cp '+outputDir+'/doCondorTemplates.sh '+outDir+'/'+catDir+'/'+cat[0]+'T'+cat[1]+'W'+cat[2]+'B'+cat[3]+'J'+cat[4]+iplot+'.sh')
			shutil.copy('../analyze.py', './')
                        shutil.copy('../doHists.py', './')
                        shutil.copy('../utils.py', './')
                        shutil.copy('../weights.py', './')
                        shutil.copy('../samples.py', '.')						
	                #os.system('cp ../analyze.py ../doHists.py ../utils.py ../weights.py ../samples.py '+outDir+'/'+catDir+'/')
			dict={'dir':outputDir,'iPlot':iplot,'region':region,'isCategorized':categorize,
			      'isEM':cat[0],'nttag':cat[1],'nWtag':cat[2],'nbtag':cat[3],'njets':cat[4],
			      'exeDir':thisDir}
	
			jdf=open('condor_'+iplot+'.job','w')
			jdf.write(
"""universe = vanilla
Executable = %(isEM)sT%(nttag)sW%(nWtag)sB%(nbtag)sJ%(njets)s%(iPlot)s.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = analyze.py,doHists.py,utils.py,weights.py,samples.py
request_memory = 10000
Output = condor_%(iPlot)s.out
Error = condor_%(iPlot)s.err
Log = condor_%(iPlot)s.log
DesiredOS = SL7
Arguments = %(exeDir)s %(iPlot)s %(region)s %(isCategorized)s %(isEM)s %(nttag)s %(nWtag)s %(nbtag)s %(njets)s 
Queue 1"""%dict)
			jdf.close()

			os.system('condor_submit condor_'+iplot+'.job')
			#os.system('sleep 0.5')
			os.chdir('..')
			count+=1

print "Total jobs submitted:", count
                  
