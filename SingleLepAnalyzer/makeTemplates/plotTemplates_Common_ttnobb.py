#!/usr/bin/python		legy1 = 0.63


import os,sys,time,math,pickle,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as rt
from weights import *
from modSyst import *
from utils import *
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)
start_time = time.time()

lumi=str(targetlumi/1000).replace('.','p') #for plots
lumiInTemplates= str(targetlumi/1000).replace('.','p') # 1/fb

whichSig = 'X53'
doBkg = False#True
doSig =True 
plotttnobb = False #False#True #RFile2 is CR!!!

plottop = False
plotewk = False
plotqcd = False
region='' #SR,PS
isCategorized=False#True
iPlot='XGB1300_SR1'
if len(sys.argv)>2: iPlot=str(sys.argv[2])
cutString=''
pfix='templates'
if not isCategorized: pfix='kinematics_'+region

if len(sys.argv)>3: massPt=str(sys.argv[3])

if len(sys.argv)>1: 
	templateDir=os.getcwd()+'/'+str(sys.argv[1])+'/'
else:
    templateDir=os.getcwd()+'/kinematics_R17_SR_2024_3_24/'#'/templates_R18_SR_2024_2_13/'
    templateDir2 = os.getcwd()+'/kinematics_R17_CR_2024_3_24/'#'/kinematics_R17_CR_2024_3_24/'#'/kinematics_R17_sinancuts_PS_2024_3_10/'#'/kinematics_CR_2024_2_13/'#'/templates_R18_SR_2024_2_14/'#'/kinematics_CR_2024_2_13/'#'/templates_SR_2024_2_13/'#'/templates_2023_11_9/'

splitTTbar = True
isRebinned= '_wNegBinsCorrec_'#_rebinned_stat0p3'#_killFirstBins_syFist' #post for ROOT file names
saveKey = '' # tag for plot names

sig1leg='ttnobb SR' 
sig1 = 'ttnobbSR'

sig2 = 'ttnobbCR'
sig2leg='ttnobb CR'

plotCombine = True ### make it False for YLD plot
scaleSignals =False ##check
scaleFact1 = 100
scaleFact2 = 100
scaleFact3 = 100
scaleFact4 = 100
scaleFact5 = 100
scaleFact6 = 100

scaleFact1merged = 100
scaleFact2merged = 100
scaleFact3merged = 100
scaleFact4merged = 100
scaleFact5merged = 100
scaleFact6merged = 100
#scaleFact1merged = 40
#scaleFact2merged = 40
#scaleFact3merged = 40
#scaleFact4merged = 40
#scaleFact5merged = 40
#scaleFact6merged = 40


if plotCombine: tempsig='templates_'+iPlot+'_'+lumiInTemplates+'fb'+isRebinned+'.root'

tempsig='templates_'+iPlot+'_'+lumiInTemplates+'fb'+isRebinned+'.root'
if iPlot=='YLD': tempsig='templates_'+iPlot+'_'+sig1+'_'+lumiInTemplates+'fb'+isRebinned+'.root'
print "tempsig : ",tempsig
if splitTTbar: 

    bkgTTBarList = ['ttnobb','ttbb'] 
    bkgProcList = bkgTTBarList+['top','ewk','qcd']
    #bkgProcList = ['ewk','top', 'ttnobb', 'ttbb','qcd']
    #    bkgProcList = ['ttbb','tt2b','tt1b','ttcc','ttjj','top','ewk','qcd']
    #    bkgProcList = ['ttb','ttcc','ttlf','top','ewk','qcd']
else: 
    bkgProcList = ['ttbar','top','ewk','qcd']

plotbkg =''
if plotttnobb: 
    bkgProcList = ['ttnobb']
    plotbkg = 'ttnobb'
if plottop: 
    bkgProcList = ['top']
    plotbkg = 'top'
if plotewk: 
    bkgProcList = ['ewk']
    plotbkg = 'ewk'
if plotqcd: 
    bkgProcList = ['qcd']
    plotbkg = 'qcd'

bkgHistColors = {'tt2b':rt.kRed+3,'ttbb':rt.kRed,'tt1b':rt.kRed-3,'ttcc':rt.kRed-5,'ttjj':rt.kRed-7,'top':rt.kBlue,'ewk':rt.kGreen-8,'qcd':rt.kOrange+5,'ttbar':rt.kRed,'ttnobb':rt.kRed-7} #HTB
bkgHistColors2 = {'ttnobb':rt.kBlue} #HTB

#systematicList = ['pileup','LF','LFstat1', 'LFstat2','HF','HFstat1','HFstat2','CFerr1','CFerr2','muRFcorrd','jec','jer','prefire']#,'jmst','jmrt','jmsW','jmrW','trigeff','pileup','muRFcorrd','muR','muF','toppt','jec','jer','ht','LF','LFstat1', 'LFstat2','HF','HFstat1','HFstat2','CFerr1','CFerr2']
systematicList = [
'pileup','muRFcorrd','muR','muF','toppt','jec','jer','ht','LF','LFstat1', 'LFstat2','HF','HFstat1','HFstat2','CFerr1','CFerr2', 'DJjes',
'PNT',
'PNW',
#'CMS_scale_j'       , 'CMS_HPTB_mcreweight_ewk', 'CMS_res_j'        , 'muR_ttbar', 'muF_ttbar',
#'CMS_btag_LF'       , 'CMS_pileup'             , 'CMS_btag_HF'      , 'muR_top'  , 'muF_top'  , 
#'CMS_topreweight' ,
#'CMS_btag_LFstat1'  , 'CMS_btag_CFerr1'        , 'CMS_btag_HFstat1' ,  #'QCDscaleHptb'    , 
#'CMS_btag_LFstat2'  , 'CMS_btag_CFerr2'        , 'CMS_btag_HFstat2' , 'muR_ewk'  , 'muF_ewk'   
]

doAllSys = True
doQ2sys  = False
if not doAllSys: doQ2sys = False
addCRsys = False
doOneBand = True#False
if not doAllSys: doOneBand = True # Don't change this!
blind =True
if region =='PS' or region == 'CR': blind=False
if plotttnobb: 
	blind =True
	doSig = False
blindYLD = False
yLog  = True#False#True
if iPlot=='deltaRjet2':yLog  = False#False#True
doRealPull = False
if doRealPull: doOneBand=False
drawYields = False
plotBkgShapes = True #not yet implemented

isEMlist =['E','M']
if region=='SR' or region=='CR': nttaglist=['0','1p']
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

print(doSig)

tagList = list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))
#print tagList
lumiSys = 0.023 # lumi uncertainty
trigSys = 0.#05 # trigger uncertainty
lepIdSys = 0.03 # lepton id uncertainty
lepIsoSys = 0.01 # lepton isolation uncertainty
corrdSys = math.sqrt(lumiSys**2+trigSys**2+lepIdSys**2+lepIsoSys**2) #cheating while total e/m values are close

for tag in tagList:
	tagStr='nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]
	modTag = tagStr[tagStr.find('nT'):tagStr.find('nJ')-3]
	print tagStr
        print modTag
	modelingSys['data_'+modTag] = 0.
	for proc in bkgProcList:
		if proc in ['ttbar','ttbb','tt1b','ttcc','ttjj','tt2b']: 
			modelingSys[proc+'_'+modTag] = math.sqrt(0.042**2+0.027**2)
	if not addCRsys: #else CR uncertainties are defined in modSyst.py module
		for proc in bkgProcList:
			modelingSys[proc+'_'+modTag] = 0.


def getNormUnc(hist,ibin,modelingUnc):
	contentsquared = hist.GetBinContent(ibin)**2
	error = corrdSys*corrdSys*contentsquared  #correlated uncertainties
	error += modelingUnc*modelingUnc*contentsquared #background modeling uncertainty from CRs
	return error

def formatUpperHist(histogram):
	histogram.GetXaxis().SetLabelSize(0)

	if blind == True:
		histogram.GetXaxis().SetLabelSize(0.045)
		histogram.GetXaxis().SetTitleSize(0.055)
		histogram.GetYaxis().SetLabelSize(0.040)
		histogram.GetYaxis().SetTitleSize(0.055)
		histogram.GetYaxis().SetTitleOffset(1.15)
		histogram.GetXaxis().SetNdivisions(506)
	else:
		histogram.GetYaxis().SetLabelSize(0.040)
		histogram.GetYaxis().SetTitleSize(0.08)
		histogram.GetYaxis().SetTitleOffset(.71)

	if 'nB0' in histogram.GetName() and 'minMlb' in histogram.GetName(): histogram.GetXaxis().SetTitle("min[M(l,jets)] (GeV)")
	histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.01) #check?
	#if not doNormByBinWidth: histogram.SetMaximum(1.5*histogram.GetMaximum())
	if not yLog: 
		histogram.SetMaximum(1.02*histogram.GetMaximum())
		#histogram.SetMinimum(0.25)
	if yLog:
		uPad.SetLogy()
		histogram.SetMaximum(200*histogram.GetMaximum())
		if region == 'SR': histogram.SetMaximum(20*histogram.GetMaximum())
		else: histogram.SetMaximum(200*histogram.GetMaximum())

		
def formatLowerHist(histogram):
	histogram.GetXaxis().SetLabelSize(.12)
	histogram.GetXaxis().SetTitleSize(0.15)
	histogram.GetXaxis().SetTitleOffset(0.95)
	histogram.GetXaxis().SetNdivisions(506)

	histogram.GetYaxis().SetLabelSize(0.065)
	histogram.GetYaxis().SetTitleSize(0.14)
	histogram.GetYaxis().SetTitleOffset(.37)
	histogram.GetYaxis().SetTitle('Data/Bkg')
	histogram.GetYaxis().SetNdivisions(5)
	if doRealPull: histogram.GetYaxis().SetRangeUser(min(-2.99,0.8*histogram.GetBinContent(histogram.GetMaximumBin())),max(2.99,1.2*histogram.GetBinContent(histogram.GetMaximumBin())))
	else: 
		if iPlot=='YLD': histogram.GetYaxis().SetRangeUser(0.5,1.5)
		else: histogram.GetYaxis().SetRangeUser(0.01,1.99)
	histogram.GetYaxis().CenterTitle()

legx1 = 0.55
legx2 = legx1+0.50
legx3 = legx2+0.50
legx4 = legx3+0.50
legx5 = legx4+0.50
legx6 = legx5+0.50

legy1 = 0.5
legy2 = legy1+0.37
legy3 = legy2+0.37
legy4 = legy3+0.37
legy5 = legy4+0.37
legy6 = legy5+0.37

tagPosX = 0.76
tagPosY = 0.52
# 	if drawQCDmerged: legmerged = rt.TLegend(0.45,0.52,0.95,0.87)
# 	if not drawQCDmerged or blind: legmerged = rt.TLegend(0.45,0.64,0.95,0.89)


RFile1 = rt.TFile(templateDir+tempsig)
#print RFile1
RFile2 = rt.TFile(templateDir2+tempsig)#.replace('_wNegBinsCorrec_',''))
print RFile2
#RFile3 = rt.TFile("kinematics_R17_SR_2024_3_24/templates_XGB1300_SR1_41p48fb_wNegBinsCorrec_.root")
#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.lumi_13TeV= str(targetlumi/1000)+" fb^{-1}"#"59.83 fb^{-1}"#"41.5 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"#"Preliminary"#Work in Progress"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 800; 
W_ref = 800; 
W = W_ref
H  = H_ref

# 
# Simple example of macro: plot with CMS name and lumi text
#  (this script does not pretend to work in all configurations)
# iPeriod = 1*(0/1 7 TeV) + 2*(0/1 8 TeV)  + 4*(0/1 13 TeV) 
# For instance: 
#               iPeriod = 3 means: 7 TeV + 8 TeV
#               iPeriod = 7 means: 7 TeV + 8 TeV + 13 TeV 
#               iPeriod = 0 means: free form (uses lumi_sqrtS)
# Initiated by: Gautier Hamel de Monchenault (Saclay)
# Translated in Python by: Joshua Hardenbrook (Princeton)
# Updated by:   Dinko Ferencek (Rutgers)
#

iPeriod = 4

# references for T, B, L, R
T = 0.10*H_ref
B = 0.35*H_ref 
if blind == True: B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref

bkghists = {}
bkghistsmerged = {}
bkghists2 = {}
bkghistsmerged2 = {}
systHists = {}
systHists2 = {}
totBkgTemp1 = {}
totBkgTemp2 = {}
totBkgTemp3 = {}
totBkgTemp1_2 = {}
totBkgTemp2_2 = {}
totBkgTemp3_2 = {}

if plotCombine:
	dataName = 'data_obs'
	upTag = 'Up'
	downTag = 'Down'
else: #theta
	dataName = 'DATA'
	upTag = '__plus'
	downTag = '__minus'
blindGlob = blind
for tag in tagList:
	tagStr='nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]

	postTag = '' 
#	if isCR(tag[3],tag[2]): 
#		postTag = 'isCR_'
#		#postTag = 'isSR_'
#                blind = False
#	else: 
#		postTag = 'isSR_'
#		blind = blindGlob
	if not blind:
		legx1 = 0.30
		legy1 = 0.65

		legx2 = legx1+0.65
		legx3 = legx2+0.3
		legx4 = legx3+0.3
		legx5 = legx4+0.3
		legx6 = legx5+0.3

		legy2 = legy1+0.25
		legy3 = legy2+0.2
		legy4 = legy3+0.2
		legy5 = legy4+0.2
		legy6 = legy5+0.2

 		tagPosX = 0.25#0.76
 		tagPosY = 0.65#0.52

	else:
		legx1 = 0.30
		legy1 = 0.65
		legx2 = legx1+0.65
		legx3 = legx2+0.75
		legx4 = legx3+0.75
		legx5 = legx4+0.75
		legx6 = legx5+0.75

		legy2 = legy1+0.23
		legy3 = legy2+0.32
		legy4 = legy3+0.32
		legy5 = legy4+0.32
		legy6 = legy5+0.32

		tagPosX = 0.76
		tagPosY = 0.52

#	if not isCategorized: blind = blindGlob
	if not plotCombine: postTag=''
	#if skip(tag[3],tag[2]) and isCategorized: continue
	modTag = tagStr[tagStr.find('nT'):tagStr.find('nJ')-3]
	for isEM in isEMlist:
		histPrefix=iPlot+'_'+lumiInTemplates+'fb_'
		catStr=postTag+'is'+isEM+'_'+tagStr
		histPrefix+=catStr
		print histPrefix
		print dataName
		print 
		##for proc in bkgProcList: 
		##	try: bkghists[proc+catStr] = RFile1.Get(histPrefix+'__'+proc).Clone()
		##	except:
				##print "There is no "+proc+"!!!!!!!!"
				##print "Skipping "+proc+"....."
				##pass
#		if plotttnobb:
#			for proc in ['ttnobb2']:#bkgProcList: 
#				bkghists2[proc+catStr] = RFile2.Get(histPrefix+'__'+'ttnobb').Clone()
#				#except:
#				#	print "There is no "+proc+"!!!!!!!!"
#				#	print "Skipping "+proc+"....."
#				#	pass


		print histPrefix
                print "Above this line ^^^^^^^ ====================================="
                ##if blindYLD and iPlot=='YLD': hData = RFile1.Get(histPrefix+'__'+dataName+'_blind').Clone()
		##else: hData = RFile1.Get(histPrefix+'__'+dataName).Clone()
		
		if plotCombine:
			print "histPrefix", histPrefix
			hsig1 = RFile1.Get(histPrefix+'__'+'ttnobb').Clone(histPrefix+'__ttnobb1')

			hsig2 = RFile2.Get(histPrefix+'__'+'ttnobb').Clone(histPrefix+'__ttnobb2')
		else:
			hsig1 = RFile1.Get(histPrefix+'__ttnobb').Clone(histPrefix+'__ttnobb1')

			hsig2 = RFile2.Get(histPrefix+'__ttnobb').Clone(histPrefix+'__ttnobb2')
		print "Debugging "
		##print RFile1
		print RFile2
#reapplies the xsec just for plotting--I turned of scale to 1pb in doTemplates
		#hsig1.Scale(xsec[sig1])
		#if whichSig == 'X53H':
		#	hsig2.Scale(xsec[sig2])
		#	hsig3.Scale(xsec[sig3])
		#	hsig4.Scale(xsec[sig4])
		#	hsig5.Scale(xsec[sig5])
		#	hsig6.Scale(xsec[sig6])


#		if doAllSys:
#			q2list = []
#			if doQ2sys: q2list=['q2']
#			print systematicList
#			for syst in systematicList+q2list:
#				print syst
#				for ud in [upTag,downTag]:
#					for proc in bkgProcList:
#						try: 
#							##systHists[proc+catStr+syst+ud] = RFile1.Get(histPrefix+'__'+proc+'__'+syst+ud).Clone()
#							if plotttnobb: systHists2[proc+catStr+syst+ud] = RFile2.Get(histPrefix+'__'+proc+'__'+syst+ud).Clone()
#							#if whichSig == 'X53H' and not plotttnobb: 
#							#	systHists[proc+catStr+syst+ud] = RFile2.Get(histPrefix+'__'+proc+'__'+syst+ud).Clone()
#							#	systHists[proc+catStr+syst+ud] = RFile3.Get(histPrefix+'__'+proc+'__'+syst+ud).Clone()
#							#	systHists[proc+catStr+syst+ud] = RFile4.Get(histPrefix+'__'+proc+'__'+syst+ud).Clone()
#							#	systHists[proc+catStr+syst+ud] = RFile5.Get(histPrefix+'__'+proc+'__'+syst+ud).Clone()
#							#	systHists[proc+catStr+syst+ud] = RFile6.Get(histPrefix+'__'+proc+'__'+syst+ud).Clone()
#
#							##if doNormByBinWidth: normByBinWidth(systHists[proc+catStr+syst+ud])
#							##if doNormbyBinWidth and plotttnobb: normByBinWidth(systHists2[proc+catStr+syst+ud])
#						except: pass
#
#		bkgHT = bkghists[bkgProcList[0]+catStr].Clone()
#		if plotttnobb: bkgHT2 = bkghists2['ttnobb2'+catStr].Clone()
#
#		for proc in bkgProcList:
#			if proc==bkgProcList[0]: continue
#			try: bkgHT.Add(bkghists[proc+catStr])
#			except: pass
#			if plotttnobb: 
#				bkgHT2.Add(bkghists2['ttnobb2'+catStr])
#				#except: pass
#
#		totBkgTemp1[catStr] = rt.TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapeOnly'))
#		totBkgTemp2[catStr] = rt.TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapePlusNorm'))
#		totBkgTemp3[catStr] = rt.TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'All'))
#		
#		if plotttnobb:
#			totBkgTemp1_2[catStr] = rt.TGraphAsymmErrors(bkgHT2.Clone(bkgHT2.GetName()+'shapeOnly'))
#			totBkgTemp2_2[catStr] = rt.TGraphAsymmErrors(bkgHT2.Clone(bkgHT2.GetName()+'shapePlusNorm'))
#			totBkgTemp3_2[catStr] = rt.TGraphAsymmErrors(bkgHT2.Clone(bkgHT2.GetName()+'All'))
#	
#		for ibin in range(1,bkghists[bkgProcList[0]+catStr].GetNbinsX()+1):
#			errorUp = 0.
#			errorDn = 0.
#			errorStatOnly = bkgHT.GetBinError(ibin)**2
#			errorNorm = 0.
#			for proc in bkgProcList:
#				try: errorNorm += getNormUnc(bkghists[proc+catStr],ibin,modelingSys[proc+'_'+modTag])
#				except: pass
#			if doAllSys:
#				q2list=[]
#				if doQ2sys: q2list=['q2']
#				for syst in systematicList+q2list:
#					for proc in bkgProcList:
#						try:
#							errorPlus = systHists[proc+catStr+syst+upTag].GetBinContent(ibin)-bkghists[proc+catStr].GetBinContent(ibin)
#							errorMinus = bkghists[proc+catStr].GetBinContent(ibin)-systHists[proc+catStr+syst+downTag].GetBinContent(ibin)
#							if errorPlus > 0: errorUp += errorPlus**2
#							else: errorDn += errorPlus**2
#							if errorMinus > 0: errorDn += errorMinus**2
#							else: errorUp += errorMinus**2
#						except: pass
#
#			totBkgTemp1[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
#			totBkgTemp1[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn))
#			totBkgTemp2[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
#			totBkgTemp2[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm))
#			totBkgTemp3[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
#			totBkgTemp3[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatOnly))
#		
#		if plotttnobb:
#			for ibin in range(1,bkghists2['ttnobb2'+catStr].GetNbinsX()+1):
#				errorUp = 0.
#				errorDn = 0.
#				errorStatOnly = bkgHT2.GetBinError(ibin)**2
#				errorNorm = 0.
#				for proc in bkgProcList:
#					try: errorNorm += getNormUnc(bkghists2['ttnobb2'+catStr],ibin,modelingSys[proc+'_'+modTag])
#					except: pass
#
#				if doAllSys:
#					q2list=[]
#					if doQ2sys: q2list=['q2']
#					for syst in systematicList+q2list:
#						for proc in bkgProcList:
#							try:
#								errorPlus = systHists2['ttnobb2'+catStr+syst+upTag].GetBinContent(ibin)-bkghists2['ttnobb2'+catStr].GetBinContent(ibin)
#								errorMinus = bkghists2['ttnobb2'+catStr].GetBinContent(ibin)-systHists2['ttnobb2'+catStr+syst+downTag].GetBinContent(ibin)
#								if errorPlus > 0: errorUp += errorPlus**2
#								else: errorDn += errorPlus**2
#								if errorMinus > 0: errorDn += errorMinus**2
#								else: errorUp += errorMinus**2
#							except: pass
#
#				totBkgTemp1_2[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
#				totBkgTemp1_2[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn))
#				totBkgTemp2_2[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
#				totBkgTemp2_2[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm))
#				totBkgTemp3_2[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
#				totBkgTemp3_2[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatOnly))
#	
#		
#		bkgHTgerr = totBkgTemp3[catStr].Clone()
#		if plotttnobb: bkgHTgerr2 = totBkgTemp3_2[catStr].Clone()
## 		if scaleFact1==0: scaleFact1=int((bkgHT.GetMaximum()/hsig1.GetMaximum())*0.5)
## 		if scaleFact2==0: scaleFact2=int((bkgHT.GetMaximum()/hsig2.GetMaximum())*0.5)
#		if scaleFact1==0: scaleFact1=1
#		if scaleFact2==0: scaleFact2=1
#		if scaleFact3==0: scaleFact3=1
#		if scaleFact4==0: scaleFact4=1
#		if scaleFact5==0: scaleFact5=1
#		if scaleFact6==0: scaleFact6=1
#
#		if not scaleSignals:
#			scaleFact1=1
#			scaleFact2=1
#			scaleFact3=1
#			scaleFact4=1
#			scaleFact3=1
#			scaleFact6=1
#
# 		hsig1.Scale(scaleFact1)
#		if whichSig == 'X53H':
# 			hsig2.Scale(scaleFact2)

                ############################################################
		############## Making Plots of e+jets, mu+jets and e/mu+jets 
                ############################################################
		
#		drawQCD = False
#		try: drawQCD = bkghists['qcd'+catStr].Integral()/bkgHT.Integral()>.005 #don't plot QCD if it is less than 0.5%
#		except: pass
#
#		stackbkgHT = rt.THStack("stackbkgHT","")
#		#stackbkgHT2 = rt.THStack("stackbkgHT2","")
#		for proc in bkgProcList:
#			try: 
#				if drawQCD or proc!='qcd': stackbkgHT.Add(bkghists[proc+catStr])
#				if plotttnobb: stackbkgHT.Add(bkghists2['ttnobb2'+catStr])
#			except: pass

		sig1Color= rt.kBlack
		sig2Color= rt.kBlue
			
#		for proc in bkgProcList:
#			try: 
#				bkghists[proc+catStr].SetLineColor(bkgHistColors[proc])
#				if not plotttnobb: bkghists[proc+catStr].SetFillColor(bkgHistColors[proc])
#				bkghists[proc+catStr].SetLineWidth(2)
#				if plotttnobb:
#					bkghists2['ttnobb2'+catStr].SetLineColor(bkgHistColors2[proc])
#					bkghists2['ttnobb2'+catStr].SetFillColor(bkgHistColors2[proc])
#					bkghists2['ttnobb2'+catStr].SetLineWidth(2)
#			except: pass
#			
#		if drawYields: 
#			bkgHT.SetMarkerSize(4)
#			bkgHT.SetMarkerColor(rt.kRed)
#
#			if plotttnobb:
#				bkgHT2.SetMarkerSize(4)
#				bkgHT2.SetMarkerColor(rt.kBlue)

		hsig1.SetLineColor(sig1Color)
		hsig1.SetFillStyle(0)
		hsig1.SetLineWidth(3)
		hsig2.SetLineColor(sig2Color)
		#hsig2.SetLineStyle(7)#5)
		hsig2.SetFillStyle(0)
		hsig2.SetLineWidth(3)

#		if not drawYields: hData.SetMarkerStyle(20)
#		hData.SetMarkerSize(1.2)
#		hData.SetMarkerColor(rt.kBlack)
#		hData.SetLineWidth(2)
#		hData.SetLineColor(rt.kBlack)
#		if drawYields: hData.SetMarkerSize(4)
#
#		#bkgHTgerr.SetFillStyle(3002)
#		bkgHTgerr.SetFillColorAlpha(rt.kBlack, 0.5)
#		bkgHTgerr.SetLineColor(rt.kBlack)
#
#		if plotttnobb:
#			bkgHTgerr2.SetFillColorAlpha(rt.kBlack, 0.5)
#			bkgHTgerr2.SetLineColor(rt.kBlack)

		c1 = rt.TCanvas("c1","c1",50,50,W,H)
		c1.SetFillColor(0)
		c1.SetBorderMode(0)
		c1.SetFrameFillStyle(0)
		c1.SetFrameBorderMode(0)
		c1.SetTickx(0)
		c1.SetTicky(0)
	
		yDiv=0.35
		if blind == True: yDiv=0.0
		uPad=rt.TPad("uPad","",0,yDiv,1,1) #for actual plots
	
		uPad.SetLeftMargin( L/W )
		uPad.SetRightMargin( R/W )
		uPad.SetTopMargin( T/H )
		uPad.SetBottomMargin( 0 )
		if blind == True: uPad.SetBottomMargin( B/H )
	
		uPad.SetFillColor(0)
		uPad.SetBorderMode(0)
		uPad.SetFrameFillStyle(0)
		uPad.SetFrameBorderMode(0)
		uPad.SetTickx(0)
		uPad.SetTicky(0)
		uPad.Draw()
#		if blind == False:
#			lPad=rt.TPad("lPad","",0,0,1,yDiv) #for sigma runner
#
#			lPad.SetLeftMargin( L/W )
#			lPad.SetRightMargin( R/W )
#			lPad.SetTopMargin( 0 )
#			lPad.SetBottomMargin( B/H )
#
#			lPad.SetGridy()
#			lPad.SetFillColor(0)
#			lPad.SetBorderMode(0)
#			lPad.SetFrameFillStyle(0)
#			lPad.SetFrameBorderMode(0)
#			lPad.SetTickx(0)
#			lPad.SetTicky(0)
#			lPad.Draw()
#		hData.SetMaximum(1.5*max(hData.GetMaximum(),bkgHT.GetMaximum()))
#		hData.SetMinimum(0.1)#check?
#		hData.SetTitle("")
#
#		hData.GetYaxis().SetTitle("Events / bin")
#		formatUpperHist(hData)
		uPad.cd()
#		hData.SetTitle("")
#		if not blind: hData.Draw("esamex0")
		if blind: 
			hsig1.SetMinimum(0.1)#check?
			hsig1.GetYaxis().SetTitle("Events / bin")
			#if doNormByBinWidth: normByBinWidth(bkgHT_test)
			formatUpperHist(hsig1)
			formatUpperHist(hsig2)
			#if blind: formatUpperHist(stackbkgHT)			
			hsig1.SetMaximum(1.5*hsig1.GetMaximum())
			if plottop or plotewk or plotqcd:#here
				hsig1.SetMaximum(1.1*hsig1.GetMaximum())
			#if doSig: 
			hsig1.Draw("HIST")
                	hsig2.Draw("SAME HIST")
			#stackbkgHT.Draw("SAME HIST")
			#else: stackbkgHT.Draw("HIST")
		#if plotttnobb: stackbkgHT2.Draw("SAME HIST")
		#if not blind: 
			#stackbkgHT.Draw("HIST")
			#if plotttnobb: stackbkgHT2.Draw("SAME HIST")
		#if drawYields: 
		#	rt.gStyle.SetPaintTextFormat("1.0f")
		#	bkgHT.Draw("SAME TEXT90")
		#	if plotttnobb: bkgHT2.Draw("SAME TEXT90")
 		#if doSig: hsig1.Draw("SAME HIST")
                #hsig2.Draw("SAME HIST")
               
                #print 'IM HERE'
 		#print '======'*10

#		if not blind: 
#			hData.Draw("esamex0") #redraw data so its not hidden
#			if drawYields: hData.Draw("SAME TEXT00") 
		uPad.RedrawAxis()
#		bkgHTgerr.Draw("SAME E2")
#		if plotttnobb: bkgHTgerr2.Draw("SAME E2")
			
		chLatex = rt.TLatex()
		chLatex.SetNDC()
		chLatex.SetTextSize(0.06)
		if blind: chLatex.SetTextSize(0.03)#0.04
		chLatex.SetTextAlign(21) # align center
		flvString = ''
		tagString = ''
		if isEM=='E': flvString+='e+jets'
		if isEM=='M': flvString+='#mu+jets'
		if tag[0]!='0p': 
			if 'p' in tag[0]: tagString+='#geq'+tag[0][:-1]+' t, '
			else: tagString+=tag[0]+' t, '
		if tag[1]!='0p': 
			if 'p' in tag[1]: tagString+='#geq'+tag[1][:-1]+' W, '
			else: tagString+=tag[1]+' W, '
		if tag[2]!='0p': 
			if 'p' in tag[2]: tagString+='#geq'+tag[2][:-1]+' b, '
			else: tagString+=tag[2]+' b, '
		if tag[3]!='0p': 
			if 'p' in tag[3]: tagString+='#geq'+tag[3][:-1]+' j'
			else: tagString+=tag[3]+' j'
		if tagString.endswith(', '): tagString = tagString[:-2]
		chLatex.DrawLatex(tagPosX, tagPosY, flvString)
		if isCategorized and not iPlot == 'YLD':
			chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)
		if not isCategorized and iPlot != 'YLD':
			chLatex.DrawLatex(tagPosX, tagPosY-0.06, 'PS')#tagString)


		leg = rt.TLegend(legx1,legy1,legx2,legy2) #edit

		leg.SetShadowColor(0)
		leg.SetFillColor(0)
		leg.SetFillStyle(0)
		leg.SetLineColor(0)
		leg.SetLineStyle(0)
		leg.SetBorderSize(0) 
		leg.SetNColumns(2)
# 		leg.SetTextFont(50)
		scaleFact1Str = ' x'+str(scaleFact1)
		scaleFact2Str = ' x'+str(scaleFact2)
		scaleFact3Str = ' x'+str(scaleFact3)
		scaleFact4Str = ' x'+str(scaleFact4)
		scaleFact5Str = ' x'+str(scaleFact5)
		scaleFact6Str = ' x'+str(scaleFact6)

		if not scaleSignals:
			scaleFact1Str = ''
			scaleFact2Str = ''
			scaleFact3Str = ''
			scaleFact4Str = ''
			scaleFact5Str = ''
			scaleFact6Str = ''

 		leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")
 		leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l")

#		if doBkg:
#			try: leg.AddEntry(bkghists['ttlf'+catStr],"t#bar{t}+lf","f")
#			except: pass
#			try: leg.AddEntry(bkghists['ttcc'+catStr],"t#bar{t}+c#bar{c}","f")
#			except: pass
#			try: leg.AddEntry(bkghists['ttb'+catStr],"t#bar{t}+b","f")
#			except: pass
#			try: leg.AddEntry(bkghists['top'+catStr],"TOP","f")
#			except: pass
#                	try: leg.AddEntry(bkghists['tt2b'+catStr],"t#bar{t}+2b","f")
#			except: pass
#                	print bkghists['ttnobb'+catStr]
#                	try: leg.AddEntry(bkghists['ttnobb'+catStr],"t#bar{t}+!b#bar{b}","f")
#                	except: pass
#			try: leg.AddEntry(bkghists['ewk'+catStr],"EWK","f")
#			except: pass
#			try: leg.AddEntry(bkghists['ttbb'+catStr],"t#bar{t}+b#bar{b}","f")
#			except: pass
#			try: leg.AddEntry(bkghists['qcd'+catStr],"QCD","f")
#			except: pass
#		if not blind: 
#			leg.AddEntry(hData,"Data","ep")
#			leg.AddEntry(bkgHTgerr,"Bkg uncert","f")
#		else:
#			leg.AddEntry(0, "", "")
#			if not plotttnobb: leg.AddEntry(bkgHTgerr,"Bkg uncert","f")
#			if plotttnobb: leg.AddEntry(bkgHTgerr,"Bkg uncert--SR","f")
#			if plotttnobb: leg.AddEntry(bkgHTgerr2,"Bkg uncert--CR","f")
		leg.Draw("same")

		#draw the lumi text on the canvas
		CMS_lumi.CMS_lumi(uPad, iPeriod, iPos)
	
		uPad.Update()
		uPad.RedrawAxis()
		frame = uPad.GetFrame()
		uPad.Draw()

#		if blind == False and not doRealPull:
#			lPad.cd()
#			pull=hData.Clone("pull")
#			pull.Divide(hData, bkgHT)
#			#pull2=hsig1.Clone("pull2")
#			#pull2.Divide(hsig1,bkgHT)
#
#			for binNo in range(0,hData.GetNbinsX()+2):
#				if bkgHT.GetBinContent(binNo)!=0:
#					pull.SetBinError(binNo,hData.GetBinError(binNo)/bkgHT.GetBinContent(binNo))
#			if iPlot=='YLD':
#				pull.SetMaximum(1.5)
#				pull.SetMinimum(0.1)
#			else: 
#				pull.SetMaximum(2)
#				pull.SetMinimum(0.1)
#			pull.SetFillColor(1)
#			pull.SetLineColor(1)
#			formatLowerHist(pull)
#			pull.Draw("E0")#"E1")
#			
#			BkgOverBkg = pull.Clone("bkgOverbkg")
#			BkgOverBkg.Divide(bkgHT, bkgHT)
#			pullUncBandTot=rt.TGraphAsymmErrors(BkgOverBkg.Clone("pulluncTot"))
#			for binNo in range(0,hData.GetNbinsX()+2):
#				if bkgHT.GetBinContent(binNo)!=0:
#					pullUncBandTot.SetPointEYhigh(binNo-1,totBkgTemp3[catStr].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
#					pullUncBandTot.SetPointEYlow(binNo-1,totBkgTemp3[catStr].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
#			if not doOneBand: pullUncBandTot.SetFillStyle(3002)
#			else: pullUncBandTot.SetFillStyle(3002)
#			pullUncBandTot.SetFillColor(14)
#			pullUncBandTot.SetLineColor(14)
#			pullUncBandTot.SetMarkerSize(0)
#			rt.gStyle.SetHatchesLineWidth(1)
#			pullUncBandTot.Draw("SAME E2")
#			
#			pullUncBandNorm=rt.TGraphAsymmErrors(BkgOverBkg.Clone("pulluncNorm"))
#			for binNo in range(0,hData.GetNbinsX()+2):
#				if bkgHT.GetBinContent(binNo)!=0:
#					pullUncBandNorm.SetPointEYhigh(binNo-1,totBkgTemp2[catStr].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
#					pullUncBandNorm.SetPointEYlow(binNo-1,totBkgTemp2[catStr].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
#			pullUncBandNorm.SetFillStyle(3002)
#			pullUncBandNorm.SetFillColor(2)
#			pullUncBandNorm.SetLineColor(2)
#			pullUncBandNorm.SetMarkerSize(0)
#			rt.gStyle.SetHatchesLineWidth(1)
#			if not doOneBand: pullUncBandNorm.Draw("SAME E2")
#			
#			pullUncBandStat=rt.TGraphAsymmErrors(BkgOverBkg.Clone("pulluncStat"))
#			for binNo in range(0,hData.GetNbinsX()+2):
#				if bkgHT.GetBinContent(binNo)!=0:
#					pullUncBandStat.SetPointEYhigh(binNo-1,totBkgTemp1[catStr].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
#					pullUncBandStat.SetPointEYlow(binNo-1,totBkgTemp1[catStr].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
#			pullUncBandStat.SetFillStyle(3002)
#			pullUncBandStat.SetFillColor(3)
#			pullUncBandStat.SetLineColor(3)
#			pullUncBandStat.SetMarkerSize(0)
#			rt.gStyle.SetHatchesLineWidth(1)
#			if not doOneBand: pullUncBandStat.Draw("SAME E2")
#
#			pullLegend=rt.TLegend(0.14,0.87,0.85,0.96)
#			rt.SetOwnership( pullLegend, 0 )   # 0 = release (not keep), 1 = keep
#			pullLegend.SetShadowColor(0)
#			pullLegend.SetNColumns(2)
#			pullLegend.SetFillColor(0)
#			pullLegend.SetFillStyle(0)
#			pullLegend.SetLineColor(0)
#			pullLegend.SetLineStyle(0)
#			pullLegend.SetBorderSize(0)
## 			pullLegend.SetTextFont(40)
#			if not doOneBand: 
#				pullLegend.AddEntry(pullUncBandStat , "Bkg uncert. (shape syst.)" , "f")
#				pullLegend.AddEntry(pullUncBandNorm , "Bkg uncert. (shape #oplus norm. syst.)" , "f")
#				pullLegend.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus all syst.)" , "f")
#			elif not doAllSys: pullLegend.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus norm.)" , "f")
#			else: pullLegend.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus syst.)" , "f")
#			#pullLegend.AddEntry(pullQ2up , "Q^{2} Up" , "l")
#			#pullLegend.AddEntry(pullQ2dn , "Q^{2} Down" , "l")
## 			pullLegend.Draw("SAME")
#			pull.Draw("SAME E0")
#			lPad.RedrawAxis()
#
#		if blind == False and doRealPull:
#			lPad.cd()
#			pull=hData.Clone("pull")
#			for binNo in range(0,hData.GetNbinsX()+2):
#				if hData.GetBinContent(binNo)!=0:
#					MCerror = 0.5*(totBkgTemp3[catStr].GetErrorYhigh(binNo-1)+totBkgTemp3[catStr].GetErrorYlow(binNo-1))
#					pull.SetBinContent(binNo,(hData.GetBinContent(binNo)-bkgHT.GetBinContent(binNo))/math.sqrt(MCerror**2+hData.GetBinError(binNo)**2))
#				else: pull.SetBinContent(binNo,0.)
#			pull.SetMaximum(3)
#			pull.SetMinimum(-3)
#			pull.SetFillColor(kGray+2)
#			pull.SetLineColor(kGray+2)
#			formatLowerHist(pull)
#			pull.GetYaxis().SetTitle('Pull')
#			pull.Draw("HIST")

		#c1.Write()
# 		savePrefix = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+cutString+'/plots/'
		savePrefix = templateDir.replace(cutString,'')+cutString+'/plots/'
		if not os.path.exists(savePrefix): os.system('mkdir '+savePrefix)
		savePrefix+=histPrefix+isRebinned.replace('_rebinned_stat1p1','')+saveKey
		if nttaglist[0]=='0p': savePrefix=savePrefix.replace('nT0p_','')
		if nWtaglist[0]=='0p': savePrefix=savePrefix.replace('nW0p_','')
		if nbtaglist[0]=='0p': savePrefix=savePrefix.replace('nB0p_','')
		if njetslist[0]=='0p': savePrefix=savePrefix.replace('nJ0p_','')
		if doRealPull: savePrefix+='_pull'
		if yLog: savePrefix+='_logy'
		if blind or blindYLD: savePrefix+='_blind'
		if doOneBand:
			c1.SaveAs(savePrefix+plotbkg+"totBand.pdf")
			c1.SaveAs(savePrefix+plotbkg+"totBand.png")
			c1.SaveAs(savePrefix+plotbkg+"totBand.eps")
			#c1.SaveAs(savePrefix+"totBand.root")
			#c1.SaveAs(savePrefix+"totBand.C")
		else:
			c1.SaveAs(savePrefix+plotbkg+".pdf")
			c1.SaveAs(savePrefix+plotbkg+".png")
			c1.SaveAs(savePrefix+plotbkg+".eps")
			#c1.SaveAs(savePrefix+".root")
			#c1.SaveAs(savePrefix+".C")
#		for proc in bkgProcList:
#			try: del bkghists[proc+catStr]
#			except: pass
#					
#			if plotttnobb: del bkghists2['ttnobb2'+catStr]

	# Making plots for e+jets/mu+jets combined #
	histPrefixE = iPlot+'_'+lumiInTemplates+'fb_'+postTag+'isE_'+tagStr
	histPrefixM = iPlot+'_'+lumiInTemplates+'fb_'+postTag+'isM_'+tagStr

#	for proc in bkgProcList:
#		##try: 
#		##	bkghistsmerged[proc+'isL'+tagStr] = RFile1.Get(histPrefixE+'__'+proc).Clone()
#		##	bkghistsmerged[proc+'isL'+tagStr].Add(RFile1.Get(histPrefixM+'__'+proc))
#		##except: pass
#        	if plotttnobb:            
#			try: 
#				bkghistsmerged2['ttnobb2'+'isL'+tagStr] = RFile2.Get(histPrefixE+'__'+proc).Clone()
#				bkghistsmerged2['ttnobb2'+'isL'+tagStr].Add(RFile2.Get(histPrefixM+'__'+proc))
#			except: pass
# 
#
#	##if blindYLD and iPlot=='YLD': hDatamerged = RFile1.Get(histPrefixE+'__'+dataName+'_blind').Clone()
#	##else: hDatamerged = RFile1.Get(histPrefixE+'__'+dataName).Clone()
#	##if blindYLD and iPlot=='YLD': hDatamerged.Add(RFile1.Get(histPrefixM+'__DATA_blind').Clone())
#	##else: hDatamerged.Add(RFile1.Get(histPrefixM+'__'+dataName).Clone())
#	if plotttnobb:
#		if blindYLD and iPlot=='YLD': hDatamerged2 = RFile2.Get(histPrefixE+'__'+dataName+'_blind').Clone()
#		else: hDatamerged2 = RFile2.Get(histPrefixE+'__'+dataName).Clone()
#		if blindYLD and iPlot=='YLD': hDatamerged2.Add(RFile2.Get(histPrefixM+'__DATA_blind').Clone())
#		else: hDatamerged2.Add(RFile2.Get(histPrefixM+'__'+dataName).Clone())


 	hsig1merged = RFile1.Get(histPrefixE+'__'+'ttnobb')#, 'ttnobb1merged')#.Clone(histPrefixE+'__ttnobb1merged')
	hsig1merged.Add(RFile1.Get(histPrefixM+'__'+'ttnobb').Clone())

	hsig2merged = RFile2.Get(histPrefixE+'__'+'ttnobb')#, 'ttnobb2merged')#.SetName(histPrefixE+'__'+'ttnobb2')
 	#hsig2merged = RFile2.Get(histPrefixE+'__'+'ttnobb').Clone(histPrefixE+'__ttnobb2merged')
  	hsig2merged.Add(RFile2.Get(histPrefixM+'__'+'ttnobb').Clone())
	#hsig3merged = RFile3.Get(iPlot+'_'+lumiInTemplates+'fb_'+postTag+'isE_'+tagStr+'__ttnobb')

##Turned off scale to 1pb in doTemplates
#	#hsig1merged.Scale(xsec[sig1]) #check!
#	#if whichSig == 'X53H':
# 	#	hsig2merged.Scale(xsec[sig2])
# 	#	hsig3merged.Scale(xsec[sig2])
# 	#	hsig4merged.Scale(xsec[sig2])
# 	#	hsig5merged.Scale(xsec[sig2])
# 	#	hsig6merged.Scale(xsec[sig2])
#
#	if doAllSys:
#		q2list=[]
#		if doQ2sys: q2list=['q2']
#		for syst in systematicList+q2list:
#			for ud in [upTag,downTag]:
#				for proc in bkgProcList:
#					try: 
#						systHists[proc+'isL'+tagStr+syst+ud] = systHists[proc+postTag+'isE_'+tagStr+syst+ud].Clone()
#						systHists[proc+'isL'+tagStr+syst+ud].Add(systHists[proc+postTag+'isM_'+tagStr+syst+ud])
#					except: pass
#
#	bkgHTmerged = bkghistsmerged[bkgProcList[0]+'isL'+tagStr].Clone()
#	if plotttnobb:	bkgHTmerged2 = bkghistsmerged2['ttnobb2'+'isL'+tagStr].Clone()
# 
#	for proc in bkgProcList:
#		if proc==bkgProcList[0]: continue
#		try: bkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
#		except: pass
#		if plotttnobb:
#			try: bkgHTmerged2.Add(bkghistsmerged2['ttnobb2'+'isL'+tagStr])
#			except: pass
#
#	totBkgTemp1['isL'+tagStr] = rt.TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapeOnly'))
#	totBkgTemp2['isL'+tagStr] = rt.TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapePlusNorm'))
#	totBkgTemp3['isL'+tagStr] = rt.TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'All'))
#
#	if plotttnobb:
#		totBkgTemp1_2['isL'+tagStr] = rt.TGraphAsymmErrors(bkgHTmerged2.Clone(bkgHTmerged2.GetName()+'shapeOnly'))
#		totBkgTemp2_2['isL'+tagStr] = rt.TGraphAsymmErrors(bkgHTmerged2.Clone(bkgHTmerged2.GetName()+'shapePlusNorm'))
#		totBkgTemp3_2['isL'+tagStr] = rt.TGraphAsymmErrors(bkgHTmerged2.Clone(bkgHTmerged2.GetName()+'All'))
#
#		
#	for ibin in range(1,bkghistsmerged[bkgProcList[0]+'isL'+tagStr].GetNbinsX()+1):
#		errorUp = 0.
#		errorDn = 0.
#		errorStatOnly = bkgHTmerged.GetBinError(ibin)**2
#		errorNorm = 0.
#		for proc in bkgProcList:
#			try: errorNorm += getNormUnc(bkghistsmerged[proc+'isL'+tagStr],ibin,modelingSys[proc+'_'+modTag])
#			except: pass
#
#		if doAllSys:
#			q2list=[]
#			if doQ2sys: q2list=['q2']
#			for syst in systematicList+q2list:
#				for proc in bkgProcList:
#					try:
#						errorPlus = systHists[proc+'isL'+tagStr+syst+upTag].GetBinContent(ibin)-bkghistsmerged[proc+'isL'+tagStr].GetBinContent(ibin)
#						errorMinus = bkghistsmerged[proc+'isL'+tagStr].GetBinContent(ibin)-systHists[proc+'isL'+tagStr+syst+downTag].GetBinContent(ibin)
#						if errorPlus > 0: errorUp += errorPlus**2
#						else: errorDn += errorPlus**2
#						if errorMinus > 0: errorDn += errorMinus**2
#						else: errorUp += errorMinus**2
#					except: pass
#		totBkgTemp1['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
#		totBkgTemp1['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn))
#		totBkgTemp2['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
#		totBkgTemp2['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm))
#		totBkgTemp3['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
#		totBkgTemp3['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatOnly))
#
#	if plotttnobb:
#		for ibin in range(1,bkghistsmerged2['ttnobb2'+'isL'+tagStr].GetNbinsX()+1):
#			errorUp = 0.
#			errorDn = 0.
#			errorStatOnly = bkgHTmerged2.GetBinError(ibin)**2
#			errorNorm = 0.
#			for proc in bkgProcList:
#				try: errorNorm += getNormUnc(bkghistsmerged2['ttnobb2'+'isL'+tagStr],ibin,modelingSys[proc+'_'+modTag])
#				except: pass
#
#
#			if doAllSys:
#				q2list=[]
#				if doQ2sys: q2list=['q2']
#				for syst in systematicList+q2list:
#					for proc in bkgProcList:
#						try:
#							errorPlus = systHists2['ttnobb2'+'isL'+tagStr+syst+upTag].GetBinContent(ibin)-bkghistsmerged2['ttnobb2'+'isL'+tagStr].GetBinContent(ibin)
#							errorMinus = bkghistsmerged2['ttnobb2'+'isL'+tagStr].GetBinContent(ibin)-systHists2['ttnobb2'+'isL'+tagStr+syst+downTag].GetBinContent(ibin)
#							if errorPlus > 0: errorUp += errorPlus**2
#							else: errorDn += errorPlus**2
#							if errorMinus > 0: errorDn += errorMinus**2
#							else: errorUp += errorMinus**2
#						except: pass
#			totBkgTemp1_2['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
#			totBkgTemp1_2['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn))
#			totBkgTemp2_2['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
#			totBkgTemp2_2['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm))
#			totBkgTemp3_2['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
#			totBkgTemp3_2['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatOnly))
#
#
#	errorStatOnlyT = 0.
#	errorNormT = 0.
#	errorUpT = 0.
#	errorDnT = 0.	
#	bkgHTgerrmerged = totBkgTemp3['isL'+tagStr].Clone()
#	if plotttnobb: bkgHTgerrmerged2 = totBkgTemp3_2['isL'+tagStr].Clone()
#
#	##if scaleFact1merged==0: scaleFact1merged=int((bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum())*0.5)
#	if scaleFact2merged==0: scaleFact2merged=int((bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum())*0.5)
#	if scaleFact3merged==0: scaleFact3merged=int((bkgHTmerged.GetMaximum()/hsig3merged.GetMaximum())*0.5)
#	if scaleFact4merged==0: scaleFact4merged=int((bkgHTmerged.GetMaximum()/hsig4merged.GetMaximum())*0.5)
#	if scaleFact5merged==0: scaleFact5merged=int((bkgHTmerged.GetMaximum()/hsig5merged.GetMaximum())*0.5)
#	if scaleFact6merged==0: scaleFact6merged=int((bkgHTmerged.GetMaximum()/hsig6merged.GetMaximum())*0.5)
#
#	if not scaleSignals:
#		scaleFact1merged=1
#		scaleFact2merged=1
#		scaleFact3merged=1
#		scaleFact4merged=1
#		scaleFact5merged=1
#		scaleFact6merged=1
#
## 	hsig1merged.Scale(scaleFact1merged)
#
## 	hsig2merged.Scale(scaleFact2merged)
## 	hsig2merged.Scale(scaleFact2merged)
#		
#	drawQCDmerged = False
#	try: drawQCDmerged = bkghistsmerged['qcdisL'+tagStr].Integral()/bkgHTmerged.Integral()>.005
#	except: pass
#
#	stackbkgHTmerged = rt.THStack("stackbkgHTmerged","")
#	#stackbkgHTmerged2= rt.THStack("stackbkgHTmerged2","")
#
#	for proc in bkgProcList:
#		try: 
#			if drawQCDmerged or proc!='qcd': stackbkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
#			if plotttnobb: stackbkgHTmerged.Add(bkghistsmerged2['ttnobb2'+'isL'+tagStr])
#		except: pass
#
#	for proc in bkgProcList:
#		try: 
#			bkghistsmerged[proc+'isL'+tagStr].SetLineColor(bkgHistColors[proc])
#			bkghistsmerged[proc+'isL'+tagStr].SetFillColor(bkgHistColors[proc])
#			bkghistsmerged[proc+'isL'+tagStr].SetLineWidth(2)
#		except: pass
#		if plotttnobb:
#			try: 
#				bkghistsmerged2['ttnobb2'+'isL'+tagStr].SetLineColor(bkgHistColors2[proc])
#				bkghistsmerged2['ttnobb2'+'isL'+tagStr].SetFillColor(bkgHistColors2[proc])
#				bkghistsmerged2['ttnobb2'+'isL'+tagStr].SetLineWidth(2)
#			except: pass
#
#	if drawYields: 
#		bkgHTmerged.SetMarkerSize(4)
#		bkgHTmerged.SetMarkerColor(rt.kRed)
#		if plotttnobb: 
#			bkgHTmerged2.SetMarkerSize(4)
#			bkgHTmerged2.SetMarkerColor(rt.kBlue)
 	hsig1merged.SetLineColor(sig1Color)
	hsig1merged.SetFillStyle(0)
	hsig1merged.SetLineWidth(3)
 	hsig2merged.SetLineColor(sig2Color)
	hsig2merged.SetFillStyle(0)
 	hsig2merged.SetLineWidth(3)
   	
 	hsig2merged.SetLineColor(sig2Color)
 	hsig2merged.SetFillStyle(0)
 	hsig2merged.SetLineWidth(3)
  	
#	hsig3merged.SetLineColor(rt.kOrange)
#	hsig3merged.SetFillStyle(0)
#	hsig3merged.SetLineWidth(3)

#	if not drawYields: hDatamerged.SetMarkerStyle(20)
#	hDatamerged.SetMarkerSize(1.2)
#	hDatamerged.SetMarkerColor(rt.kBlack)
#	hDatamerged.SetLineWidth(2)
#	hDatamerged.SetLineColor(rt.kBlack)
#	if drawYields: hDatamerged.SetMarkerSize(4)
#
#	if plotttnobb:
#		if not drawYields: hDatamerged2.SetMarkerStyle(20)
#		hDatamerged2.SetMarkerSize(1.2)
#		hDatamerged2.SetMarkerColor(rt.kBlue)
#		hDatamerged2.SetLineWidth(2)
#		hDatamerged2.SetLineColor(rt.kBlue)
#		if drawYields: hDatamerged2.SetMarkerSize(4)
#
#
#	bkgHTgerrmerged.SetFillStyle(3002)
#	bkgHTgerrmerged.SetFillColor(rt.kBlack)
#	bkgHTgerrmerged.SetLineColor(rt.kBlack)
#	if plotttnobb:
#		bkgHTgerrmerged2.SetFillStyle(3002)	
#		bkgHTgerrmerged2.SetFillColor(rt.kBlack)
#		bkgHTgerrmerged2.SetLineColor(rt.kBlack)
	c1merged = rt.TCanvas("c1merged","c1merged",50,50,W,H)
	c1merged.SetFillColor(0)
	c1merged.SetBorderMode(0)
	c1merged.SetFrameFillStyle(0)
	c1merged.SetFrameBorderMode(0)
	c1merged.SetTickx(0)
	c1merged.SetTicky(0)
	
	yDiv=0.35
	if blind == True: yDiv=0.0
	uPad=rt.TPad("uPad","",0,yDiv,1,1) #for actual plots
	
	uPad.SetLeftMargin( L/W )
	uPad.SetRightMargin( R/W )
	uPad.SetTopMargin( T/H )
	uPad.SetBottomMargin( 0 )
	if blind == True: uPad.SetBottomMargin( B/H )
	
	uPad.SetFillColor(0)
	uPad.SetBorderMode(0)
	uPad.SetFrameFillStyle(0)
	uPad.SetFrameBorderMode(0)
	uPad.SetTickx(0)
	uPad.SetTicky(0)
	uPad.Draw()
#	if blind == False:
#		lPad=rt.TPad("lPad","",0,0,1,yDiv) #for sigma runner
#
#		lPad.SetLeftMargin( L/W )
#		lPad.SetRightMargin( R/W )
#		lPad.SetTopMargin( 0 )
#		lPad.SetBottomMargin( B/H )
#
#		lPad.SetGridy()
#		lPad.SetFillColor(0)
#		lPad.SetBorderMode(0)
#		lPad.SetFrameFillStyle(0)
#		lPad.SetFrameBorderMode(0)
#		lPad.SetTickx(0)
#		lPad.SetTicky(0)
#		lPad.Draw()
#	hDatamerged.SetMaximum(1.5*max(hDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
#	hDatamerged.SetMinimum(0.1)#check?
#	hDatamerged.GetYaxis().SetTitle("Events / bin")
#	formatUpperHist(hDatamerged)
	uPad.cd()
#	hDatamerged.SetTitle("")
#	stackbkgHTmerged.SetTitle("")
	#if plotttnobb: stackbkgHTmerged2.SetTitle("")
#	if not blind: 
#		hDatamerged.Draw("esamex0")
        if blind: 
            ##hsig1merged.SetMinimum(0.1)#check?
            ##hsig1merged.GetYaxis().SetTitle("Events / bin")
            formatUpperHist(hsig1merged)
#	    formatUpperHist(hsig2merged)
            ##hsig1merged.SetMaximum(1.5*hDatamerged.GetMaximum()) #uncomment!
            if plottop or plotewk or plotqcd or plotttnobb:
                hsig1merged.SetMaximum(1.1*hsig1merged.GetMaximum())
            hsig1merged.Draw("HIST") #if doSig
	    #c1merged.Update()
            hsig2merged.Draw("SAME HIST") #if doSig
	    #c1merged.Update()
	    print "Debugging merged"
            print RFile1
	    print RFile2

#	if doBkg and plotttnobb: stackbkgHTmerged.Draw("SAME HIST")
#	if doBkg and not plotttnobb: stackbkgHTmerged.Draw("SAME HIST")
##	if doBkg and plotttnobb: stackbkgHTmerged2.Draw("SAME HIST")
##        hsig1merged.Draw("HIST") #if doSig CHANGE FOR TTNOBB
##	c1merged.Update()
##	hsig3merged.Draw("SAME HIST")
##	c1merged.Update()
##	if doBkg: stackbkgHTmerged.Draw("SAME HIST")
##	if doBkg and plotttnobb: stackbkgHTmerged2.Draw("SAME HIST")
#
#
#	if drawYields: 
#		rt.gStyle.SetPaintTextFormat("1.0f")
#		bkgHTmerged.Draw("SAME TEXT90")
#		if plotttnobb:
#			bkgHTmerged2.Draw("SAME TEXT90")
#
#
# 	#hsig2merged.Draw("SAME HIST")
# 	#hsig1merged.Draw("SAME HIST")
#
#
#	if not blind: 
#		hDatamerged.Draw("esamex0") #redraw data so its not hidden
#		if drawYields: hDatamerged.Draw("SAME TEXT00") 
	uPad.RedrawAxis()
#	if doBkg: bkgHTgerrmerged.Draw("SAME E2")
#	if doBkg and plotttnobb: bkgHTgerrmerged2.Draw("SAME E2")
#
#	chLatexmerged = rt.TLatex()
#	chLatexmerged.SetNDC()
#	chLatexmerged.SetTextSize(0.06)
#	if blind: chLatexmerged.SetTextSize(0.04)
#	chLatexmerged.SetTextAlign(21) # align center
#	flvString = 'e/#mu+jets'
#	tagString = ''
#	if tag[0]!='0p':
#		if 'p' in tag[0]: tagString+='#geq'+tag[0][:-1]+' t, '
#		else: tagString+=tag[0]+' t,  '
#	if tag[1]!='0p':
#		if 'p' in tag[1]: tagString+='#geq'+tag[1][:-1]+' W, '
#		else: tagString+=tag[1]+' W, '
#	if tag[2]!='0p':
#		if 'p' in tag[2]: tagString+='#geq'+tag[2][:-1]+' b, '
#		else: tagString+=tag[2]+' b, '
#	if tag[3]!='0p':
#		if 'p' in tag[3]: tagString+='#geq'+tag[3][:-1]+' j'
#		else: tagString+=tag[3]+' j'
#	if tagString.endswith(', '): tagString = tagString[:-2]
#	chLatexmerged.DrawLatex(tagPosX, tagPosY, flvString)
#	
#        if isCategorized and iPlot != 'YLD':
#		chLatexmerged.DrawLatex(tagPosX, tagPosY-0.06, tagString)
#        if not isCategorized and iPlot != 'YLD' and region != 'CR':
#		chLatexmerged.DrawLatex(tagPosX, tagPosY-0.06, tagString)#'BDT region')#tagString)
#        if not isCategorized and iPlot != 'YLD' and region == 'CR':
#                chLatexmerged.DrawLatex(tagPosX, tagPosY-0.06, 'CR')
	legmerged = rt.TLegend(legx1,legy1,legx2,legy2) #edit

	legmerged.SetShadowColor(0)
	legmerged.SetFillColor(0)
	legmerged.SetFillStyle(0)
	legmerged.SetLineColor(0)
	legmerged.SetLineStyle(0)
	legmerged.SetBorderSize(0) 
	legmerged.SetNColumns(2)
 #	legmerged.SetTextFont(62)
#	legmerged.SetTextSize(2.)
	scaleFact1Str = ' x'+str(scaleFact1merged)
	scaleFact2Str = ' x'+str(scaleFact2merged)
	scaleFact3Str = ' x'+str(scaleFact3merged)
	scaleFact4Str = ' x'+str(scaleFact4merged)
	scaleFact5Str = ' x'+str(scaleFact5merged)
	scaleFact6Str = ' x'+str(scaleFact6merged)

	if not scaleSignals:
		scaleFact1Str = ''
		scaleFact2Str = ''
		scaleFact3Str = ''
		scaleFact4Str = ''
		scaleFact5Str = ''
		scaleFact6Str = ''

	try: legmerged.AddEntry(bkghistsmerged['ttlfisL'+tagStr],"t#bar{t}+lf","f")
	except: pass
 	legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")
 	legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l")
	if doBkg:
		try: legmerged.AddEntry(bkghistsmerged['ttccisL'+tagStr],"t#bar{t}+c#bar{c}","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['ttbisL'+tagStr],"t#bar{t}+b","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['topisL'+tagStr],"TOP","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['tt2bisL'+tagStr],"t#bar{t}+2b","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['ewkisL'+tagStr],"EWK","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['ttbbisL'+tagStr],"t#bar{t}+b#bar{b}","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['qcdisL'+tagStr],"QCD","f")
		except: pass
        	print "===============YESSIR=============="
        	if not plotttnobb:
			try: legmerged.AddEntry(bkghistsmerged['ttnobbisL'+tagStr],"t#bar{t}+!b#bar{b}","f")
        		except: pass
	if plotttnobb:
		try: legmerged.AddEntry(bkghistsmerged2['ttnobb2isL'+tagStr],"t#bar{t}+!b#bar{b} CR","f")
		except: pass
        	try: legmerged.AddEntry(bkghistsmerged['ttnobbisL'+tagStr],"t#bar{t}+!b#bar{b} SR","f")
        	except: pass

        if not blind: 
		legmerged.AddEntry(hDatamerged,"Data","ep")
		legmerged.AddEntry(bkgHTgerrmerged,"Bkg uncert","f")
	elif doBkg:
		legmerged.AddEntry(0, "", "")
		if not plotttnobb: legmerged.AddEntry(bkgHTgerrmerged,"Bkg uncert","f")
		if plotttnobb:
			legmerged.AddEntry(bkgHTgerrmerged,"Bkg uncert SR","f")
			legmerged.AddEntry(bkgHTgerrmerged2,"Bkg uncert CR","f")
		
	legmerged.Draw("same")

	#draw the lumi text on the canvas
	CMS_lumi.CMS_lumi(uPad, iPeriod, iPos)
	
	uPad.Update()
	uPad.RedrawAxis()
	frame = uPad.GetFrame()
	uPad.Draw()
	
##	if blind == False and not doRealPull:
##		lPad.cd()
##		pullmerged=hDatamerged.Clone("pullmerged")
##		pullmerged.Divide(hDatamerged, bkgHTmerged)
##		for binNo in range(0,hDatamerged.GetNbinsX()+2):
##			if bkgHTmerged.GetBinContent(binNo)!=0 and hDatamerged.GetBinContent(binNo) > 0:
##				pullmerged.SetBinError(binNo,hDatamerged.GetBinError(binNo)/bkgHTmerged.GetBinContent(binNo))
### 				print "hDatamerged.GetBinError(binNo) : ", hDatamerged.GetBinError(binNo)
##			else:
##				pullmerged.SetBinError(binNo,0) 
##		if iPlot=='YLD':
##			pullmerged.SetMaximum(1.5)
##			pullmerged.SetMinimum(0.1)
##		else:
##			pullmerged.SetMaximum(2)
##			pullmerged.SetMinimum(0)
##		pullmerged.SetFillColor(1)
##		pullmerged.SetLineColor(1)
##		formatLowerHist(pullmerged)
##		pullmerged.Draw("E0")#"E1")
##		
##		BkgOverBkgmerged = pullmerged.Clone("bkgOverbkgmerged")
##		BkgOverBkgmerged.Divide(bkgHTmerged, bkgHTmerged)
##		pullUncBandTotmerged=rt.TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncTotmerged"))
##		for binNo in range(0,hDatamerged.GetNbinsX()+2):
##			if bkgHTmerged.GetBinContent(binNo)!=0:
##				pullUncBandTotmerged.SetPointEYhigh(binNo-1,totBkgTemp3['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
##				pullUncBandTotmerged.SetPointEYlow(binNo-1, totBkgTemp3['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
##		if 'NBJets' in iPlot:
##			pullUncBandTotmerged.SetPointEYhigh(4,0)
##			pullUncBandTotmerged.SetPointEYlow(4,0)
##		if not doOneBand: pullUncBandTotmerged.SetFillStyle(3002)
##		else: pullUncBandTotmerged.SetFillStyle(3002)
##		pullUncBandTotmerged.SetFillColor(14)
##		pullUncBandTotmerged.SetLineColor(14)
##		pullUncBandTotmerged.SetMarkerSize(0)
##		rt.gStyle.SetHatchesLineWidth(1)
##		pullUncBandTotmerged.Draw("SAME E2")
##		
##		pullUncBandNormmerged=rt.TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncNormmerged"))
##		for binNo in range(0,hData.GetNbinsX()+2):
##			if bkgHTmerged.GetBinContent(binNo)!=0:
##				pullUncBandNormmerged.SetPointEYhigh(binNo-1,totBkgTemp2['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
##				pullUncBandNormmerged.SetPointEYlow(binNo-1, totBkgTemp2['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
##		pullUncBandNormmerged.SetFillStyle(3002)
##		pullUncBandNormmerged.SetFillColor(2)
##		pullUncBandNormmerged.SetLineColor(2)
##		pullUncBandNormmerged.SetMarkerSize(0)
##		rt.gStyle.SetHatchesLineWidth(1)
##		if not doOneBand: pullUncBandNormmerged.Draw("SAME E2")
##		
##		pullUncBandStatmerged=rt.TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncStatmerged"))
##		for binNo in range(0,hDatamerged.GetNbinsX()+2):
##			if bkgHTmerged.GetBinContent(binNo)!=0:
##				pullUncBandStatmerged.SetPointEYhigh(binNo-1,totBkgTemp1['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
##				pullUncBandStatmerged.SetPointEYlow(binNo-1, totBkgTemp1['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
##		pullUncBandStatmerged.SetFillStyle(3002)
##		pullUncBandStatmerged.SetFillColor(3)
##		pullUncBandStatmerged.SetLineColor(3)
##		pullUncBandStatmerged.SetMarkerSize(0)
##		rt.gStyle.SetHatchesLineWidth(1)
##		if not doOneBand: pullUncBandStatmerged.Draw("SAME E2")
##
##		pullLegendmerged=rt.TLegend(0.14,0.87,0.85,0.96)
##		rt.SetOwnership( pullLegendmerged, 0 )   # 0 = release (not keep), 1 = keep
##		pullLegendmerged.SetShadowColor(0)
##		pullLegendmerged.SetNColumns(2)
##		pullLegendmerged.SetFillColor(0)
##		pullLegendmerged.SetFillStyle(0)
##		pullLegendmerged.SetLineColor(0)
##		pullLegendmerged.SetLineStyle(0)
##		pullLegendmerged.SetBorderSize(0)
## 		#pullLegendmerged.SetTextFont(22)#42)
##		if not doOneBand: 
##			pullLegendmerged.AddEntry(pullUncBandStat , "Bkg uncert. (shape syst.)" , "f")
##			pullLegendmerged.AddEntry(pullUncBandNorm , "Bkg uncert. (shape #oplus norm. syst.)" , "f")
##			pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus all syst.)" , "f")
##		elif not doAllSys: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus norm.)" , "f")
##		else: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus syst.)" , "f")
## 		#pullLegendmerged.Draw("SAME")
##		pullmerged.Draw("SAME E0")
##		lPad.RedrawAxis()
##
##	if blind == False and doRealPull:
##		lPad.cd()
##		pullmerged=hDatamerged.Clone("pullmerged")
##		for binNo in range(0,hDatamerged.GetNbinsX()+2):
##			if hDatamerged.GetBinContent(binNo)!=0:
##				MCerror = 0.5*(totBkgTemp3['isL'+tagStr].GetErrorYhigh(binNo-1)+totBkgTemp3['isL'+tagStr].GetErrorYlow(binNo-1))
##				pullmerged.SetBinContent(binNo,(hDatamerged.GetBinContent(binNo)-bkgHTmerged.GetBinContent(binNo))/math.sqrt(MCerror**2+hDatamerged.GetBinError(binNo)**2))
##			else: pullmerged.SetBinContent(binNo,0.)
##		pullmerged.SetMaximum(3)
##		pullmerged.SetMinimum(-3)
##		pullmerged.SetFillColor(kGray+2)
##		pullmerged.SetLineColor(kGray+2)
##		formatLowerHist(pullmerged)
##		pullmerged.GetYaxis().SetTitle('Pull')
##		pullmerged.Draw("HIST")

	#c1merged.Write()
# 	savePrefixmerged = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'/plots/'
# 	savePrefixmerged = templateDir.replace(cutString,'')+'/plots/'+sig2
	savePrefixmerged = templateDir.replace(cutString,'')+'/plots/'
	if not os.path.exists(savePrefixmerged): os.system('mkdir '+savePrefixmerged)
	savePrefixmerged+=histPrefixE.replace('isE','isL')+isRebinned.replace('_rebinned_stat1p1','')+saveKey
	if nttaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nT0p_','')
	if nWtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nW0p_','')
	if nbtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nB0p_','')
	if njetslist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nJ0p_','')
	if doRealPull: savePrefixmerged+='_pull'
	if yLog: savePrefixmerged+='_logy'
	if blind or blindYLD: savePrefixmerged+='_blind'

	if doOneBand: 
		c1merged.SaveAs(savePrefixmerged+plotbkg+"totBand.pdf")
		c1merged.SaveAs(savePrefixmerged+plotbkg+"totBand.png")
		#c1merged.SaveAs(savePrefixmerged+plotbkg+"totBand.eps")
		#c1merged.SaveAs(savePrefixmerged+"totBand.root")
		#c1merged.SaveAs(savePrefixmerged+"totBand.C")
	else: 
		c1merged.SaveAs(savePrefixmerged+plotbkg+".pdf")
		c1merged.SaveAs(savePrefixmerged+plotbkg+".png")
		#c1merged.SaveAs(savePrefixmerged+plotbkg+".eps")
		#c1merged.SaveAs(savePrefixmerged+".root")
		#c1merged.SaveAs(savePrefixmerged+".C")
	for proc in bkgProcList:
		try: del bkghistsmerged[proc+'isL'+tagStr]
		except: pass
		if plotttnobb:
			try: del bkghistsmerged2['ttnobb2'+'isL'+tagStr]
			except: pass
				
RFile1.Close()
RFile2.Close()
#RFile3.Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))



