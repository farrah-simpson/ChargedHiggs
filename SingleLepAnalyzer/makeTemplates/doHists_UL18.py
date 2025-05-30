#!/usr/bin/python
  
import os,sys,time,math,datetime,pickle,itertools,getopt
from ROOT import TH1D,gROOT,TFile,TTree
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from numpy import linspace
import argparse
from weights_UL18 import *
from analyze_UL18 import *
from samples_UL18 import *
from utils import *

gROOT.SetBatch(1)
start_time = time.time()

# parser = argparse.ArgumentParser(description='Welcome to singleLepAnalyzer!')
# parser.add_argument('-i','--input', help='Input file name',required=True)
# parser.add_argument('-o','--output',help='Output file name', required=True)
# args = parser.parse_args()
doOpt = False
lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb
ntupleDir = '/isilon/hadoop/store/user/fsimpson/UL18/step3_XGB_final/nominal/'#'root://cmseos.fnal.gov//store/user/fsimpson/FWLJMET106XUL_singleLep2017UL_RunIISummer20v2_step2/nominal/' 
#step1Dir = 'root://cmseos.fnal.gov//store/user/fsimpson/UL17/step3_XGB/nominal/'#'root://cmseos.fnal.gov//store/user/fsimpson/FWLJMET106XUL_singleLep2018UL_RunIISummer20v2_step2/nominal/' #lpcbril/FWLJMET106X_1lep2017_UL_step2_b0_XGBs_added_sys_new/nominal/'
#ntupleDir  = 'root://cmseos.fnal.gov//store/user/fsimpson/FWLJMET106XUL_singleLep2017UL_RunIISummer20v2_step2/nominal/'#/UL17/step3_XGB_final/nominal/'
#ntupleDir  = 'root://cmseos.fnal.gov//store/user/fsimpson/FWLJMET106XUL_singleLep2016APVUL_RunIISummer20v2_step2/nominal/'#'root://cmseos.fnal.gov//store/user/fsimpson/UL17/step3_XGB/nominal/'

"""
Note: 
--Each process in step1 (or step2) directories should have the root files hadded! 
--The code will look for <ntupleDir>/<process>_hadd.root for nominal trees.
The uncertainty shape shifted files will be taken from <ntupleDir>/../<shape>/<process>_hadd.root,
where <shape> is for example "JECUp". hadder.py can be used to prepare input files this way! 
--Each process given in the lists below must have a definition in "samples.py"
--Check the set of cuts in "analyze.py"
"""	
N=10

bkgList = [
		  #'DYMG', 
		  'TTWl','TTWq','TTZlM10','TTZlM1to10', 'TTHH', 'TTWH', 'TTWW','TTWZ','TTZH','TTZZ','TTHB','TTHnoB',#'TTTT',
                  'DYMG200','DYMG400','DYMG600','DYMG800','DYMG1200','DYMG2500',
		  'QCDht200','QCDht300',
                  'QCDht500',
                  'QCDht700','QCDht1000','QCDht1500','QCDht2000',
		  'Tt','Tbt','Ts','TtW','TbtW',
                  #'WJetsMG',
		  'WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800', 'WJetsMG1200', 'WJetsMG2500',
		  #'WJetsMG1200_1','WJetsMG1200_2','WJetsMG1200_3','WJetsMG1200_4','WJetsMG1200_5',
		  #'WJetsMG2500_1','WJetsMG2500_2','WJetsMG2500_3','WJetsMG2500_4','WJetsMG2500_5', 'WJetsMG2500_6',
	 	  #'TTJets2L2nu0','TTJets2L2nu700','TTJets2L2nu1000',		  
		  #'TTJetsHad0','TTJetsHad700','TTJetsHad1000',		 
		  #'TTJetsSemiLep0','TTJetsSemiLep700','TTJetsSemiLep1000',
                  'TTToHadronic', 'TTTo2L2Nu', 'TTToSemiLeptonic', 
		  #'TTJetsSemiLepNjet9bin1','TTJetsSemiLepNjet9bin2','TTJetsSemiLepNjet9bin3',
		  #'TTJetsSemiLep1','TTJetsSemiLep2','TTJetsSemiLep3','TTJetsSemiLep4','TTJetsSemiLep5','TTJetsSemiLep6',		  
		  #'TTJets700mtt','TTJets1000mtt',
          'WW','WZ','ZZ',
		  ]
		  
ttFlvs = ['_tt2b','_ttbb','_tt1b','_ttcc','_ttjj']
dataList = ['DataE','DataM']

whichSignal = 'X53' #Hptb,HTB, TTM, BBM, or X53X53M
#massList = [300] 
if whichSignal == 'X53H':sigList = ['X53M600MH200','X53M600MH400','X53M700MH200','X53M700MH400','X53M800MH200','X53M800MH400','X53M800MH600','X53M900MH200','X53M900MH400','X53M900MH600','X53M1000MH200','X53M1000MH400','X53M1000MH600','X53M1000MH800','X53M1100MH200','X53M1100MH400','X53M1100MH600','X53M1100MH800','X53M1200MH200','X53M1200MH400','X53M1200MH600','X53M1200MH800','X53M1200MH1000','X53M1500MH200','X53M1500MH400','X53M1500MH600','X53M1500MH800','X53M1500MH1000']
if whichSignal == 'X53':
	sigList= [whichSignal+'RHM'+str(mass) for mass in range(700,1700+1,100)]

#sigList = [whichSignal+str(mass) for mass in massList]
#sigList = []
if whichSignal=='Hptb' or 'X53' or 'X53H': decays = ['']

 
sigTrained = 'Low1'
if not doOpt:
	if len(sys.argv)>10: sigTrained=sys.argv[10]
iPlot = 'XGB1300_SR1' #choose a discriminant from plotList below!
if len(sys.argv)>2: iPlot=sys.argv[2]
region = 'CR'
if len(sys.argv)>3: region=sys.argv[3]
isCategorized = False
BDTSR_Merged = False
if len(sys.argv)>4: isCategorized=int(sys.argv[4])
doJetRwt= 0
doAllSys=True 
doPDF = True


if region=='PS' or region=='CR' or region=='SR': sigList =['X53M1600MH200','X53M1600MH400','X53M1600MH600','X53M1600MH800','X53M1600MH1000','X53M1700MH200','X53M1700MH400','X53M1700MH600','X53M1700MH800','X53M1700MH1000','X53M1300MH200','X53M1300MH400','X53M1300MH600','X53M1300MH800','X53M1300MH1000','X53M1400MH200','X53M1400MH400','X53M1400MH600','X53M1400MH800','X53M1400MH1000','X53M600MH200','X53M600MH400','X53M700MH200','X53M700MH400','X53M800MH200','X53M800MH400','X53M800MH600','X53M900MH200','X53M900MH400','X53M900MH600','X53M1000MH200','X53M1000MH400','X53M1000MH600','X53M1000MH800','X53M1100MH200','X53M1100MH400','X53M1100MH600','X53M1100MH800','X53M1200MH200','X53M1200MH400','X53M1200MH600','X53M1200MH800','X53M1200MH1000','X53M1500MH200','X53M1500MH400','X53M1500MH600','X53M1500MH800','X53M1500MH1000'] + [whichSignal+'RHM'+str(mass) for mass in range(700,1700+1,100)]
 

#lepPtCut= 100#, 80, 100] 
#metCut = 100#,100,150]
#drCut = 1#,1,1.25]
#jet1PtCut =200#,250,300] 
#jet2PtCut = 100#,150,200]
#jet3PtCut = 0
#AK4HTCut = 510
#DISABLED LEP PT CUT IN ANALYZE!!!
cutList = {'lepPtCut':30,'metCut':30,'mtCut':0,'drCut':1.0,'jet1PtCut':30,'jet2PtCut':30,'jet3PtCut':0, 'AK4HTCut':350} 
#if region=='CR':cutList = {'lepPtCut':30,'metCut':30,'mtCut':0,'drCut':0,'jet1PtCut':30,'jet2PtCut':30,'jet3PtCut':0, 'AK4HTCut':350} 
if region=='SR':cutList = {'lepPtCut':30,'metCut':30,'mtCut':0,'drCut':1.0,'jet1PtCut':30,'jet2PtCut':30,'jet3PtCut':0, 'AK4HTCut':500}#, 'XGB':'XGB1300_SR1'}

#if region=='SR' and whichSignal == 'X53':cutList = {'lepPtCut':30,'metCut':30,'mtCut':0,'drCut':1.0,'jet1PtCut':250,'jet2PtCut':130,'jet3PtCut':30, 'AK4HTCut':350, 'XGB':'XGB1300_SR1'}
#if region=='SR' and whichSignal == 'X53H':cutList = {'lepPtCut':30,'metCut':30,'mtCut':0,'drCut':1.0,'jet1PtCut':250,'jet2PtCut':130,'jet3PtCut':30, 'AK4HTCut':350, 'XGB':'XGB200_SR1'}
#cutList = {'lepPtCut':100,'metCut':100,'mtCut':0,'drCut':1.0,'jet1PtCut':200,'jet2PtCut':100,'jet3PtCut':0, 'AK4HTCut':450}
#cutList = {'lepPtCut':100,'metCut':150,'mtCut':0,'drCut':1.25,'jet1PtCut':200,'jet2PtCut':100,'jet3PtCut':0, 'AK4HTCut':510}
if region=='PS': cutList = {'lepPtCut':30,'metCut':30,'mtCut':0,'drCut':0,'jet1PtCut':30,'jet2PtCut':30, 'jet3PtCut':0, 'AK4HTCut':500}#{'lepPtCut':80,'metCut':100,'mtCut':0,'drCut':0,'jet1PtCut':250,'jet2PtCut':150, 'jet3PtCut':0, 'AK4HTCut':510}
if region=='CR': cutList = {'lepPtCut':30,'metCut':30,'mtCut':0,'drCut':0,'jet1PtCut':30,'jet2PtCut':30, 'jet3PtCut':0, 'AK4HTCut':500}#,'XGB':'XGB1300_SR1'}

#if region=='CR' and whichSignal == 'X53': cutList = {'lepPtCut':30,'metCut':30,'mtCut':0,'drCut':0,'jet1PtCut':250,'jet2PtCut':130, 'jet3PtCut':30, 'AK4HTCut':350,'XGB':'XGB1300_SR1'}
#if region=='CR' and whichSignal == 'X53H': cutList = {'lepPtCut':30,'metCut':30,'mtCut':0,'drCut':0,'jet1PtCut':250,'jet2PtCut':130, 'jet3PtCut':30, 'AK4HTCut':350,'XGB':'XGB200_SR1'}

#if region=='PS' or region=='CR': cutList = {'lepPtCut':80,'metCut':100,'mtCut':0,'drCut':0,'jet1PtCut':250,'jet2PtCut':150, 'jet3PtCut':30, 'AK4HTCut':510}

#if (region=='SR' or 'CR' in region) and (iPlot=='ST' or iPlot=='HT'):
#    cutList = {'lepPtCut':80,'metCut':100,'mtCut':0,'drCut':1,'jet1PtCut':250,'jet2PtCut':150, 'jet3PtCut':0, 'AK4HTCut':510}
#    cutList = {'lepPtCut':100,'metCut':100,'mtCut':0,'drCut':1.0,'jet1PtCut':200,'jet2PtCut':100, 'jet3PtCut':0, 'AK4HTCut':450}
if doOpt:
	if len(sys.argv)>10: lepPtCut = float(sys.argv[10]) 
	if len(sys.argv)>11: metCut = float(sys.argv[11]) 
	if len(sys.argv)>12: drCut = float(sys.argv[12]) 
	if len(sys.argv)>13: jet1PtCut = float(sys.argv[13]) 
	if len(sys.argv)>14: jet2PtCut = float(sys.argv[14]) 
	if len(sys.argv)>15: AK4HTCut = float(sys.argv[15]) 
	cutList = {'lepPtCut':lepPtCut,'metCut':metCut,'mtCut':0,'drCut':drCut,'jet1PtCut':jet1PtCut,'jet2PtCut':jet2PtCut,'jet3PtCut':0,'AK4HTCut':AK4HTCut} 
	
cutString  = 'lep'+str(int(cutList['lepPtCut']))
cutString += '_MET'+str(int(cutList['metCut']))+'_DR'+str(cutList['drCut'])+'_HT'+str(cutList['AK4HTCut']) 
cutString += '_jet1Pt'+str(int(cutList['jet1PtCut']))+'_jet2Pt'+str(int(cutList['jet2PtCut']))

cTime=datetime.datetime.now()
datestr='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
timestr='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix='templates_TEST'
if not isCategorized: pfix='kinematics_TEST'+region
pfix+='_'+datestr#+'_'+timestr
		
if len(sys.argv)>5: isEMlist=[str(sys.argv[5])]
else: isEMlist = ['E','M']
if len(sys.argv)>6: nttaglist=[str(sys.argv[6])]
else: nttaglist = ['0p']
if len(sys.argv)>7: nWtaglist=[str(sys.argv[7])]
else: nWtaglist = ['0p']
if len(sys.argv)>8: nbtaglist=[str(sys.argv[8])]
else: 
	if not isCategorized: nbtaglist = ['1p']
	#if not isCategorized and BDTSR_Merged : nbtaglist = ['2p']
	else: nbtaglist = ['1','2p']

if len(sys.argv)>9: njetslist=[str(sys.argv[9])]
else:
	if not isCategorized: njetslist = ['4p']
	if not isCategorized and region=='PS': njetslist = ['3p']

	#if not isCategorized and BDTSR_Merged : njetslist = ['5p']
	else: njetslist = ['4p']


catList = list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist))

def readTree(file):
	#if not os.path.exists(file): 
	#	print "Error: File does not exist! Aborting ...",file
	#	os._exit(1)
	tFile = TFile.Open(file,'READ')
	tTree = tFile.Get('ljmet')
	return tFile, tTree 

bigbins = [0,50,100,150,200,250,300,350,400,450,500,600,700,800,1000,1200,1500]

plotList = {#discriminantName:(discriminantLJMETName, binning, xAxisLabel)
	'NPV':('nPV_MultiLepCalc',linspace(0, 40, 41).tolist(),';PV multiplicity'),
	'MTlmet':('MT_lepMet',linspace(0,250,51).tolist(),';M_{T}(l,#slash{E}_{T}) [GeV]'),
	'topPt':('topPt',linspace(0,1500,51).tolist(),';p_{T}^{rec}(t) [GeV]'),
	'Bjet1Pt':('BJetLeadPt',linspace(0,1500,51).tolist(),';p_{T}(b_{1}) [GeV]'),
	'lepPt':('leptonPt_MultiLepCalc',linspace(0, 1000, 51).tolist(),';Lepton p_{T} [GeV]'),
	'lepEta':('leptonEta_MultiLepCalc',linspace(-4, 4, 41).tolist(),';Lepton #eta'),
	'lepEnergy':('leptonEnergy_MultiLepCalc',linspace(0, 1000, 51).tolist(),';Lepton Energy [GeV]'),
	'JetEta':('theJetEta_JetSubCalc_PtOrdered',linspace(-4, 4, 41).tolist(),';AK4 Jet #eta'),
	'JetPt' :('theJetPt_JetSubCalc_PtOrdered',linspace(0, 1500, 51).tolist(),';jet p_{T} [GeV]'),
	'Jet1Pt':('theJetPt_JetSubCalc_PtOrdered[0]',linspace(0, 1500, 51).tolist(),';p_{T}(j_{1}), AK4 [GeV]'),
	'Jet2Pt':('theJetPt_JetSubCalc_PtOrdered[1]',linspace(0, 1500, 51).tolist(),';p_{T}(j_{2}), AK4 [GeV]'),
	'Jet3Pt':('theJetPt_JetSubCalc_PtOrdered[2]',linspace(0, 800, 51).tolist(),';p_{T}(j_{3}), AK4 [GeV]'),
	'Jet4Pt':('theJetPt_JetSubCalc_PtOrdered[3]',linspace(0, 800, 51).tolist(),';p_{T}(j_{4}), AK4 [GeV]'),
	'Jet5Pt':('theJetPt_JetSubCalc_PtOrdered[4]',linspace(0, 800, 51).tolist(),';p_{T}(j_{5}), AK4 [GeV]'),
	'Jet6Pt':('theJetPt_JetSubCalc_PtOrdered[5]',linspace(0, 800, 51).tolist(),';p_{T}(j_{6}), AK4 [GeV]'),	

	'deltaPhi_METjets':('deltaPhi_METjets',linspace(0,3.2,51).tolist(),';#Delta#phi(MET,j)'),
	'min_deltaPhi_METjets':('min_deltaPhi_METjets',linspace(0,0.05,51).tolist(),';min#Delta#phi(MET,j)'),
	'deltaPhilepJets':('deltaPhi_lepJets',linspace(0,3.2,51).tolist(),';#Delta#phi(l,j)'),
	
	'deltaPhilepJets0':('deltaPhi_lepJets0',linspace(0,3.2,51).tolist(),';#Delta#phi(l,j_{1})'),
	'deltaPhilepJets1':('deltaPhi_lepJets1',linspace(0,3.2,51).tolist(),';#Delta#phi(l,j_{2})'),
	'deltaPhilepJets2':('deltaPhi_lepJets2',linspace(0,3.2,51).tolist(),';#Delta#phi(l,j_{3})'),
	
	'DR':('deltaR_lepJets[1]',linspace(0,6,51).tolist(),';#DeltaR(l,j_{2})'),
	'deltaRlepJets':('deltaR_lepJets',linspace(0,6,51).tolist(),';#DeltaR(l,j)'),
	'deltaRlepJets0':('deltaR_lepJets0',linspace(0,6,51).tolist(),';#DeltaR(l,j_{1})'),
	'deltaRlepJets1':('deltaR_lepJets1',linspace(0,6,51).tolist(),';#DeltaR(l,j_{2})'),
	'deltaRlepJets2':('deltaR_lepJets2',linspace(0,6,51).tolist(),';#DeltaR(l,j_{3})'),
	'deltaR_lepBJets0':('deltaR_lepBJets0',linspace(0,6,51).tolist(),';#DeltaR(l,b_{1})'),
	'mindeltaRlb':('minDR_lepBJet',linspace(0,6,51).tolist(),';min[#DeltaR(l,b)]'),
        'deltaR':('minDR_lepBJet',linspace(0,6,51).tolist(),';min[#DeltaR(l,b)]'),
        
        'deltaPhi_lepJetInMinMljet':('deltaPhi_lepJetInMinMljet', linspace(-4, 4, 51).tolist(),';#DeltaPhi(l,j) with min M(l, j)'),
        'deltaPhi_lepbJetInMinMlb':('deltaPhi_lepbJetInMinMlb', linspace(-11, 5, 101).tolist(),';#DeltaPhi(l,b) with min M(l, b)'),
        'deltaR_lepbJetInMinMlb':('deltaR_lepbJetInMinMlb',linspace(0, 6.0, 51).tolist(),';#DeltaR(l,b) with min M(l, b)'),
        'deltaR_lepJetInMinMljet':('deltaR_lepJetInMinMljet', linspace(0, 4.5, 101).tolist(),';#DeltaR(l,j) with min M(l, j)'),
        'deltaR_minBB':('deltaR_minBB', linspace(0,6,51).tolist(),';min[#DeltaR(b,b)]'),
        'M_allJet_W':('M_allJet_W', linspace(0, 10000, 201).tolist(),';M(allJets, leptoninc W) [GeV]'),
        'HT_bjets':('HT_bjets',linspace(0, 1800, 101).tolist(),';HT(bjets) [GeV]'),
        'ratio_HTdHT3leadjets':('ratio_HTdHT3leadjets',linspace(0, 2.6, 51).tolist(),';HT/HT(3 leading jets)'),
       
        'csvJet1':('csvJet1', linspace(-2.2, 1.2, 101).tolist(),';DeepJet(1stPtJet)'),
        'csvJet2':('csvJet2', linspace(-2.2, 1.2, 101).tolist(),';DeepJet(2ndPtJet)'),
        'csvJet3':('csvJet3', linspace(-2.2, 1.2, 101).tolist(),';DeepJet(3rdPtJet)'),
        'csvJet4':('csvJet4', linspace(-2.2, 1.2, 101).tolist(),';DeepJet(4thPtJet)'),
        
        #Changed below here
        'firstcsvb_bb':('firstcsvb_bb',linspace(-2, 1.5, 51).tolist(),';DeepJet(1stDeepJet Jet)'),
        'secondcsvb_bb':('secondcsvb_bb',linspace(-2, 1.5, 51).tolist(),';DeepJet(2ndDeepJet Jet)'),
        'thirdcsvb_bb':('thirdcsvb_bb',linspace(-2, 1.5, 51).tolist(),';DeepJet(3rdDeepJet Jet)'),
        'fourthcsvb_bb':('fourthcsvb_bb',linspace(-2, 1.5, 51).tolist(),';DeepJet(4thDeepJet Jet)'),
        'HT_2m':('HT_2m', linspace(-20, 5000, 201).tolist(),';HTwoTwoPtBjets [GeV]'),
        'Sphericity':('Sphericity',linspace(0, 1.0, 51).tolist(), ';Sphericity'),
        'Aplanarity':('Aplanarity',linspace(0, 0.5, 51).tolist(), ';Aplanarity'),

        #'MT_lepMet':('MT_lepMet',linspace(0, 1500, 51).tolist(),';#slash{E}_{T,l} [GeV]')),

	'masslepJets':('mass_lepJets',linspace(0,1000,51).tolist(),';M(l,j) [GeV]'),
	'masslepJets0':('mass_lepJets0',linspace(0,1000,51).tolist(),';M(l,j_{1}) [GeV]'),
	'masslepJets1':('mass_lepJets1',linspace(0,1000,51).tolist(),';M(l,j_{2}) [GeV]'),
	'masslepJets2':('mass_lepJets2',linspace(0,1000,51).tolist(),';M(l,j_{3}) [GeV]'),
	'masslepBJets0':('mass_lepBJet0',linspace(0,1000,51).tolist(),';M(l,b_{1}) [GeV]'),
        'mindeltaR':('minDR_lepJet',linspace(0, 6, 51).tolist(),';min[#DeltaR(l,j)]'),
        'MET':('corr_met_MultiLepCalc',linspace(0, 1500, 51).tolist(),';#slash{E}_{T} [GeV]'),
        'NJets':('NJets_JetSubCalc',linspace(0, 15, 16).tolist(),';jet multiplicity'),
	'NBJetsNoSF':('NJetsCSV_MultiLepCalc',linspace(0, 10, 11).tolist(),';b tag multiplicity'),
        'NBJets':('NJetsCSV_JetSubCalc',linspace(0, 10, 11).tolist(),';b tag multiplicity'),
	'PtRel':('ptRel_lepJet',linspace(0,500,51).tolist(),';p_{T,rel}(l, closest jet) [GeV]'),
        'theLeadJetPt':('theJetLeadPt',linspace(0, 1500, 51).tolist(),';p_{T}(j_{1}) [GeV]'),
	'aveBBdr':('aveBBdr',linspace(0, 6, 51).tolist(),';#bar{#DeltaR(b,b)}'),
	'minBBdr':('minBBdr',linspace(0, 6, 51).tolist(),';min[#DeltaR(b,b)]'),
	'mass_maxJJJpt':('mass_maxJJJpt',linspace(0, 3000, 51).tolist(),';M(jjj) with max[p_{T}(jjj)] [GeV]'),
	'mass_maxBBmass':('mass_maxBBmass',linspace(0, 1500, 51).tolist(),';max[M(b,b)] [GeV]'),
	'mass_maxBBpt':('mass_maxBBpt',linspace(0, 1500, 51).tolist(),';M(b,b) with max[p_{T}(bb)] [GeV]'),
	'lepDR_minBBdr':('lepDR_minBBdr',linspace(0, 6, 51).tolist(),';#DeltaR(l,bb) with min[#DeltaR(b,b)]'),
	'mass_minBBdr':('mass_minBBdr',linspace(0, 1000, 51).tolist(),';M(b,b) with min[#DeltaR(b,b)] [GeV]'),
	'mass_minLLdr':('mass_minLLdr',linspace(0, 1000, 51).tolist(),';M(j,j) with min[#DeltaR(j,j)], j #neq b [GeV]'),
 	'mass_lepBB_minBBdr':('mass_lepBB_minBBdr',linspace(0, 1000, 51).tolist(),';M(l,bb) with min[#DeltaR(b,b)] [GeV]'),
	'mass_lepJJ_minJJdr':('mass_lepJJ_minJJdr',linspace(0, 1000, 51).tolist(),';M(l,jj) with min[#DeltaR(j,j)], j #neq b [GeV]'),
	'mass_lepBJet_mindr':('mass_lepBJet_mindr',linspace(0, 1000, 51).tolist(),';M(l,b) with min[#DeltaR(l,b)], [GeV]'),
   	'HTb':('AK4HT',bigbins,';H_{T} [GeV]'),
	'ST':('AK4HTpMETpLepPt',linspace(0, 3000, 51).tolist(),';S_{T} [GeV]'),
        'minMlb':('minMleppBjet',linspace(0, 1000, 51).tolist(),';min[M(l,b)] [GeV]'),
	'BDT':('BDT'+sigTrained,linspace(-1, 1, 126).tolist(),';BDT'),

	'MT2bb':('MT2bb',linspace(0, 700, 71).tolist(),';MT2bb'),
	'MT2bbl':('MT2bbl',linspace(0, 700, 71).tolist(),';MT2bbl'),
	'centrality':('centrality',linspace(0, 1, 51).tolist(),';Centrality'),
	'hemiout':('hemiout',linspace(0, 1700, 51).tolist(),';Hemiout'),
    	'deltaEta_maxBB':('deltaEta_maxBB',linspace(0, 5, 51).tolist(),';max[#Delta#eta(b,b)]'),
    	'deltaR_lepBJet_maxpt':('deltaR_lepBJet_maxpt',linspace(0, 6, 51).tolist(),';#DeltaR(l,b) with max[pT(l,b)]'),
    
	'aveCSVpt':('aveCSVpt',linspace(0, 1, 51).tolist(),';aveCSVpt'),
	'PtFifthJet':('PtFifthJet',linspace(0, 200, 51).tolist(),';p_{T}(j_{5}) [GeV]'),
	'FW_momentum_2':('FW_momentum_2',linspace(0, 1, 51).tolist(),';FW_momentum_{2}'),

	'STpBDT':('AK4HTpMETpLepPt',linspace(0, 3000, 51).tolist(),';S_{T} [GeV]','BDT'+sigTrained,linspace(-1, 1, 201).tolist(),';BDT'),
	'HT':('AK4HT',linspace(0, 5000, 101).tolist(),';H_{T} [GeV]'),
        'BestTop_Disc':('BestTop_Discriminator', linspace(0, 1, 20).tolist(),';Best Top Score'),
        'BestTop_Pt': ('BestTop_Pt', linspace(0, 800, 80).tolist(),';Best Top p_{T} [GeV]'),
        'NoTop_Jet1_CSV': ('NoTop_Jet1_CSV', linspace(-1.0, 1, 30).tolist(),'; No-Top 1stDeepJet Jet, DeepJet'),
        'NoTop_Jet1_Pt': ('NoTop_Jet1_Pt', linspace(40, 1000, 100).tolist(),'; No-Top 1stDeepJet Jet, p_{T} [GeV]'),
        
        'NoTop_Jet2_CSV': ('NoTop_Jet2_CSV', linspace(-1.0, 1, 30).tolist(),'; No-Top 2ndDeepJet Jet, DeepJet'),
        'NoTop_Jet2_Pt': ('NoTop_Jet2_Pt', linspace(40, 1000, 100).tolist(),'; No-Top 2ndDeepJet Jet, p_{T} [GeV]'),
   
        'recLeptonicTopJetCSV': ('recLeptonicTopJetCSV', linspace(-1.0, 1, 30).tolist(),';t_{lep} Jet DeepJet'),
        'recLeptonicTopJetPt': ('recLeptonicTopJetPt', linspace(40, 1000, 100).tolist(),';t_{lep} Jet p_{T}[GeV]'),
        
        'LeptonicTB1_M': ('LeptonicTB1_M', linspace(40, 2000, 100).tolist(),';M(t_{lep}, b_{1}^{non-top})[GeV]'),
        'LeptonicTB2_M': ('LeptonicTB2_M', linspace(40, 2000, 100).tolist(),';M(t_{lep}, b_{2}^{non-top})[GeV]'),

        'HadronicTB1_M': ('HadronicTB1_M', linspace(40, 2000, 100).tolist(),';M(t_{had}, b_{1}^{non-top})[GeV]'),
        'HadronicTB2_M': ('HadronicTB2_M', linspace(40, 2000, 100).tolist(),';M(t_{had}, b_{2}^{non-top})[GeV]'),

##        'XGB700' : ( 'XGB200', linspace(0, 1, 40).tolist(), '; XGB (700 GeV)'),
##        'XGB800' : ( 'XGB220', linspace(0, 1, 40).tolist(), '; XGB (800 GeV)'),
##        'XGB900' : ( 'XGB250', linspace(0, 1, 40).tolist(), '; XGB (900 GeV)'),
##        'XGB1000' : ( 'XGB300', linspace(0, 1, 40).tolist(), '; XGB (1000 GeV)'),
##        'XGB1100' : ( 'XGB350', linspace(0, 1, 40).tolist(), '; XGB (1100 GeV)'),
##        'XGB1200' : ( 'XGB400', linspace(0, 1, 40).tolist(), '; XGB (1200 GeV)'),
##        'XGB1300' : ( 'XGB500', linspace(0, 1, 40).tolist(), '; XGB (1300 GeV)'),
##        'XGB1400' : ( 'XGB600', linspace(0, 1, 40).tolist(), '; XGB (1400 GeV)'),
##        'XGB1500' : ( 'XGB700', linspace(0, 1, 40).tolist(), '; XGB (1500 GeV)'),
##        'XGB1600' : ( 'XGB800', linspace(0, 1, 40).tolist(), '; XGB (1600 GeV)'),
##
# X53H       
#        'XGB200_SR1' : ( 'XGB200_SR1', linspace(0, 1, 40).tolist(), '; XGB SR1 (1200 GeV MH+ 200GeV)'),
#        'XGB400_SR1' : ( 'XGB400_SR1', linspace(0, 1, 40).tolist(), '; XGB SR1 (1200 GeV MH+ 400GeV)'),
#        'XGB600_SR1' : ( 'XGB600_SR1', linspace(0, 1, 40).tolist(), '; XGB SR1 (1200 GeV MH+ 600GeV)'),
#        'XGB800_SR1' : ( 'XGB800_SR1', linspace(0, 1, 40).tolist(), '; XGB SR1 (1200 GeV MH+ 800GeV)'),
#        'XGB1000_SR1' : ( 'XGB1000_SR1', linspace(0, 1, 40).tolist(), '; XGB SR1 (1200 GeV MH+ 1000GeV)'),

#        'XGB700_SR1' : ( 'XGB700_SR1', linspace(0, 1, 40).tolist(), '; XGB (700 GeV)'),
#        'XGB800_SR1' : ( 'XGB800_SR1', linspace(0, 1, 40).tolist(), '; XGB SR1 (800 GeV)'),
#        'XGB900_SR1' : ( 'XGB900_SR1', linspace(0, 1, 40).tolist(), '; XGB SR1 (900 GeV)'),
        #'XGB1000_SR1' : ( 'XGB1000_SR1', linspace(0, 1, 40).tolist(), '; XGB SR1 (1000 GeV)'),
#        'XGB1100_SR1' : ( 'XGB1100_SR1', linspace(0, 1, 40).tolist(), '; XGB SR1 (1100 GeV)'),
#        'XGB1200_SR1' : ( 'XGB1200_SR1', linspace(0, 1, 40).tolist(), '; XGB SR1 (1200 GeV)'),
        'XGB200_SR1' : ( 'XGB200_SR1', linspace(0, 1, 40).tolist(), '; XGB (MX 1200 GeV MH+ 200 GeV)'),
        'XGB400_SR1' : ( 'XGB400_SR1', linspace(0, 1, 40).tolist(), '; XGB (MX 1200 GeV MH+ 400 GeV)'),
        'XGB600_SR1' : ( 'XGB600_SR1', linspace(0, 1, 40).tolist(), '; XGB (MX 1200 GeV MH+ 600 GeV)'),
        'XGB800_SR1' : ( 'XGB800_SR1', linspace(0, 1, 40).tolist(), '; XGB (MX 1200 GeV MH+ 800 GeV)'),
        'XGB1000_SR1' : ( 'XGB1000_SR1', linspace(0, 1, 40).tolist(), '; XGB (MX 1200 GeV MH+ 1000 GeV)'),

        'XGB1300_SR1' : ( 'XGB1300_SR1', linspace(0, 1, 40).tolist(), '; XGB (1300 GeV)'),
#        'XGB1400_SR1' : ( 'XGB1400_SR1', linspace(0, 1, 40).tolist(), '; XGB SR1 (1400 GeV)'),
#        'XGB1500_SR1' : ( 'XGB1500_SR1', linspace(0, 1, 40).tolist(), '; XGB SR1 (1500 GeV)'),
#        'XGB1600_SR1' : ( 'XGB1600_SR1', linspace(0, 1, 40).tolist(), '; XGB SR1 (1600 GeV)'),
#
#        'XGB700_SR2' : ( 'XGB700_SR2', linspace(0, 1, 40).tolist(), '; XGB SR2 (700 GeV)'),
#        'XGB800_SR2' : ( 'XGB800_SR2', linspace(0, 1, 40).tolist(), '; XGB SR2 (800 GeV)'),
#        'XGB900_SR2' : ( 'XGB900_SR2', linspace(0, 1, 40).tolist(), '; XGB SR2 (900 GeV)'),
#        'XGB1000_SR2' : ( 'XGB1000_SR2', linspace(0, 1, 40).tolist(), '; XGB SR2 (1000 GeV)'),
#        'XGB1100_SR2' : ( 'XGB1100_SR2', linspace(0, 1, 40).tolist(), '; XGB SR2 (1100 GeV)'),
#        'XGB1200_SR2' : ( 'XGB1200_SR2', linspace(0, 1, 40).tolist(), '; XGB SR2 (1200 GeV)'),
#        'XGB1300_SR2' : ( 'XGB1300_SR2', linspace(0, 1, 40).tolist(), '; XGB SR2 (1300 GeV)'),
#        'XGB1400_SR2' : ( 'XGB1400_SR2', linspace(0, 1, 40).tolist(), '; XGB SR2 (1400 GeV)'),
#        'XGB1500_SR2' : ( 'XGB1500_SR2', linspace(0, 1, 40).tolist(), '; XGB SR2 (1500 GeV)'),
#        'XGB1600_SR2' : ( 'XGB1600_SR2', linspace(0, 1, 40).tolist(), '; XGB SR2 (1600 GeV)'),
#
#        'XGB700_SR3' : ( 'XGB700_SR3', linspace(0, 1, 40).tolist(), '; XGB SR3 (700 GeV)'),
#        'XGB800_SR3' : ( 'XGB800_SR3', linspace(0, 1, 40).tolist(), '; XGB SR3 (800 GeV)'),
#        'XGB900_SR3' : ( 'XGB900_SR3', linspace(0, 1, 40).tolist(), '; XGB SR3 (900 GeV)'),
#        'XGB1000_SR3' : ( 'XGB1000_SR3', linspace(0, 1, 40).tolist(), '; XGB SR3 (1000 GeV)'),
#        'XGB1100_SR3' : ( 'XGB1100_SR3', linspace(0, 1, 40).tolist(), '; XGB SR3 (1100 GeV)'),
#        'XGB1200_SR3' : ( 'XGB1200_SR3', linspace(0, 1, 40).tolist(), '; XGB SR3 (1200 GeV)'),
#        'XGB1300_SR3' : ( 'XGB1300_SR3', linspace(0, 1, 40).tolist(), '; XGB SR3 (1300 GeV)'),
#        'XGB1400_SR3' : ( 'XGB1400_SR3', linspace(0, 1, 40).tolist(), '; XGB SR3 (1400 GeV)'),
#        'XGB1500_SR3' : ( 'XGB1500_SR3', linspace(0, 1, 40).tolist(), '; XGB SR3 (1500 GeV)'),
#        'XGB1600_SR3' : ( 'XGB1600_SR3', linspace(0, 1, 40).tolist(), '; XGB SR3 (1600 GeV)'),

#        'HTpt40':('HT_pt40', linspace(0, 5000, 101).tolist(),';H_{T} (pt>40) [GeV]'),
#	'HTpBDT':('AK4HT',linspace(0, 5000, 126).tolist(),';H_{T} [GeV]','BDT'+sigTrained,linspace(-1, 1, 126).tolist(),';BDT'),
#	'HTpDNN':('AK4HT',linspace(0, 5000, 126).tolist(),';H_{T} [GeV]','DNN'+sigTrained,linspace(-1, 1, 126).tolist(),';DNN'),
#	'minMlbpBDT':('minMleppBjet',linspace(0, 1000, 51).tolist(),';min[M(l,b)] [GeV]','BDT'+sigTrained,linspace(-1, 1, 201).tolist(),';BDT'),

	'NJets_vs_NBJets':('NJets_MultiLepCalc:NJetsCSV_MultiLepCalc',linspace(0, 15, 16).tolist(),';jet multiplicity',linspace(0, 10, 11).tolist(),';b tag multiplicity'),

	'deltaRAK8':('minDR_leadAK8otherAK8',linspace(0,5,51).tolist(),';min #DeltaR(1^{st} AK8 jet, other AK8 jet)'),
	'MTlmet':('MT_lepMet',linspace(0,250,51).tolist(),';M_{T}(l,#slash{E}_{T}) [GeV]'),
	'nTrueInt':('nTrueInteractions_MultiLepCalc',linspace(0, 75, 76).tolist(),';# true interactions'),
	'NWJets':('NJetsWtagged',linspace(0, 6, 7).tolist(),';W-tagged jet multiplicity'),
	'NTJets':('NJetsTtagged',linspace(0, 4, 5).tolist(),';t-tagged jet multiplicity'),
	'NJetsAK8':('NJetsAK8_JetSubCalc',linspace(0, 8, 9).tolist(),';AK8 jet multiplicity'),
	'JetPtAK8':('theJetAK8Pt_JetSubCalc_PtOrdered',linspace(0, 1500, 51).tolist(),';AK8 jet p_{T} [GeV]'),
	'JetEtaAK8':('theJetAK8Eta_JetSubCalc_PtOrdered',linspace(-4, 4, 41).tolist(),';AK8 jet #eta'),
	'mindeltaR':('minDR_lepJet',linspace(0, 5, 51).tolist(),';#DeltaR(l, closest jet)'),
	'deltaRjet1':('deltaR_lepJets[0]',linspace(0, 5, 51).tolist(),';#DeltaR(l,j_{1})'),
	'deltaRjet2':('deltaR_lepJets[1]',linspace(0, 5, 51).tolist(),';#DeltaR(l,j_{2})'),
	'deltaRjet3':('deltaR_lepJets[2]',linspace(0, 5, 51).tolist(),';#DeltaR(l,j_{3})'),
	'METphi':('corr_met_phi_MultiLepCalc',linspace(-3.2,3.2,65).tolist(),';#phi(#slash{E}_{T})'),
	'lepPhi':('leptonPhi_MultiLepCalc',linspace(-3.2,3.2,65).tolist(),';#phi(l)'),
	'WvsQCD':('theJetParticleNeWvsQCD_JetSubCalc_PtOrdered',linspace(0,1,51).tolist(),';AK8 Jet #ParticleNetWvsQCD'),
	'TvsQCD':('theJetParticleNetTvsQCD_JetSubCalc_PtOrdered',linspace(0,1,51).tolist(),';AK8 Jet #ParticleNet:TvsQCD'),
	'JetPhi':('theJetPhi_JetSubCalc_PtOrdered',linspace(-3.2,3.2,65).tolist(),';AK4 Jet #phi'),
	'JetPhiAK8':('theJetAK8Phi_JetSubCalc_PtOrdered',linspace(-3.2,3.2,65).tolist(),';AK8 Jet #phi'),
	'Wjet1Pt':('WJetLeadPt',linspace(0,1500,51).tolist(),';p_{T}(W_{1}) [GeV]'),
	'Tjet1Pt':('TJetLeadPt',linspace(0,1500,51).tolist(),';p_{T}(t_{1}) [GeV]'),
	'minMlj':('minMleppJet',linspace(0,1000,51).tolist(),';min[M(l,j)] [GeV], j #neq b'),
	'PtRel':('ptRel_lepJet',linspace(0,500,51).tolist(),';p_{T,rel}(l, closest jet) [GeV]'),
	'pileupWeight':('pileupWeight',linspace(0,2,2001).tolist(),'Pileup Weight'),

	}

print "PLOTTING:",iPlot
print "         LJMET Variable:",plotList[iPlot][0]
print "         X-AXIS TITLE  :",plotList[iPlot][2]
print "         BINNING USED  :",plotList[iPlot][1]

runData =True
runBkgs =True
runSigs =True
nCats  = len(catList)


catInd = 1

print "READING TREES"
shapesFiles = ['jec','jer']
tTreeData = {}
tFileData = {}

for cat in catList:
	if not runData: break
        catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]
        datahists = {}
        if len(sys.argv)>1: outDir=sys.argv[1]
        else:
                outDir = os.getcwd()
                outDir+='/'+pfix
                if not os.path.exists(outDir): os.system('mkdir '+outDir)
                outDir+='/'+cutString
                if not os.path.exists(outDir): os.system('mkdir '+outDir)
                outDir+='/'+catDir
                if not os.path.exists(outDir): os.system('mkdir '+outDir)
        category = {'isEM':cat[0],'nttag':cat[1],'nWtag':cat[2],'nbtag':cat[3],'njets':cat[4]}

	for data in dataList:
		print "READING:", data
		tFileData[data],tTreeData[data]=readTree(ntupleDir+'/'+samples[data]+'_hadd.root')
		datahists.update(analyze(tTreeData,data,data,cutList,False,doPDF,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
                if catInd==nCats:
                        del tFileData[data]
                        del tTreeData[data]
        pickle.dump(datahists,open(outDir+'/datahists_'+iPlot+'.p','wb'))
        catInd+=1


tTreeSig = {}
tFileSig = {}
catInd=1


for cat in catList:
	if not runSigs: break
	catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]
	sighists  = {}
	if len(sys.argv)>1: outDir=sys.argv[1]
	else:
		outDir = os.getcwd()
		outDir+='/'+pfix
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		outDir+='/'+cutString
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		outDir+='/'+catDir
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
	category = {'isEM':cat[0],'nttag':cat[1],'nWtag':cat[2],'nbtag':cat[3],'njets':cat[4]}
	
	for sig in sigList:
	        #if isCategorized and ("XGB" in iPlot):
	        #            sigmass = sig.lstrip("Hptb")
	        #            XGBmass = iPlot.split("_")[0].lstrip("XGB")
	        #            if (int(sigmass)!=int(XGBmass)): continue
	
		for decay in decays:
			print "READING:", sig+decay
			print "        nominal"
			tFileSig[sig+decay],tTreeSig[sig+decay]=readTree(ntupleDir+'/'+samples[sig+decay]+'_hadd.root')
			if doAllSys:
				for syst in shapesFiles:
					for ud in ['Up','Down']:
						print "        "+syst+ud
						tFileSig[sig+decay+syst+ud],tTreeSig[sig+decay+syst+ud]=readTree(ntupleDir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[sig+decay]+'_hadd.root')
			sighists.update(analyze(tTreeSig,sig+decay,sig+decay,cutList,doAllSys,doPDF,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
	                if catInd==nCats:
	                        del tFileSig[sig+decay]
	                        del tTreeSig[sig+decay]
	                if doAllSys and catInd==nCats:
	                        for syst in shapesFiles:
	                                for ud in ['Up','Down']:
	                                        del tFileSig[sig+decay+syst+ud]
	                                        del tTreeSig[sig+decay+syst+ud]
	pickle.dump(sighists,open(outDir+'/sighists_'+iPlot+'.p','wb'))
	catInd+=1


tTreeBkg = {}
tFileBkg = {}
catInd=1


for cat in catList:
        if not runBkgs: break
        catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]
        bkghists  = {}
        if len(sys.argv)>1: outDir=sys.argv[1]
        else:
                outDir = os.getcwd()
                outDir+='/'+pfix
                if not os.path.exists(outDir): os.system('mkdir '+outDir)
                outDir+='/'+cutString
                if not os.path.exists(outDir): os.system('mkdir '+outDir)
                outDir+='/'+catDir
                if not os.path.exists(outDir): os.system('mkdir '+outDir)
        category = {'isEM':cat[0],'nttag':cat[1],'nWtag':cat[2],'nbtag':cat[3],'njets':cat[4]}

	for bkg in bkgList:
		print "READING:",bkg
		print "        nominal"
	        if (('TTToHadronic' in bkg) or ('TTTo2L2Nu' in bkg)) and len(ttFlvs)!=0:
	            for flv in ttFlvs:
	                tFileBkg[bkg+flv],tTreeBkg[bkg+flv] = readTree(ntupleDir+'/'+samples[bkg]+flv+'_hadd.root')
	        elif ('TTToSemiLeptonic' in bkg) and len(ttFlvs)!=0:
                    for flv in ttFlvs:
                        if flv=="_ttjj": 
                            for i in range(1, 12):
                                tFileBkg[bkg+"_HT0Njet0_"+str(i)+flv], tTreeBkg[bkg+"_HT0Njet0_"+str(i)+flv] = readTree(ntupleDir+'/'+samples[bkg]+"_HT0Njet0"+flv+"_"+str(i)+"_hadd.root")
                            tFileBkg[bkg+"_HT500Njet9"+flv], tTreeBkg[bkg+"_HT500Njet9"+flv] = readTree(ntupleDir+'/'+samples[bkg]+"_HT500Njet9"+flv+"_hadd.root")
                        else:
                            tFileBkg[bkg+"_HT0Njet0"+flv], tTreeBkg[bkg+"_HT0Njet0"+flv] = readTree(ntupleDir+'/'+samples[bkg]+"_HT0Njet0"+flv+"_hadd.root")
                            tFileBkg[bkg+"_HT500Njet9"+flv], tTreeBkg[bkg+"_HT500Njet9"+flv] = readTree(ntupleDir+'/'+samples[bkg]+"_HT500Njet9"+flv+"_hadd.root")
                
                else:
		    tFileBkg[bkg],tTreeBkg[bkg]=readTree(ntupleDir+'/'+samples[bkg]+'_hadd.root')


		if doAllSys:
			if (('TTToHadronic' in bkg) or ('TTTo2L2Nu' in bkg)) and len(ttFlvs)!=0:
                        	for flv in ttFlvs:
                                        for syst in shapesFiles:
                                                for ud in ['Up','Down']:
                                                        print "        "+bkg+flv+syst+ud
                                                        tFileBkg[bkg+flv+syst+ud],tTreeBkg[bkg+flv+syst+ud]=readTree(ntupleDir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[bkg]+flv+'_hadd.root')
			elif ('TTToSemiLeptonic' in bkg) and len(ttFlvs)!=0:
				for flv in ttFlvs:
					for syst in shapesFiles:
                                                for ud in ['Up','Down']:
							print "        "+bkg+flv+syst+ud
							if flv=="_ttjj": 
                            					for i in range(1, 12):
									tFileBkg[bkg+"_HT0Njet0_"+str(i)+flv+syst+ud],tTreeBkg[bkg+"_HT0Njet0_"+str(i)+flv+syst+ud] = readTree(ntupleDir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[bkg]+"_HT0Njet0"+flv+"_"+str(i)+'_hadd.root') 
								tFileBkg[bkg+"_HT500Njet9"+flv+syst+ud], tTreeBkg[bkg+"_HT500Njet9"+flv+syst+ud] = readTree(ntupleDir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[bkg]+"_HT500Njet9"+flv+"_hadd.root")
							else:
								tFileBkg[bkg+"_HT0Njet0"+flv+syst+ud], tTreeBkg[bkg+"_HT0Njet0"+flv+syst+ud] = readTree(ntupleDir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[bkg]+"_HT0Njet0"+flv+"_hadd.root")
								tFileBkg[bkg+"_HT500Njet9"+flv+syst+ud], tTreeBkg[bkg+"_HT500Njet9"+flv+syst+ud] = readTree(ntupleDir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[bkg]+"_HT500Njet9"+flv+"_hadd.root")


 
			#if 'TTTo' in bkg and len(ttFlvs)!=0:
			#	for flv in ttFlvs:
			#		for syst in shapesFiles:
			#			for ud in ['Up','Down']:
			#				print "        "+bkg+flv+syst+ud
			#				tFileBkg[bkg+flv+syst+ud],tTreeBkg[bkg+flv+syst+ud]=readTree(ntupleDir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[bkg]+flv+'_hadd.root')
			else:
				for syst in shapesFiles:
					for ud in ['Up','Down']:
						print "        "+bkg+syst+ud
						tFileBkg[bkg+syst+ud],tTreeBkg[bkg+syst+ud]=readTree(ntupleDir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[bkg]+'_hadd.root')

                if (('TTToHadronic' in bkg) or ('TTTo2L2Nu' in bkg)) and len(ttFlvs)!=0:
                        for flv in ttFlvs:
                                bkghists.update(analyze(tTreeBkg,bkg+flv,bkg+flv,cutList,doAllSys,doPDF,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
                                if catInd==nCats: del tFileBkg[bkg+flv]
                                if doAllSys and catInd==nCats:
                                        for syst in shapesFiles:
                                                for ud in ['Up','Down']:
                                                        del tFileBkg[bkg+flv+syst+ud]
                                                        del tTreeBkg[bkg+flv+syst+ud]

                elif ('TTToSemiLeptonic' in bkg) and len(ttFlvs)!=0:
                        for flv in ttFlvs:
                                if flv=="_ttjj":
                                        for i in range(1, 12):
                                                bkghists.update(analyze(tTreeBkg,bkg+"_HT0Njet0_"+str(i)+flv,bkg+"_HT0Njet0_"+str(i)+flv,cutList,doAllSys,doPDF,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
                                                if catInd==nCats: del tFileBkg[bkg+"_HT0Njet0_"+str(i)+flv]
                                                if doAllSys and catInd==nCats:
                                                        for syst in shapesFiles:
                                                                for ud in ['Up','Down']:
                                                                        del tFileBkg[bkg+"_HT0Njet0_"+str(i)+flv+syst+ud]
                                                                        del tTreeBkg[bkg+"_HT0Njet0_"+str(i)+flv+syst+ud]        
 
                                        bkghists.update(analyze(tTreeBkg,bkg+"_HT500Njet9"+flv,bkg+"_HT500Njet9"+flv,cutList,doAllSys,doPDF,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
                                        if catInd==nCats: del tFileBkg[bkg+"_HT500Njet9"+flv]
                                        if doAllSys and catInd==nCats:
                                                for syst in shapesFiles:
                                                        for ud in ['Up','Down']:
                                                                del tFileBkg[bkg+"_HT500Njet9"+flv+syst+ud]
                                                                del tTreeBkg[bkg+"_HT500Njet9"+flv+syst+ud]
 
                                else:
                                        bkghists.update(analyze(tTreeBkg,bkg+"_HT0Njet0"+flv,bkg+"_HT0Njet0"+flv,cutList,doAllSys,doPDF,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
                                        if catInd==nCats: del tFileBkg[bkg+"_HT0Njet0"+flv]
                                        if doAllSys and catInd==nCats:
                                                for syst in shapesFiles:
                                                        for ud in ['Up','Down']:
                                                                del tFileBkg[bkg+"_HT0Njet0"+flv+syst+ud]
                                                                del tTreeBkg[bkg+"_HT0Njet0"+flv+syst+ud]


                                        bkghists.update(analyze(tTreeBkg,bkg+"_HT500Njet9"+flv,bkg+"_HT500Njet9"+flv,cutList,doAllSys,doPDF,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
                                        if catInd==nCats: del tFileBkg[bkg+"_HT500Njet9"+flv]
                                        if doAllSys and catInd==nCats:
                                                for syst in shapesFiles:
                                                        for ud in ['Up','Down']:
                                                                del tFileBkg[bkg+"_HT500Njet9"+flv+syst+ud]
                                                                del tTreeBkg[bkg+"_HT500Njet9"+flv+syst+ud]
   


                #if 'TTTo' in bkg and len(ttFlvs)!=0:
                #        for flv in ttFlvs:
                #                bkghists.update(analyze(tTreeBkg,bkg+flv,bkg+flv,cutList,doAllSys,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
                #                if catInd==nCats: del tFileBkg[bkg+flv]
                #                if doAllSys and catInd==nCats:
                #                        for syst in shapesFiles:
                #                                for ud in ['Up','Down']:
                #                                        del tFileBkg[bkg+flv+syst+ud]
                #                                        del tTreeBkg[bkg+flv+syst+ud]
                else:
                        bkghists.update(analyze(tTreeBkg,bkg,bkg,cutList,doAllSys,doPDF,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
                        if catInd==nCats: del tFileBkg[bkg]
                        if doAllSys and catInd==nCats:
                                for syst in shapesFiles:
                                        for ud in ['Up','Down']:
                                                del tFileBkg[bkg+syst+ud]
                                                del tTreeBkg[bkg+syst+ud]
        pickle.dump(bkghists,open(outDir+'/bkghists_'+iPlot+'.p','wb'))
        catInd+=1



print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))



