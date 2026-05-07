#!/usr/bin/python


import os,sys,time,math,pickle,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as rt
from weights_UL16 import *
from modSyst import *
from utils import *
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)
start_time = time.time()

lumi=str(targetlumi/1000).replace('.','p') #for plots
lumiInTemplates= str(targetlumi/1000).replace('.','p') # 1/fb
blind = True
iPlot='XGB1300_SR1'
if len(sys.argv)>1: 
	templateDir=os.getcwd()+'/'+str(sys.argv[1])+'/'
else:
    templateDir=os.getcwd()+'/kinematics_R16_final_SR_2025_6_24/'#limits_kinematics_R17_final_SR_2024_4_5/'#'/templates_R18_SR_2024_2_13/'

sys = 'lowessmuR'
process = 'X53RHM1200'
bkgProcList = [process,process+'__'+sys+'Up',process+'__'+sys+'Down']

isRebinned= '_wNegBinsCorrec__rebinned_stat0p2'

totBkgTemp3 = {}

tempsig='templates_'+iPlot+'_'+lumiInTemplates+'fb'+isRebinned+'.root'

bkgHistColors = {bkgProcList[0]:rt.kBlack, bkgProcList[1]:rt.kRed, bkgProcList[2]:rt.kBlue} #HTB

systematicList = [
'muR','muF']#''pileup','muRFcorrd','muR','muF','toppt','jec','jer','ht','LF','LFstat1', 'LFstat2','HF','HFstat1','HFstat2','CFerr1','CFerr2', 'DJjes',
#'PNT',
#'PNW',
#]

doAllSys = True
doQ2sys  = False
if not doAllSys: doQ2sys = False
blind =True
blindYLD = False
yLog  = True
drawYields = False

isEMlist =['E','M']
nttaglist = ['0p']
nWtaglist = ['0p']
nbtaglist = ['1p']
njetslist = ['4p']

tagList = list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))
lumiSys = 0.023 # lumi uncertainty
trigSys = 0.#05 # trigger uncertainty
lepIdSys = 0.03 # lepton id uncertainty
lepIsoSys = 0.01 # lepton isolation uncertainty
corrdSys = math.sqrt(lumiSys**2+trigSys**2+lepIdSys**2+lepIsoSys**2) #cheating while total e/m values are close


for tag in tagList:
	tagStr='nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]
	modTag = tagStr[tagStr.find('nT'):tagStr.find('nJ')-3]
	modelingSys['data_'+modTag] = 0.
	for proc in bkgProcList:
		if proc in ['ttbar','ttbb','tt1b','ttcc','ttjj','tt2b']: 
			modelingSys[proc+'_'+modTag] = math.sqrt(0.042**2+0.027**2)
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

	histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.01) #check?
	if not yLog: 
		histogram.SetMaximum(1.02*histogram.GetMaximum())
	if yLog:
		uPad.SetLogy()
		histogram.SetMaximum(200*histogram.GetMaximum())
def formatLowerHist(histogram):
	histogram.GetXaxis().SetLabelSize(.12)
	histogram.GetXaxis().SetTitleSize(0.15)
	histogram.GetXaxis().SetTitleOffset(0.95)
	histogram.GetXaxis().SetNdivisions(506)

	histogram.GetYaxis().SetLabelSize(0.065)
	histogram.GetYaxis().SetTitleSize(0.14)
	histogram.GetYaxis().SetTitleOffset(.37)
	histogram.GetYaxis().SetTitle('Ratio')
	histogram.GetYaxis().SetNdivisions(5)
	histogram.GetYaxis().SetRangeUser(0.01,2.99)
	histogram.GetYaxis().CenterTitle()


		
legx1 = 0.4#0.55
legx2 = legx1+0.50

legy1 = 0.7#0.5
legy2 = legy1+0.37

tagPosX = 0.76
tagPosY = 0.52

RFile1 = rt.TFile(templateDir+tempsig)
print(RFile1)
tdrstyle.setTDRStyle()

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

iPeriod = 4

T = 0.10*H_ref
B = 0.35*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref

bkghists = {}
bkghistsmerged = {}
bkghists2 = {}
systHists = {}

dataName = 'data_obs'
blindGlob = blind

for tag in tagList:
	tagStr='nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]

	postTag = 'isSR_' 
	legx1 = 0.6#30
	legy1 = 0.75#65

	legx2 = legx1+0.45
	legy2 = legy1+0.15

 	tagPosX = 0.25#0.76
 	tagPosY = 0.65#0.52

	sig1Color= rt.kRed
	sig2Color= rt.kBlack
	sig3Color= rt.kBlue

	modTag = tagStr[tagStr.find('nT'):tagStr.find('nJ')-3]
	# Making plots for e+jets/mu+jets combined #
	histPrefixE = iPlot+'_'+lumiInTemplates+'fb_'+postTag+'isE_'+tagStr
	histPrefixM = iPlot+'_'+lumiInTemplates+'fb_'+postTag+'isM_'+tagStr


	for proc in bkgProcList:
		#hsig1merged = RFile1.Get(histPrefixE+'__'+proc+'__'+sys+Tag)
		#hsig1merged.Add(RFile1.Get(histPrefixM+'__'+proc+'__'+sys+Tag))
		bkghistsmerged[proc+'isL'+tagStr] = RFile1.Get(histPrefixE+'__'+proc)
		bkghistsmerged[proc+'isL'+tagStr].Add(RFile1.Get(histPrefixM+'__'+proc))

		sig1leg=proc+sys+'Up' 
		sig2leg=proc+'no sys'
                sig3leg=proc+sys+'Down'

        bkgHTmerged = bkghistsmerged[bkgProcList[0]+'isL'+tagStr].Clone()
        for proc in bkgProcList:
                if proc==bkgProcList[0]: continue
                bkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
                	

	yDiv=0.35

	totBkgTemp3['isL'+tagStr] = rt.TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'All'))

	for ibin in range(1,bkgHTmerged.GetNbinsX()+1):
		errorStatOnly = bkgHTmerged.GetBinError(ibin)**2
		totBkgTemp3['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorStatOnly))
		totBkgTemp3['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorStatOnly))

	bkgHTgerrmerged = totBkgTemp3['isL'+tagStr].Clone()
	for proc in bkgProcList:
		try: 
			bkgHTmerged.SetLineColor(bkgHistColors[proc])
			bkgHTmerged.SetFillStyle(0)
			bkgHTmerged.SetLineWidth(3)
		except: pass

	stackbkgHTmerged = rt.THStack("stackbkgHTmerged","")
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

	uPad.cd()
        for proc in bkgProcList:
                #try:
                bkghistsmerged[proc+'isL'+tagStr].SetLineColor(bkgHistColors[proc])
                bkghistsmerged[proc+'isL'+tagStr].SetFillStyle(0)
                bkghistsmerged[proc+'isL'+tagStr].SetLineWidth(3)
                #except: pass

	for proc in bkgProcList:
		 stackbkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])


	stackbkgHTmerged.SetTitle("")

	formatUpperHist(bkghistsmerged[bkgProcList[0]+'isL'+tagStr])

	#hsig1merged.SetMaximum(1.1*hsig1merged.GetMaximum())
	bkghistsmerged[bkgProcList[0]+'isL'+tagStr].Draw("HIST") #if doSig
	bkghistsmerged[bkgProcList[1]+'isL'+tagStr].Draw("SAME HIST") #if doSig
	bkghistsmerged[bkgProcList[2]+'isL'+tagStr].Draw("SAME HIST") #if doSig
	#stackbkgHTmerged.Draw("HIST")

	uPad.RedrawAxis()
	#bkgHTgerrmerged.Draw("SAME E2")

	legmerged = rt.TLegend(legx1,legy1,legx2,legy2) #edit
	legmerged.SetShadowColor(0)
	legmerged.SetFillColor(0)
	legmerged.SetFillStyle(0)
	legmerged.SetLineColor(0)
	legmerged.SetLineStyle(0)
	legmerged.SetBorderSize(0) 
	legmerged.SetNColumns(1)

	#legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")
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
        for tag in ["Up","Down"]:
            try: legmerged.AddEntry(bkghistsmerged['ttcc'+'__'+sys+tag+'isL'+tagStr],"t#bar{t}+c#bar{c}"+" "+sys+" "+tag,"f")
            except: pass
            try: legmerged.AddEntry(bkghistsmerged['ttb'+'__'+sys+tag+'isL'+tagStr],"t#bar{t}+b"+" "+sys+" "+tag,"f")
            except: pass
            try: legmerged.AddEntry(bkghistsmerged['top'+'__'+sys+tag+'isL'+tagStr],"TOP"+" "+sys+" "+tag,"f")
            except: pass
            try: legmerged.AddEntry(bkghistsmerged['tt2b'+'__'+sys+tag+'isL'+tagStr],"t#bar{t}+2b"+" "+sys+" "+tag,"f")
            except: pass
            try: legmerged.AddEntry(bkghistsmerged['ewk'+'__'+sys+tag+'isL'+tagStr],"EWK"+" "+sys+" "+tag,"f")
            except: pass
            try: legmerged.AddEntry(bkghistsmerged['ttbb'+'__'+sys+tag+'isL'+tagStr],"t#bar{t}+b#bar{b}"+" "+sys+" "+tag,"f")
            except: pass
            try: legmerged.AddEntry(bkghistsmerged['qcd'+'__'+sys+tag+'isL'+tagStr],"QCD"+" "+sys+" "+tag,"f")
            except: pass
            try: legmerged.AddEntry(bkghistsmerged['ttnobb'+'__'+sys+tag+'isL'+tagStr],"t#bar{t}+!b#bar{b}"+" "+sys+" "+tag,"f")
            except: pass


	#legmerged.AddEntry(bkgHTgerrmerged,"Bkg uncert","f")

	legmerged.Draw("same")

	#draw the lumi text on the canvas
	CMS_lumi.CMS_lumi(uPad, iPeriod, iPos)
	
	uPad.Update()
	uPad.RedrawAxis()
	frame = uPad.GetFrame()
	uPad.Draw()

	lPad.cd()
	pullmerged=bkghistsmerged[bkgProcList[0]+'isL'+tagStr].Clone("pullmerged")
	pullmerged.Divide(bkghistsmerged[bkgProcList[1]+'isL'+tagStr], bkghistsmerged[bkgProcList[0]+'isL'+tagStr])
	for binNo in range(0,bkghistsmerged[bkgProcList[0]+'isL'+tagStr].GetNbinsX()+2):
		if bkghistsmerged[bkgProcList[1]+'isL'+tagStr].GetBinContent(binNo)!=0 and bkghistsmerged[bkgProcList[0]+'isL'+tagStr].GetBinContent(binNo) > 0:
			pullmerged.SetBinError(binNo,bkghistsmerged[bkgProcList[1]+'isL'+tagStr].GetBinError(binNo)/bkghistsmerged[bkgProcList[0]+'isL'+tagStr].GetBinContent(binNo))
		else:
			pullmerged.SetBinError(binNo,0) 
		pullmerged.SetMaximum(2)
		pullmerged.SetMinimum(0)
		pullmerged.SetFillColor(2)
		pullmerged.SetLineColor(2)
		formatLowerHist(pullmerged)

	pullmerged2=bkghistsmerged[bkgProcList[0]+'isL'+tagStr].Clone("pullmerged2")
	pullmerged2.Divide(bkghistsmerged[bkgProcList[2]+'isL'+tagStr], bkghistsmerged[bkgProcList[0]+'isL'+tagStr])
	for binNo in range(0,bkghistsmerged[bkgProcList[0]+'isL'+tagStr].GetNbinsX()+2):
		if bkghistsmerged[bkgProcList[2]+'isL'+tagStr].GetBinContent(binNo)!=0 and bkghistsmerged[bkgProcList[0]+'isL'+tagStr].GetBinContent(binNo) > 0:
			pullmerged2.SetBinError(binNo,bkghistsmerged[bkgProcList[2]+'isL'+tagStr].GetBinError(binNo)/bkghistsmerged[bkgProcList[0]+'isL'+tagStr].GetBinContent(binNo))
		else:
			pullmerged2.SetBinError(binNo,0) 
		pullmerged2.SetMaximum(2)
		pullmerged2.SetMinimum(0)
		pullmerged2.SetFillColor(4)
		pullmerged2.SetLineColor(4)
		formatLowerHist(pullmerged2)

		pullmerged.Draw("E0")#"E1")
		pullmerged2.Draw("SAME E0")#"E1")
		
	BkgOverBkgmerged = pullmerged.Clone("bkgOverbkgmerged")
	BkgOverBkgmerged.Divide(bkgHTmerged,bkgHTmerged)

	pullUncBandStatmerged=rt.TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncStatmerged"))
	for binNo in range(0,bkghistsmerged[bkgProcList[0]+'isL'+tagStr].GetNbinsX()+2):
		if bkgHTmerged.GetBinContent(binNo)!=0:
			pullUncBandStatmerged.SetPointEYhigh(binNo-1,totBkgTemp3['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
			pullUncBandStatmerged.SetPointEYlow(binNo-1, totBkgTemp3['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
	pullUncBandStatmerged.SetFillStyle(3002)
	pullUncBandStatmerged.SetFillColor(2)
	pullUncBandStatmerged.SetLineColor(2)
	pullUncBandStatmerged.SetMarkerSize(0)
	rt.gStyle.SetHatchesLineWidth(1)
	pullUncBandStatmerged.Draw("SAME E2")

	pullLegendmerged=rt.TLegend(0.14,0.87,0.85,0.96)
	rt.SetOwnership( pullLegendmerged, 0 )   # 0 = release (not keep), 1 = keep
	pullLegendmerged.SetShadowColor(0)
	pullLegendmerged.SetNColumns(2)
	pullLegendmerged.SetFillColor(0)
	pullLegendmerged.SetFillStyle(0)
	pullLegendmerged.SetLineColor(0)
	pullLegendmerged.SetLineStyle(0)
	pullLegendmerged.SetBorderSize(0)
	pullLegendmerged.AddEntry(pullUncBandStatmerged , "Bkg uncert. (stat.)" , "f")
	pullLegendmerged.Draw("SAME")
	pullmerged.Draw("SAME E0")
	lPad.RedrawAxis()

	
	savePrefixmerged = templateDir+'/plots/'
	if not os.path.exists(savePrefixmerged): os.system('mkdir '+savePrefixmerged)
	savePrefixmerged+=histPrefixE.replace('isE','isL')+isRebinned.replace('_rebinned_stat1p1','')
	if nttaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nT0p_','')
	if nWtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nW0p_','')
	if nbtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nB0p_','')
	if njetslist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nJ0p_','')
	
	if yLog: savePrefixmerged+='_logy'
	if blind or blindYLD: savePrefixmerged+='_blind'

	c1merged.SaveAs(savePrefixmerged+sys+process+".pdf")
	c1merged.SaveAs(savePrefixmerged+sys+process+".png")
	#for proc in bkgProcList:
	#	try: del bkghistsmerged[proc+'isL'+tagStr]
	#	except: pass
				
RFile1.Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))
