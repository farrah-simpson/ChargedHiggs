#!/usr/bin/python
import os,sys,time,math,datetime,pickle,itertools,fnmatch
import argparse
from ROOT import gROOT,TFile,TH1F
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from modSyst import *
from utils import *

parser = argparse.ArgumentParser(description="template building for the charged Higgs analysis")
parser.add_argument("-d", "--directory", help="the directory to be processed")
parser.add_argument("-c", "--Categorized", default=False, action="store_true", help="Categorize or not")
parser.add_argument("-y", "--year", default="17", help="The data taking year")
#parser.add_argument("-cut", "--cutString", default="", help="The cut string")

args = parser.parse_args()

year = args.year

if year == 'R17':from weights_UL17 import *
elif year == 'R18':from weights_UL18 import *
elif year == 'R16':from weights_UL16 import *
elif year == 'R16APV':from weights_UL16APV import *
 
gROOT.SetBatch(1)
start_time = time.time()

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb

sigTrainedList=[]#'1000']
massPt=''
if len(sys.argv)>1: massPt=str(sys.argv[1])
region = 'SR' #PS,SR,CR
whichSignal = 'X53' #Hptb,HTB, TTM, BBM, or X53

isCategorized=args.Categorized#False#False
doTempEachCategory = False
cutString=''#args.cutString#MET30_1jet40_2jet40'#'lep35_MET30_DR0_1jet40_2jet40'

pfix = args.directory#'templates_M500_2020_11_23_topPtRW_NC_allweights_DJ'#'kinematics_CR_M500_2020_11_23_topPtRW_NC_allweights_DJ' 
#if not isCategorized: pfix='/kinematics_'+region+'_M1000'
#if not isCategorized: pfix='v113/withSys/kinematics_'+region+'_M'

#pfix+=massPt+'_2020_11_23_topPtRW_NC_allweights'
outDir = os.getcwd()+'/'+pfix

scaleSignalXsecTo1pb =True#False # this has to be "True" if you are making templates for limit calculation!!!!!!!!#doAllSys = False3True
doAllSys = True
doQ2sys = False
doPDFsys = True#False
if not doAllSys: doQ2sys = False
addCRsys = False
#systematicList = ['muR','muF','isr','fsr','LF','LFstat1', 'LFstat2','HF','HFstat1','HFstat2','CFerr1','CFerr2','pileup','muRFcorrd','PNT','PNW','jec','jer','prefire']#,'jmst','jmrt','jmsW','jmrW','trigeff','pileup','muRFcorrd','muR','muF','toppt','jec','jer','ht','LF','LFstat1', 'LFstat2','HF','HFstat1','HFstat2','CFerr1','CFerr2'] include any of these??
#systematicList = ['trigeff','pileup','muRFcorrd','muR','muF','toppt','jec','jer','ht','LF','LFstat1', 'LFstat2','HF','HFstat1','HFstat2','CFerr1','CFerr2']
systematicList = ['jetpileup','isr','fsr','pileup','muRFcorrd','muR','muF','toppt','jec','jer','ht','LF','LFstat1', 'LFstat2','HF','HFstat1','HFstat2','CFerr1','CFerr2', 'DJjes','PNT','PNW'] 
systList_jsf = ['jsfJES','jsfJESAbsoluteMPFBias', 'jsfJESAbsoluteScale', 'jsfJESAbsoluteStat', 'jsfJESFlavorQCD', 'jsfJESFragmentation', 'jsfJESPileUpDataMC',
'jsfJESPileUpPtBB', 'jsfJESPileUpPtEC1', 'jsfJESPileUpPtEC2', 'jsfJESPileUpPtHF', 'jsfJESPileUpPtRef', 'jsfJESRelativeBal', 'jsfJESRelativeFSR',
'jsfJESRelativeJEREC1', 'jsfJESRelativeJEREC2', 'jsfJESRelativeJERHF', 'jsfJESRelativeJERHF', 'jsfJESRelativePtBB', 'jsfJESRelativePtEC1',
'jsfJESRelativePtEC2', 'jsfJESRelativePtHF', 'jsfJESRelativeStatEC', 'jsfJESRelativeStatFSR', 'jsfJESRelativeStatHF', 'jsfJESSinglePionECAL',
'jsfJESSinglePionHCAL', 'jsfJESTimePtEta']
if year != 'R18': systematicList += ['prefire']

#systematicList += systList_jsf
normalizeRENORM_PDF = False #normalize the renormalization/pdf uncertainties to nominal templates --> normalizes signal processes only !!!!
rebinBy = -1#4#performs a regular rebinning with "Rebin(rebinBy)", put -1 if rebinning is not wanted

saveKey = '_wNegBinsCorrec_'
splitTTbar = True
splitST = False
if splitTTbar:  
	bkgTTBarList = ['ttnobb','ttbb']
        #bkgGrupList = bkgTTBarList + ['top','ewk','qcd','WJets', 'ZJets', 'TTToHadronic', 'TTTo2L2Nu', 'TTToSemiLeptonic']
        bkgGrupList = bkgTTBarList + ['top','ewk','qcd']
	bkgProcList = ['tt2b','ttbb','tt1b','ttcc','ttjj','T','TTV','WJets','ZJets','qcd']#,'VV'
        #bkgProcList = ['TT2B','TTBB','TTB','TTCC','TTLF','T','WJets','ZJets','qcd']#,'VV'
	if splitST:
		bkgGrupList = ['tt2b','ttbb','ttb','ttcc','ttlf','T','TTV','ewk','qcd']
		bkgProcList = ['TT2B','TTBB','TTB','TTCC','TTLF','T','TTV','WJets','ZJets','qcd']#,'VV'	
                #bkgGrupList = ['tt2b','ttbb','ttb','ttcc','ttlf','T','OtherT','ewk','qcd']
                #bkgProcList = ['TT2B','TTBB','TTB','TTCC','TTLF','T','OtherT','WJets','ZJets','qcd']#,'VV'

else:
	bkgGrupList = ['ttbar','top','ewk','qcd', 'WJets']
	#bkgGrupList = ['ttbar','top','ewk','qcd']
	bkgProcList = ['TTJets','T','WJets','ZJets','VV','qcd']#,'TTV']
bkgProcs = {}
bkgProcs['WJets']  =  ['WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800', 'WJetsMG1200', 'WJetsMG2500']
#bkgProcs['WJets']  =  ['WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800', 'WJetsMG1200', 'WJetsMG2500']
#bkgProcs['WJets'] += ['WJetsMG1200_1','WJetsMG1200_2','WJetsMG1200_3','WJetsMG1200_4','WJetsMG1200_5']
#bkgProcs['WJets'] += ['WJetsMG2500_1','WJetsMG2500_2','WJetsMG2500_3','WJetsMG2500_4','WJetsMG2500_5']#,'WJetsMG2500_6']

bkgProcs['ZJets'] = ['DYMG200','DYMG400','DYMG600','DYMG800','DYMG1200','DYMG2500']

bkgProcs['VV']    = ['WW','WZ','ZZ']
bkgProcs['T']     = ['Tt','Tbt','Ts','TtW','TbtW',]
#bkgProcs['TTV']   = ['TTWl','TTWq','TTZl']
bkgProcs['TTV']   = ['TTWl','TTWq','TTZlM10', 'TTZlM1to10']
bkgProcs['OtherT']= ['TTHB', 'TTHnoB']#['TTHH', 'TTWH', 'TTWW', 'TTWZ', 'TTZH', 'TTZZ', 'TTHB', 'TTHnoB']#['TTHB','TTHnoB', 'TTTT']

#bkgProcs['TTTo2L2Nu'] = ['TTTo2L2Nu_'+flavor for flavor in ['tt1b', 'tt2b', 'ttbb', 'ttcc', 'ttjj']]
#bkgProcs['TTToHadronic'] = ['TTToHadronic_'+flavor for flavor in ['tt1b', 'tt2b', 'ttbb', 'ttcc', 'ttjj']]
#bkgProcs['TTToSemiLeptonic'] = ['TTJetsSemiLeptonic_'+flavor for flavor in ['tt1b', 'tt2b', 'ttbb', 'ttcc', 'ttjj']]
bkgProcs['TTJets'] = []
bkgProcs['TTJets'] += ['TTTo2L2Nu']
bkgProcs['TTJets'] += ['TTToHadronic']
bkgProcs['TTJets'] += ['TTToSemiLeptonic']
#bkgProcs['TTJets'] += ['TTJets2L2nu0','TTJets2L2nu700','TTJets2L2nu1000']
#bkgProcs['TTJets'] += ['TTJetsHad0','TTJetsHad700','TTJetsHad1000']
#bkgProcs['TTJets'] += ['TTJetsSemiLep0','TTJetsSemiLep700','TTJetsSemiLep1000']
#bkgProcs['TTJets'] += ['TTJetsHad0','TTJetsHad700','TTJetsHad1000'] 
#bkgProcs['TTJets'] += ['TTJetsSemiLepNjet9bin1','TTJetsSemiLepNjet9bin2','TTJetsSemiLepNjet9bin3'] 
#bkgProcs['TTJets'] += ['TTJetsSemiLepbin1','TTJetsSemiLepbin2','TTJetsSemiLepbin3']#,'TTJetsSemiLep4','TTJetsSemiLep5']#,'TTJetsSemiLep6']
#bkgProcs['TTJets'] += ['TTJets700mtt','TTJets1000mtt']

#bkgProcs['top'] = bkgProcs['T']+bkgProcs['OtherT']+bkgProcs['TTV']+bkgProcs['TTJets']

bkgProcs['tt2b']  = [tt+'_tt2b' for tt in ['TTTo2L2Nu', 'TTToHadronic']]
bkgProcs['tt2b'] += ['TTToSemiLeptonic_HT500Njet9_tt2b']
bkgProcs['tt2b'] += ['TTToSemiLeptonic_HT0Njet0_tt2b']

#bkgProcs['ttbb']  = [tt+'_ttbb' for tt in bkgProcs['TTJets']]
bkgProcs['ttbb']  = [tt+'_ttbb' for tt in ['TTTo2L2Nu', 'TTToHadronic']]
bkgProcs['ttbb'] += ['TTToSemiLeptonic_HT500Njet9_ttbb']
bkgProcs['ttbb'] += ['TTToSemiLeptonic_HT0Njet0_ttbb']

#bkgProcs['tt1b']   = [tt+'_tt1b' for tt in bkgProcs['TTJets']]
bkgProcs['tt1b']   = [tt+'_tt1b' for tt in ['TTTo2L2Nu', 'TTToHadronic']]
bkgProcs['tt1b'] += ['TTToSemiLeptonic_HT500Njet9_tt1b']
bkgProcs['tt1b'] += ['TTToSemiLeptonic_HT0Njet0_tt1b']

#bkgProcs['ttcc']  = [tt+'_ttcc' for tt in bkgProcs['TTJets']]
bkgProcs['ttcc']  = [tt+'_ttcc' for tt in ['TTTo2L2Nu', 'TTToHadronic']]
bkgProcs['ttcc'] += ['TTToSemiLeptonic_HT500Njet9_ttcc']
bkgProcs['ttcc'] += ['TTToSemiLeptonic_HT0Njet0_ttcc']

#bkgProcs['ttjj']  = [tt+'_ttjj' for tt in bkgProcs['TTJets']]
bkgProcs['ttjj'] = [tt+'_ttjj' for tt in ['TTTo2L2Nu', 'TTToHadronic']]
bkgProcs['ttjj'] += ['TTToSemiLeptonic_HT500Njet9_ttjj']
bkgProcs['ttjj'] += ['TTToSemiLeptonic_HT0Njet0_'+str(i)+'_ttjj' for i in range(1, 11)] #change

bkgProcs['ttnobb']  = bkgProcs['ttjj'] + bkgProcs['ttcc'] + bkgProcs['tt1b'] + bkgProcs['tt2b']

bkgProcs['qcd']   = ['QCDht200','QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000']
bkgProcs['top']   = bkgProcs['TTV']+bkgProcs['T']+bkgProcs['OtherT']
bkgProcs['ewk']   = bkgProcs['WJets']+bkgProcs['ZJets']+bkgProcs['VV']
#bkgProcs['ttbb']  = bkgProcs['TTBB']
#bkgProcs['ttcc']  = bkgProcs['TTCC']
#bkgProcs['ttlf']  = bkgProcs['TTLF']

#bkgProcs['ttbb']  = bkgProcs['TTBB']
#bkgProcs['tt2b']  = bkgProcs['TT2B']
#bkgProcs['ttb']  = bkgProcs['TTB']
#bkgProcs['ttcc']  = bkgProcs['TTCC']
#bkgProcs['ttlf']  = bkgProcs['TTLF']

bkgProcs['ttbar'] = bkgProcs['TTJets']
bkgProcs['wjets'] = bkgProcs['WJets']

dataList = ['DataE','DataM']

htProcs = ['ewk','WJets']
topptProcs = ['ttbb', 'ttnobb']#'tt2b','ttbb','ttb','ttcc','ttlf','ttbar','TTJets']#['top','ttbar','TTJets']#['tt2b','ttbb','ttb','ttcc','ttlf','ttbar','TTJets']
#bkgProcs['ttbar_q2up'] = ['TTJetsPHQ2U']#,'TtWQ2U','TbtWQ2U']
#bkgProcs['ttbar_q2dn'] = ['TTJetsPHQ2D']#,'TtWQ2D','TbtWQ2D']


#if massPt not in massList:    MICHAEL COMMENTED OUT THESE TWO LINES
#	massList.append(massPt)
#sigList = [whichSignal+str(mass) for mass in massList]
sigList = [] 
if whichSignal=='Hptb' or whichSignal == 'Hptb1000': decays = ['']
if whichSignal == 'X53H':sigList = ['X53M1300MH200','X53M1300MH400','X53M1300MH600','X53M1300MH800','X53M1300MH1000','X53M1400MH200','X53M1400MH400','X53M1400MH600','X53M1400MH800','X53M1400MH1000','X53M600MH200','X53M600MH400','X53M700MH200','X53M700MH400','X53M800MH200','X53M800MH400','X53M800MH600','X53M900MH200','X53M900MH400','X53M900MH600','X53M1000MH200','X53M1000MH400','X53M1000MH600','X53M1000MH800','X53M1100MH200','X53M1100MH400','X53M1100MH600','X53M1100MH800','X53M1200MH200','X53M1200MH400','X53M1200MH600','X53M1200MH800','X53M1200MH1000','X53M1500MH200','X53M1500MH400','X53M1500MH600','X53M1500MH800','X53M1500MH1000','X53M1600MH200','X53M1600MH400','X53M1600MH600','X53M1600MH800','X53M1600MH1000','X53M1700MH200','X53M1700MH400','X53M1700MH600','X53M1700MH800','X53M1700MH1000']
#if whichSignal == 'X53H':sigList = ['X53M600MH200','X53M600MH400','X53M700MH200','X53M700MH400','X53M800MH200','X53M800MH400','X53M800MH600','X53M900MH200','X53M900MH400','X53M900MH600','X53M1000MH200','X53M1000MH400','X53M1000MH600','X53M1000MH800','X53M1100MH200','X53M1100MH400','X53M1100MH600','X53M1100MH800','X53M1200MH200','X53M1200MH400','X53M1200MH600','X53M1200MH800','X53M1200MH1000','X53M1500MH200','X53M1500MH400','X53M1500MH600','X53M1500MH800','X53M1500MH1000']

if whichSignal == 'X53':
#	sigList = [whichSignal+'LHM'+str(mass) for mass in [1100,1200,1400,1700]]
	sigList= [whichSignal+'RHM'+str(mass) for mass in range(700,1700+1,100)]#1600+1,100)]
if whichSignal=='Hptb'or 'X53' or 'X53H': decays = ['']

doBRScan = False
BRs={}
BRs['BW']=[0.0,0.50,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0]
BRs['TH']=[0.5,0.25,0.0,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0]
BRs['TZ']=[0.5,0.25,1.0,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
nBRconf=len(BRs['BW'])
if not doBRScan: nBRconf=1

isEMlist = ['E','M']
if region=='SR'or region=='CR': nttaglist=['0','1p']
else: nttaglist = ['0p']
if region=='TTCR': nWtaglist = ['0p']
else: nWtaglist = ['0','1p']
if region=='WJCR': nbtaglist = ['0']
#elif region=='CR': nbtaglist = ['0','0p','1p']
else: nbtaglist = ['1','2p']
if region=='PS': njetslist=['3p']
else: njetslist = ['4p']
if not isCategorized:
    nttaglist = ['0p']
    nWtaglist = ['0p']
    nbtaglist = ['1p']
    njetslist = ['4p']
if not isCategorized and region =='PS':
    nttaglist = ['0p']
    nWtaglist = ['0p']
    nbtaglist = ['1p']
    njetslist = ['3p']


catList = ['is'+item[0]+'_nT'+item[1]+'_nW'+item[2]+'_nB'+item[3]+'_nJ'+item[4] for item in list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist))] #if not skip(item[4] ,item[3])]
tagList = ['nT'+item[0]+'_nW'+item[1]+'_nB'+item[2]+'_nJ'+item[3] for item in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))] #if not skip(item[3] ,item[2])]

if year == 'R17':lumiSys = 0.023 #lumi uncertainty in 2017 0.025 in 2018, 0.012 in 2016
if year == 'R16' or year =='R16APV': lumiSys = 0.012
if year == 'R18': lumiSys = 0.025
eltrigSys = 0.05 #electron trigger uncertainty
mutrigSys = 0.05 #muon trigger uncertainty
elIdSys = 0.015 #0.02#electron id uncertainty
muIdSys = 0.01 #muon id uncertainty
elIsoSys = 0.025 #0#electron isolation uncertainty
muIsoSys = 0.025 #0#muon isolation uncertainty

elcorrdSys = math.sqrt(lumiSys**2+eltrigSys**2+elIdSys**2+elIsoSys**2)
mucorrdSys = math.sqrt(lumiSys**2+mutrigSys**2+muIdSys**2+muIsoSys**2)

for tag in tagList:
	modTag = tag[tag.find('nT'):tag.find('nJ')-3]
	modelingSys['data_'+modTag] = 0.
	modelingSys['qcd_'+modTag] = 0.
	if not addCRsys: #else CR uncertainties are defined in modSyst.py module
		for proc in bkgProcs.keys():
			modelingSys[proc+'_'+modTag] = 0.

###########################################################
#################### CATEGORIZATION #######################
###########################################################
def makeThetaCats(datahists,sighists,bkghists,discriminant,categor):
	yieldTable = {}
	yieldStatErrTable = {}
	for cat in catList:
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
		yieldTable[histoPrefix]={}
		yieldStatErrTable[histoPrefix]={}
		if doAllSys:
			for syst in systematicList:
				for ud in ['Up','Down']:
					yieldTable[histoPrefix+syst+ud]={}
			
		if doQ2sys:
			yieldTable[histoPrefix+'q2Up']={}
			yieldTable[histoPrefix+'q2Down']={}

	#Initialize dictionaries for histograms
	hists={}
	for cat in catList:
		if doTempEachCategory and 'nB1' in cat:
			if 'LL' in discriminant or 'bb' in discriminant or 'BB' in discriminant: continue
# 			print "              processing cat: "+cat
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
		i=cat
		#Group data processes
		hists['data'+i] = datahists[histoPrefix+'_'+dataList[0]].Clone(histoPrefix+'__DATA')
		for dat in dataList:
			if dat!=dataList[0]: hists['data'+i].Add(datahists[histoPrefix+'_'+dat])
	    #Here	
		#Group processes
		for proc in bkgProcList+bkgGrupList:
			print proc
                        hists[proc+i] = bkghists[histoPrefix+'_'+bkgProcs[proc][0]].Clone(histoPrefix+'__'+proc)
			for bkg in bkgProcs[proc]:
				if bkg!=bkgProcs[proc][0]: hists[proc+i].Add(bkghists[histoPrefix+'_'+bkg])

        #get signal
 			for signal in sigList:
 				#print "histoPrefix ", histoPrefix
 				#print "signal+decays[0]", signal+decays[0]
 				#print sighists
                                hists[signal+i] = sighists[histoPrefix+'_'+signal+decays[0]].Clone(histoPrefix+'__sig')
 				for decay in decays:
 					if decay!=decays[0]:
 						htemp = sighists[histoPrefix+'_'+signal+decay].Clone()
 						hists[signal+i].Add(htemp)

        #systematics
		if doAllSys:
			for syst in systematicList:
				for ud in ['Up','Down']:
					for proc in bkgProcList+bkgGrupList:
						if syst=='toppt' and proc not in topptProcs: continue
						if syst=='ht' and proc not in htProcs: continue
#  							print "proc+i+syst+ud : ", proc+i+syst+ud
						hists[proc+i+syst+ud] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkgProcs[proc][0]].Clone(histoPrefix+'__'+proc+'__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
						for bkg in bkgProcs[proc]:
							if bkg!=bkgProcs[proc][0]: hists[proc+i+syst+ud].Add(bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
					if syst=='toppt' or syst=='ht': continue
					for signal in sigList:
						hists[signal+i+syst+ud] = sighists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+signal+decays[0]].Clone(histoPrefix+'__sig__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
						if doBRScan: hists[signal+i+syst+ud].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
						for decay in decays:
							htemp = sighists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+signal+decay].Clone()
							if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
							if decay!=decays[0]: hists[signal+i+syst+ud].Add(htemp)
		if doPDFsys:
			for pdfInd in range(100):
				for proc in bkgProcList+bkgGrupList:
					hists[proc+i+'pdf'+str(pdfInd)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkgProcs[proc][0]].Clone(histoPrefix+'__'+proc+'__pdf'+str(pdfInd))
					for bkg in bkgProcs[proc]:
						if bkg!=bkgProcs[proc][0]: hists[proc+i+'pdf'+str(pdfInd)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
				for signal in sigList:
					hists[signal+i+'pdf'+str(pdfInd)] = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decays[0]].Clone(histoPrefix+'__sig__pdf'+str(pdfInd))
					if doBRScan: hists[signal+i+'pdf'+str(pdfInd)].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
					for decay in decays:
						htemp = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decay].Clone()
						if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
						if decay!=decays[0]:hists[signal+i+'pdf'+str(pdfInd)].Add(htemp)
                                        
		if doQ2sys:
			for proc in bkgProcList+bkgGrupList:
				if proc+'_q2up' not in bkgProcs.keys(): continue
				hists[proc+i+'q2Up'] = bkghists[histoPrefix+'_'+bkgProcs[proc+'_q2up'][0]].Clone(histoPrefix+'__'+proc+'__q2__plus')
				hists[proc+i+'q2Down'] = bkghists[histoPrefix+'_'+bkgProcs[proc+'_q2dn'][0]].Clone(histoPrefix+'__'+proc+'__q2__minus')
				for bkg in bkgProcs[proc+'_q2up']:
					if bkg!=bkgProcs[proc+'_q2up'][0]: hists[proc+i+'q2Up'].Add(bkghists[histoPrefix+'_'+bkg])
				for bkg in bkgProcs[proc+'_q2dn']:
					if bkg!=bkgProcs[proc+'_q2dn'][0]: hists[proc+i+'q2Down'].Add(bkghists[histoPrefix+'_'+bkg])
    
        #+/- 1sigma variations of shape systematics
		if doAllSys:
			for syst in systematicList:
				for ud in ['Up','Down']:
					for proc in bkgGrupList+bkgProcList+sigList:
						if syst=='toppt' and proc not in topptProcs: continue
						if syst=='ht' and proc not in htProcs: continue
						yieldTable[histoPrefix+syst+ud][proc] = hists[proc+i+syst+ud].Integral()
		if doQ2sys:
			for proc in bkgProcList+bkgGrupList:
				if proc+'_q2up' not in bkgProcs.keys(): continue
				yieldTable[histoPrefix+'q2Up'][proc] = hists[proc+i+'q2Up'].Integral()
				yieldTable[histoPrefix+'q2Down'][proc] = hists[proc+i+'q2Down'].Integral()

        #prepare yield table
 		for proc in bkgGrupList+bkgProcList+sigList+['data']: 
#		for proc in bkgGrupList+bkgProcList+['data']: 			
			yieldTable[histoPrefix][proc] = hists[proc+i].Integral()
# 				print "proc : ",proc
# 				print "i : ",i
# 				print hists[proc+i].GetEntries()
            
		print bkgGrupList
		yieldTable[histoPrefix]['totBkg'] = sum([hists[proc+i].Integral() for proc in bkgGrupList])
                print yieldTable[histoPrefix]['totBkg']
                print histoPrefix
		if yieldTable[histoPrefix]['totBkg']==0:
			yieldTable[histoPrefix]['dataOverBkg'] =0
		else:
			yieldTable[histoPrefix]['dataOverBkg'] = yieldTable[histoPrefix]['data']/yieldTable[histoPrefix]['totBkg']
			print yieldTable[histoPrefix]['dataOverBkg']
        #prepare MC yield error table
		for proc in bkgGrupList+bkgProcList+sigList+['data']: yieldStatErrTable[histoPrefix][proc] = 0.
		yieldStatErrTable[histoPrefix]['totBkg'] = 0.
		yieldStatErrTable[histoPrefix]['dataOverBkg']= 0.

		for ibin in range(1,hists[bkgGrupList[0]+i].GetXaxis().GetNbins()+1):
# 				print "ibin ", ibin
# 				print "##########"*20
 			for proc in bkgGrupList+bkgProcList+sigList+['data']: 
#			for proc in bkgGrupList+bkgProcList+['data']: 				
				yieldStatErrTable[histoPrefix][proc] += hists[proc+i].GetBinError(ibin)**2
# 					if 'qcd' in proc:
# 						print 'hists[proc+i].GetBinError(ibin)**2 : ',hists[proc+i].GetBinError(ibin)**2
# 						print 'proc+i : ',proc+i
			yieldStatErrTable[histoPrefix]['totBkg'] += sum([hists[proc+i].GetBinError(ibin)**2 for proc in bkgGrupList])
# 			print "%%%%%%%%"*20
		for key in yieldStatErrTable[histoPrefix].keys(): 
			yieldStatErrTable[histoPrefix][key] = math.sqrt(yieldStatErrTable[histoPrefix][key])
# 				print 'yieldStatErrTable[histoPrefix][key] : ', yieldStatErrTable[histoPrefix][key]
# 				print 'histoPrefix : ',histoPrefix
# 				print 'key : ', key
# 				print "!!!!!!!!"*20
    #scale signal cross section to 1pb
	if scaleSignalXsecTo1pb:
		print "       SCALING SIGNAL TEMPLATES TO 1pb ..."
		for signal in sigList:
			for cat in catList:
				if 'nB1' in cat:
					if 'LL' in discriminant or'bb' in discriminant or 'BB' in discriminant: continue
				i=cat
                                print signal
				hists[signal+i].Scale(1./xsec[signal])
				if doAllSys:
					for syst in systematicList:
						if syst=='toppt' or syst=='ht': continue
						hists[signal+i+syst+'Up'].Scale(1./xsec[signal])
						hists[signal+i+syst+'Down'].Scale(1./xsec[signal])
						if normalizeRENORM_PDF and (syst.startswith('mu') or syst=='pdf'):
							hists[signal+i+syst+'Up'].Scale(hists[signal+i].Integral()/hists[signal+i+syst+'Up'].Integral())
							hists[signal+i+syst+'Down'].Scale(hsihistsg[signal+i].Integral()/hists[signal+i+syst+'Down'].Integral())
				if doPDFsys:
					for pdfInd in range(100): 
						hists[signal+i+'pdf'+str(pdfInd)].Scale(1./xsec[signal])

    #Theta templates:
	print "       WRITING THETA TEMPLATES: "
	for signal in sigList:
		print "              ... "+signal
		thetaRfileName = outDir+'/templates_'+discriminant+'_'+signal+'_'+lumiStr+'fb'+saveKey+'.root'
		if doTempEachCategory:
			thetaRfileName = outDir+'/'+categor+'/templates_'+discriminant+'_'+signal+'_'+lumiStr+'fb'+saveKey+'.root'

		thetaRfile = TFile(thetaRfileName,'RECREATE')
		for cat in catList:
			i=cat
			if doTempEachCategory and 'nB1' in cat:
				if 'LL' in discriminant or'bb' in discriminant or 'BB' in discriminant: continue
 			for proc in bkgGrupList+[signal]:
#			for proc in bkgGrupList:				
				if hists[proc+i].Integral() > 0:
					hists[proc+i].Write()
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt' and proc not in topptProcs: continue
							if syst=='ht' and proc not in htProcs: continue
							hists[proc+i+syst+'Up'].Write()
							hists[proc+i+syst+'Down'].Write()
					if doPDFsys:
						for pdfInd in range(100): hists[proc+i+'pdf'+str(pdfInd)].Write()
					if doQ2sys:
						if proc+'_q2up' not in bkgProcs.keys(): continue
						hists[proc+i+'q2Up'].Write()
						hists[proc+i+'q2Down'].Write()
			hists['data'+i].Write()
		thetaRfile.Close()

	#Combine templates:
	print "       WRITING COMBINE TEMPLATES: "
	combineRfileName = outDir+'/templates_'+discriminant+'_'+lumiStr+'fb'+saveKey+'.root'
	if doTempEachCategory:
		combineRfileName = outDir+'/'+categor+'/templates_'+discriminant+'_'+lumiStr+'fb'+saveKey+'.root'
	combineRfile = TFile(combineRfileName,'RECREATE')
	for cat in catList:
		if doTempEachCategory and 'nB1' in cat:
			if 'LL' in discriminant or'bb' in discriminant or 'BB' in discriminant: continue
		print "              ... "+cat
		i=cat
                print cat
                print "=============================================="
		postTag = ''
		if 'CR' in pfix: postTag = 'isCR_'
		elif 'SR' in pfix: postTag = 'isSR_'
		print postTag
                for signal in sigList:
                        #mass = [str(mass) for mass in massList if signal.endswith(str(mass))][0]
                        hists[signal+i].SetName(hists[signal+i].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal))#.replace('M'+mass,''))+'M'+mass))
                        hists[signal+i].Write()
			if doAllSys: #check??
				 for syst in systematicList:
				 	if syst=='toppt' or syst=='ht': continue
				 	hists[signal+i+syst+'Up'].SetName(hists[signal+i+syst+'Up'].GetName().replace('fb_','fb_'+postTag).replace('__plus','Up').replace('__sig','__'+signal))#.replace('M'+mass,'')+'M'+mass))
				 	hists[signal+i+syst+'Down'].SetName(hists[signal+i+syst+'Down'].GetName().replace('fb_','fb_'+postTag).replace('__minus','Down').replace('__sig','__'+signal))#.replace('M'+mass,'')+'M'+mass))
				 	hists[signal+i+syst+'Up'].Write()
				 	hists[signal+i+syst+'Down'].Write()
				 if doPDFsys:
				 	for pdfInd in range(100): 
				 		hists[signal+i+'pdf'+str(pdfInd)].SetName(hists[signal+i+'pdf'+str(pdfInd)].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal))#.replace('M'+mass,'')+'M'+mass))
				 		hists[signal+i+'pdf'+str(pdfInd)].Write()
		for proc in bkgGrupList:
			hists[proc+i].SetName(hists[proc+i].GetName().replace('fb_','fb_'+postTag))
			hists[proc+i].Write()
			if doAllSys:
				for syst in systematicList:
					if syst=='toppt' and proc not in topptProcs: continue
					if syst=='ht' and proc not in htProcs: continue
					hists[proc+i+syst+'Up'].SetName(hists[proc+i+syst+'Up'].GetName().replace('fb_','fb_'+postTag).replace('__plus','Up'))
					hists[proc+i+syst+'Down'].SetName(hists[proc+i+syst+'Down'].GetName().replace('fb_','fb_'+postTag).replace('__minus','Down'))
					hists[proc+i+syst+'Up'].Write()
					hists[proc+i+syst+'Down'].Write()
			if doPDFsys:
				for pdfInd in range(100): 
					hists[proc+i+'pdf'+str(pdfInd)].SetName(hists[proc+i+'pdf'+str(pdfInd)].GetName().replace('fb_','fb_'+postTag))
					hists[proc+i+'pdf'+str(pdfInd)].Write()
			if doQ2sys:
				if proc+'_q2up' not in bkgProcs.keys(): continue
				hists[proc+i+'q2Up'].SetName(hists[proc+i+'q2Up'].GetName().replace('fb_','fb_'+postTag).replace('__plus','Up'))
				hists[proc+i+'q2Down'].SetName(hists[proc+i+'q2Down'].GetName().replace('fb_','fb_'+postTag).replace('__minus','Down'))
				hists[proc+i+'q2Up'].Write()
				hists[proc+i+'q2Down'].Write()
		hists['data'+i].SetName(hists['data'+i].GetName().replace('fb_','fb_'+postTag).replace('DATA','data_obs'))
		hists['data'+i].Write()
	combineRfile.Close()

	print "       WRITING SUMMARY TEMPLATES: "
# 		for signal in sigList:
# 			print "              ... "+signal
# 			yldRfileName = outDir+'/templates_YLD_'+signal+'_'+lumiStr+'fb'+saveKey+'.root'
# 			if doTempEachCategory:
# 				yldRfileName = outDir+'/'+categor+'/templates_YLD_'+signal+'_'+lumiStr+'fb'+saveKey+'.root'
# 			yldRfile = TFile(yldRfileName,'RECREATE')
# 			for isEM in isEMlist:	
# 				for proc in bkgGrupList+['data',signal]:
# 					yldHists = {}
# 					yldHists[isEM+proc]=TH1F('YLD_'+lumiStr+'fb_is'+isEM+'_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA'),'',len(tagList),0,len(tagList))
# 					if doAllSys and proc!='data':
# 						for syst in systematicList:
# 							for ud in ['Up','Down']:
# 								if syst=='toppt' and proc not in topptProcs: continue
# 								if syst=='ht' and proc not in htProcs: continue
# 								yldHists[isEM+proc+syst+ud]=TH1F('YLD_'+lumiStr+'fb_is'+isEM+'_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA')+'__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'),'',len(tagList),0,len(tagList))
# 					if doQ2sys and proc+'_q2up' in bkgProcs.keys(): 
# 						yldHists[isEM+proc+'q2Up']  =TH1F('YLD_'+lumiStr+'fb_is'+isEM+'_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA')+'__q2__plus','',len(tagList),0,len(tagList))
# 						yldHists[isEM+proc+'q2Down']=TH1F('YLD_'+lumiStr+'fb_is'+isEM+'_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA')+'__q2__minus','',len(tagList),0,len(tagList))
# 					ibin = 1
# 					for cat in catList:
# 						if doTempEachCategory and 'nB1' in cat:
# 							if 'LL' in discriminant or'bb' in discriminant or 'BB' in discriminant: continue
# 
# 						if 'is'+isEM not in cat: continue
# 						nttag = cat.split('_')[-4][2:]
# 						nWtag = cat.split('_')[-3][2:]
# 						nbtag = cat.split('_')[-2][2:]
# 						njets = cat.split('_')[-1][2:]
# 						binStr = ''
# 						if nttag!='0p':
# 							if 'p' in nttag: binStr+='#geq'+nttag[:-1]+'t/'
# 							else: binStr+=nttag+'t/'
# 						if nWtag!='0p':
# 							if 'p' in nWtag: binStr+='#geq'+nWtag[:-1]+'W/'
# 							else: binStr+=nWtag+'W/'
# 						if nbtag!='0p':
# 							if 'p' in nbtag: binStr+='#geq'+nbtag[:-1]+'b/'
# 							else: binStr+=nbtag+'b/'
# 						if njets!='0p' and len(njetslist)>1:
# 							if 'p' in njets: binStr+='#geq'+njets[:-1]+'j'
# 							else: binStr+=njets+'j'
# 						if binStr.endswith('/'): binStr=binStr[:-1]
# 						histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
# 						yldHists[isEM+proc].SetBinContent(ibin,yieldTable[histoPrefix][proc])
# 						yldHists[isEM+proc].SetBinError(ibin,yieldStatErrTable[histoPrefix][proc])
# 						yldHists[isEM+proc].GetXaxis().SetBinLabel(ibin,binStr)
# 						if doAllSys and proc!='data':
# 							for syst in systematicList:
# 								for ud in ['Up','Down']:
# 									if syst=='toppt' and proc not in topptProcs: continue
# 									if syst=='ht' and proc not in htProcs: continue
# 									yldHists[isEM+proc+syst+ud].SetBinContent(ibin,yieldTable[histoPrefix+syst+ud][proc])
# 									yldHists[isEM+proc+syst+ud].GetXaxis().SetBinLabel(ibin,binStr)
# 						if doQ2sys and proc+'_q2up' in bkgProcs.keys(): 
# 							yldHists[isEM+proc+'q2Up'].SetBinContent(ibin,yieldTable[histoPrefix+'q2Up'][proc])
# 							yldHists[isEM+proc+'q2Up'].GetXaxis().SetBinLabel(ibin,binStr)
# 							yldHists[isEM+proc+'q2Down'].SetBinContent(ibin,yieldTable[histoPrefix+'q2Down'][proc])
# 							yldHists[isEM+proc+'q2Down'].GetXaxis().SetBinLabel(ibin,binStr)
# 						ibin+=1
# 					yldHists[isEM+proc].Write()
# 					if doAllSys and proc!='data':
# 						for syst in systematicList:
# 							for ud in ['Up','Down']:
# 								if syst=='toppt' and proc not in topptProcs: continue
# 								if syst=='ht' and proc not in htProcs: continue
# 								yldHists[isEM+proc+syst+ud].Write()
# 					if doQ2sys and proc+'_q2up' in bkgProcs.keys(): 
# 						yldHists[isEM+proc+'q2Up'].Write()
# 						yldHists[isEM+proc+'q2Down'].Write()
# 			yldRfile.Close()
            
	table = []
	table.append(['CUTS:',cutString])
	table.append(['break'])
	table.append(['break'])
    
    #yields without background grouping
	table.append(['YIELDS']+[proc for proc in bkgProcList+['data']])
	for cat in catList:
		if doTempEachCategory and 'nB1' in cat:
			if 'LL' in discriminant or'bb' in discriminant or 'BB' in discriminant: continue

		row = [cat]
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
		for proc in bkgProcList+['data']:
			row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
		table.append(row)			
	table.append(['break'])
	table.append(['break'])
    
    #yields with top,ewk,qcd grouping
	table.append(['YIELDS']+[proc for proc in bkgGrupList+['data']])
	for cat in catList:
		if doTempEachCategory and 'nB1' in cat:
			if 'LL' in discriminant or'bb' in discriminant or 'BB' in discriminant: continue

		row = [cat]
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
		for proc in bkgGrupList+['data']:
			row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
		table.append(row)
	table.append(['break'])
	table.append(['break'])
    
    #yields for signals
	table.append(['YIELDS']+[proc for proc in sigList])
	for cat in catList:
		if doTempEachCategory and 'nB1' in cat:
			if 'LL' in discriminant or'bb' in discriminant or 'BB' in discriminant: continue
		row = [cat]
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
 		for proc in sigList:
 			row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
		table.append(row)

    #yields for AN tables (yields in e/m channels)
	for isEM in isEMlist:
		if isEM=='E': corrdSys = elcorrdSys
		if isEM=='M': corrdSys = mucorrdSys
		for nttag in nttaglist:
			table.append(['break'])
			table.append(['','is'+isEM+'_nT'+nttag+'_yields'])
			table.append(['break'])
			table.append(['YIELDS']+[cat for cat in catList if 'is'+isEM in cat and 'nT'+nttag in cat]+['\\\\'])
			for proc in bkgGrupList+['totBkg','data','dataOverBkg']+sigList:
				row = [proc]
				for cat in catList:
					if doTempEachCategory and 'nB1' in cat:
						if 'LL' in discriminant or'bb' in discriminant or 'BB' in discriminant: continue
					if not ('is'+isEM in cat and 'nT'+nttag in cat): continue
					modTag = cat[cat.find('nT'):cat.find('nJ')-3]
					histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
					yieldtemp = 0.
					yielderrtemp = 0.
					if proc=='totBkg' or proc=='dataOverBkg':
						for bkg in bkgGrupList:
							try:
								yieldtemp += yieldTable[histoPrefix][bkg]
								yielderrtemp += yieldStatErrTable[histoPrefix][bkg]**2
								yielderrtemp += (modelingSys[bkg+'_'+modTag]*yieldTable[histoPrefix][bkg])**2
							except:
								print "Missing",bkg,"for channel:",cat
								pass
						yielderrtemp += (corrdSys*yieldtemp)**2
						if proc=='dataOverBkg':
							dataTemp = yieldTable[histoPrefix]['data']+1e-20
							dataTempErr = yieldStatErrTable[histoPrefix]['data']**2
							if yieldtemp ==0 or dataTemp ==0:
								yielderrtemp = 0
							else:
								yielderrtemp = ((dataTemp/yieldtemp)**2)*(dataTempErr/dataTemp**2+yielderrtemp/yieldtemp**2)
								yieldtemp = dataTemp/yieldtemp
					else:
						try:
							yieldtemp += yieldTable[histoPrefix][proc]
							yielderrtemp += yieldStatErrTable[histoPrefix][proc]**2
						except:
							print "Missing",proc,"for channel:",cat
							pass
						if proc not in sigList: 
							yielderrtemp += (modelingSys[proc+'_'+modTag]*yieldtemp)**2
						yielderrtemp += (corrdSys*yieldtemp)**2
					yielderrtemp = math.sqrt(yielderrtemp)
					if proc=='data': row.append(' & '+str(int(yieldTable[histoPrefix][proc])))
					else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,5)))
				row.append('\\\\')
				table.append(row)
	
	#yields for PAS tables (yields in e/m channels combined)
	for nttag in nttaglist:
		table.append(['break'])
		table.append(['','isL_nT'+nttag+'_yields'])
		table.append(['break'])
		table.append(['YIELDS']+[cat.replace('isE','isL') for cat in catList if 'isE' in cat and 'nT'+nttag in cat]+['\\\\'])
		for proc in bkgGrupList+['totBkg','data','dataOverBkg']+sigList:
			row = [proc]
			for cat in catList:
				if doTempEachCategory and 'nB1' in cat:
					if 'LL' in discriminant or'bb' in discriminant or 'BB' in discriminant: continue
				if not ('isE' in cat and 'nT'+nttag in cat): continue
				modTag = cat[cat.find('nT'):cat.find('nJ')-3]
				histoPrefixE = discriminant+'_'+lumiStr+'fb_'+cat
				histoPrefixM = histoPrefixE.replace('isE','isM')
				yieldtemp = 0.
				yieldtempE = 0.
				yieldtempM = 0.
				yielderrtemp = 0. 
				if proc=='totBkg' or proc=='dataOverBkg':
					for bkg in bkgGrupList:
						try:
							yieldtempE += yieldTable[histoPrefixE][bkg]
							yieldtempM += yieldTable[histoPrefixM][bkg]
							yieldtemp  += yieldTable[histoPrefixE][bkg]+yieldTable[histoPrefixM][bkg]
							yielderrtemp += yieldStatErrTable[histoPrefixE][bkg]**2+yieldStatErrTable[histoPrefixM][bkg]**2
							yielderrtemp += (modelingSys[bkg+'_'+modTag]*(yieldTable[histoPrefixE][bkg]+yieldTable[histoPrefixM][bkg]))**2 #(modelingSys*(Nelectron+Nmuon))**2 --> correlated across e/m
						except:
							print "Missing",bkg,"for channel:",cat
							pass
					yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
					if proc=='dataOverBkg':
						dataTemp = yieldTable[histoPrefixE]['data']+yieldTable[histoPrefixM]['data']+1e-20
						dataTempErr = yieldStatErrTable[histoPrefixE]['data']**2+yieldStatErrTable[histoPrefixM]['data']**2
						if yieldtemp ==0:
							yielderrtemp = 0
						else:
							yielderrtemp = ((dataTemp/yieldtemp)**2)*(dataTempErr/dataTemp**2+yielderrtemp/yieldtemp**2)
							yieldtemp = dataTemp/yieldtemp
				else:
					try:
						yieldtempE += yieldTable[histoPrefixE][proc]
						yieldtempM += yieldTable[histoPrefixM][proc]
						yieldtemp  += yieldTable[histoPrefixE][proc]+yieldTable[histoPrefixM][proc]
						yielderrtemp += yieldStatErrTable[histoPrefixE][proc]**2+yieldStatErrTable[histoPrefixM][proc]**2
					except:
						print "Missing",proc,"for channel:",cat
						pass
					if proc not in sigList: yielderrtemp += (modelingSys[proc+'_'+modTag]*yieldtemp)**2 #(modelingSys*(Nelectron+Nmuon))**2 --> correlated across e/m
					yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
				yielderrtemp = math.sqrt(yielderrtemp)
				if proc=='data': row.append(' & '+str(int(yieldTable[histoPrefixE][proc]+yieldTable[histoPrefixM][proc])))
				else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,5)))
			row.append('\\\\')
			table.append(row)

	#systematics
	if doAllSys:
		table.append(['break'])
		table.append(['','Systematics'])
		table.append(['break'])
		for proc in bkgGrupList+sigList:
			table.append([proc]+[cat for cat in catList]+['\\\\'])
			for syst in sorted(systematicList+['q2']):
				for ud in ['Up','Down']:
					row = [syst+ud]
					for cat in catList:
						histoPrefix = discriminant+'_'+lumiStr+'fb_'+cat
						nomHist = histoPrefix
						shpHist = histoPrefix+syst+ud
						try: row.append(' & '+str(round(yieldTable[shpHist][proc]/(yieldTable[nomHist][proc]+1e-20),2)))
						except:
							if not ((syst=='toppt' and proc not in topptProcs) or (syst=='ht' and proc not in htProcs) or (syst=='q2' and (proc+'_q2up' not in bkgProcs.keys() or not doQ2sys))):
								print "Missing",proc,"for channel:",cat,"and systematic:",syst
							pass
					row.append('\\\\')
					table.append(row)
			table.append(['break'])
		
	if not addCRsys: 
		out=open(outDir+'/yields_noCRunc_'+discriminant+'_'+lumiStr+'fb'+saveKey+'.txt','w')
		if doTempEachCategory:
			out=open(outDir+'/'+categor+'/yields_noCRunc_'+discriminant+'_'+lumiStr+'fb'+saveKey+'.txt','w')
	else: out=open(outDir+'/yields_'+discriminant+'_'+lumiStr+'fb'+saveKey+'.txt','w')
	printTable(table,out)

def findfiles(path, filtre):
	for root, dirs, files in os.walk(path):
		for f in fnmatch.filter(files, filtre):
			yield os.path.join(root, f)



def rundoTemp(category):
        iPlotList = [
#        'ST',
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
#'MET',
#'NWJets',
#'NTJets',
# 'lepPt',
## 'lepPhi',
# 'lepEnergy',
#'ST',
#'mindeltaRlb',
#'JetPt',
#'JetEta',
#'theLeadJetPt',
#'JetPhi',
#'NWJets',
#'NTJets',
#'ratio_HTdHT3leadjets',
#'masslepJets1',
#'masslepJets2',
##'minDR_lepJet',
#'MT2bb',
#'masslepBJets0',
#'mass_lepBJet_mindr',
##'mass_lepJets2',
##'fifthJetPt',
##'sixthJetPt',
#'M_allJet_W',
#'HT_bjets',
#'firstcsvb_bb',
#'secondcsvb_bb',
#'thirdcsvb_bb',
#'deltaR_lepJetInMinMljet',
#'deltaR_lepbJetInMinMlb',
#'Sphericity',
#'minMlb',
#'MTlmet',
#'lepDR_minBBdr',
#'NPU',
#'METphi',
#'NPV',
#'NJets',
#'deltaRjet2',
#'NWJets',
#'NTJets',
#'MET',
#'NBJets',
#'ST',
#'theLeadJetPt',
#'JetEta',
#'JetPhi',
#'JetPt',
#'XGB200_SR1',
#'XGB400_SR1',
#'XGB600_SR1',
#'XGB800_SR1',
#'XGB1000_SR1',
'XGB1300_SR1',
#'XGB1500_SR1',
#'lepPt',
#'lepEta',
#'lepPhi',
                #'HT',
                #'minMlb',
                #'centrality',
                #'FW_momentum_0',
                #'FW_momentum_1', ##TODO
                #'FW_momentum_2', ##TODO
                #'FW_momentum_3',
                #'FW_momentum_4',
                #'FW_momentum_5',
                #'FW_momentum_6',
                #'mass_maxJJJpt',
                #'Bjet1Pt',
                #'deltaR_minBB', ##TODO
                ##'deltaR',  ##TODO
                #'MTlmet',
                ##'HT',
                #'hemiout',
                ##'MT2bb',
                ##'masslepBJets0',
                #'mass_lepBJet_mindr',
                ##'fifthJetPt',  ## TODO
                ##'sixthJetPt', ##TODO
               # 'PtFifthJet', ## TODO
                #'mass_minLLdr',
                #'mass_maxBBmass',
                #'deltaR_lepJetInMinMljet',
                #'deltaPhi_lepJetInMinMljet',
                #'deltaR_lepbJetInMinMlb',
                #'deltaPhi_lepbJetInMinMlb',
                #'M_allJet_W',
                #'HT_bjets',
                #'ratio_HTdHT4leadjets',
                #'csvJet1',
                #'csvJet2',
                #'csvJet3',
                #'csvJet4',
                #'firstcsvb_bb',
                #'secondcsvb_bb',
                #'thirdcsvb_bb',
                #'fourthcsvb_bb',
                #'HT_2m',
                #'Sphericity',
                #'Aplanarity',
                ]
#	for file in findfiles(outDir+'/'+category+'/', '*.p'): check!
#		if 'lepPt' not in file: continue
#		if 'bkghists' not in file: continue
#		if not os.path.exists(file.replace('bkghists','datahists')): continue
 #               if not os.path.exists(file.replace('bkghists','sighists')): continue
#		iPlotList.append(file.split('/')[-1].replace('bkghists_','')[:-2])

	print "WORKING DIR:",outDir
	print iPlotList
	for iPlot in iPlotList:
		datahists = {}
		bkghists  = {}
		sighists  = {}

		print "LOADING DISTRIBUTION: "+iPlot
		for cat in catList:
			datahists.update(pickle.load(open(outDir+'/'+cat[2:]+'/datahists_'+iPlot+'.p','rb')))
			bkghists.update(pickle.load(open(outDir+'/'+cat[2:]+'/bkghists_'+iPlot+'.p','rb')))
                        sighists.update(pickle.load(open(outDir+'/'+cat[2:]+'/sighists_'+iPlot+'.p','rb')))

#		for data in datahists.keys(): 
#			if 'XGB' in iPlot and region == 'CR': datahists[data].GetXaxis().SetRangeUser(0., 0.95)
#		for bkg in bkghists.keys():
#			if 'XGB' in iPlot and region == 'CR': bkghists[bkg].GetXaxis().SetRangeUser(0., 0.95)
#		for sig in sighists.keys():
#			if 'XGB' in iPlot and region == 'CR': sighists[sig].GetXaxis().SetRangeUser(0., 0.95)


		if iPlot=='BDTdontscale':
			for key in bkghists.keys(): 
				if key.startswith(iPlot+'jecUp') or key.startswith(iPlot+'jecDown'): continue
				if key.startswith(iPlot+'jerUp') or key.startswith(iPlot+'jerDown'): continue
				if 'TTJetsPHQ2U' in key or 'TTJetsPHQ2D' in key: continue
				bkghists[key].Scale(2)
			for key in sighists.keys(): 
				if key.startswith(iPlot+'jecUp') or key.startswith(iPlot+'jecDown'): continue
				if key.startswith(iPlot+'jerUp') or key.startswith(iPlot+'jerDown'): continue
				sighists[key].Scale(2)

		#Rebin
		if rebinBy>0:
			print "REBINNING HISTOGRAMS: MERGING",rebinBy,"BINS ..."
			for data in datahists.keys(): 
				if datahists[data].GetXaxis().GetNbins()<=50: continue
				datahists[data] = datahists[data].Rebin(rebinBy)
			for bkg in bkghists.keys():
				if bkghists[bkg].GetXaxis().GetNbins()<=50: continue
				bkghists[bkg] = bkghists[bkg].Rebin(rebinBy)
			for sig in sighists.keys():
				if sighists[sig].GetXaxis().GetNbins()<=50: continue
				sighists[sig] = sighists[sig].Rebin(rebinBy)
		
		#Negative Bin Correction
		if '_wNegBinsCorrec' in saveKey:
			print "CORRECTING NEGATIVE BINS ..."
			for bkg in bkghists.keys(): negBinCorrection(bkghists[bkg])
                        for sig in sighists.keys(): negBinCorrection(sighists[sig]) #should we do the correction after rebinning? -- SS

		#OverFlow Correction
#	  	print "CORRECTING OVERFLOW BINS ..."
#	  	for data in datahists.keys(): overflow(datahists[data])
#	  	for bkg in bkghists.keys():   overflow(bkghists[bkg])
#	  	for sig in sighists.keys():   overflow(sighists[sig])

		print "       MAKING CATEGORIES FOR TOTAL SIGNALS ..."
		makeThetaCats(datahists,sighists,bkghists,iPlot,category)
print "outDir+'/'+catList[0][2:]+'/' : ", outDir+'/'+catList[0][2:]+'/'

if doTempEachCategory:
	for category in catList:
		print "Category : ",category[2:]
		rundoTemp(category[2:])
else: rundoTemp(catList[0][2:])
print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))


