import sys, os
import argparse
import math 

sys.path.append('/anaconda2/envs/fireworks/lib')
import ROOT
from ROOT import TFile, TCanvas, TH1F 
from ROOT import gStyle


fout = TFile("X53_HT_njets_SF_sys.root", "RECREATE")

#tfile_Mtt0 = TFile("X53_weights_Mtt0to700_extended_HT_cuts_sys.root")
#tfile_Mtt700 = TFile("X53_weights_Mtt700to1000_extended_HT_cuts_sys.root")
#tfile_Mtt1000 = TFile("X53_weights_Mtt1000toInf_extended_HT_cuts_sys.root")
#tfile_tt2b = TFile("CHiggs_Weights_tt2b_extended_HT_cuts_sys.root")
#tfile_tt1b = TFile("CHiggs_Weights_tt1b_extended_HT_cuts_sys.root")
#tfile_STs = TFile("CHiggs_Weights_STs_extended_HT_cuts_sys.root")
#tfile_STtw = TFile("CHiggs_Weights_STtw_extended_HT_cuts_sys.root")
#tfile_STt  = TFile("CHiggs_Weights_STt_extended_HT_cuts_sys.root")
#tfile_WJets = TFile("CHiggs_Weights_WJets_extended_HT_cuts_sys.root")

tfile_XXM600MH200  = TFile("X53_weights_M600_MH200_extended_HT_cuts_Sys.root")
tfile_XXM600MH400  = TFile("X53_weights_M600_MH400_extended_HT_cuts_Sys.root")
tfile_XXM700MH400  = TFile("X53_weights_M700_MH400_extended_HT_cuts_Sys.root")
tfile_XXM800MH200  = TFile("X53_weights_M800_MH200_extended_HT_cuts_Sys.root")
tfile_XXM800MH400  = TFile("X53_weights_M800_MH400_extended_HT_cuts_Sys.root")
tfile_XXM800MH600  = TFile("X53_weights_M800_MH600_extended_HT_cuts_Sys.root")
tfile_XXM900MH200  = TFile("X53_weights_M900_MH200_extended_HT_cuts_Sys.root")
tfile_XXM900MH400  = TFile("X53_weights_M900_MH400_extended_HT_cuts_Sys.root")
tfile_XXM1000MH200  = TFile("X53_weights_M1000_MH200_extended_HT_cuts_Sys.root")
tfile_XXM1000MH400  = TFile("X53_weights_M1000_MH400_extended_HT_cuts_Sys.root")
tfile_XXM1000MH800  = TFile("X53_weights_M1000_MH800_extended_HT_cuts_Sys.root")
tfile_XXM1100MH200  = TFile("X53_weights_M1100_MH200_extended_HT_cuts_Sys.root")
tfile_XXM1100MH400  = TFile("X53_weights_M1100_MH400_extended_HT_cuts_Sys.root")
tfile_XXM1100MH600  = TFile("X53_weights_M1100_MH600_extended_HT_cuts_Sys.root")
tfile_XXM1100MH800 = TFile("X53_weights_M1100_MH800_extended_HT_cuts_Sys.root")
tfile_XXM1200MH200  = TFile("X53_weights_M1200_MH200_extended_HT_cuts_Sys.root")
tfile_XXM1200MH400  = TFile("X53_weights_M1200_MH400_extended_HT_cuts_Sys.root")
tfile_XXM1200MH600  = TFile("X53_weights_M1200_MH600_extended_HT_cuts_Sys.root")
tfile_XXM1200MH800 = TFile("X53_weights_M1200_MH800_extended_HT_cuts_Sys.root")
tfile_XXM1200MH1000 = TFile("X53_weights_M1200_MH1000_extended_HT_cuts_Sys.root")
tfile_XXM1500MH200 = TFile("X53_weights_M1500_MH200_extended_HT_cuts_Sys.root")
tfile_XXM1500MH400 = TFile("X53_weights_M1500_MH400_extended_HT_cuts_Sys.root")
tfile_XXM1500MH600 = TFile("X53_weights_M1500_MH600_extended_HT_cuts_Sys.root")
tfile_XXM1500MH800 = TFile("X53_weights_M1500_MH800_extended_HT_cuts_Sys.root")
tfile_XXM1500MH1000 = TFile("X53_weights_M1500_MH1000_extended_HT_cuts_Sys.root")
tfile_TTToHad0 =       TFile("TTToHad0weights_extended_HT_cuts_Sys.root")
tfile_TTToHad700 =     TFile("TTToHad700weights_extended_HT_cuts_Sys.root")
tfile_TTToHad1000 =     TFile("TTToHad1000weights_extended_HT_cuts_Sys.root")
tfile_TTToSemiLep0 =   TFile("TTToSemiLep0weights_extended_HT_cuts_Sys.root")
tfile_TTToSemiLep700 = TFile("TTToSemiLep700weights_extended_HT_cuts_Sys.root")
tfile_TTToSemiLep1000 = TFile("TTToSemiLep1000weights_extended_HT_cuts_Sys.root")
tfile_TTToLNu0 =        TFile("TTToLNu0weights_extended_HT_cuts_Sys.root")       
tfile_TTToLNu700 =      TFile("TTToLNu700weights_extended_HT_cuts_Sys.root")  
tfile_TTToLNu1000  =     TFile("TTToLNu1000weights_extended_HT_cuts_Sys.root")


sys_postfix = ["", "_HFup", "_HFdn", "_LFup", "_LFdn", "_jesup", "_jesdn", "_hfstats1up", "_hfstats1dn", "_hfstats2up", "_hfstats2dn", "_cferr1up", 
        "_cferr1dn", "_cferr2up", "_cferr2dn", "_lfstats1up", "_lfstats1dn", "_lfstats2up", "_lfstats2dn"]

hscale_XXM600MH200   = {}
hscale_XXM600MH400   = {}
hscale_XXM700MH400   = {}
hscale_XXM800MH200   = {} 
hscale_XXM800MH400   = {}
hscale_XXM800MH600   = {}
hscale_XXM900MH200   = {}
hscale_XXM900MH400   = {}
hscale_XXM1000MH200  = {}
hscale_XXM1000MH400  = {} 
hscale_XXM1000MH800  = {}
hscale_XXM1100MH200  = {}
hscale_XXM1100MH400  = {}
hscale_XXM1100MH600  = {}
hscale_XXM1100MH800  = {}
hscale_XXM1200MH200  = {}
hscale_XXM1200MH400  = {}
hscale_XXM1200MH600  = {}
hscale_XXM1200MH800  = {}
hscale_XXM1200MH1000 = {}
hscale_XXM1500MH200  = {}
hscale_XXM1500MH400  = {}
hscale_XXM1500MH600  = {}
hscale_XXM1500MH800  = {}
hscale_XXM1500MH1000 = {}
hscale_TTToHad0        = {}
hscale_TTToHad700      = {}
hscale_TTToHad1000      = {}
hscale_TTToSemiLep0    = {}
hscale_TTToSemiLep700  = {}
hscale_TTToSemiLep1000  = {}
hscale_TTToLNu0       = {}
hscale_TTToLNu700      = {}
hscale_TTToLNu1000    = {}



for sys in sys_postfix:

    hscale_XXM600MH200[sys]   = tfile_XXM600MH200.Get("h2D_scale"+sys).Clone()
    hscale_XXM600MH400[sys]   = tfile_XXM600MH400.Get("h2D_scale"+sys).Clone()
    hscale_XXM700MH400[sys]   = tfile_XXM700MH400.Get("h2D_scale"+sys).Clone()
    hscale_XXM800MH200[sys]   = tfile_XXM800MH200.Get("h2D_scale"+sys).Clone()
    hscale_XXM800MH400[sys]   = tfile_XXM800MH400.Get("h2D_scale"+sys).Clone()
    hscale_XXM800MH600[sys]   = tfile_XXM800MH600.Get("h2D_scale"+sys).Clone()
    hscale_XXM900MH200[sys]   = tfile_XXM900MH200.Get("h2D_scale"+sys).Clone()
    hscale_XXM900MH400[sys]   = tfile_XXM900MH400.Get("h2D_scale"+sys).Clone()
    hscale_XXM1000MH200[sys]  = tfile_XXM1000MH200.Get("h2D_scale"+sys).Clone() 
    hscale_XXM1000MH400[sys]  = tfile_XXM1000MH400.Get("h2D_scale"+sys).Clone()  
    hscale_XXM1000MH800[sys]  = tfile_XXM1000MH800.Get("h2D_scale"+sys).Clone() 
    hscale_XXM1100MH200[sys]  = tfile_XXM1100MH200.Get("h2D_scale"+sys).Clone() 
    hscale_XXM1100MH400[sys]  = tfile_XXM1100MH400.Get("h2D_scale"+sys).Clone() 
    hscale_XXM1100MH600[sys]  = tfile_XXM1100MH600.Get("h2D_scale"+sys).Clone() 
    hscale_XXM1100MH800[sys]  = tfile_XXM1100MH800.Get("h2D_scale"+sys).Clone() 
    hscale_XXM1200MH200[sys]  = tfile_XXM1200MH200.Get("h2D_scale"+sys).Clone() 
    hscale_XXM1200MH400[sys]  = tfile_XXM1200MH400.Get("h2D_scale"+sys).Clone() 
    hscale_XXM1200MH600[sys]  = tfile_XXM1200MH600.Get("h2D_scale"+sys).Clone() 
    hscale_XXM1200MH800[sys]  = tfile_XXM1200MH800.Get("h2D_scale"+sys).Clone() 
    hscale_XXM1200MH1000[sys] = tfile_XXM1200MH1000.Get("h2D_scale"+sys).Clone() 
    hscale_XXM1500MH200[sys] =  tfile_XXM1500MH200.Get("h2D_scale"+sys).Clone()
    hscale_XXM1500MH400[sys] =  tfile_XXM1500MH400.Get("h2D_scale"+sys).Clone()
    hscale_XXM1500MH600[sys] =  tfile_XXM1500MH600.Get("h2D_scale"+sys).Clone()
    hscale_XXM1500MH800[sys] =  tfile_XXM1500MH800.Get("h2D_scale"+sys).Clone()
    hscale_XXM1500MH1000[sys]=  tfile_XXM1500MH1000.Get("h2D_scale"+sys).Clone()
    hscale_TTToHad0[sys]        = tfile_TTToHad0.Get("h2D_scale"+sys).Clone() 
    hscale_TTToHad700[sys]  = tfile_TTToHad700.Get("h2D_scale"+sys).Clone() 
    hscale_TTToHad1000[sys]  = tfile_TTToHad1000.Get("h2D_scale"+sys).Clone() 
    hscale_TTToSemiLep0[sys] =  tfile_TTToSemiLep0.Get("h2D_scale"+sys).Clone() 
    hscale_TTToSemiLep700[sys] =  tfile_TTToSemiLep700.Get("h2D_scale"+sys).Clone()
    hscale_TTToSemiLep1000[sys] =  tfile_TTToSemiLep1000.Get("h2D_scale"+sys).Clone()
    hscale_TTToLNu0[sys] =  tfile_TTToLNu0.Get("h2D_scale"+sys).Clone()
    hscale_TTToLNu700[sys] =  tfile_TTToLNu700.Get("h2D_scale"+sys).Clone()
    hscale_TTToLNu1000[sys] =  tfile_TTToLNu1000.Get("h2D_scale"+sys).Clone()

    fout.WriteTObject( hscale_XXM600MH200[sys],     "hscale_XXM600MH200"  +sys)
    fout.WriteTObject( hscale_XXM600MH400[sys],     "hscale_XXM600MH400"  +sys)
    fout.WriteTObject( hscale_XXM700MH400[sys],     "hscale_XXM700MH400"  +sys)
    fout.WriteTObject( hscale_XXM800MH200[sys],     "hscale_XXM800MH200"  +sys)
    fout.WriteTObject( hscale_XXM800MH400[sys],     "hscale_XXM800MH400"  +sys)
    fout.WriteTObject( hscale_XXM800MH600[sys],     "hscale_XXM800MH600"  +sys)
    fout.WriteTObject( hscale_XXM900MH200[sys],     "hscale_XXM900MH200"  +sys)
    fout.WriteTObject( hscale_XXM900MH400[sys],     "hscale_XXM900MH400"  +sys)
    fout.WriteTObject( hscale_XXM1000MH200[sys],     "hscale_XXM1000MH200" +sys)
    fout.WriteTObject( hscale_XXM1000MH400[sys] ,    "hscale_XXM1000MH400" +sys)  
    fout.WriteTObject( hscale_XXM1000MH800[sys] ,    "hscale_XXM1000MH800" +sys)  
    fout.WriteTObject( hscale_XXM1100MH200[sys] ,    "hscale_XXM1100MH200" +sys)  
    fout.WriteTObject( hscale_XXM1100MH400[sys] ,    "hscale_XXM1100MH400" +sys)  
    fout.WriteTObject( hscale_XXM1100MH600[sys] ,    "hscale_XXM1100MH600" +sys)  
    fout.WriteTObject( hscale_XXM1100MH800[sys] ,    "hscale_XXM1100MH800" +sys)  
    fout.WriteTObject( hscale_XXM1200MH200[sys] ,    "hscale_XXM1200MH200" +sys)  
    fout.WriteTObject( hscale_XXM1200MH400[sys] ,    "hscale_XXM1200MH400" +sys)  
    fout.WriteTObject( hscale_XXM1200MH600[sys] ,    "hscale_XXM1200MH600" +sys)  
    fout.WriteTObject( hscale_XXM1200MH800[sys] ,    "hscale_XXM1200MH800" +sys)  
    fout.WriteTObject( hscale_XXM1200MH1000[sys] ,    "hscale_XXM1200MH1000" +sys) 
    fout.WriteTObject( hscale_XXM1500MH200[sys] ,    "hscale_XXM1500MH200" +sys) 
    fout.WriteTObject( hscale_XXM1500MH400[sys] ,    "hscale_XXM1500MH400" +sys) 
    fout.WriteTObject( hscale_XXM1500MH600[sys] ,    "hscale_XXM1500MH600" +sys) 
    fout.WriteTObject( hscale_XXM1500MH800[sys] ,    "hscale_XXM1500MH800" +sys) 
    fout.WriteTObject( hscale_XXM1500MH1000[sys] ,    "hscale_XXM1500MH1000" +sys) 
    fout.WriteTObject( hscale_TTToHad0[sys] ,    "hscale_TTToHad0" +sys) 
    fout.WriteTObject( hscale_TTToHad700[sys] ,    "hscale_TTToHad700" +sys) 
    fout.WriteTObject( hscale_TTToHad1000[sys] ,    "hscale_TTToHad1000" +sys) 
    fout.WriteTObject( hscale_TTToSemiLep0[sys] ,    "hscale_TTToSemiLep0" +sys) 
    fout.WriteTObject( hscale_TTToSemiLep700[sys] ,    "hscale_TTToSemiLep700" +sys) 
    fout.WriteTObject( hscale_TTToSemiLep1000[sys] ,    "hscale_TTToSemiLep1000" +sys) 
    fout.WriteTObject( hscale_TTToLNu0[sys] ,    "hscale_TTToLNu0" +sys) 
    fout.WriteTObject( hscale_TTToLNu700[sys] ,    "hscale_TTToLNu700" +sys) 
    fout.WriteTObject( hscale_TTToLNu1000[sys] ,    "hscale_TTToLNu1000" +sys) 






fout.Close()
