import os,sys,datetime,itertools,shutil
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from utils import *

thisDir = os.getcwd()
outputDir = thisDir+'/'

region='SR' #SR,CR --> matters only when plotting kinematics
categorize=1 #==categorize into t/W/b/j, 0==only split into flavor
#sigTrainedList=['500']#['300', '500', '800', '1000', '1500']#,'500','1000']

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)

lepPtCutList = [60,80,100] 
metCutList = [80,100,150]
drCutList = [0.25,1,1.25]
jet1PtCutList =[200,250,300] 
jet2PtCutList = [100,150,200]
AK4HTCutList = [510]

cutConfigs = list(itertools.product(lepPtCutList,metCutList,drCutList,jet1PtCutList,jet2PtCutList,AK4HTCutList))
iPlotList = [#distribution name as defined in "doHists.py"
#'Jet1Pt',
'ST',
#'minMlb',
#'topPt',
#'mass_minBBdr',
#'deltaR_lepBJet_maxpt',
#'lepDR_minBBdr',
#'centrality',
#'deltaEta_maxBB',
#'aveCSVpt',
#'aveBBdr',
#'FW_momentum_0',
#'FW_momentum_1',
#'FW_momentum_2',
#'FW_momentum_3',
#'FW_momentum_4',
#'FW_momentum_5',
#'FW_momentum_6',
#'mass_maxJJJpt',
#'Bjet1Pt',
#'deltaR_minBB',
#'deltaR',
#'MTlmet',
#'HT',
#'hemiout',
#'theLeadJetPt',
#'MET',
#'lepPt',
#'masslepJets0',
#'masslepJets1',
#'masslepJets2',
#'MT2bb',
#'masslepBJets0',
#'mass_lepBJet_mindr',
#'secondJetPt',
#'fifthJetPt',
#'sixthJetPt',
#'PtFifthJet',
#'mass_minLLdr',
#'mass_maxBBmass',
#'deltaR_lepJetInMinMljet',
#'deltaPhi_lepJetInMinMljet',
#'deltaR_lepbJetInMinMlb',
#'deltaPhi_lepbJetInMinMlb',
#'M_allJet_W',
#'HT_bjets',
#'HTpt40',
#'ratio_HTdHT4leadjets',
#'csvJet1',
#'csvJet2',
#'csvJet3',
#'csvJet4',
#'firstcsvb_bb',
#'secondcsvb_bb',
#'thirdcsvb_bb',
#'fourthcsvb_bb',
#'NJets',
#'NBJets',
#'NBJetsNoSF',
#'HT_2m',
#'Sphericity',
#'Aplanarity',
#'BestTop_Disc', 
#'BestTop_Pt', 
#'NoTop_Jet1_CSV', 
#'NoTop_Jet1_Pt', 
#'NoTop_Jet2_CSV', 
#'NoTop_Jet2_Pt',
#
#'XGB200_SR1',
#'XGB220_SR1',
#'XGB250_SR1',
#'XGB300_SR1',
#'XGB350_SR1',
#'XGB400_SR1',
#'XGB500_SR1',
#'XGB600_SR1',
#'XGB700_SR1',
#'XGB800_SR1',
#'XGB1000_SR1',
#'XGB1250_SR1',
#'XGB1500_SR1',
#'XGB1750_SR1',
#'XGB2000_SR1',
#'XGB2500_SR1',
#'XGB3000_SR1',
#
#'XGB200_SR2',
#'XGB220_SR2',
#'XGB250_SR2',
#'XGB300_SR2',
#'XGB350_SR2',
#'XGB400_SR2',
#'XGB500_SR2',
#'XGB600_SR2',
#'XGB700_SR2',
#'XGB800_SR2',
#'XGB1000_SR2',
#'XGB1250_SR2',
#'XGB1500_SR2',
#'XGB1750_SR2',
#'XGB2000_SR2',
#'XGB2500_SR2',
#'XGB3000_SR2',
#
#'XGB200_SR3',
#'XGB220_SR3',
#'XGB250_SR3',
#'XGB300_SR3',
#'XGB350_SR3',
#'XGB400_SR3',
#'XGB500_SR3',
#'XGB600_SR3',
#'XGB700_SR3',
#'XGB800_SR3',
#'XGB1000_SR3',
#'XGB1250_SR3',
#'XGB1500_SR3',
#'XGB1750_SR3',
#'XGB2000_SR3',
#'XGB2500_SR3',
#'XGB3000_SR3',






# 			'minBBdr',
# 			'aveBBdr',
# 			'deltaEta_maxBB',
# 			'FW_momentum_2',
# 			'centrality',
# 			'aveCSVpt',
# 			'HT',
# 			'minMlb',
# 			'Bjet1Pt',
# 			'mass_maxJJJpt',
# 			'MTlmet',
# 			'lepDR_minBBdr',
# 			'MET',
# #  
# 			'NPV',
#       		'lepPt',
#       		'lepEta',
#       		'JetEta',
# 'JetPt',
# 			'NJets',
# 			'NBJets',
# 			'HTpBDT',
# 			'deltaPhi_METjets',
#			'min_deltaPhi_METjets'

## 			'HTpDNN',	
			]

isEMlist = ['E','M']
if region=='SR': nttaglist=['0','1p']
else: nttaglist = ['0p']
if region=='TTCR': nWtaglist = ['0p']
else: nWtaglist = ['0','1p']
if region=='WJCR': nbtaglist = ['0']
elif region=='CR': nbtaglist = ['0','0p','1p']
else: nbtaglist = ['1','2p']
if region=='PS': njetslist=['3p']
else: njetslist = ['4p']
if not categorize:
    nttaglist = ['0p']
    nWtaglist = ['0p']
    nbtaglist = ['1p']
    njetslist = ['3p']

catList = list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist))

pfix='templates'
if not categorize: pfix='kinematics_'+region
pfix+='_'+date#+'_'+time
#pfix+='_M'+sigTrained+'_'+date+"_topPtRW_NOHTWeight_Full_FixTrig_forlimit"#+'_'+time
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


count=0
#for sigTrained in sigTrainedList:
for conf in cutConfigs:
	lepPtCut,metCut,drCut,jet1PtCut,jet2PtCut,AK4HTCut=conf[0],conf[1],conf[2],conf[3],conf[4],conf[5]
	#if jet2PtCut > jet1PtCut: continue
	cutString = 'lep'+str(int(lepPtCut))+'_MET'+str(int(metCut))+'_DR'+str(drCut)
	cutString+= '_HT'+str(AK4HTCut)
	cutString+= '_jet1Pt'+str(jet1PtCut) + '_jet2Pt'+str(jet2PtCut)
	os.chdir(outDir)
	if not os.path.exists(outDir+'/'+cutString): os.system('mkdir '+cutString)
	os.chdir(cutString)
	#os.system('cp ../analyze.py doHists.py ../utils.py ../weights.py ../samples.py doCondorTemplates.py doCondorTemplates.sh '+outDir+'/')
        #shutil.copy('../analyze.py', outDir+'/')
        #shutil.copy('doHists.py', './')
        #shutil.copy('../utils.py', './')
        #shutil.copy('../weights.py', './')
        #shutil.copy('../samples.py', './')
	#os.chdir(outDir)

	for iplot in iPlotList:

		for cat in catList:
			#if skip(cat[4],cat[3]) and categorize: continue #DO YOU WANT TO HAVE THIS??
			catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]
#			print "Training: "+sigTrained+", iPlot: "+iplot+", cat: "+catDir
			if not os.path.exists(outDir+'/'+cutString+'/'+catDir): os.system('mkdir '+catDir)
			os.chdir(catDir)
			os.system('cp '+outputDir+'/doCondorTemplates_opt.sh '+outDir+'/'+cutString+'/'+catDir+'/'+cat[0]+'T'+cat[1]+'W'+cat[2]+'B'+cat[3]+'J'+cat[4]+iplot+'.sh')
			shutil.copy('../../analyze.py', './')
                        shutil.copy('../../doHists.py', './')
                        shutil.copy('../../utils.py', './')
                        shutil.copy('../../weights.py', './')
                        shutil.copy('../../samples.py', '.')						
	                #os.system('cp ../analyze.py ../doHists.py ../utils.py ../weights.py ../samples.py '+outDir+'/'+catDir+'/')
			dict={'dir':outputDir,'iPlot':iplot,'region':region,'isCategorized':categorize,
			      'isEM':cat[0],'nttag':cat[1],'nWtag':cat[2],'nbtag':cat[3],'njets':cat[4],
			      'lepPtCut':conf[0],'metCut':conf[1],'drCut':conf[2],'jet1PtCut':conf[3],'jet2PtCut':conf[4],'AK4HTCut':conf[5],
			      'exeDir':thisDir}
	
			jdf=open('condor_'+iplot+'.job','w')
			jdf.write(

"""universe = vanilla
Executable = %(isEM)sT%(nttag)sW%(nWtag)sB%(nbtag)sJ%(njets)s%(iPlot)s.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = analyze.py,doHists.py,utils.py,weights.py,samples.py
request_memory = 3072
Output = condor_%(iPlot)s.out
Error = condor_%(iPlot)s.err
Log = condor_%(iPlot)s.log
Arguments = %(exeDir)s %(iPlot)s %(region)s %(isCategorized)s %(isEM)s %(nttag)s %(nWtag)s %(nbtag)s %(njets)s %(lepPtCut)s %(metCut)s %(drCut)s %(jet1PtCut)s %(jet2PtCut)s %(AK4HTCut)s 
Queue 1"""%dict)
			jdf.close()

			os.system('condor_submit condor_'+iplot+'.job')
			#os.system('sleep 0.5')
			os.chdir('..')
			count+=1

print "Total jobs submitted:", count
                  
