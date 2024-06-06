#!/usr/bin/python		legy1 = 0.63


import os,sys,time,math,pickle,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as rt
from modSyst import *
from utils import *
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)
start_time = time.time()

year = 'R17'

if year == 'R17':from weights_UL17 import *
elif year == 'R18':from weights_UL18 import *
elif year == 'R16':from weights_UL16 import *
elif year == 'R16APV':from weights_UL16APV import *
 
lumi=str(targetlumi/1000).replace('.','p') #for plots
lumiInTemplates= str(targetlumi/1000).replace('.','p') # 1/fb

whichSig = 'X53H'
doBkg = False#True
doSig =True 
region='PS' #SR,PS
isCategorized=False#True
iPlot='theLeadJetPt'#'NJets'
massPtH = '400'
splitTTbar = True

if len(sys.argv)>2: iPlot=str(sys.argv[2])
pfix='templates'
if not isCategorized: pfix='kinematics_'+region

massPt='600'
massPt2 = '700'
massPt3 = '800'
massPt4 = '900'
massPt5 = '1000'
massPt6 = '1100'
massPt7 = '1200'
massPt8 = '1300'
massPt9 = '1400'
massPt10 = '1500'


if len(sys.argv)>3: massPt=str(sys.argv[3])

if len(sys.argv)>1: 
	templateDir=os.getcwd()+'/'+str(sys.argv[1])+'/'
else:
    templateDir=os.getcwd()+'/kinematics_R17_final_PS_2024_4_2_X53H/'#'/kinematics_R17_final_SR_2024_4_5/'

isRebinned= '_wNegBinsCorrec_'#_rebinned_stat0p3'#_killFirstBins_syFist' #post for ROOT file names
saveKey = '' # tag for plot names

sig1='X53M'+massPt+'MH'+massPtH # choose the 1st signal to plot
sig1leg='X_{5/3}#bar{X}_{5/3} ('+massPt+' GeV) H^{+} ('+massPtH+' GeV)'

sig2='X53M'+massPt2+'MH'+massPtH
sig3 = 'X53M'+massPt3+'MH'+massPtH
sig4 = 'X53M'+massPt4+'MH'+massPtH
sig5 = 'X53M'+massPt5+'MH'+massPtH
sig6 = 'X53M'+massPt6+'MH'+massPtH
sig7 = 'X53M'+massPt7+'MH'+massPtH
sig8 = 'X53M'+massPt8+'MH'+massPtH
sig9 = 'X53M'+massPt9+'MH'+massPtH
sig10 = 'X53M'+massPt10+'MH'+massPtH
    
sig2leg='X_{5/3}#bar{X}_{5/3} ('+massPt2+' GeV) H^{+} ('+massPtH+' GeV)'
sig3leg='X_{5/3}#bar{X}_{5/3} ('+massPt3+' GeV) H^{+} ('+massPtH+' GeV)'
sig4leg='X_{5/3}#bar{X}_{5/3} ('+massPt4+' GeV) H^{+} ('+massPtH+' GeV)'
sig5leg='X_{5/3}#bar{X}_{5/3} ('+massPt5+' GeV) H^{+} ('+massPtH+' GeV)'
sig6leg='X_{5/3}#bar{X}_{5/3} ('+massPt6+' GeV) H^{+} ('+massPtH+' GeV)'
sig7leg='X_{5/3}#bar{X}_{5/3} ('+massPt7+' GeV) H^{+} ('+massPtH+' GeV)'
sig8leg='X_{5/3}#bar{X}_{5/3} ('+massPt8+' GeV) H^{+} ('+massPtH+' GeV)'
sig9leg='X_{5/3}#bar{X}_{5/3} ('+massPt9+' GeV) H^{+} ('+massPtH+' GeV)'
sig10leg='X_{5/3}#bar{X}_{5/3} ('+massPt10+' GeV) H^{+} ('+massPtH+' GeV)'

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

if plotCombine: tempsig='templates_'+iPlot+'_'+lumiInTemplates+'fb'+isRebinned+'.root'
tempsig='templates_'+iPlot+'_'+lumiInTemplates+'fb'+isRebinned+'.root'
if iPlot=='YLD': tempsig='templates_'+iPlot+'_'+sig1+'_'+lumiInTemplates+'fb'+isRebinned+'.root'
if splitTTbar: 
    bkgTTBarList = ['ttnobb','ttbb'] 
    bkgProcList = bkgTTBarList+['top','ewk','qcd']
else: 
    bkgProcList = ['ttbar','top','ewk','qcd']

bkgHistColors = {'tt2b':rt.kRed+3,'ttbb':rt.kRed,'tt1b':rt.kRed-3,'ttcc':rt.kRed-5,'ttjj':rt.kRed-7,'top':rt.kBlue,'ewk':rt.kGreen-8,'qcd':rt.kOrange+5,'ttbar':rt.kRed,'ttnobb':rt.kRed-7} #HTB
bkgHistColors2 = {'ttnobb':rt.kBlue} #HTB

systematicList = [
'pileup','muRFcorrd','muR','muF','toppt','jec','jer','ht','LF','LFstat1', 'LFstat2','HF','HFstat1','HFstat2','CFerr1','CFerr2', 'DJjes',
'PNT',
'PNW',
'isr','fsr',
]

if year != 'R18': systematicList += ['prefire']
doAllSys = True
doQ2sys  = False
if not doAllSys: doQ2sys = False
addCRsys = False
doNormByBinWidth=False#True check!#set true, to see the actual shape of the distributions when the binning is not uniform, e.g binning with 0.3
doOneBand = True#False
if not doAllSys: doOneBand = True # Don't change this!
blind =True
blindYLD = False
yLog  = True#False#True
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
		#if 'XGB' in iPlot: histogram.GetXaxis().SetRangeUser(0,0.95)
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
		if not doNormByBinWidth: histogram.SetMaximum(200*histogram.GetMaximum())
		else: histogram.SetMaximum(200000*histogram.GetMaximum())
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

legx1 = 0.1#0.5
legx2 = legx1+0.7#0.7#0.60

legy1 = 0.2#0.5
legy2 = 0.89#legy1+0.37 0.87

tagPosX = 0.4
tagPosY = 0.32#0.52

RFile1 = rt.TFile(templateDir+tempsig)
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
	if not blind:
		legx1 = 0.26
		legy1 = 0.60

		legx2 = legx1+0.68

		legy2 = legy1+0.285

 		tagPosX = 0.22#0.76
 		tagPosY = 0.63#0.52

	else:
		legx1 = 0.32
		legy1 = 0.65
		legx2 = legx1+0.67

		tagPosX = 0.76
		tagPosY = 0.52
	if not plotCombine: postTag=''
	modTag = tagStr[tagStr.find('nT'):tagStr.find('nJ')-3]
	for isEM in isEMlist:
		histPrefix=iPlot+'_'+lumiInTemplates+'fb_'
		catStr=postTag+'is'+isEM+'_'+tagStr
		histPrefix+=catStr
	# Making plots for e+jets/mu+jets combined #
	histPrefixE = iPlot+'_'+lumiInTemplates+'fb_'+postTag+'isE_'+tagStr
	histPrefixM = iPlot+'_'+lumiInTemplates+'fb_'+postTag+'isM_'+tagStr

	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+'isL'+tagStr] = RFile1.Get(histPrefixE+'__'+proc).Clone()
			bkghistsmerged[proc+'isL'+tagStr].Add(RFile1.Get(histPrefixM+'__'+proc))
		except: pass

	sig1Color= rt.kBlack
	sig2Color= rt.kRed
	sig3Color= rt.kRed-3
	sig4Color= rt.kMagenta
	sig5Color= rt.kRed-7
	sig6Color= rt.kRed-9
	sig7Color= rt.kRed-13
	sig8Color= rt.kRed-15
	sig9Color= rt.kBlue-7
	sig10Color= rt.kBlue

 	hsig1merged = RFile1.Get(histPrefixE+'__'+sig1).Clone(histPrefixE+'__sig1merged')
	hsig1merged.Add(RFile1.Get(histPrefixM+'__'+sig1).Clone())
 	hsig2merged = RFile1.Get(histPrefixE+'__'+sig2).Clone(histPrefixE+'__sig2merged')
 	hsig3merged = RFile1.Get(histPrefixE+'__'+sig3).Clone(histPrefixE+'__sig3merged')
 	hsig4merged = RFile1.Get(histPrefixE+'__'+sig4).Clone(histPrefixE+'__sig4merged')
 	hsig5merged = RFile1.Get(histPrefixE+'__'+sig5).Clone(histPrefixE+'__sig5merged')
 	hsig6merged = RFile1.Get(histPrefixE+'__'+sig6).Clone(histPrefixE+'__sig6merged')
 	hsig7merged = RFile1.Get(histPrefixE+'__'+sig7).Clone(histPrefixE+'__sig7merged')
 	hsig8merged = RFile1.Get(histPrefixE+'__'+sig8).Clone(histPrefixE+'__sig8merged')
 	hsig9merged = RFile1.Get(histPrefixE+'__'+sig9).Clone(histPrefixE+'__sig9merged')
 	hsig10merged = RFile1.Get(histPrefixE+'__'+sig10).Clone(histPrefixE+'__sig10merged')

  	hsig2merged.Add(RFile1.Get(histPrefixM+'__'+sig2).Clone())
 	hsig3merged.Add(RFile1.Get(histPrefixM+'__'+sig3).Clone())
 	hsig4merged.Add(RFile1.Get(histPrefixM+'__'+sig4).Clone())
 	hsig5merged.Add(RFile1.Get(histPrefixM+'__'+sig5).Clone())
 	hsig6merged.Add(RFile1.Get(histPrefixM+'__'+sig6).Clone())
 	hsig7merged.Add(RFile1.Get(histPrefixM+'__'+sig7).Clone())
 	hsig8merged.Add(RFile1.Get(histPrefixM+'__'+sig8).Clone())
 	hsig9merged.Add(RFile1.Get(histPrefixM+'__'+sig9).Clone())
 	hsig10merged.Add(RFile1.Get(histPrefixM+'__'+sig10).Clone())

	hDatamerged = RFile1.Get(histPrefixE+'__'+dataName).Clone()
	hDatamerged.Add(RFile1.Get(histPrefixM+'__'+dataName).Clone())

	if doNormByBinWidth:
		for proc in bkgProcList:
			try: normByBinWidth(bkghistsmerged[proc+'isL'+tagStr])
			except: pass

# 		normByBinWidth(hsig1merged) #comment out?
# 		normByBinWidth(hsig2merged)
#		normByBinWidth(hDatamerged)
# 		normByBinWidth(hsig2merged)
# 		normByBinWidth(hsig3merged)
# 		normByBinWidth(hsig4merged)
# 		normByBinWidth(hsig5merged)
# 		normByBinWidth(hsig6merged)
#

	if doAllSys:
		q2list=[]
		if doQ2sys: q2list=['q2']
		for syst in systematicList+q2list:
			for ud in [upTag,downTag]:
				for proc in bkgProcList:
					try: 
						systHists[proc+'isL'+tagStr+syst+ud] = systHists[proc+postTag+'isE_'+tagStr+syst+ud].Clone()
						systHists[proc+'isL'+tagStr+syst+ud].Add(systHists[proc+postTag+'isM_'+tagStr+syst+ud])
					except: pass

	bkgHTmerged = bkghistsmerged[bkgProcList[0]+'isL'+tagStr].Clone()
 
	for proc in bkgProcList:
		if proc==bkgProcList[0]: continue
		try: bkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
		except: pass
	totBkgTemp1['isL'+tagStr] = rt.TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapeOnly'))
	totBkgTemp2['isL'+tagStr] = rt.TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapePlusNorm'))
	totBkgTemp3['isL'+tagStr] = rt.TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'All'))

	for ibin in range(1,bkghistsmerged[bkgProcList[0]+'isL'+tagStr].GetNbinsX()+1):
		errorUp = 0.
		errorDn = 0.
		errorStatOnly = bkgHTmerged.GetBinError(ibin)**2
		errorNorm = 0.
		for proc in bkgProcList:
			try: errorNorm += getNormUnc(bkghistsmerged[proc+'isL'+tagStr],ibin,modelingSys[proc+'_'+modTag])
			except: pass

		if doAllSys:
			q2list=[]
			if doQ2sys: q2list=['q2']
			for syst in systematicList+q2list:
				for proc in bkgProcList:
					try:
						errorPlus = systHists[proc+'isL'+tagStr+syst+upTag].GetBinContent(ibin)-bkghistsmerged[proc+'isL'+tagStr].GetBinContent(ibin)
						errorMinus = bkghistsmerged[proc+'isL'+tagStr].GetBinContent(ibin)-systHists[proc+'isL'+tagStr+syst+downTag].GetBinContent(ibin)
						if errorPlus > 0: errorUp += errorPlus**2
						else: errorDn += errorPlus**2
						if errorMinus > 0: errorDn += errorMinus**2
						else: errorUp += errorMinus**2
					except: pass
		totBkgTemp1['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
		totBkgTemp1['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn))
		totBkgTemp2['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
		totBkgTemp2['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm))
		totBkgTemp3['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
		totBkgTemp3['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatOnly))

	errorStatOnlyT = 0.
	errorNormT = 0.
	errorUpT = 0.
	errorDnT = 0.	
	bkgHTgerrmerged = totBkgTemp3['isL'+tagStr].Clone()

	if scaleFact1merged==0: scaleFact1merged=int((bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum())*0.5)
	if scaleFact2merged==0: scaleFact2merged=int((bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum())*0.5)
	if scaleFact3merged==0: scaleFact3merged=int((bkgHTmerged.GetMaximum()/hsig3merged.GetMaximum())*0.5)
	if scaleFact4merged==0: scaleFact4merged=int((bkgHTmerged.GetMaximum()/hsig4merged.GetMaximum())*0.5)
	if scaleFact5merged==0: scaleFact5merged=int((bkgHTmerged.GetMaximum()/hsig5merged.GetMaximum())*0.5)
	if scaleFact6merged==0: scaleFact6merged=int((bkgHTmerged.GetMaximum()/hsig6merged.GetMaximum())*0.5)

	if not scaleSignals:
		scaleFact1merged=1
		scaleFact2merged=1
		scaleFact3merged=1
		scaleFact4merged=1
		scaleFact5merged=1
		scaleFact6merged=1

 	#hsig1merged.Scale(scaleFact1merged)
 	#hsig2merged.Scale(scaleFact2merged)
 	#hsig3merged.Scale(scaleFact3merged)
 	#hsig4merged.Scale(scaleFact4merged)
 	#hsig5merged.Scale(scaleFact5merged)
 	#hsig6merged.Scale(scaleFact6merged)
		
	stackbkgHTmerged = rt.THStack("stackbkgHTmerged","")

	for proc in bkgProcList:
		try: 
			if drawQCDmerged or proc!='qcd': stackbkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
			if plotttnobb: stackbkgHTmerged.Add(bkghistsmerged2['ttnobb2'+'isL'+tagStr])
		except: pass

	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+'isL'+tagStr].SetLineColor(bkgHistColors[proc])
			bkghistsmerged[proc+'isL'+tagStr].SetFillColor(bkgHistColors[proc])
			bkghistsmerged[proc+'isL'+tagStr].SetLineWidth(2)
		except: pass

 	hsig1merged.SetLineColor(sig1Color)
	hsig1merged.SetFillStyle(0)
 	hsig1merged.SetLineWidth(3)
 	hsig2merged.SetLineColor(sig2Color)
 	hsig2merged.SetFillStyle(0)
 	hsig2merged.SetLineWidth(3)
 	hsig3merged.SetLineColor(sig3Color)
 	hsig3merged.SetFillStyle(0)
 	hsig3merged.SetLineWidth(3)
 	hsig4merged.SetLineColor(sig4Color)
 	hsig4merged.SetFillStyle(0)
 	hsig4merged.SetLineWidth(3)
 	hsig5merged.SetLineColor(sig5Color)
 	hsig5merged.SetFillStyle(0)
 	hsig5merged.SetLineWidth(3)
 	hsig6merged.SetLineColor(sig6Color)
 	hsig6merged.SetFillStyle(0)
 	hsig6merged.SetLineWidth(3)
 	hsig7merged.SetLineColor(sig7Color)
 	hsig7merged.SetFillStyle(0)
 	hsig7merged.SetLineWidth(3)
 	hsig8merged.SetLineColor(sig8Color)
 	hsig8merged.SetFillStyle(0)
 	hsig8merged.SetLineWidth(3)
 	hsig9merged.SetLineColor(sig9Color)
 	hsig9merged.SetFillStyle(0)
 	hsig9merged.SetLineWidth(3)
 	hsig10merged.SetLineColor(sig10Color)
 	hsig10merged.SetFillStyle(0)
 	hsig10merged.SetLineWidth(3)
   	
	hDatamerged.SetMarkerSize(1.2)
	hDatamerged.SetMarkerColor(rt.kBlack)
	hDatamerged.SetLineWidth(2)
	hDatamerged.SetLineColor(rt.kBlack)

	bkgHTgerrmerged.SetFillStyle(3002)
	bkgHTgerrmerged.SetFillColor(rt.kBlack)
	bkgHTgerrmerged.SetLineColor(rt.kBlack)
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
	if blind == False:
		lPad=rt.TPad("lPad","",0,0,1,yDiv) #for sigma runner

		lPad.SetLeftMargin( L/W )
		lPad.SetRightMargin( R/W )
		lPad.SetTopMargin( 0 )
		lPad.SetBottomMargin( B/H )

		lPad.SetGridy()
		lPad.SetFillColor(0)
		lPad.SetBorderMode(0)
		lPad.SetFrameFillStyle(0)
		lPad.SetFrameBorderMode(0)
		lPad.SetTickx(0)
		lPad.SetTicky(0)
		lPad.Draw()
	if not doNormByBinWidth: hDatamerged.SetMaximum(1.5*max(hDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
	hDatamerged.SetMinimum(0.1)#check?
	if doNormByBinWidth: 
		hDatamerged.GetYaxis().SetTitle("< Events / GeV >")
		if 'BDT' in iPlot and isSR(tag[3],tag[2]): hDatamerged.GetYaxis().SetTitle("< Events / 1.0 units >")
	elif isRebinned!='': hDatamerged.GetYaxis().SetTitle("Events / bin")
	else: hDatamerged.GetYaxis().SetTitle("Events / bin")
	formatUpperHist(hDatamerged)
	uPad.cd()
	hDatamerged.SetTitle("")
	stackbkgHTmerged.SetTitle("")
	if not blind: 
		hDatamerged.Draw("esamex0")
        if blind: 
            hsig1merged.SetMinimum(0.1)#check?
            if doNormByBinWidth: 
                hsig1merged.GetYaxis().SetTitle("< Events / GeV >")
                if 'BDT' in iPlot and isSR(tag[3],tag[2]): hsig1merged.GetYaxis().SetTitle("< Events / 1.0 units >")
            elif isRebinned!='': hsig1merged.GetYaxis().SetTitle("Events / bin")
            else: hsig1merged.GetYaxis().SetTitle("Events / bin")
            formatUpperHist(hsig1merged)
	    formatUpperHist(hsig2merged)
            formatUpperHist(hsig3merged)
            formatUpperHist(hsig4merged)
            formatUpperHist(hsig5merged)
            formatUpperHist(hsig6merged)
            formatUpperHist(hsig7merged)
            formatUpperHist(hsig8merged)
            formatUpperHist(hsig9merged)
            formatUpperHist(hsig10merged)

            hsig1merged.SetMaximum(1.5*hDatamerged.GetMaximum()) #uncomment!
            hsig1merged.Draw("SAME HIST") #if doSig
	if doBkg: stackbkgHTmerged.Draw("SAME HIST")

	if drawYields: 
		rt.gStyle.SetPaintTextFormat("1.0f")
		bkgHTmerged.Draw("SAME TEXT90")

 	hsig1merged.Draw("SAME HIST")
	hsig2merged.Draw("SAME HIST")
	hsig3merged.Draw("SAME HIST")
	hsig4merged.Draw("SAME HIST")
	hsig5merged.Draw("SAME HIST")
	hsig6merged.Draw("SAME HIST")
	hsig7merged.Draw("SAME HIST")
	hsig8merged.Draw("SAME HIST")
	hsig9merged.Draw("SAME HIST")
	hsig10merged.Draw("SAME HIST")

	if not blind: 
		hDatamerged.Draw("esamex0") #redraw data so its not hidden
		if drawYields: hDatamerged.Draw("SAME TEXT00") 
	uPad.RedrawAxis()
	if doBkg: bkgHTgerrmerged.Draw("SAME E2")

	chLatexmerged = rt.TLatex()
	chLatexmerged.SetNDC()
	chLatexmerged.SetTextSize(0.05)
	if blind: chLatexmerged.SetTextSize(0.03)
	chLatexmerged.SetTextAlign(21) # align center
	flvString = 'e/#mu+jets'
	tagString = ''
	if tag[0]!='0p':
		if 'p' in tag[0]: tagString+='#geq'+tag[0][:-1]+' t, '
		else: tagString+=tag[0]+' t,  '
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
	chLatexmerged.DrawLatex(tagPosX, tagPosY, flvString)
	
        if isCategorized and iPlot != 'YLD':
		chLatexmerged.DrawLatex(tagPosX, tagPosY-0.06, tagString)
        if not isCategorized and iPlot != 'YLD' and region != 'CR':
		chLatexmerged.DrawLatex(tagPosX, tagPosY-0.06, tagString)#'BDT region')#tagString)
        if not isCategorized and iPlot != 'YLD' and region == 'CR':
                chLatexmerged.DrawLatex(tagPosX, tagPosY-0.06, 'CR')
	legmerged = rt.TLegend(legx1,legy1,legx2,legy2) #edit

	legmerged.SetShadowColor(0)
	legmerged.SetFillColor(0)
	legmerged.SetFillStyle(0)
	legmerged.SetLineColor(0)
	legmerged.SetLineStyle(0)
	legmerged.SetBorderSize(0) 
	legmerged.SetNColumns(2)

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
 	legmerged.AddEntry(hsig3merged,sig3leg+scaleFact3Str,"l")
 	legmerged.AddEntry(hsig4merged,sig4leg+scaleFact4Str,"l")
 	legmerged.AddEntry(hsig5merged,sig5leg+scaleFact5Str,"l")
 	legmerged.AddEntry(hsig6merged,sig6leg+scaleFact6Str,"l")
 	legmerged.AddEntry(hsig7merged,sig7leg,"l")
 	legmerged.AddEntry(hsig8merged,sig8leg,"l")
 	legmerged.AddEntry(hsig9merged,sig9leg,"l")
 	legmerged.AddEntry(hsig10merged,sig10leg,"l")

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
	
	if blind == False and not doRealPull:
		lPad.cd()
		pullmerged=hDatamerged.Clone("pullmerged")
		pullmerged.Divide(hDatamerged, bkgHTmerged)
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0 and hDatamerged.GetBinContent(binNo) > 0:
				pullmerged.SetBinError(binNo,hDatamerged.GetBinError(binNo)/bkgHTmerged.GetBinContent(binNo))
			else:
				pullmerged.SetBinError(binNo,0) 
		if iPlot=='YLD':
			pullmerged.SetMaximum(1.5)
			pullmerged.SetMinimum(0.1)
		else:
			pullmerged.SetMaximum(2)
			pullmerged.SetMinimum(0)
		pullmerged.SetFillColor(1)
		pullmerged.SetLineColor(1)
		formatLowerHist(pullmerged)
		pullmerged.Draw("E0")#"E1")
		
		BkgOverBkgmerged = pullmerged.Clone("bkgOverbkgmerged")
		BkgOverBkgmerged.Divide(bkgHTmerged, bkgHTmerged)
		pullUncBandTotmerged=rt.TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncTotmerged"))
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullUncBandTotmerged.SetPointEYhigh(binNo-1,totBkgTemp3['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandTotmerged.SetPointEYlow(binNo-1, totBkgTemp3['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
		if 'NBJets' in iPlot:
			pullUncBandTotmerged.SetPointEYhigh(4,0)
			pullUncBandTotmerged.SetPointEYlow(4,0)
		if not doOneBand: pullUncBandTotmerged.SetFillStyle(3002)
		else: pullUncBandTotmerged.SetFillStyle(3002)
		pullUncBandTotmerged.SetFillColor(14)
		pullUncBandTotmerged.SetLineColor(14)
		pullUncBandTotmerged.SetMarkerSize(0)
		rt.gStyle.SetHatchesLineWidth(1)
		pullUncBandTotmerged.Draw("SAME E2")
		
		pullUncBandNormmerged=rt.TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncNormmerged"))
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullUncBandNormmerged.SetPointEYhigh(binNo-1,totBkgTemp2['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandNormmerged.SetPointEYlow(binNo-1, totBkgTemp2['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
		pullUncBandNormmerged.SetFillStyle(3002)
		pullUncBandNormmerged.SetFillColor(2)
		pullUncBandNormmerged.SetLineColor(2)
		pullUncBandNormmerged.SetMarkerSize(0)
		rt.gStyle.SetHatchesLineWidth(1)
		if not doOneBand: pullUncBandNormmerged.Draw("SAME E2")
		
		pullUncBandStatmerged=rt.TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncStatmerged"))
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullUncBandStatmerged.SetPointEYhigh(binNo-1,totBkgTemp1['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandStatmerged.SetPointEYlow(binNo-1, totBkgTemp1['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
		pullUncBandStatmerged.SetFillStyle(3002)
		pullUncBandStatmerged.SetFillColor(3)
		pullUncBandStatmerged.SetLineColor(3)
		pullUncBandStatmerged.SetMarkerSize(0)
		rt.gStyle.SetHatchesLineWidth(1)
		if not doOneBand: pullUncBandStatmerged.Draw("SAME E2")

		pullLegendmerged=rt.TLegend(0.14,0.87,0.85,0.96)
		rt.SetOwnership( pullLegendmerged, 0 )   # 0 = release (not keep), 1 = keep
		pullLegendmerged.SetShadowColor(0)
		pullLegendmerged.SetNColumns(2)
		pullLegendmerged.SetFillColor(0)
		pullLegendmerged.SetFillStyle(0)
		pullLegendmerged.SetLineColor(0)
		pullLegendmerged.SetLineStyle(0)
		pullLegendmerged.SetBorderSize(0)
		if not doOneBand: 
			pullLegendmerged.AddEntry(pullUncBandStat , "Bkg uncert. (shape syst.)" , "f")
			pullLegendmerged.AddEntry(pullUncBandNorm , "Bkg uncert. (shape #oplus norm. syst.)" , "f")
			pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus all syst.)" , "f")
		elif not doAllSys: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus norm.)" , "f")
		else: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus syst.)" , "f")
		pullmerged.Draw("SAME E0")
		lPad.RedrawAxis()

	if blind == False and doRealPull:
		lPad.cd()
		pullmerged=hDatamerged.Clone("pullmerged")
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if hDatamerged.GetBinContent(binNo)!=0:
				MCerror = 0.5*(totBkgTemp3['isL'+tagStr].GetErrorYhigh(binNo-1)+totBkgTemp3['isL'+tagStr].GetErrorYlow(binNo-1))
				pullmerged.SetBinContent(binNo,(hDatamerged.GetBinContent(binNo)-bkgHTmerged.GetBinContent(binNo))/math.sqrt(MCerror**2+hDatamerged.GetBinError(binNo)**2))
			else: pullmerged.SetBinContent(binNo,0.)
		pullmerged.SetMaximum(3)
		pullmerged.SetMinimum(-3)
		pullmerged.SetFillColor(kGray+2)
		pullmerged.SetLineColor(kGray+2)
		formatLowerHist(pullmerged)
		pullmerged.GetYaxis().SetTitle('Pull')
		pullmerged.Draw("HIST")

	savePrefixmerged = templateDir+'/plots/'
	if not os.path.exists(savePrefixmerged): os.system('mkdir '+savePrefixmerged)
	savePrefixmerged+=histPrefixE.replace('isE','isL')+isRebinned.replace('_rebinned_stat1p1','')+saveKey
	if nttaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nT0p_','')
	if nWtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nW0p_','')
	if nbtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nB0p_','')
	if njetslist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nJ0p_','')
	if doRealPull: savePrefixmerged+='_pull'
	if doNormByBinWidth: savePrefixmerged+='_NBBW'
	if yLog: savePrefixmerged+='_logy'
	if blind or blindYLD: savePrefixmerged+='_blind'

	if doOneBand: 
		c1merged.SaveAs(savePrefixmerged+"totBand_sig_MH"+massPtH+".pdf")
		c1merged.SaveAs(savePrefixmerged+"totBand_sig"+massPtH+".png")
	else: 
		c1merged.SaveAs(savePrefixmerged+"_sig"+massPtH+".pdf")
		c1merged.SaveAs(savePrefixmerged+"_sig"+massPtH+".png")
	for proc in bkgProcList:
		try: del bkghistsmerged[proc+'isL'+tagStr]
		except: pass
RFile1.Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))




