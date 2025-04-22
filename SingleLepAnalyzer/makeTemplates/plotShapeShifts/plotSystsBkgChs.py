#!/usr/bin/python

import os,sys,math,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as rt
from array import array
from utils import *
import CMS_lumi, tdrstyle
import argparse


parser = argparse.ArgumentParser(description = "The script to plot shape shifts due to systematic uncertainties")
parser.add_argument("-d", "--directory", help="the directory to be processed")
parser.add_argument("-i", "--iplot", default="XGB200_SR1",  help="The variable to be processed")
parser.add_argument("-l", "--lowess", default=False, action="store_true", help="use the lowess algorithm for shape smoothing")
parser.add_argument("-y", "--year", help="")

args = parser.parse_args()

#set the tdr style
tdrstyle.setTDRStyle()
rt.gROOT.SetBatch(1)

outDir = os.getcwd()+'/'
iPlot = args.iplot
region = 'SR'
isCategorized = False
era=args.year
if era=='R16': 
	lumiStr = '16p81fb'
	lumi = 16.81
elif era=='R16APV': 
	lumiStr = '19p52fb'
	lumi = 19.5
elif era=='R17': 
	lumiStr = '41p48fb'
	lumi = 41.5
elif era=='R18': 
	lumiStr = '59p83fb'
	lumi = 59.83
sig1 = 'X53RHM1200' #  choose the 1st signal to plot
isRebinned = '_rebinned_stat0p2'
isNegCorr = '_wNegBinsCorrec_'
if args.lowess:
    islowess = 'lowess'
else: 
    islowess = ''
useCombine = True
tempVersion = args.directory#'templates_M500_2021_4_25_topPtRW_allweights_UL17_Reshape_ReNorm2D_HTnj_WJetsHTbinned_HTonly' 
cutString = ''
saveDir = 'bkgIndChannels'
if useCombine: templateFile = '../'+tempVersion+'/'+cutString+'/templates_'+iPlot+'_'+lumiStr+isNegCorr+isRebinned+'.root'
else: templateFile = '../'+tempVersion+'/'+cutString+'/templates_'+iPlot+'_'+sig1+'_'+lumiStr+isRebinned+'.root'
if not os.path.exists(outDir+tempVersion): os.system('mkdir '+outDir+tempVersion)
if not os.path.exists(outDir+tempVersion+'/'+saveDir): os.system('mkdir '+outDir+tempVersion+'/'+saveDir)

bkgTTBarList = ['ttnobb', 'ttbb']#jj','ttcc','ttbb','tt2b', 'tt1b']
bkgList = bkgTTBarList+['top','ewk','qcd'] #some uncertainties will be skipped depending on the bkgList[0] process!!!!

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

systematics = ['pdf']#'jetpileup','isr','fsr','pileup','muRF','muR','muF','toppt','jec','jer','ht','LF','LFstat1', 'LFstat2','HF','HFstat1','HFstat2','CFerr1','CFerr2', 'DJjes','PNT','PNW'] 


#systematics = ['pileup','muRFcorrd','muR','muF','toppt','jec','jer','ht','LF','LFstat1', 'LFstat2','HF','HFstat1','HFstat2','CFerr1','CFerr2', 'DJjes']#['pileup','prefire','btag','mistag','jec','jer','hotstat','hotcspur','hotclosure','PSwgt','muRF','pdf','hdamp','ue','njet']#,'ht','trigeff','toppt','tau32','jmst','jmrt','tau21','jmsW','jmrW','tau21pt'] #
nSys = len(systematics)
for isys in range(nSys):
    systematics[isys] = islowess+systematics[isys] 

#tagList = list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist))
catList = ['is'+item[0]+'_nT'+item[1]+'_nW'+item[2]+'_nB'+item[3]+'_nJ'+item[4] for item in list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist))]
print catList
RFile = rt.TFile(templateFile)
print templateFile
if useCombine:
	upTag = 'Up'
	downTag = 'Down'
else: #theta
	upTag = '__plus'
	downTag = '__minus'

for syst in systematics:
	if not os.path.exists(outDir+tempVersion+'/'+saveDir+'/'+syst): os.system('mkdir '+outDir+tempVersion+'/'+saveDir+'/'+syst)
	if not os.path.exists(outDir+tempVersion+'/'+saveDir+'/'+syst+'/'+iPlot): os.system('mkdir '+outDir+tempVersion+'/'+saveDir+'/'+syst+'/'+iPlot)

	for cat in catList:
                postTag = 'is'+region 
		Prefix = iPlot+'_'+lumiStr+'_'+postTag+'_'+cat+'__'+bkgList[0]
		print Prefix+'__'+syst
		try: hNm = RFile.Get(Prefix).Clone()
		except: 
			print bkgList[0]+" NOT FOUND for category "+cat
			continue
		try:
			hUp = RFile.Get(Prefix+'__'+syst+upTag).Clone()
			hDn = RFile.Get(Prefix+'__'+syst+downTag).Clone()
		except:
			print "No shape for",bkgList[0],cat,syst
			hUp = RFile.Get(Prefix).Clone()
			hDn = RFile.Get(Prefix).Clone()
		for bkg in bkgList:
			if bkg==bkgList[0]: continue
			try: 
				htemp = RFile.Get(Prefix.replace(bkgList[0],bkg)).Clone()
				hNm.Add(htemp)
			except: 
				print "No nominal for",bkg,cat,syst
				pass
			try:
				htempUp = RFile.Get(Prefix.replace(bkgList[0],bkg)+'__'+syst+upTag).Clone()
				hUp.Add(htempUp)
			except:
				print "No shape for",bkg,cat,syst
				try:
					htempUp = RFile.Get(Prefix.replace(bkgList[0],bkg)).Clone()
					hUp.Add(htempUp)
				except: 
					print "No nominal for",bkg,cat,syst
					pass
			
			try:
				htempDown = RFile.Get(Prefix.replace(bkgList[0],bkg)+'__'+syst+downTag).Clone()
				hDn.Add(htempDown)
			except:
				print "No shape for",bkg,cat,syst
				try:
					htempDown = RFile.Get(Prefix.replace(bkgList[0],bkg)).Clone()
					hDn.Add(htempDown)
				except: 
					print "No nominal for",bkg,cat,syst
					pass

		hNm.Draw()
		hUp.Draw()
		hDn.Draw()

		canv = rt.TCanvas(Prefix+'__'+syst,Prefix+'__'+syst,1000,700)
		yDiv = 0.35
		uPad=rt.TPad('uPad','',0,yDiv,1,1)
		uPad.SetTopMargin(0.07)
		uPad.SetBottomMargin(0)
		uPad.SetRightMargin(.05)
		uPad.SetLeftMargin(.18)
		uPad.SetLogy()
		uPad.Draw()

		lPad=rt.TPad("lPad","",0,0,1,yDiv) #for sigma runner
		lPad.SetTopMargin(0)
		lPad.SetBottomMargin(.4)
		lPad.SetRightMargin(.05)
		lPad.SetLeftMargin(.18)
		lPad.SetGridy()
		lPad.Draw()

		uPad.cd()

		rt.gStyle.SetOptTitle(0)

		#canv.SetLogy()
		hNm.SetFillColor(rt.kWhite)
		hUp.SetFillColor(rt.kWhite)
		hDn.SetFillColor(rt.kWhite)
		hNm.SetMarkerColor(rt.kBlack)
		hUp.SetMarkerColor(rt.kRed)
		hDn.SetMarkerColor(rt.kBlue)
		hNm.SetLineColor(rt.kBlack)
		hUp.SetLineColor(rt.kRed)
		hDn.SetLineColor(rt.kBlue)
		hNm.SetLineWidth(2)
		hNm.SetLineStyle(1)
		hUp.SetLineWidth(2)
		hUp.SetLineStyle(1)
		hDn.SetLineWidth(2)
		hDn.SetLineStyle(1)
		hNm.SetMarkerSize(.05)
		hUp.SetMarkerSize(.05)
		hDn.SetMarkerSize(.05)

		hUp.GetYaxis().SetTitle('Events')
		hUp.GetYaxis().SetLabelSize(0.10)
		hUp.GetYaxis().SetTitleSize(0.1)
		hUp.GetYaxis().SetTitleOffset(.6)

		#hUp.SetMaximum(1.1*max(hUp.GetMaximum(),hNm.GetMaximum(),hDn.GetMaximum()))
		hUp.GetYaxis().SetRangeUser(0.0001,1.1*max(hUp.GetMaximum(),hNm.GetMaximum(),hDn.GetMaximum()))

# 		hUp.Draw()
# 		hNm.Draw('same')
# 		hDn.Draw('same')
		hUp.Draw('hist')
		hNm.Draw('samehist')
		hDn.Draw('samehist')
		#uPad.RedrawAxis()

		lPad.cd()
		rt.gStyle.SetOptTitle(0)
		pullUp = hUp.Clone()
		for iBin in range(0,pullUp.GetXaxis().GetNbins()+2):
			pullUp.SetBinContent(iBin,pullUp.GetBinContent(iBin)-hNm.GetBinContent(iBin))
			pullUp.SetBinError(iBin,math.sqrt(pullUp.GetBinError(iBin)**2+hNm.GetBinError(iBin)**2))
		pullUp.Divide(hNm)
		pullUp.SetTitle('')
		pullUp.SetFillColor(rt.kWhite)
		pullUp.SetLineColor(rt.kRed)

		#pullUp.GetXaxis().SetTitle(histName)
		pullUp.GetXaxis().SetLabelSize(.15)
		pullUp.GetXaxis().SetTitleSize(0.18)
		pullUp.GetXaxis().SetTitleOffset(0.95)

		pullUp.GetYaxis().SetTitle('#frac{Up/Down-Nom}{Nom}')#'Python-C++'
		pullUp.GetYaxis().CenterTitle(1)
		pullUp.GetYaxis().SetLabelSize(0.125)
		pullUp.GetYaxis().SetTitleSize(0.1)
		pullUp.GetYaxis().SetTitleOffset(.55)
		pullUp.GetYaxis().SetNdivisions(506)
		#pullUp.SetMinimum(pullDown.GetMinimum())
		#pullUp.SetMaximum(pullUp.GetMaximum())

		pullDown = hDn.Clone()
		for iBin in range(0,pullDown.GetXaxis().GetNbins()+2):
			pullDown.SetBinContent(iBin,pullDown.GetBinContent(iBin)-hNm.GetBinContent(iBin))
			pullDown.SetBinError(iBin,math.sqrt(pullDown.GetBinError(iBin)**2+hNm.GetBinError(iBin)**2))
		pullDown.Divide(hNm)
		pullDown.SetTitle('')
		pullDown.SetFillColor(rt.kWhite)
		pullDown.SetLineColor(rt.kBlue)

		#pullDown.GetXaxis().SetTitle(histName)
		pullDown.GetXaxis().SetLabelSize(.15)
		pullDown.GetXaxis().SetTitleSize(0.18)
		pullDown.GetXaxis().SetTitleOffset(0.95)

		pullDown.GetYaxis().SetTitle('#frac{Up/Down-Nom}{Nom}')#'Python-C++'
		pullDown.GetYaxis().CenterTitle(1)
		pullDown.GetYaxis().SetLabelSize(0.125)
		pullDown.GetYaxis().SetTitleSize(0.1)
		pullDown.GetYaxis().SetTitleOffset(.55)
		pullDown.GetYaxis().SetNdivisions(506)
		pullUp.SetMinimum(-0.6)#min(pullDown.GetMinimum(),pullUp.GetMinimum()))
		pullUp.SetMaximum(0.6)#max(pullDown.GetMaximum(),pullUp.GetMaximum()))
		#pullDown.SetMinimum(pullDown.GetMinimum())
		#pullDown.SetMaximum(pullDown.GetMaximum())
# 		pullUp.Draw()
# 		pullDown.Draw('same')
		pullUp.Draw('hist')
		pullDown.Draw('samehist')
		lPad.RedrawAxis()

		uPad.cd()

		legend = rt.TLegend(0.6,0.65,0.9,0.90)
		legend.SetShadowColor(0);
		legend.SetFillColor(0);
		legend.SetLineColor(0);
		legend.AddEntry(hNm,'Nominal','l')

		legend.AddEntry(hUp,syst.replace('pileup','PU').replace('prefire','Prefire').replace('btag','b tag').replace('mistag','udsg mistag').replace('jec','JEC').replace('jer','JER').replace('hotstat','res-t stat').replace('hotcspur','res-t CSpurity').replace('hotclosure','res-t closure').replace('PSwgt','PS weight').replace('pdf','PDF').replace('hdamp','hDamp').replace('ue','UE').replace('njet','Njet').replace('tau21','#tau_{2}/#tau_{1}').replace('toppt','top p_{T}').replace('q2','Q^{2}').replace('jmr','JMR').replace('jms','JMS').replace('tau21pt','#tau_{2}/#tau_{1} p_{T}').replace('tau21','#tau_{2}/#tau_{1}').replace('tau32','#tau_{3}/#tau_{2}')+' Up','l')
		legend.AddEntry(hDn,syst.replace('pileup','PU').replace('prefire','Prefire').replace('btag','b tag').replace('mistag','udsg mistag').replace('jec','JEC').replace('jer','JER').replace('hotstat','res-t stat').replace('hotcspur','res-t CSpurity').replace('hotclosure','res-t closure').replace('PSwgt','PS weight').replace('pdf','PDF').replace('hdamp','hDamp').replace('ue','UE').replace('njet','Njet').replace('tau21','#tau_{2}/#tau_{1}').replace('toppt','top p_{T}').replace('q2','Q^{2}').replace('jmr','JMR').replace('jms','JMS').replace('tau21pt','#tau_{2}/#tau_{1} p_{T}').replace('tau21','#tau_{2}/#tau_{1}').replace('tau32','#tau_{3}/#tau_{2}')+' Down','l')
		legend.Draw('same')

		prelimTex=rt.TLatex()
		prelimTex.SetNDC()
		prelimTex.SetTextAlign(31) # align right
		prelimTex.SetTextFont(42)
		prelimTex.SetTextSize(0.05)
		prelimTex.SetLineWidth(2)
		prelimTex.DrawLatex(0.90,0.943,str(lumi)+" fb^{-1} (13 TeV)")

		prelimTex2=rt.TLatex()
		prelimTex2.SetNDC()
		prelimTex2.SetTextFont(61)
		prelimTex2.SetLineWidth(2)
		prelimTex2.SetTextSize(0.07)
		prelimTex2.DrawLatex(0.18,0.9364,"CMS")

		prelimTex3=rt.TLatex()
		prelimTex3.SetNDC()
		prelimTex3.SetTextAlign(13)
		prelimTex3.SetTextFont(52)
		prelimTex3.SetTextSize(0.040)
		prelimTex3.SetLineWidth(2)
		prelimTex3.DrawLatex(0.25175,0.9664,"Preliminary")

		chLatex = rt.TLatex()
		chLatex.SetNDC()
		chLatex.SetTextSize(0.05)
		chLatex.SetTextAlign(21)
		flv = cat.split('_')[0]
		#hottag = cat.split('_')[1]
		ttag = cat.split('_')[1]
		wtag = cat.split('_')[2]
		btag = cat.split('_')[3]
		njet = cat.split('_')[4]
		flvString = ''
		tagString = ''
		tagString2 = ''
		if flv=='isE': flvString+='e+jets'
		if flv=='isM': flvString+='#mu+jets'
		#if hottag!='0p': 
		#	if 'p' in hottag: tagString2+='#geq'+hottag[4:-1]+' resolved t'
		#	else: tagString2+=hottag[4:]+' resolved t'
		if ttag!='0p': 
			if 'p' in ttag: tagString+='#geq'+ttag[2:-1]+' t, '
			else: tagString+=ttag[2:]+' t, '
		if wtag!='0p': 
			if 'p' in wtag: tagString+='#geq'+wtag[2:-1]+' W, '
			else: tagString+=wtag[2:]+' W, '
		if btag!='0p': 
			if 'p' in btag: tagString+='#geq'+btag[2:-1]+' b, '
			else: tagString+=btag[2:]+' b, '
		if njet!='0p': 
			if 'p' in njet: tagString+='#geq'+njet[2:-1]+' j'
			else: tagString+=njet[2:]+' j'
		if tagString.endswith(', '): tagString = tagString[:-2]
		chLatex.DrawLatex(0.45, 0.84, flvString)
		chLatex.DrawLatex(0.45, 0.78, tagString)
		chLatex.DrawLatex(0.45, 0.72, tagString2)

		canv.SaveAs(tempVersion+'/'+saveDir+'/'+syst+'/'+iPlot+'/'+syst+'_'+cat+'UL'+era+'.pdf')
		canv.SaveAs(tempVersion+'/'+saveDir+'/'+syst+'/'+iPlot+'/'+syst+'_'+cat+'UL'+era+'.png')
		#canv.SaveAs(tempVersion+'/'+saveDir+'/'+syst+'/'+syst+'_'+cat+'.eps')
RFile.Close()
