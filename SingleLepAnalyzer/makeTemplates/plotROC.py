import sys, os
import argparse
import math

from math import log10 

import ROOT
from ROOT import TFile, TCanvas, TH1F
from ROOT import gStyle
from ROOT import kGreen, kRed, kBlue,kBlack


gStyle.SetOptStat(ROOT.kFALSE)

parser = argparse.ArgumentParser()

parser.add_argument("-y", "--year", default="18", help="year= 16APV,16,17,18")
parser.add_argument("-b", "--background", default="", help="The input file for background")
parser.add_argument("-o", "--output", default="", help="The name of the output file")
parser.add_argument("-m", "--mass", default="", help="Mass point of the XGB output mass point")

args = parser.parse_args()


year = args.year

tfile_bkg = ROOT.TFile('/eos/uscms/store/user/fsimpson/UL'+year+'/step3_XGB_final/nominal/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_9_hadd.root')

can = ROOT.TCanvas("can", "can", 800, 800)
can.cd()
can.SetLogy()
multigra_ROC = ROOT.TMultiGraph()

sigcolor={600:kBlue,700:kBlue-9,800:kGreen,900:kGreen-9,1000:kRed-12,1100:kRed-9,1200:kRed,1300:kBlack-12,1400:kBlack-12,1500:kBlack-9,1600:kBlack}
#fout = ROOT.TFile("ROC_"+args.output+".root", "RECREATE")
#sigcolor = {600:ROOT.kBlack,700:,800:,900,1000:}
ttree_bkg = tfile_bkg.Get("ljmet")
h_XGB_b = ROOT.TH1F("h_XGB_b", "h_XGB_b", 40, 0, 1)
ttree_bkg.SetBranchStatus("*", 0)
ttree_bkg.SetBranchStatus("XGB1300_SR1", 1)
#ttree_bkg.SetBranchStatus("XGB800_SR1", 1)

nevents_bkg = ttree_bkg.GetEntries()

for iev in range(nevents_bkg):
    if iev%1000==1:
        print("processing background", iev)
    ttree_bkg.GetEntry(iev)
    h_XGB_b.Fill(ttree_bkg.XGB1300_SR1)
#    h_XGB_b.Fill(ttree_bkg.XGB800_SR1)

leg = ROOT.TLegend(0.1,0.6,0.7,0.885) #0.26,0.6,0.94,0.885


for mass in range(700,1700,100):
#for mass in range(1000,1600,100):
	tfile_sig = ROOT.TFile('/eos/uscms/store/user/fsimpson/UL'+year+'/step3_XGB_final/nominal/PairVLQ_x53x53_tWtW_narrow_RH_M'+str(mass)+'_TuneCP5_13TeV-madgraph-pythia8_hadd.root')
#	tfile_sig = ROOT.TFile('/eos/uscms/store/user/fsimpson/UL'+year+'/step3_XGB_final/nominal/PairVLQ_x53x53_tHtH_narrow_RH_MX'+str(mass)+'_MH800_TuneCP5_13TeV-madgraph-pythia8_hadd.root')

	ttree_sig = tfile_sig.Get("ljmet")
	
	h_XGB_s = ROOT.TH1F("h_XGB_s"+str(mass), "h_XGB_s"+str(mass), 40, 0, 1)
	ttree_sig.SetBranchStatus("*", 0)
	ttree_sig.SetBranchStatus("XGB1300_SR1", 1)
#	ttree_sig.SetBranchStatus("XGB800_SR1", 1)

	nevents_sig = ttree_sig.GetEntries()


	for iev in range(nevents_sig):
    		if iev%1000==1:
        		print("processing signal", iev)
    		ttree_sig.GetEntry(iev)
    		h_XGB_s.Fill(ttree_sig.XGB1300_SR1)
#    		h_XGB_s.Fill(ttree_sig.XGB800_SR1)

	gra_ROC = ROOT.TGraph()
	gra_ROC.GetXaxis().SetTitle("Signal Efficiency")
	gra_ROC.GetYaxis().SetTitle("Background Efficiency")
	#gra_ROC.SetLineColor(sigcolor[mass])
	gra_ROC.GetXaxis().SetRangeUser(0, 1)
	gra_ROC.SetLineWidth(2)

	ip = 0 
	bkg_eff = 1.
	sig_eff = 1.


	aucscore = 0
	print mass
	print aucscore

	for ibin in range(41):
	    gra_ROC.SetPoint(ip, sig_eff, bkg_eff)
	    bkg_eff -= float(h_XGB_b.GetBinContent(ibin))/float(h_XGB_b.Integral())
	    sig_eff -= float(h_XGB_s.GetBinContent(ibin))/float(h_XGB_s.Integral())
	    aucscore += float(sig_eff)*float(h_XGB_b.GetBinContent(ibin))/float(h_XGB_b.Integral())
	    ip+=1
	
	print("AUC score !!! = {}".format(aucscore))

	gra_ROC.SetTitle("Mass = {0} AUC = {1:.{2}f}".format(mass,aucscore, 3))
	gra_ROC.SetName("Mass = {0} {1:.{2}f}".format(mass,aucscore, 3))
	multigra_ROC.Add(gra_ROC,"ACP")

	leg.AddEntry(gra_ROC,"Mass = "+str(mass)+" AUC= "+str(aucscore),"f")

	del(h_XGB_s)

leg.SetShadowColor(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetLineColor(0)
leg.SetLineStyle(0)
leg.SetBorderSize(0) 
#leg.SetNColumns(2)


multigra_ROC.Draw("ACP plc")
multigra_ROC.GetXaxis().SetTitle("Signal Efficiency")
multigra_ROC.GetYaxis().SetTitle("Background Efficiency")
multigra_ROC.GetYaxis().SetRangeUser(1e-6, 1000)

leg.Draw("same")

#gra_ROC.Draw("ACP")
	#fout.WriteTObject(h_XGB_s, "h_XGB_s_"+mass)
#can.BuildLegend()
can.SaveAs("XGBH1300_log_"+year+".png")
can.SaveAs("XGBH1300_log_"+year+".pdf")

#fout.WriteTObject(gra_ROC, "gra_ROC")
#fout.WriteTObject(h_XGB_b, "h_XGB_b")
#fout.Close()
