
import os,sys,time,math,pickle,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as rt
from weights_UL18 import *
from modSyst import *
from utils import *
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)
start_time = time.time()

lumi=str(targetlumi/1000).replace('.','p') #for plots
lumiInTemplates= str(targetlumi/1000).replace('.','p') # 1/fb

sig1leg='t#bar{t}+!b#bar{b} with weight' 

sig2leg='t#bar{t}+!b#bar{b} with no weight'

RFile1 = rt.TFile("kinematics_R18_NPV/templates_NPV_59p83fb_wNegBinsCorrec_.root")#kinematics_R17_SR_2024_3_24/templates_XGB1300_SR1_41p48fb_wNegBinsCorrec_.root")

RFile2 = rt.TFile("kinematics_R18_nowgt_PS_2024_6_6/templates_NPV_59p83fb_wNegBinsCorrec_.root")#kinematics_R17_sinancuts_CR_2024_3_26/templates_XGB1300_SR1_41p48fb_wNegBinsCorrec_.root")

hsig1merged = RFile1.Get('NPV_'+lumiInTemplates+'fb_'+'isE_'+'nT0p_nW0p_nB1p_nJ3p'+'__ttnobb').Clone()
hsig2merged = RFile2.Get('NPV_'+lumiInTemplates+'fb_'+'isE_'+'nT0p_nW0p_nB1p_nJ3p'+'__ttnobb').Clone()
hsig1merged.Add(RFile1.Get('NPV_'+lumiInTemplates+'fb_'+'isM_'+'nT0p_nW0p_nB1p_nJ3p'+'__ttnobb').Clone())
hsig2merged.Add(RFile2.Get('NPV_'+lumiInTemplates+'fb_'+'isM_'+'nT0p_nW0p_nB1p_nJ3p'+'__ttnobb').Clone())
 
c1merged = rt.TCanvas("c1merged","c1merged",50,50,800,800)
c1merged.SetFillColor(0)
c1merged.SetBorderMode(0)
c1merged.SetFrameFillStyle(0)
c1merged.SetFrameBorderMode(0)
c1merged.SetTickx(0)
c1merged.SetTicky(0)
	
#hsig1merged = RFile1.Get('XGB1300_SR1_'+lumiInTemplates+'fb_'+'isE_'+'nT0p_nW0p_nB1p_nJ4p'+'__ttnobb')
#hsig2merged = RFile2.Get('XGB1300_SR1_'+lumiInTemplates+'fb_'+'isE_'+'nT0p_nW0p_nB1p_nJ4p'+'__ttnobb')
uPad=rt.TPad("uPad","",0,0.,1,1) #for actual plots
T = 0.10*800
B = 0.12*800
L = 0.12*800
R = 0.04*800
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

CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.lumi_13TeV= str(targetlumi/1000)+" fb^{-1}"#"59.83 fb^{-1}"#"41.5 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"#"Preliminary"#Work in Progress"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)


tagPosX = 0.76
tagPosY = 0.52
iPeriod = 4
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
	
uPad.SetLeftMargin( L/800 )
uPad.SetRightMargin( R/900 )
uPad.SetTopMargin( T/800 )
uPad.SetBottomMargin( B/800 )

uPad.SetFillColor(0)
uPad.SetBorderMode(0)
uPad.SetFrameFillStyle(0)
uPad.SetFrameBorderMode(0)
uPad.SetTickx(0)
uPad.SetTicky(0)
uPad.Draw()
	
uPad.cd()

hsig1merged.SetLineColor(rt.kOrange)
hsig1merged.SetFillStyle(0)
hsig1merged.SetLineWidth(3)

hsig2merged.SetLineColor(rt.kBlue)
hsig2merged.SetFillStyle(0)
hsig2merged.SetLineWidth(3)

hsig1merged.SetMaximum(100000*hsig2merged.GetMaximum())
uPad.SetLogy()

hsig1merged.SetStats(0)
hsig1merged.Draw("HIST") #if doSig
hsig2merged.Draw("SAME HIST") #if doSig

legmerged = rt.TLegend(legx1,legy1,legx2,legy2) #edit

legmerged.AddEntry(hsig1merged,sig1leg,"l")
legmerged.AddEntry(hsig2merged,sig2leg,"l")
legmerged.Draw("same")

CMS_lumi.CMS_lumi(uPad, iPeriod, iPos)
	
uPad.Update()
uPad.RedrawAxis()
frame = uPad.GetFrame()
uPad.Draw()
	
c1merged.SaveAs("NPV.png")

RFile1.Close()
RFile2.Close()


