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
#'mindeltaRlb',
#'ratio_HTdHT3leadjets',
#'masslepJets1',
#'masslepJets2',
#'mindeltaR',
#'MT2bb',
#'masslepBJets0',
#'mass_lepBJet_mindr',
#'M_allJet_W',
#'HT_bjets',
#'lepEnergy',
#'firstcsvb_bb',
#'secondcsvb_bb',
#'thirdcsvb_bb',
#'deltaR_lepJetInMinMljet',
#'deltaR_lepbJetInMinMlb',
#'Sphericity',
#'minMlb',
#'MTlmet',
#'lepDR_minBBdr',
#'Jet5Pt',
#'Jet6Pt',
'XGB200_SR1',
'XGB400_SR1',
'XGB600_SR1',
'XGB800_SR1',
'XGB1000_SR1',
'XGB1300_SR1',
#'XGB1500_SR1',
#'lepEta',
#'lepPt',
#'lepPhi',
#'ST',
#'JetPt',
#'JetEta',
#'theLeadJetPt',
#'JetPhi',
#'MET',
#'NWJets',
#'NTJets',
#'deltaRjet2',
# 'NJets',
# 'NBJets',
#'HT',
#'METphi',
#'NPV',
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
	if not categorize: pfix='kinematics_R17_XGBcut_'+region#'kinematics_'+region
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
request_memory = 8000
Output = condor_%(iPlot)s.out
Error = condor_%(iPlot)s.err
Log = condor_%(iPlot)s.log
Priority = 20
Arguments = %(exeDir)s %(iPlot)s %(region)s %(isCategorized)s %(isEM)s %(nttag)s %(nWtag)s %(nbtag)s %(njets)s 
Queue 1"""%dict)
			jdf.close()

			os.system('condor_submit condor_'+iplot+'.job')
			#os.system('sleep 0.5')
			os.chdir('..')
			count+=1

print "Total jobs submitted:", count
                  
