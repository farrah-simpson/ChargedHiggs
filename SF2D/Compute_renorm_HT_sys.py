import ROOT
import sys
import numpy
import argparse
import array
from ROOT import TFile, TTree

parser = argparse.ArgumentParser(description="compute the renormalization factors for charged Higgs analysis")

parser.add_argument("-f", "--file", default="", help="The path to the analysis tree")
parser.add_argument("-l", "--label", default="", help="The name of the output file")

args = parser.parse_args()

filename = args.file

tfile = TFile.Open("/eos/uscms/store/user/fsimpson/FWLJMET106X_1lep2017UL_step1_hadds/nominal/"+filename)

fout = ROOT.TFile(args.label+"weights_extended_HT_cuts_Sys.root", "RECREATE")


h2D_origin = ROOT.TH2F("h2D_origin", "h2D_origin", 3, 4, 7, 40, 150, 4000)
h2D_origin.Sumw2()
h2D_weight = ROOT.TH2F("h2D_weight", "h2D_weight", 3, 4, 7, 40, 150, 4000)
h2D_weight.Sumw2()

h2D_origin_HFup = ROOT.TH2F("h2D_origin_HFup", "h2D_origin_HFup", 3, 4, 7, 40, 150, 4000)
h2D_origin_HFup.Sumw2()
h2D_weight_HFup = ROOT.TH2F("h2D_weight_HFup", "h2D_weight_HFup", 3, 4, 7, 40, 150, 4000)
h2D_weight_HFup.Sumw2()

h2D_origin_HFdn = ROOT.TH2F("h2D_origin_HFdn", "h2D_origin_HFdn", 3, 4, 7, 40, 150, 4000)
h2D_origin_HFdn.Sumw2()
h2D_weight_HFdn = ROOT.TH2F("h2D_weight_HFdn", "h2D_weight_HFdn", 3, 4, 7, 40, 150, 4000)
h2D_weight_HFdn.Sumw2()

h2D_origin_LFup = ROOT.TH2F("h2D_origin_LFup", "h2D_origin_LFup", 3, 4, 7, 40, 150, 4000)
h2D_origin_LFup.Sumw2()
h2D_weight_LFup = ROOT.TH2F("h2D_weight_LFup", "h2D_weight_LFup", 3, 4, 7, 40, 150, 4000)
h2D_weight_LFup.Sumw2()

h2D_origin_LFdn = ROOT.TH2F("h2D_origin_LFdn", "h2D_origin_LFdn", 3, 4, 7, 40, 150, 4000)
h2D_origin_LFdn.Sumw2()
h2D_weight_LFdn = ROOT.TH2F("h2D_weight_LFdn", "h2D_weight_LFdn", 3, 4, 7, 40, 150, 4000)
h2D_weight_LFdn.Sumw2()

h2D_origin_jesup = ROOT.TH2F("h2D_origin_jesup", "h2D_origin_jesup", 3, 4, 7, 40, 150, 4000)
h2D_origin_jesup.Sumw2()
h2D_weight_jesup = ROOT.TH2F("h2D_weight_jesup", "h2D_weight_jesup", 3, 4, 7, 40, 150, 4000)
h2D_weight_jesup.Sumw2()

h2D_origin_jesdn = ROOT.TH2F("h2D_origin_jesdn", "h2D_origin_jesdn", 3, 4, 7, 40, 150, 4000)
h2D_origin_jesdn.Sumw2()
h2D_weight_jesdn = ROOT.TH2F("h2D_weight_jesdn", "h2D_weight_jesdn", 3, 4, 7, 40, 150, 4000)
h2D_weight_jesdn.Sumw2()

h2D_origin_hfstats1up = ROOT.TH2F("h2D_origin_hfstats1up", "h2D_origin_hfstats1up", 3, 4, 7, 40, 150, 4000)
h2D_origin_hfstats1up.Sumw2()
h2D_weight_hfstats1up = ROOT.TH2F("h2D_weight_hfstats1up", "h2D_weight_hfstats1up", 3, 4, 7, 40, 150, 4000)
h2D_weight_hfstats1up.Sumw2()

h2D_origin_hfstats1dn = ROOT.TH2F("h2D_origin_hfstats1dn", "h2D_origin_hfstats1dn", 3, 4, 7, 40, 150, 4000)
h2D_origin_hfstats1dn.Sumw2()
h2D_weight_hfstats1dn = ROOT.TH2F("h2D_weight_hfstats1dn", "h2D_weight_hfstats1dn", 3, 4, 7, 40, 150, 4000)
h2D_weight_hfstats1dn.Sumw2()

h2D_origin_hfstats2up = ROOT.TH2F("h2D_origin_hfstats2up", "h2D_origin_hfstats2up", 3, 4, 7, 40, 150, 4000)
h2D_origin_hfstats2up.Sumw2()
h2D_weight_hfstats2up = ROOT.TH2F("h2D_weight_hfstats2up", "h2D_weight_hfstats2up", 3, 4, 7, 40, 150, 4000)
h2D_weight_hfstats2up.Sumw2()

h2D_origin_hfstats2dn = ROOT.TH2F("h2D_origin_hfstats2dn", "h2D_origin_hfstats2dn", 3, 4, 7, 40, 150, 4000)
h2D_origin_hfstats2dn.Sumw2()
h2D_weight_hfstats2dn = ROOT.TH2F("h2D_weight_hfstats2dn", "h2D_weight_hfstats2dn", 3, 4, 7, 40, 150, 4000)
h2D_weight_hfstats2dn.Sumw2()

h2D_origin_cferr1up = ROOT.TH2F("h2D_origin_cferr1up", "h2D_origin_cferr1up", 3, 4, 7, 40, 150, 4000)
h2D_origin_cferr1up.Sumw2()
h2D_weight_cferr1up = ROOT.TH2F("h2D_weight_cferr1up", "h2D_weight_cferr1up", 3, 4, 7, 40, 150, 4000)
h2D_weight_cferr1up.Sumw2()

h2D_origin_cferr1dn = ROOT.TH2F("h2D_origin_cferr1dn", "h2D_origin_cferr1dn", 3, 4, 7, 40, 150, 4000)
h2D_origin_cferr1dn.Sumw2()
h2D_weight_cferr1dn = ROOT.TH2F("h2D_weight_cferr1dn", "h2D_weight_cferr1dn", 3, 4, 7, 40, 150, 4000)
h2D_weight_cferr1dn.Sumw2()

h2D_origin_cferr2up = ROOT.TH2F("h2D_origin_cferr2up", "h2D_origin_cferr2up", 3, 4, 7, 40, 150, 4000)
h2D_origin_cferr2up.Sumw2()
h2D_weight_cferr2up = ROOT.TH2F("h2D_weight_cferr2up", "h2D_weight_cferr2up", 3, 4, 7, 40, 150, 4000)
h2D_weight_cferr2up.Sumw2()

h2D_origin_cferr2dn = ROOT.TH2F("h2D_origin_cferr2dn", "h2D_origin_cferr2dn", 3, 4, 7, 40, 150, 4000)
h2D_origin_cferr2dn.Sumw2()
h2D_weight_cferr2dn = ROOT.TH2F("h2D_weight_cferr2dn", "h2D_weight_cferr2dn", 3, 4, 7, 40, 150, 4000)
h2D_weight_cferr2dn.Sumw2()

h2D_origin_lfstats1up = ROOT.TH2F("h2D_origin_lfstats1up", "h2D_origin_lfstats1up", 3, 4, 7, 40, 150, 4000)
h2D_origin_lfstats1up.Sumw2()
h2D_weight_lfstats1up = ROOT.TH2F("h2D_weight_lfstats1up", "h2D_weight_lfstats1up", 3, 4, 7, 40, 150, 4000)
h2D_weight_lfstats1up.Sumw2()

h2D_origin_lfstats1dn = ROOT.TH2F("h2D_origin_lfstats1dn", "h2D_origin_lfstats1dn", 3, 4, 7, 40, 150, 4000)
h2D_origin_lfstats1dn.Sumw2()
h2D_weight_lfstats1dn = ROOT.TH2F("h2D_weight_lfstats1dn", "h2D_weight_lfstats1dn", 3, 4, 7, 40, 150, 4000)
h2D_weight_lfstats1dn.Sumw2()

h2D_origin_lfstats2up = ROOT.TH2F("h2D_origin_lfstats2up", "h2D_origin_lfstats2up", 3, 4, 7, 40, 150, 4000)
h2D_origin_lfstats2up.Sumw2()
h2D_weight_lfstats2up = ROOT.TH2F("h2D_weight_lfstats2up", "h2D_weight_lfstats2up", 3, 4, 7, 40, 150, 4000)
h2D_weight_lfstats2up.Sumw2()

h2D_origin_lfstats2dn = ROOT.TH2F("h2D_origin_lfstats2dn", "h2D_origin_lfstats2dn", 3, 4, 7, 40, 150, 4000)
h2D_origin_lfstats2dn.Sumw2()
h2D_weight_lfstats2dn = ROOT.TH2F("h2D_weight_lfstats2dn", "h2D_weight_lfstats2dn", 3, 4, 7, 40, 150, 4000)
h2D_weight_lfstats2dn.Sumw2()


ttree = tfile.Get("ljmet")


ttree.SetBranchStatus("*", 0)
ttree.SetBranchStatus("NJets_JetSubCalc*", 1)
ttree.SetBranchStatus("theJetPt_JetSubCalc_PtOrdered*", 1)
ttree.SetBranchStatus("AK4HT*", 1)
ttree.SetBranchStatus("btagDeepJetWeight*", 1)
ttree.SetBranchStatus("leptonPt_MultiLepCalc*", 1)
ttree.SetBranchStatus("isElectron*", 1)
ttree.SetBranchStatus("isMuon*", 1)
ttree.SetBranchStatus("corr_met_MultiLepCalc*", 1)
ttree.SetBranchStatus("MCPastTrigger*", 1)

nevents = ttree.GetEntries()

for iev in range(nevents):
    if iev%1000==1:
        print(iev)
    ttree.GetEntry(iev)
    njet = ttree.NJets_JetSubCalc
    if not ((ttree.leptonPt_MultiLepCalc > 35 and ttree.isElectron) or (ttree.leptonPt_MultiLepCalc > 30 and ttree.isMuon)): continue
    if not (ttree.corr_met_MultiLepCalc > 30): continue
    if not (ttree.MCPastTrigger): continue 
    HT = ttree.AK4HT
    if njet>6: njet=6
    #for ijet in range(njet):
    #    if ttree.theJetPt_JetSubCalc_PtOrdered.at(ijet)>120:
    #        n_fastjet+=1
    #    elif (ttree.theJetPt_JetSubCalc_PtOrdered.at(ijet)<=120 and ttree.theJetPt_JetSubCalc_PtOrdered.at(ijet)>40):
    #        n_slowjet+=1

    #if n_fastjet>5: n_fastjet=5
    #if n_slowjet>5: n_slowjet=5
    h2D_origin.Fill(njet, HT)
    h2D_weight.Fill(njet, HT, ttree.btagDeepJetWeight)
    h2D_weight_HFup.Fill(njet, HT, ttree.btagDeepJetWeight_HFup)
    h2D_weight_HFdn.Fill(njet, HT, ttree.btagDeepJetWeight_HFdn)
    h2D_weight_LFup.Fill(njet, HT, ttree.btagDeepJetWeight_LFup)
    h2D_weight_LFdn.Fill(njet, HT, ttree.btagDeepJetWeight_LFdn)
    h2D_weight_jesup.Fill(njet, HT, ttree.btagDeepJetWeight_jesup)
    h2D_weight_jesdn.Fill(njet, HT, ttree.btagDeepJetWeight_jesdn)
    h2D_weight_hfstats1up.Fill(njet, HT, ttree.btagDeepJetWeight_hfstats1up)
    h2D_weight_hfstats1dn.Fill(njet, HT, ttree.btagDeepJetWeight_hfstats1dn)
    h2D_weight_hfstats2up.Fill(njet, HT, ttree.btagDeepJetWeight_hfstats2up)
    h2D_weight_hfstats2dn.Fill(njet, HT, ttree.btagDeepJetWeight_hfstats2dn)
    h2D_weight_cferr1up.Fill(njet, HT, ttree.btagDeepJetWeight_cferr1up)
    h2D_weight_cferr1dn.Fill(njet, HT, ttree.btagDeepJetWeight_cferr1dn)
    h2D_weight_cferr2up.Fill(njet, HT, ttree.btagDeepJetWeight_cferr2up)
    h2D_weight_cferr2dn.Fill(njet, HT, ttree.btagDeepJetWeight_cferr2dn)
    h2D_weight_lfstats1up.Fill(njet, HT, ttree.btagDeepJetWeight_lfstats1up)
    h2D_weight_lfstats1dn.Fill(njet, HT, ttree.btagDeepJetWeight_lfstats1dn)
    h2D_weight_lfstats2up.Fill(njet, HT, ttree.btagDeepJetWeight_lfstats2up)
    h2D_weight_lfstats2dn.Fill(njet, HT, ttree.btagDeepJetWeight_lfstats2dn)

   

h2D_scale = h2D_origin.Clone()
h2D_scale_HFup       = h2D_origin.Clone()
h2D_scale_HFdn       = h2D_origin.Clone()
h2D_scale_LFup       = h2D_origin.Clone()
h2D_scale_LFdn       = h2D_origin.Clone()
h2D_scale_jesup      = h2D_origin.Clone()
h2D_scale_jesdn      = h2D_origin.Clone()
h2D_scale_hfstats1up = h2D_origin.Clone()
h2D_scale_hfstats1dn = h2D_origin.Clone()
h2D_scale_hfstats2up = h2D_origin.Clone()
h2D_scale_hfstats2dn = h2D_origin.Clone()
h2D_scale_cferr1up   = h2D_origin.Clone()
h2D_scale_cferr1dn   = h2D_origin.Clone()
h2D_scale_cferr2up   = h2D_origin.Clone()
h2D_scale_cferr2dn   = h2D_origin.Clone()
h2D_scale_lfstats1up = h2D_origin.Clone()
h2D_scale_lfstats1dn = h2D_origin.Clone()
h2D_scale_lfstats2up = h2D_origin.Clone()
h2D_scale_lfstats2dn = h2D_origin.Clone()


h2D_scale.SetTitle("h2D_scale")
h2D_scale_HFup.SetTitle("h2D_scale_HFup")      
h2D_scale_HFdn.SetTitle("h2D_scale_HFdn")      
h2D_scale_LFup.SetTitle("h2D_scale_LFup")      
h2D_scale_LFdn.SetTitle("h2D_scale_LFdn")      
h2D_scale_jesup.SetTitle("h2D_scale_jesup")     
h2D_scale_jesdn.SetTitle("h2D_scale_jesdn")     
h2D_scale_hfstats1up.SetTitle("h2D_scale_hfstats1up")
h2D_scale_hfstats1dn.SetTitle("h2D_scale_hfstats1dn")
h2D_scale_hfstats2up.SetTitle("h2D_scale_hfstats2up")
h2D_scale_hfstats2dn.SetTitle("h2D_scale_hfstats2dn")
h2D_scale_cferr1up.SetTitle("h2D_scale_cferr1up")  
h2D_scale_cferr1dn.SetTitle("h2D_scale_cferr1dn")  
h2D_scale_cferr2up.SetTitle("h2D_scale_cferr2up")  
h2D_scale_cferr2dn.SetTitle("h2D_scale_cferr2dn")  
h2D_scale_lfstats1up.SetTitle("h2D_scale_lfstats1up")
h2D_scale_lfstats1dn.SetTitle("h2D_scale_lfstats1dn")
h2D_scale_lfstats2up.SetTitle("h2D_scale_lfstats2up")
h2D_scale_lfstats2dn.SetTitle("h2D_scale_lfstats2dn")


h2D_scale.Divide(h2D_weight)
h2D_scale_HFup.Divide(h2D_weight_HFup)      
h2D_scale_HFdn.Divide(h2D_weight_HFdn)    
h2D_scale_LFup.Divide(h2D_weight_LFup)      
h2D_scale_LFdn.Divide(h2D_weight_LFdn)      
h2D_scale_jesup.Divide(h2D_weight_jesup)     
h2D_scale_jesdn.Divide(h2D_weight_jesdn) 
h2D_scale_hfstats1up.Divide(h2D_weight_hfstats1up)
h2D_scale_hfstats1dn.Divide(h2D_weight_hfstats1dn)
h2D_scale_hfstats2up.Divide(h2D_weight_hfstats2up)
h2D_scale_hfstats2dn.Divide(h2D_weight_hfstats2dn)
h2D_scale_cferr1up.Divide(h2D_weight_cferr1up)  
h2D_scale_cferr1dn.Divide(h2D_weight_cferr1dn)  
h2D_scale_cferr2up.Divide(h2D_weight_cferr2up)  
h2D_scale_cferr2dn.Divide(h2D_weight_cferr2dn)  
h2D_scale_lfstats1up.Divide(h2D_weight_lfstats1up)
h2D_scale_lfstats1dn.Divide(h2D_weight_lfstats1dn)
h2D_scale_lfstats2up.Divide(h2D_weight_lfstats2up)
h2D_scale_lfstats2dn.Divide(h2D_weight_lfstats2dn)


fout.WriteTObject(h2D_origin, "h2D_origin")
fout.WriteTObject(h2D_weight, "h2D_weight")
fout.WriteTObject(h2D_scale, "h2D_scale")
fout.WriteTObject(h2D_scale_HFup      ,    "h2D_scale_HFup")        
fout.WriteTObject(h2D_scale_HFdn      ,    "h2D_scale_HFdn")      
fout.WriteTObject(h2D_scale_LFup      ,    "h2D_scale_LFup")      
fout.WriteTObject(h2D_scale_LFdn      ,    "h2D_scale_LFdn")      
fout.WriteTObject(h2D_scale_jesup     ,    "h2D_scale_jesup")     
fout.WriteTObject(h2D_scale_jesdn     ,    "h2D_scale_jesdn")     
fout.WriteTObject(h2D_scale_hfstats1up,    "h2D_scale_hfstats1up")  
fout.WriteTObject(h2D_scale_hfstats1dn,    "h2D_scale_hfstats1dn")
fout.WriteTObject(h2D_scale_hfstats2up,    "h2D_scale_hfstats2up")
fout.WriteTObject(h2D_scale_hfstats2dn,    "h2D_scale_hfstats2dn")
fout.WriteTObject(h2D_scale_cferr1up  ,    "h2D_scale_cferr1up")  
fout.WriteTObject(h2D_scale_cferr1dn  ,    "h2D_scale_cferr1dn")  
fout.WriteTObject(h2D_scale_cferr2up  ,    "h2D_scale_cferr2up")  
fout.WriteTObject(h2D_scale_cferr2dn  ,    "h2D_scale_cferr2dn")  
fout.WriteTObject(h2D_scale_lfstats1up,    "h2D_scale_lfstats1up") 
fout.WriteTObject(h2D_scale_lfstats1dn,    "h2D_scale_lfstats1dn")
fout.WriteTObject(h2D_scale_lfstats2up,    "h2D_scale_lfstats2up")
fout.WriteTObject(h2D_scale_lfstats2dn,    "h2D_scale_lfstats2dn")











fout.Close()
